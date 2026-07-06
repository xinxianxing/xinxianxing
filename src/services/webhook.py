"""Webhook notification service for 信先行."""

import json
import logging
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timezone
from typing import Any, List, Optional, Union, cast
from urllib.parse import urlparse
import httpx

from ..ai.markdown_utils import clean_app_summary_markdown
from ..models import ContentItem, SignalType, WebhookConfig
from ..ai.summarizer import DailySummarizer

logger = logging.getLogger(__name__)


# Pattern: #{key} or #{key?param1=val1&param2=val2}
_PLACEHOLDER_RE = re.compile(r"#\{(\w+)(\?\w+=[^}]+)?\}")
_SENSITIVE_HEADER_RE = re.compile(
    r"(authorization|token|secret|signature|key|password)", re.IGNORECASE
)
_UNRESOLVED_ENV_REF_RE = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_]*\}$")
_DEFAULT_SITE_BASE_URL = "https://xinxianxing.com"
_SIGNAL_TYPE_LABELS_ZH = {
    SignalType.TUTORIAL: "教程",
    SignalType.MONEY_CASE: "赚钱案例",
    SignalType.PRODUCTIVITY_TIP: "效率技巧",
    SignalType.NEWS: "新闻",
    SignalType.TOOL: "工具",
    SignalType.TREND: "趋势",
    SignalType.CASE: "案例",
    SignalType.DEMAND: "需求",
    SignalType.POLICY: "政策",
    SignalType.RESEARCH: "研究",
}
_SIGNAL_TYPE_LABELS_EN = {
    SignalType.TUTORIAL: "Tutorial",
    SignalType.MONEY_CASE: "Money Case",
    SignalType.PRODUCTIVITY_TIP: "Productivity Tip",
    SignalType.NEWS: "News",
    SignalType.TOOL: "Tool",
    SignalType.TREND: "Trend",
    SignalType.CASE: "Case",
    SignalType.DEMAND: "Demand",
    SignalType.POLICY: "Policy",
    SignalType.RESEARCH: "Research",
}


def _truncate(value: str, limit: int, split: str) -> str:
    """Truncate a string to at most *limit* characters by splitting on *split*.

    Segments are accumulated in order until adding the next one would
    exceed *limit* characters.  Remaining segments are dropped.

    Args:
        value: The full text to truncate
        limit: Maximum number of characters allowed
        split: Delimiter to split value into segments

    Returns:
        Truncated text
    """
    segments = value.split(split)
    kept: list[str] = []
    current_chars = 0

    for seg in segments:
        # +len(split) for the delimiter that will be re-joined
        seg_chars = len(seg) + (len(split) if kept else 0)
        if kept and current_chars + seg_chars > limit:
            break
        kept.append(seg)
        current_chars += seg_chars

    return split.join(kept)


def _render(
    template: Union[str, dict, list], variables: dict
) -> Union[str, dict, list]:
    """Replace #{key} and #{key?params} placeholders in a template.

    Supports strings, dicts, and lists.  For dicts/lists, walks all
    string values recursively and replaces placeholders.

    Parameterized syntax: #{key?limit=N&split=DELIM}
      - limit: maximum number of output characters
      - split: delimiter to split the value into segments before
               accumulating up to *limit* characters

    Args:
        template: Template with #{key} placeholders — str, dict, or list
        variables: Dict mapping placeholder keys to replacement values

    Returns:
        Same type as template, with placeholders replaced
    """
    if isinstance(template, dict):
        return {k: _render(v, variables) for k, v in template.items()}
    if isinstance(template, list):
        return [_render(item, variables) for item in template]
    if isinstance(template, str):

        def _replace(match: re.Match) -> str:
            key = match.group(1)
            params_str = match.group(2)  # e.g. "?limit=500&split=---"

            value = variables.get(key)
            if value is None:
                return match.group(0)  # leave placeholder unchanged

            if not params_str:
                return str(value)

            # Parse params: ?limit=500&split=---
            raw_params = params_str.lstrip("?")
            params: dict[str, str] = {}
            for pair in raw_params.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    params[k] = v

            limit = int(params.get("limit", "0")) if "limit" in params else 0
            split_delim = params.get("split", "---")

            if limit and split_delim:
                return _truncate(str(value), limit, split_delim)

            return str(value)

        return _PLACEHOLDER_RE.sub(_replace, template)
    # int, float, bool, None — return as-is
    return template


def _format_markdown_for_webhook(value: str) -> str:
    """Flatten HTML constructs that chat/webhook Markdown often cannot render."""
    return clean_app_summary_markdown(value)


def _prepare_variables_for_body(
    raw_body: Union[str, dict, list, None], variables: dict
) -> dict:
    """Apply webhook-safe variable formatting before body rendering."""
    if raw_body is None or "summary" not in variables:
        return variables

    prepared = dict(variables)
    prepared["summary"] = _format_markdown_for_webhook(str(variables["summary"]))
    return prepared


def _isjson(s: str) -> bool:
    """Return True if the string starts with a JSON open brace."""
    s = s.strip()
    return s.startswith("{") or s.startswith("[")


def _is_feishu_platform(platform: str) -> bool:
    """Return whether platform should use Feishu/Lark card rendering."""
    return platform.lower() in {"feishu", "lark"}


