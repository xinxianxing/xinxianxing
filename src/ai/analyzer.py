"""Content analysis using AI."""

import asyncio
import re
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from .client import AIClient
from .prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from .utils import parse_json_response
from ..models import ContentItem, SignalType

DEFAULT_THROTTLE_SEC = 0.0


class ContentAnalyzer:
    """Analyzes content items using AI to determine importance."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    def _get_throttle_sec(self) -> float:
        """Return the configured inter-item throttle, clamped to zero or above."""
        config = getattr(self.client, "config", None)
        throttle_sec = getattr(config, "throttle_sec", DEFAULT_THROTTLE_SEC)
        return max(throttle_sec, 0.0)

    def _get_concurrency(self) -> int:
        """Return the configured analysis concurrency, clamped to 1 or above."""
        config = getattr(self.client, "config", None)
        concurrency = getattr(config, "analysis_concurrency", 1)
        return max(concurrency, 1)

    @staticmethod
    def _as_text(value, default: str = "") -> str:
        if value is None:
            return default
        if isinstance(value, str):
            return value.strip()
        return str(value).strip()

    @staticmethod
    def _as_list(value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(x).strip() for x in value if str(x).strip()]
        if isinstance(value, str):
            parts = re.split(r"[,，/、\n]+", value)
            return [part.strip() for part in parts if part.strip()]
        return [str(value).strip()] if str(value).strip() else []

    @staticmethod
    def _as_score(value) -> float:
        try:
            score = float(value)
        except (TypeError, ValueError):
            score = 0.0
        return min(max(score, 0.0), 10.0)

    @staticmethod
    def _as_signal_type(value) -> SignalType:
        try:
            return SignalType(str(value).strip().upper())
        except ValueError:
            return SignalType.NEWS

    async def analyze_batch(self, items: List[ContentItem]) -> List[ContentItem]:
        throttle_sec = self._get_throttle_sec()
        concurrency = self._get_concurrency()
        semaphore = asyncio.Semaphore(concurrency)

        async def _process(item: ContentItem, index: int, progress_task) -> ContentItem:
            async with semaphore:
                try:
                    await self._analyze_item(item)
                except Exception as e:
                    print(f"Error analyzing item {item.id}: {e}")
                    item.ai_score = 0.0
                    item.ai_reason = "Analysis failed"
                    item.ai_summary = item.title
                if throttle_sec > 0 and index < len(items) - 1:
                    await asyncio.sleep(throttle_sec)
            progress.advance(progress_task)
            return item

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))
            coros = [
                _process(item, i, task) for i, item in enumerate(items)
            ]
            analyzed_items = await asyncio.gather(*coros)

        return analyzed_items

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10)
    )
    async def _analyze_item(self, item: ContentItem) -> None:
        """Analyze a single content item.

        Args:
            item: Content item to analyze (modified in-place)
        """
        # Prepare content section
        content_section = ""
        if item.content:
            # Split off comments if present
            content_text = item.content
            if "--- Top Comments ---" in content_text:
                main, comments_part = content_text.split("--- Top Comments ---", 1)
                content_section = f"Content: {main.strip()[:800]}"
            else:
                content_section = f"Content: {content_text[:1000]}"

        # Prepare discussion section (comments, engagement)
        discussion_parts = []
        if item.content and "--- Top Comments ---" in item.content:
            comments_part = item.content.split("--- Top Comments ---", 1)[1]
            discussion_parts.append(f"Community Comments:\n{comments_part[:1500]}")

        meta = item.metadata
        engagement_items = []
        if meta.get("score"):
            engagement_items.append(f"score: {meta['score']}")
        if meta.get("descendants"):
            engagement_items.append(f"{meta['descendants']} comments")
        if meta.get("favorite_count"):
            engagement_items.append(f"{meta['favorite_count']} likes")
        if meta.get("retweet_count"):
            engagement_items.append(f"{meta['retweet_count']} retweets")
        if meta.get("reply_count"):
            engagement_items.append(f"{meta['reply_count']} replies")
        if meta.get("views"):
            engagement_items.append(f"{meta['views']} views")
        if meta.get("bookmarks"):
            engagement_items.append(f"{meta['bookmarks']} bookmarks")
        if meta.get("upvote_ratio"):
            engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
        if engagement_items:
            discussion_parts.append(f"Engagement: {', '.join(engagement_items)}")
        if meta.get("discussion_url"):
            discussion_parts.append(f"Discussion: {meta['discussion_url']}")
        if meta.get("community_note"):
            discussion_parts.append(f"Community Note: {meta['community_note']}")

        discussion_section = "\n".join(discussion_parts) if discussion_parts else ""

        # Generate user prompt
        user_prompt = CONTENT_ANALYSIS_USER.format(
            title=item.title,
            source=f"{item.source_type.value}",
            author=item.author or "Unknown",
            url=str(item.url),
            content_section=content_section,
            discussion_section=discussion_section
        )

        # Get AI completion
        response = await self.client.complete(
            system=CONTENT_ANALYSIS_SYSTEM,
            user=user_prompt,
        )

        # Parse JSON response with robust fallback
        result = self._parse_json_response(response)
        if result is None:
            print(f"Warning: could not parse analysis response for {item.id}, using defaults")
            item.ai_score = 0.0
            item.ai_reason = "Analysis response parse failed"
            item.ai_summary = item.title
            item.ai_tags = []
            return

        # Update item with Action Card results while preserving legacy fields.
        original_title = item.title
        title = self._as_text(result.get("title"), original_title)
        intro = self._as_text(
            result.get("intro") or result.get("what_happened"),
            title,
        )
        how_to = self._as_list(result.get("how_to") or result.get("opportunities"))
        suggested_actions = self._as_list(result.get("suggested_actions"))
        suitable_for = self._as_list(
            result.get("suitable_for") or result.get("who_should_care")
        )
        evidence = self._as_text(
            result.get("evidence") or result.get("why_it_matters"),
            "未提供具体数据",
        )
        credibility_risk = self._as_text(
            result.get("credibility_risk") or result.get("risk")
        )
        score = self._as_score(result.get("score"))
        signal_type = self._as_signal_type(result.get("signal_type"))
        source_url = self._as_text(result.get("source_url"), str(item.url))

        if signal_type == SignalType.MONEY_CASE and "幸存者偏差" not in credibility_risk:
            money_case_warning = "网络案例可能存在夸大或幸存者偏差，请自行甄别"
            credibility_risk = (
                f"{credibility_risk}；{money_case_warning}"
                if credibility_risk
                else money_case_warning
            )

        if title and title != original_title:
            item.metadata.setdefault("original_title", original_title)
            item.title = title

        item.intro = intro
        item.how_to = how_to
        item.suitable_for = suitable_for
        item.evidence = evidence
        item.credibility_risk = credibility_risk or None
        item.utility_score = score
        item.what_happened = intro
        item.why_it_matters = evidence
        item.who_should_care = suitable_for
        item.opportunities = how_to
        item.suggested_actions = suggested_actions
        item.risk = credibility_risk or None
        item.score = score
        item.signal_type = signal_type

        item.ai_score = score
        item.ai_reason = evidence
        item.ai_summary = intro
        item.ai_tags = suitable_for
        item.metadata["action_card"] = {
            "title": item.title,
            "signal_type": signal_type.value,
            "intro": intro,
            "how_to": how_to,
            "suitable_for": suitable_for,
            "evidence": evidence,
            "credibility_risk": credibility_risk,
            "score": score,
            "source_url": source_url,
        }
