"""Daily summary generation — pure programmatic rendering."""

import html
import re
from typing import List, Dict

from ..models import ContentItem


_CJK = r"[\u4e00-\u9fff\u3400-\u4dbf]"
_ASCII = r"[A-Za-z0-9]"


def _pangu(text: str) -> str:
    """Insert a space between CJK and ASCII letters/digits (Pangu spacing)."""
    text = re.sub(rf"({_CJK})({_ASCII})", r"\1 \2", text)
    text = re.sub(rf"({_ASCII})({_CJK})", r"\1 \2", text)
    return text


LABELS = {
    "en": {
        "header": "Xinxianxing Practical Cards",
        "source": "Source",
        "background": "Background",
        "discussion": "Discussion",
        "references": "References",
        "tags": "Tags",
        "category": "Column",
        "intro": "One-Line Intro",
        "how_to": "How To Do It",
        "suitable_for": "Best For / Use Cases",
        "evidence": "Effect or Data",
        "risk": "Credibility / Risk",
        "score": "Utility Score",
        "source_link": "Source Link",
        "selected_items": "From {total} items, {selected} tutorial/case/tip cards were selected",
        "empty_analyzed": "Analyzed {total} items, but none met the utility threshold.",
        "empty_body": (
            "No practical cards today. This might indicate:\n"
            "- A quiet day in your tracked sources\n"
            "- The AI score threshold is too high\n"
            "- Your information sources need expansion\n\n"
            "Consider:\n"
            "1. Lowering the `ai_score_threshold` in config.json\n"
            "2. Adding more diverse information sources\n"
            "3. Checking if the AI model is working correctly\n"
        ),
    },
    "zh": {
        "header": "信先行实用卡片",
        "source": "来源",
        "background": "背景",
        "discussion": "社区讨论",
        "references": "参考链接",
        "tags": "标签",
        "category": "栏目分类",
        "intro": "一句话简介",
        "how_to": "具体怎么做",
        "suitable_for": "适合谁/适用场景",
        "evidence": "效果或数据",
        "risk": "可信度/风险提示",
        "score": "实用度评分",
        "source_link": "来源链接",
        "selected_items": "从 {total} 条内容中筛选出 {selected} 条教程/案例/技巧。",
        "empty_analyzed": "已分析 {total} 条内容，但没有达到实用度阈值的条目。",
        "empty_body": (
            "今日暂无实用卡片，可能原因：\n"
            "- 今天关注的信息源较平静\n"
            "- 实用度评分阈值设置过高\n"
            "- 信息源种类有待扩充\n\n"
            "建议：\n"
            "1. 在 config.json 中降低 `ai_score_threshold`\n"
            "2. 添加更多多样化的信息源\n"
            "3. 检查 AI 模型是否正常工作\n"
        ),
    },
}