def _text(value: str) -> dict[str, str]:
    """Build a Feishu plain text object."""
    return {"tag": "plain_text", "content": value}


def _markdown(content: str) -> dict[str, str]:
    """Build a Feishu Markdown component."""
    return {"tag": "markdown", "content": content}


def _collapsible_panel(title: str, content: str) -> dict[str, Any]:
    """Build a Feishu Card JSON 2.0 collapsible panel."""
    return {
        "tag": "collapsible_panel",
        "expanded": False,
        "header": {
            "title": _text(title),
            "icon": {
                "tag": "standard_icon",
                "token": "down-small-ccm_outlined",
                "size": "16px 16px",
            },
            "icon_position": "right",
            "icon_expanded_angle": -180,
        },
        "border": {"color": "grey", "corner_radius": "5px"},
        "elements": [_markdown(content)],
    }


def _clean_markdown_text(value: object, fallback: str = "") -> str:
    """Normalize small pieces of text used in webhook card snippets."""
    text = re.sub(r"\s+", " ", str(value or fallback)).strip()
    return text


def _safe_markdown_label(value: object, fallback: str = "") -> str:
    """Avoid breaking Markdown links/headings with raw bracket characters."""
    return _clean_markdown_text(value, fallback).replace("[", "(").replace("]", ")")


def _clip_text(value: object, limit: int) -> str:
    """Clip one-line webhook text without changing the underlying Action Card."""
    text = _clean_markdown_text(value)
    if len(text) <= limit:
        return text
    return text[: max(limit - 3, 0)].rstrip() + "..."


def _format_score(value: object) -> str:
    """Format a score for compact Feishu snippets."""
    if value is None or value == "":
        return "?"
    try:
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return str(value)


def _is_blank_or_unresolved_env_ref(value: str | None) -> bool:
    """Return whether an optional URL value should be treated as unset."""
    if value is None:
        return True
    text = value.strip()
    return not text or bool(_UNRESOLVED_ENV_REF_RE.fullmatch(text))


def _site_config_value(key: str) -> str:
    """Read a simple scalar key from docs/_config.yml without a YAML dependency."""
    config_path = Path("docs/_config.yml")
    if not config_path.exists():
        return ""
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$")
    try:
        lines = config_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        value = match.group(1).split("#", 1)[0].strip()
        return value.strip("\"'")
    return ""


def _normalize_site_base_url(value: str | None) -> str:
    """Normalize a configured site base URL for joining with article paths."""
    base_url = (value or "").strip().rstrip("/")
    if not base_url:
        return ""
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return base_url


def _data_config_site_base_url() -> str:
    """Read site.base_url from data/config.json without requiring Config wiring."""
    config_path = Path("data/config.json")
    if not config_path.exists():
        return ""
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    site = raw.get("site") if isinstance(raw, dict) else None
    if not isinstance(site, dict):
        return ""
    return _normalize_site_base_url(site.get("base_url"))


def _site_base_url() -> str:
    """Return the configured website base URL for item deep links."""
    data_config_base_url = _data_config_site_base_url()
    if data_config_base_url:
        return data_config_base_url

    site_url = _site_config_value("url").rstrip("/")
    baseurl = _site_config_value("baseurl").strip("/")
    if not site_url:
        return _DEFAULT_SITE_BASE_URL
    return f"{site_url}/{baseurl}" if baseurl else site_url


def _item_page_url(
    date: str,
    lang: str,
    index: int,
    site_base_url: str | None = None,
    *,
    draft_preview: bool = False,
) -> str:
    """Build the website URL for one Action Card anchor."""
    if draft_preview:
        path = f"drafts/{date}-summary-{lang}.html"
    else:
        try:
            year, month, day = date.split("-", 2)
            path = f"{year}/{month}/{day}/summary-{lang}.html"
        except ValueError:
            path = f"{date}-summary-{lang}.html"
    base_url = _normalize_site_base_url(site_base_url) or _site_base_url()
    return f"{base_url.rstrip('/')}/{path}#item-{index}"


def _extract_headers(headers_str: Optional[str]) -> dict:
    """Parse custom headers from a multi-line "Key: Value" string.

    Args:
        headers_str: Multi-line string, each line "Key: Value"

    Returns:
        dict: Parsed headers as key-value pairs
    """
    if not headers_str:
        return {}

    headers = {}
    for line in headers_str.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(":", 1)
        if len(parts) != 2:
            logger.warning("Invalid webhook header line: %s", line)
            continue
        k, v = parts[0].strip(), parts[1].strip()
        headers[k] = v

    return headers


def redact_url(url: str) -> str:
    """Return a log-safe URL without query strings or fragments."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return "<invalid-url>"
    if not parts.scheme or not parts.netloc:
        return "<redacted-url>"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    """Mask sensitive header values for logs and dry-run output."""
    return {
        key: "<redacted>" if _SENSITIVE_HEADER_RE.search(key) else value
        for key, value in headers.items()
    }


class WebhookNotifier:
    """Sends webhook notifications after pipeline completion or failure."""

    def __init__(
        self,
        config: WebhookConfig,
        console=None,
        site_base_url: str | None = None,
        draft_preview_links: bool = False,
    ):
        self.config = config
        self.site_base_url = _normalize_site_base_url(site_base_url) or _site_base_url()
        self.draft_preview_links = draft_preview_links
        if console is None:
            try:
                from rich.console import Console

                self.console = Console()
            except ImportError:

                class DummyConsole:
                    def print(self, *args, **kwargs):
                        print(*args, **kwargs)

                self.console = DummyConsole()
        else:
            self.console = console
        self.url = None
        self.paid_feishu_url = None
        self.category_feishu_urls: dict[SignalType, str] = {}
        self._validate_config()  # sets self.url or raises ValueError
        self._validate_paid_feishu_url()
        self._validate_category_feishu_urls()

    def _item_page_url(self, date: str, lang: str, index: int) -> str:
        """Build this notifier's configured public page URL for one card."""
        return _item_page_url(
            date,
            lang,
            index,
            self.site_base_url,
            draft_preview=self.draft_preview_links,
        )

    def _validate_url(self, url: str, source_label: str | None = None) -> str:
        """Validate webhook URL has a valid scheme (http/https) and hostname.
        Raises:
            ValueError: If the URL is empty, has wrong scheme, no hostname,
                        or is structurally invalid
        """
        label = source_label or f"env var '{self.config.url_env}'"
        url = url.strip()
        # Remove shell escape artifacts: \? \= \& \% before query chars
        url = re.sub(r"\\([?=&%])", r"\1", url)
        if not url:
            raise ValueError(
                f"Webhook URL is empty ({label} is set but empty)"
            )
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Webhook URL must use http or https scheme, got '{parsed.scheme or 'none'}' "
                f"({label})"
            )
        if not parsed.hostname:
            raise ValueError(
                f"Webhook URL has no hostname: '{url}' "
                f"({label})"
            )
        try:
            httpx.URL(url)
        except httpx.InvalidURL as e:
            raise ValueError(
                f"Webhook URL is structurally invalid: '{url}' — {e} "
                f"({label})"
            ) from e
        return url

    def _validate_config(self) -> None:
        """Validate webhook URL configuration and print warnings for skip scenarios.

        Raises ValueError when URL is present but invalid.
        Sets self.url to the validated URL, or leaves it None for skip scenarios.
        """
        if not self.config.url_env:
            # url_env not configured at all
            logger.warning("Webhook enabled but url_env is not configured, skipping notification.")
            self.console.print(
                "[yellow]Webhook enabled but 'url_env' is not set in config. "
                "No notification URL available, skipping.[/yellow]"
            )
            return

        raw_url = os.getenv(self.config.url_env)
        if raw_url is None:
            # env var name configured, but the env var itself doesn't exist
            logger.warning(
                "Webhook enabled but env var '%s' is not set, skipping notification.",
                self.config.url_env,
            )
            self.console.print(
                f"[yellow]Webhook enabled but env var '{self.config.url_env}' is not set "
                f"in your environment. Skipping notification.[/yellow]"
            )
            return

        # env var exists — validate the URL value (strip + scheme + hostname + httpx check)
        self.url = self._validate_url(raw_url)

    def _validate_paid_feishu_url(self) -> None:
        """Validate optional paid-user Feishu webhook URL.

        Missing/blank paid URLs intentionally skip the paid channel without
        changing the public webhook behavior.
        """
        raw_url = getattr(self.config, "paid_feishu_url", None)
        if _is_blank_or_unresolved_env_ref(raw_url):
            return
        raw_url = raw_url.strip()

        try:
            self.paid_feishu_url = self._validate_url(
                raw_url,
                source_label="webhook.paid_feishu_url",
            )
        except ValueError as exc:
            logger.warning("Invalid paid_feishu_url configured; skipping paid webhook: %s", exc)
            self.console.print(
                "[yellow]Paid Feishu webhook URL is invalid; "
                f"skipping paid notifications: {exc}[/yellow]"
            )

    def _validate_category_feishu_urls(self) -> None:
        """Validate optional Feishu webhook URLs keyed by signal type."""
        raw_mapping = getattr(self.config, "category_feishu", None) or {}
        for raw_signal, raw_url in raw_mapping.items():
            if _is_blank_or_unresolved_env_ref(raw_url):
                continue

            try:
                signal = (
                    raw_signal
                    if isinstance(raw_signal, SignalType)
                    else SignalType(str(raw_signal).upper())
                )
            except ValueError:
                logger.warning(
                    "Ignoring category_feishu entry with unknown signal type: %s",
                    raw_signal,
                )
                self.console.print(
                    "[yellow]Category Feishu webhook signal type is unknown; "
                    f"skipping {raw_signal!r}.[/yellow]"
                )
                continue

            try:
                self.category_feishu_urls[signal] = self._validate_url(
                    str(raw_url),
                    source_label=f"webhook.category_feishu.{signal.value}",
                )
            except ValueError as exc:
                logger.warning(
                    "Invalid category_feishu URL for %s; skipping category webhook: %s",
                    signal.value,
                    exc,
                )
                self.console.print(
                    "[yellow]Category Feishu webhook URL is invalid; "
                    f"skipping {signal.value}: {exc}[/yellow]"
                )

    def _render_request_components(
        self, variables: dict
    ) -> tuple[str, str | None, dict[str, str]]:
        """Render the final request URL, body, and headers for the given variables."""
        request_url = cast(str, _render(self.url or "", variables))

        content_type = "application/x-www-form-urlencoded"
        body_content = None
        raw_body = variables.get("_request_body_override", self.config.request_body)
        body_variables = _prepare_variables_for_body(raw_body, variables)

        if raw_body:
            if isinstance(raw_body, (dict, list)):
                rendered_obj = _render(raw_body, body_variables)
                body_content = json.dumps(rendered_obj, ensure_ascii=False)
                content_type = "application/json"
            elif isinstance(raw_body, str) and raw_body.strip():
                rendered = cast(str, _render(raw_body, body_variables))
                body_content = rendered
                if _isjson(rendered):
                    try:
                        json.loads(rendered)
                        content_type = "application/json"
                    except json.JSONDecodeError:
                        pass

        headers = _extract_headers(self.config.headers)
        headers["Content-Type"] = content_type
        return request_url, body_content, headers

    def _can_use_feishu_collapsible(self) -> bool:
        """Return whether this notifier should render Feishu collapsible cards."""
        platform = getattr(self.config, "platform", "generic")
        layout = getattr(self.config, "layout", "markdown")
        return _is_feishu_platform(platform) and layout == "collapsible"

    def _build_feishu_collapsible_overview(
        self,
        item_count: int,
        all_items_count: int,
        date: str,
        lang: str,
    ) -> str:
        """Build a non-redundant overview for a card that already lists item panels."""
        if lang == "zh":
            if item_count == 0:
                return (
                    f"# 信先行实用卡片 - {date}\n\n"
                    f"> 已分析 {all_items_count} 条内容，暂无达到实用度阈值的条目。"
                )
            return (
                f"# 信先行实用卡片 - {date}\n\n"
                f"> 从 {all_items_count} 条内容中筛选出 {item_count} 条教程/案例/技巧。\n\n"
                "点击下方链接即可到站内查看完整内容页面。"
            )

        if item_count == 0:
            return (
                f"# Xinxianxing Practical Cards - {date}\n\n"
                f"> Analyzed {all_items_count} items, but none met the utility threshold."
            )

        return (
            f"# Xinxianxing Practical Cards - {date}\n\n"
            f"> Selected {item_count} tutorial/case/tip cards from {all_items_count} fetched items.\n\n"
            "Open the links below to read the full pages on the site."
        )

    def _item_intro(self, item: ContentItem) -> str:
        """Return the shortest useful intro for a webhook item snippet."""
        return _clean_markdown_text(
            item.intro
            or item.ai_summary
            or item.what_happened
            or item.metadata.get("summary")
            or item.content
            or "暂无一句话简介。"
        )

    def _item_title(self, item: ContentItem, lang: str) -> str:
        """Return localized item title for webhook snippets."""
        return _safe_markdown_label(item.metadata.get(f"title_{lang}") or item.title, "Untitled")

    def _item_signal_type(self, item: ContentItem) -> SignalType | None:
        """Return the normalized signal type for an item."""
        raw_signal = item.signal_type or item.metadata.get("signal_type")
        if isinstance(raw_signal, SignalType):
            return raw_signal
        if raw_signal:
            try:
                return SignalType(str(raw_signal).upper())
            except ValueError:
                return None
        return None

    def _item_signal_label(self, item: ContentItem, lang: str) -> str:
        """Return a short category label for Feishu snippets."""
        signal = self._item_signal_type(item)
        if lang == "zh":
            return _SIGNAL_TYPE_LABELS_ZH.get(signal, "精选") if signal else "精选"
        return _SIGNAL_TYPE_LABELS_EN.get(signal, "Pick") if signal else "Pick"

    def _item_score_label(self, item: ContentItem) -> str:
        """Return the best available score for webhook snippets."""
        return _format_score(
            item.utility_score
            if item.utility_score is not None
            else item.score
            if item.score is not None
            else item.ai_score
        )

    def _build_public_digest_summary(
        self,
        important_items: List[ContentItem],
        all_items_count: int,
        date: str,
        lang: str,
    ) -> str:
        """Build ultra-compact public webhook content: tag, title, score, and link."""
        if lang == "zh":
            lines: list[str] = []
            if not important_items:
                return "今日暂无达到推送标准的卡片。"
            link_label = "查看完整内容"
        else:
            lines = []
            if not important_items:
                return "No cards met the delivery threshold today."
            link_label = "Read full card"

        for index, item in enumerate(important_items, start=1):
            title = self._item_title(item, lang)
            category = self._item_signal_label(item, lang)
            score = self._item_score_label(item)
            link = self._item_page_url(date, lang, index)
            if lines:
                lines.append("")
            lines.extend(
                [
                    f"{index}. **[{category}] {title}**",
                    f"Score {score} · [{link_label}]({link})",
                ]
            )
        return "\n".join(lines)

    def _build_public_item_summary(
        self,
        item: ContentItem,
        date: str,
        lang: str,
        index: int,
        total: int,
    ) -> str:
        """Build an ultra-compact one-item public webhook message."""
        title = self._item_title(item, lang)
        category = self._item_signal_label(item, lang)
        score = self._item_score_label(item)
        link = self._item_page_url(date, lang, index)
        if lang == "zh":
            return (
                f"**[{category}] {title}**\n\n"
                f"Score {score} · [查看完整内容]({link})"
            )
        return (
            f"**[{category}] {title}**\n\n"
            f"Score {score} · [Read full card]({link})"
        )

    def _build_paid_item_summary(
        self,
        item: ContentItem,
        date: str,
        lang: str,
        index: int,
        total: int,
    ) -> str:
        """Build a compact paid-channel item with one short intro."""
        title = self._item_title(item, lang)
        category = self._item_signal_label(item, lang)
        score = self._item_score_label(item)
        intro = _clip_text(self._item_intro(item), 40)
        link = self._item_page_url(date, lang, index)
        if lang == "zh":
            return (
                f"**[{category}] {title}**\n\n"
                f"{intro}\n\n"
                f"Score {score} · [查看完整内容]({link})"
            )

        return (
            f"**[{category}] {title}**\n\n"
            f"{intro}\n\n"
            f"Score {score} · [Read full card]({link})"
        )

    def _build_feishu_collapsible_body(
        self,
        important_items: List[ContentItem],
        all_items_count: int,
        date: str,
        lang: str,
        summarizer: DailySummarizer,
    ) -> dict[str, Any]:
        """Build a single Feishu Card JSON 2.0 message with collapsed item details."""
        overview = self._build_feishu_collapsible_overview(
            item_count=len(important_items),
            all_items_count=all_items_count,
            date=date,
            lang=lang,
        )
        elements: list[dict[str, Any]] = [_markdown(overview)]

        for item_index, item in enumerate(important_items, start=1):
            title = str(item.metadata.get(f"title_{lang}") or item.title)
            score = item.ai_score or "?"
            panel_title = f"{item_index}. {title} ⭐️ {score}/10"
            item_content = self._build_public_item_summary(
                item,
                date=date,
                lang=lang,
                index=item_index,
                total=len(important_items),
            )
            elements.append(
                _collapsible_panel(
                    panel_title,
                    _format_markdown_for_webhook(item_content),
                )
            )

        return {
            "msg_type": "interactive",
            "card": {
                "schema": "2.0",
                "config": {
                    "wide_screen_mode": True,
                    "update_multi": True,
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": (
                            f"信先行 {date} 折叠日报"
                            if lang == "zh"
                            else f"Xinxianxing {date} Collapsible Daily"
                        ),
                    },
                    "template": "blue",
                },
                "body": {
                    "elements": elements,
                },
            },
        }

    def _build_paid_feishu_card(
        self,
        title: str,
        content: str,
        *,
        template: str = "green",
    ) -> dict[str, Any]:
        """Build a Feishu interactive card for direct bot delivery."""
        return {
            "msg_type": "interactive",
            "card": {
                "schema": "2.0",
                "config": {
                    "wide_screen_mode": True,
                    "update_multi": True,
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title,
                    },
                    "template": template,
                },
                "body": {
                    "elements": [
                        _markdown(_format_markdown_for_webhook(content)),
                    ],
                },
            },
        }

    def build_paid_feishu_messages(
        self,
        paid_items: List[ContentItem],
        all_items_count: int,
        date: str,
        lang: str,
        summarizer: DailySummarizer,
        score_threshold: float | None = None,
    ) -> List[dict[str, Any]]:
        """Build concise Action Card messages for the optional paid Feishu channel."""
        if not self.paid_feishu_url:
            return []

        sorted_items = sorted(
            paid_items,
            key=lambda item: item.ai_score or 0,
            reverse=True,
        )
        threshold_text = (
            f"实用度 >= {score_threshold:g}"
            if lang == "zh" and score_threshold is not None
            else f"score >= {score_threshold:g}"
            if score_threshold is not None
            else "已达标"
        )

        if lang == "zh":
            overview = (
                f"# 信先行付费精选 - {date}\n\n"
                f"{len(sorted_items)} 条达标（{threshold_text}），"
                "按实用度排序。点链接看完整内容。"
            )
            overview_title = f"信先行付费精选卡片 - {date}"
        else:
            overview = (
                f"# Xinxianxing Paid Picks - {date}\n\n"
                f"{len(sorted_items)} cards met {threshold_text}, sorted by utility. "
                "Open links for the full version."
            )
            overview_title = f"Xinxianxing Paid Cards - {date}"

        messages = [
            self._build_paid_feishu_card(
                overview_title,
                overview,
                template="green",
            )
        ]

        for item_index, item in enumerate(sorted_items, start=1):
            title = str(item.metadata.get(f"title_{lang}") or item.title)
            if lang == "zh":
                message_title = f"{item_index}/{len(sorted_items)} {title}"
            else:
                message_title = f"{item_index}/{len(sorted_items)} {title}"
            item_content = self._build_paid_item_summary(
                item,
                date=date,
                lang=lang,
                index=item_index,
                total=len(sorted_items),
            )
            messages.append(
                self._build_paid_feishu_card(
                    message_title[:80],
                    item_content,
                    template="blue",
                )
            )

        return messages

    def _build_category_feishu_summary(
        self,
        signal: SignalType,
        indexed_items: list[tuple[int, ContentItem]],
        date: str,
        lang: str,
    ) -> str:
        """Build one category-only Feishu card body."""
        label = (
            _SIGNAL_TYPE_LABELS_ZH.get(signal, signal.value)
            if lang == "zh"
            else _SIGNAL_TYPE_LABELS_EN.get(signal, signal.value)
        )
        link_label = "查看完整内容" if lang == "zh" else "Read full card"
        if lang == "zh":
            lines = [
                f"# 信先行 · {label} - {date}",
                "",
                f"{len(indexed_items)} 条{label}内容，点击链接查看完整页面。",
            ]
        else:
            lines = [
                f"# Xinxianxing · {label} - {date}",
                "",
                f"{len(indexed_items)} {label} items. Open links for the full pages.",
            ]

        for display_index, (page_index, item) in enumerate(indexed_items, start=1):
            title = self._item_title(item, lang)
            score = self._item_score_label(item)
            link = self._item_page_url(date, lang, page_index)
            lines.extend(
                [
                    "",
                    f"{display_index}. **[{label}] {title}**",
                    f"Score {score} · [{link_label}]({link})",
                ]
            )
        return "\n".join(lines)

    def build_category_feishu_messages(
        self,
        important_items: List[ContentItem],
        date: str,
        lang: str,
    ) -> list[tuple[SignalType, dict[str, Any]]]:
        """Build category-only Feishu messages for configured signal types."""
        if not self.category_feishu_urls:
            return []

        grouped_items: dict[SignalType, list[tuple[int, ContentItem]]] = {}
        for page_index, item in enumerate(important_items, start=1):
            signal = self._item_signal_type(item)
            if signal not in self.category_feishu_urls:
                continue
            grouped_items.setdefault(signal, []).append((page_index, item))

        messages: list[tuple[SignalType, dict[str, Any]]] = []
        for signal in self.category_feishu_urls:
            indexed_items = grouped_items.get(signal, [])
            if not indexed_items:
                continue
            label = (
                _SIGNAL_TYPE_LABELS_ZH.get(signal, signal.value)
                if lang == "zh"
                else _SIGNAL_TYPE_LABELS_EN.get(signal, signal.value)
            )
            title = (
                f"信先行 {date} {label}"
                if lang == "zh"
                else f"Xinxianxing {date} {label}"
            )
            content = self._build_category_feishu_summary(
                signal=signal,
                indexed_items=indexed_items,
                date=date,
                lang=lang,
            )
            messages.append(
                (
                    signal,
                    self._build_paid_feishu_card(
                        title[:80],
                        content,
                        template="blue",
                    ),
                )
            )

        return messages

    def build_preview(self, variables: dict) -> dict[str, Any]:
        """Build the fully rendered request for dry-run preview."""
        request_url, body_content, headers = self._render_request_components(variables)
        return {
            "url": redact_url(request_url),
            "body": body_content,
            "headers": redact_headers(headers),
        }

    def build_daily_summary_messages(
        self,
        summary: str,
        important_items: List[ContentItem],
        all_items_count: int,
        date: str,
        lang: str,
        summarizer: DailySummarizer,
    ) -> List[dict[str, Any]]:
        """Build the variables for all webhook messages for one language."""
        webhook_languages = getattr(self.config, "languages", None)
        if webhook_languages and lang not in webhook_languages:
            return []

        base_vars = {
            "date": date,
            "language": lang,
            "important_items": len(important_items),
            "all_items": all_items_count,
            "result": "success",
            "timestamp": str(int(datetime.now(timezone.utc).timestamp())),
        }

        if self._can_use_feishu_collapsible():
            return [
                {
                    **base_vars,
                    "message_title": (
                        f"信先行 {date} 折叠日报"
                        if lang == "zh"
                        else f"Xinxianxing {date} Collapsible Daily"
                    ),
                    "message_kind": "collapsible",
                    "summary": self._build_feishu_collapsible_overview(
                        item_count=len(important_items),
                        all_items_count=all_items_count,
                        date=date,
                        lang=lang,
                    ),
                    "_request_body_override": self._build_feishu_collapsible_body(
                        important_items=important_items,
                        all_items_count=all_items_count,
                        date=date,
                        lang=lang,
                        summarizer=summarizer,
                    ),
                }
            ]

        delivery = getattr(self.config, "delivery", "summary")
        if delivery == "summary_and_items":
            item_messages: List[dict[str, Any]] = []
            overview = summarizer.generate_webhook_overview(
                important_items,
                date,
                all_items_count,
                language=lang,
            )
            overview_message = {
                **base_vars,
                "message_title": (
                    f"信先行 {date} 总览"
                    if lang == "zh"
                    else f"Xinxianxing {date} Overview"
                ),
                "message_kind": "overview",
                "summary": overview,
            }
            for item_index, item in enumerate(important_items, start=1):
                title = str(item.metadata.get(f"title_{lang}") or item.title)
                item_summary = self._build_public_item_summary(
                    item,
                    date=date,
                    lang=lang,
                    index=item_index,
                    total=len(important_items),
                )
                item_messages.append(
                    {
                        **base_vars,
                        "message_title": f"{item_index}/{len(important_items)} {title}",
                        "message_kind": "item",
                        "item_index": item_index,
                        "item_count": len(important_items),
                        "item_title": title,
                        "item_url": str(item.url),
                        "item_score": item.ai_score or "",
                        "summary": item_summary,
                    }
                )

            if getattr(self.config, "overview_position", "first") == "last":
                return list(reversed(item_messages)) + [overview_message]

            return [overview_message] + item_messages

        return [
            {
                **base_vars,
                "message_title": (
                    f"信先行 {date} 今日精选"
                    if lang == "zh"
                    else f"Xinxianxing {date} Picks"
                ),
                "message_kind": "summary",
                "summary": self._build_public_digest_summary(
                    important_items=important_items,
                    all_items_count=all_items_count,
                    date=date,
                    lang=lang,
                ),
            }
        ]

    async def notify(self, variables: dict) -> None:
        """Send a webhook notification with template variable substitution.

        If request_body is empty, sends a GET request.
        If request_body is provided, sends a POST request with
        auto-detected content-type

        Args:
            variables: Dict of template variable values to replace
                       in URL, request_body, and headers.
        """
        if not self.config.enabled:
            self.console.print("[yellow]Webhook is disabled, skipping notification.[/yellow]")
            return

        if not self.url:
            logger.warning(
                "Webhook enabled but URL is empty (env var %s not set), skipping notification.",
                self.config.url_env,
            )
            self.console.print(
                f"[yellow]Webhook enabled but URL is empty — "
                f"env var '{self.config.url_env}' is not set. Skipping notification.[/yellow]"
            )
            return

        request_url, body_content, headers = self._render_request_components(variables)
        safe_url = redact_url(request_url)
        if body_content is not None:
            logger.debug(
                "Webhook POST body (%d chars): %s",
                len(body_content or ""),
                (body_content or "")[:2000],
            )

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if body_content is None:
                    response = await client.get(request_url, headers=headers)
                else:
                    response = await client.post(
                        request_url,
                        content=body_content.encode("utf-8"),
                        headers=headers,
                    )

            self._handle_response_status(response, safe_url)

        except httpx.InvalidURL as e:
            self.console.print(
                f"[red]Webhook URL is invalid: {e}[/red]"
            )
            logger.error("Webhook URL invalid: %s, env var: %s", e, self.config.url_env)
        except httpx.ConnectError as e:
            self.console.print(
                f"[red]Webhook connection failed: {e}[/red]"
            )
            logger.error("Webhook connection failed: URL=%s, error=%s", safe_url, e)
        except httpx.TimeoutException as e:
            self.console.print(
                f"[red]Webhook request timed out: {e}[/red]"
            )
            logger.error("Webhook timeout: URL=%s, error=%s", safe_url, e)
        except Exception as e:
            self.console.print(
                f"[red]Webhook call failed unexpectedly: {type(e).__name__}: {e}[/red]"
            )
            logger.error("Webhook unexpected error: URL=%s, type=%s, error=%s", safe_url, type(e).__name__, e)

    async def _post_direct_feishu(
        self,
        request_url: str | None,
        body: dict[str, Any],
        channel_label: str,
    ) -> None:
        """Send one pre-rendered Feishu card to a direct bot URL."""
        if not self.config.enabled or not request_url:
            return

        safe_url = redact_url(request_url)
        body_content = json.dumps(body, ensure_ascii=False)
        headers = {"Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    request_url,
                    content=body_content.encode("utf-8"),
                    headers=headers,
                )

            self._handle_response_status(response, safe_url)

        except httpx.InvalidURL as e:
            self.console.print(f"[red]{channel_label} Feishu webhook URL is invalid: {e}[/red]")
            logger.error("%s Feishu webhook URL invalid: %s", channel_label, e)
        except httpx.ConnectError as e:
            self.console.print(f"[red]{channel_label} Feishu webhook connection failed: {e}[/red]")
            logger.error(
                "%s Feishu webhook connection failed: URL=%s, error=%s",
                channel_label,
                safe_url,
                e,
            )
        except httpx.TimeoutException as e:
            self.console.print(f"[red]{channel_label} Feishu webhook request timed out: {e}[/red]")
            logger.error("%s Feishu webhook timeout: URL=%s, error=%s", channel_label, safe_url, e)
        except Exception as e:
            self.console.print(
                f"[red]{channel_label} Feishu webhook failed unexpectedly: {type(e).__name__}: {e}[/red]"
            )
            logger.error(
                "%s Feishu webhook unexpected error: URL=%s, type=%s, error=%s",
                channel_label,
                safe_url,
                type(e).__name__,
                e,
            )

    async def notify_paid_feishu(self, body: dict[str, Any]) -> None:
        """Send one paid-channel Feishu message."""
        await self._post_direct_feishu(self.paid_feishu_url, body, "Paid")

    async def notify_category_feishu(self, signal: SignalType, body: dict[str, Any]) -> None:
        """Send one category-channel Feishu message."""
        request_url = self.category_feishu_urls.get(signal)
        await self._post_direct_feishu(request_url, body, f"Category {signal.value}")

    def _check_body_error_code(self, body: str) -> Optional[str]:
        """Check if a 2xx response body contains a platform-specific error code.

        Returns a descriptive string if an error is detected, or None if the
        response appears successful.

        Checked patterns:
        - Feishu/Lark: {"code": non-zero, "msg": "..."} or {"StatusCode": non-zero}
        - DingTalk: {"errcode": non-zero, "errmsg": "..."}
        - Slack/Discord: {"ok": false}
        """
        try:
            data = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return None

        platform = (self.config.platform or "").lower()
        check_all = platform in ("", "generic")

        if platform in ("feishu", "lark") or check_all:
            code = data.get("code") or data.get("StatusCode")
            if code is not None and code != 0:
                msg = data.get("msg") or data.get("StatusMessage") or ""
                return f"Feishu/Lark error (code={code}): {msg}"

        if platform == "dingtalk" or check_all:
            errcode = data.get("errcode")
            if errcode is not None and errcode != 0:
                msg = data.get("errmsg") or ""
                return f"DingTalk error (errcode={errcode}): {msg}"

        if platform in ("slack", "discord") or check_all:
            if data.get("ok") is False:
                error = data.get("error") or ""
                return f"Slack/Discord error: {error}"

        return None

    def _handle_response_status(self, response: httpx.Response, safe_url: str) -> None:
        """Log and display HTTP response status by category.

        Even 2xx responses may contain platform-specific error codes
        in the JSON body (e.g. Feishu code=19001, DingTalk errcode=400,
        Slack ok=false).
        """
        status = response.status_code
        body = response.text[:500]

        if 200 <= status < 300:
            error_hint = self._check_body_error_code(body)
            if error_hint:
                logger.warning(
                    "Webhook 2xx but body contains error: URL=%s, status=%d, body=%s",
                    safe_url, status, body,
                )
                self.console.print(
                    f"[yellow]Webhook response (status={status}): {body}[/yellow]\n"
                    f"[yellow]{error_hint}[/yellow]"
                )
            else:
                logger.info("Webhook sent OK. URL: %s, body: %s", safe_url, body)
                self.console.print(
                    f"[green]Webhook response (status={status}): {body}[/green]"
                )
            return

        if 300 <= status < 400:
            location = response.headers.get("location", "")
            self.console.print(
                f"[yellow]Webhook received redirect (status={status})[/yellow]"
            )
            logger.warning(
                "Webhook redirect: URL=%s, status=%d, location=%s",
                safe_url, status, location,
            )
        elif 400 <= status < 500:
            self.console.print(
                f"[red]Webhook client error (status={status}): {response.text[:500]}[/red]"
            )
            logger.error(
                "Webhook client error: URL=%s, status=%d, body=%s",
                safe_url, status, response.text[:500],
            )
        elif 500 <= status < 600:
            self.console.print(
                f"[red]Webhook server error (status={status}): {response.text[:500]}[/red]"
            )
            logger.error(
                "Webhook server error: URL=%s, status=%d, body=%s",
                safe_url, status, response.text[:500],
            )
        else:
            self.console.print(
                f"[red]Webhook unexpected status={status}: {response.text[:500]}[/red]"
            )
            logger.error("Webhook unexpected status: URL=%s, status=%d", safe_url, status)

    async def send_daily_summary(
        self,
        summary: str,
        important_items: List[ContentItem],
        all_items_count: int,
        date: str,
        lang: str,
        summarizer: DailySummarizer,
        paid_items: Optional[List[ContentItem]] = None,
        score_threshold: float | None = None,
    ) -> None:
        """Send daily summary webhook notification.

        Handles language filtering, delivery mode (summary vs summary_and_items),
        optional paid Feishu delivery, and variable construction internally.

        Args:
            summary: Full markdown summary text
            important_items: List of important content items
            all_items_count: Total number of items fetched
            date: Date string (YYYY-MM-DD)
            lang: Language code ("en" or "zh")
            summarizer: DailySummarizer instance for generating webhook overviews
            paid_items: All score-qualified items for paid-user concise delivery
            score_threshold: Score threshold used to select paid_items
        """
        messages = self.build_daily_summary_messages(
            summary=summary,
            important_items=important_items,
            all_items_count=all_items_count,
            date=date,
            lang=lang,
            summarizer=summarizer,
        )
        if not messages:
            self.console.print(
                f"🔕 Skipping {lang.upper()} webhook notification "
                f"(filtered by webhook.languages)"
            )
            return

        self.console.print(f"🔔 Sending {lang.upper()} webhook notification...")
        for message in messages:
            await self.notify(message)

        paid_messages = self.build_paid_feishu_messages(
            paid_items=paid_items if paid_items is not None else important_items,
            all_items_count=all_items_count,
            date=date,
            lang=lang,
            summarizer=summarizer,
            score_threshold=score_threshold,
        )
        if paid_messages:
            self.console.print(f"🔐 Sending {lang.upper()} paid Feishu webhook notification...")
            for message in paid_messages:
                await self.notify_paid_feishu(message)

        category_messages = self.build_category_feishu_messages(
            important_items=important_items,
            date=date,
            lang=lang,
        )
        if category_messages:
            self.console.print(f"🗂️ Sending {lang.upper()} category Feishu webhook notifications...")
            for signal, message in category_messages:
                await self.notify_category_feishu(signal, message)

    async def send_failure(
        self,
        date: str,
        error_message: str,
    ) -> None:
        """Send webhook notification when the pipeline fails.

        Args:
            date: Date string (YYYY-MM-DD)
            error_message: Description of the failure
        """
        self.console.print("🔔 Sending webhook failure notification...")
        await self.notify(
            {
                "date": date,
                "language": "",
                "important_items": 0,
                "all_items": 0,
                "result": "failed",
                "timestamp": str(int(datetime.now(timezone.utc).timestamp())),
                "message_title": "信先行 generation failed",
                "message_kind": "failure",
                "summary": f"generation failed: {error_message}",
            }
        )