class DailySummarizer:
    """Generates daily Markdown summaries from pre-analyzed content items."""

    def __init__(self):
        pass

    async def generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate daily summary in Markdown format.

        Items are rendered in score-descending order (already sorted by orchestrator).

        Args:
            items: High-scoring content items (already enriched)
            date: Date string (YYYY-MM-DD)
            total_fetched: Total number of items fetched before filtering
            language: Output language, either "en" or "zh"

        Returns:
            str: Markdown formatted summary
        """
        labels = LABELS.get(language, LABELS["en"])

        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        header = (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['selected_items'].format(total=total_fetched, selected=len(items))}\n\n"
            "---\n\n"
        )

        # TOC
        toc_entries = []
        for i, item in enumerate(items):
            _t = item.metadata.get(f"title_{language}") or item.title
            t = str(_t).replace("[", "(").replace("]", ")")
            if language == "zh":
                t = _pangu(t)
            score = item.ai_score or "?"
            signal_type = item.signal_type.value if item.signal_type else "NEWS"
            toc_entries.append(f"{i + 1}. [{t}](#item-{i + 1}) · {signal_type} · Score: {score} / 10")
        toc = "\n".join(toc_entries) + "\n\n---\n\n"

        parts = [self._format_item(item, labels, language, i + 1) for i, item in enumerate(items)]

        return header + toc + "".join(parts)

    def generate_webhook_overview(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate a compact overview for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        if language == "zh":
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> 从 {total_fetched} 条内容中筛选出 {len(items)} 条教程/案例/技巧。\n\n"
                "下面会按卡片逐条发送详情，你可以只看感兴趣的标题。\n\n"
            )
        else:
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> Selected {len(items)} tutorial/case/tip cards from {total_fetched} fetched items.\n\n"
                "Details will be sent card by card so you can read only the topics you care about.\n\n"
            )

        entries = []
        for i, item in enumerate(items, start=1):
            title = str(item.metadata.get(f"title_{language}") or item.title).replace("[", "(").replace("]", ")")
            if language == "zh":
                title = _pangu(title)
            score = item.ai_score or "?"
            signal_type = item.signal_type.value if item.signal_type else "NEWS"
            entries.append(f"{i}. [{title}]({item.url}) · {signal_type} · Score: {score} / 10")

        return header + "\n".join(entries)

    def generate_webhook_item(
        self,
        item: ContentItem,
        language: str,
        index: int,
        total: int,
    ) -> str:
        """Generate one item message for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        prefix = f"第 {index}/{total} 条\n\n" if language == "zh" else f"Item {index}/{total}\n\n"
        return prefix + self._format_item(item, labels, language, index).rstrip("-\n ")

    def render_action_card(self, item: ContentItem, language: str, index: int) -> str:
        """Render one Action Card with the same Markdown structure as a daily draft."""
        labels = LABELS.get(language, LABELS["en"])
        return self._format_item(item, labels, language, index)

    def _format_item(self, item: ContentItem, labels: dict, language: str, index: int) -> str:
        """Format a single ContentItem into Markdown."""
        _title = item.metadata.get(f"title_{language}") or item.title
        title = str(_title).replace("[", "(").replace("]", ")")
        url = str(item.url)
        score = item.ai_score or "?"
        meta = item.metadata
        card_id = html.escape(item.id, quote=True)
        signal_type = item.signal_type.value if item.signal_type else "NEWS"

        intro = item.intro or item.ai_summary or item.what_happened or ""
        how_to = item.how_to or item.opportunities or []
        suitable_for = item.suitable_for or item.who_should_care or item.ai_tags
        evidence = item.evidence or item.why_it_matters or "未提供具体数据"
        risk = item.credibility_risk or item.risk or ""
        background = meta.get(f"background_{language}") or meta.get("background") or ""
        discussion = (
            meta.get(f"community_discussion_{language}")
            or meta.get("community_discussion")
            or ""
        )

        if language == "zh":
            title = _pangu(title)
            intro = _pangu(intro)
            evidence = _pangu(evidence)
            risk = _pangu(risk)
            background = _pangu(background)
            discussion = _pangu(discussion)

        # Source line with parts joined by " · ", link appended at end
        source_type = item.source_type.value
        source_parts = [source_type]
        if meta.get("subreddit"):
            source_parts.append(f"r/{meta['subreddit']}")
        if meta.get("feed_name"):
            source_parts.append(meta["feed_name"])
        else:
            source_parts.append(item.author or "unknown")
        if item.published_at:
            if language == "zh":
                source_parts.append(
                    f"{item.published_at.month}月{item.published_at.day}日 "
                    f"{item.published_at:%H:%M}"
                )
            else:
                day = item.published_at.strftime("%d").lstrip("0")
                source_parts.append(item.published_at.strftime(f"%b {day}, %H:%M"))
        source_line = " \u00b7 ".join(source_parts)  # ·

        discussion_url = meta.get("discussion_url")
        if discussion_url:
            discussion_url = str(discussion_url)
            if discussion_url != url:
                source_line += f' · [{labels["discussion"]}]({discussion_url})'

        lines = [
            f'<section class="action-card" data-card-id="{card_id}" markdown="1">',
            f'<a id="item-{index}"></a>',
            f"## [{title}]({url})",
            "",
            f"**{labels['category']}**: `{signal_type}`",
            "",
            f"**{labels['intro']}**: {intro}",
            "",
            f"**{labels['how_to']}**:",
        ]

        lines.extend(self._format_list(how_to))
        lines += [
            "",
            f"**{labels['suitable_for']}**: "
            + (", ".join([f"`{x}`" for x in suitable_for]) if suitable_for else "—"),
            "",
            f"**{labels['evidence']}**: {evidence}",
        ]

        if risk:
            lines += [
                "",
                f"**{labels['risk']}**: {risk}",
            ]

        lines += [
            "",
            f"**{labels['score']}**: Score: {score} / 10",
            "",
            f"**{labels['source_link']}**: [原文]({url})",
            "",
            source_line,
        ]

        if background:
            lines.append("")
            lines.append(f"**{labels['background']}**: {background}")

        sources = meta.get("sources") or []
        if sources:
            items_html = "".join(f'<li><a href="{s["url"]}">{s["title"]}</a></li>\n' for s in sources)
            lines += [
                "",
                f'<details><summary>{labels["references"]}</summary>\n<ul>\n{items_html}\n</ul>\n</details>',
            ]

        if discussion:
            lines.append("")
            lines.append(f"**{labels['discussion']}**: {discussion}")

        if item.ai_tags:
            tags_str = ", ".join([f"`#{t}`" for t in item.ai_tags])
            lines.append("")
            lines.append(f"**{labels['tags']}**: {tags_str}")

        lines.append("")
        lines.append("</section>")
        lines.append("")
        lines.append("---")

        return "\n".join(lines) + "\n\n"

    @staticmethod
    def _format_list(items: list[str]) -> list[str]:
        if not items:
            return ["- —"]
        return [f"- {item}" for item in items]

    def _generate_empty_summary(self, date: str, total_fetched: int, labels: dict) -> str:
        """Generate summary when no high-scoring items were found."""
        return (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['empty_analyzed'].format(total=total_fetched)}\n\n"
            + labels["empty_body"]
        )
