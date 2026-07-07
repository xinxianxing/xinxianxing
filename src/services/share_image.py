"""Render 信先行 Action Cards into a mobile share image."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1080
HEIGHT = 1440
MAX_CARDS = 8


@dataclass(frozen=True)
class ShareCard:
    """Minimal card data needed for a social sharing image."""

    title: str
    signal_type: str
    intro: str
    score: float | None = None


_SECTION_RE = re.compile(
    r'<section[^>]*class="action-card"[^>]*>(.*?)</section>',
    re.DOTALL,
)
_TITLE_RE = re.compile(r"^## \[(?P<title>.+?)\]\(.+?\)", re.MULTILINE)
_TYPE_RE = re.compile(r"\*\*栏目分类\*\*: `(?P<type>[A-Z_]+)`")
_INTRO_RE = re.compile(r"\*\*一句话简介\*\*:\s*(?P<intro>.+)")
_SCORE_RE = re.compile(r"\*\*实用度评分\*\*: Score: (?P<score>[0-9.]+) / 10")


TYPE_LABELS = {
    "TUTORIAL": "教程",
    "MONEY_CASE": "AI变现",
    "PRODUCTIVITY_TIP": "效率技巧",
    "NEWS": "资讯",
    "TOOL": "工具",
    "TREND": "趋势",
    "CASE": "案例",
    "DEMAND": "需求",
    "POLICY": "政策",
    "RESEARCH": "研究",
}

TYPE_COLORS = {
    "TUTORIAL": ("#1d4ed8", "#dbeafe"),
    "MONEY_CASE": ("#047857", "#d1fae5"),
    "PRODUCTIVITY_TIP": ("#7c3aed", "#ede9fe"),
    "NEWS": ("#475569", "#e2e8f0"),
    "TOOL": ("#be185d", "#fce7f3"),
    "TREND": ("#c2410c", "#ffedd5"),
    "CASE": ("#0f766e", "#ccfbf1"),
    "DEMAND": ("#a16207", "#fef3c7"),
    "POLICY": ("#334155", "#e2e8f0"),
    "RESEARCH": ("#4338ca", "#e0e7ff"),
}


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]


def parse_action_cards(markdown_text: str, max_cards: int = MAX_CARDS) -> list[ShareCard]:
    """Extract share-image fields from a generated Action Card draft."""
    cards: list[ShareCard] = []

    for match in _SECTION_RE.finditer(markdown_text):
        section = match.group(1)
        title_match = _TITLE_RE.search(section)
        type_match = _TYPE_RE.search(section)
        intro_match = _INTRO_RE.search(section)

        if not title_match or not intro_match:
            continue

        score_match = _SCORE_RE.search(section)
        score = None
        if score_match:
            try:
                score = float(score_match.group("score"))
            except ValueError:
                score = None

        cards.append(
            ShareCard(
                title=_clean_text(title_match.group("title")),
                signal_type=_clean_text(type_match.group("type") if type_match else "NEWS"),
                intro=_clean_text(intro_match.group("intro")),
                score=score,
            )
        )

    cards.sort(key=lambda card: card.score if card.score is not None else -1, reverse=True)
    return cards[:max_cards]


def generate_share_image(
    draft_path: Path | str,
    output_dir: Path | str = "data/share_images",
    *,
    date: str | None = None,
    max_cards: int = MAX_CARDS,
) -> Path:
    """Generate a 3:4 social sharing image from a daily draft Markdown file."""
    draft = Path(draft_path)
    markdown_text = draft.read_text(encoding="utf-8")
    cards = parse_action_cards(markdown_text, max_cards=max_cards)
    if not cards:
        raise ValueError(f"No Action Cards found in draft: {draft}")

    date = date or _date_from_path(draft) or datetime.now().strftime("%Y-%m-%d")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    image_path = output / f"{date}-share.png"

    image = render_share_image(cards, date)
    image.save(image_path)
    return image_path


def render_share_image(cards: Iterable[ShareCard], date: str) -> Image.Image:
    """Render cards into a Pillow image."""
    card_list = list(cards)[:MAX_CARDS]
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f8fafc")
    draw = ImageDraw.Draw(image)

    fonts = {
        "brand": _font(52),
        "date": _font(28),
        "title": _font(33),
        "intro": _font(25),
        "badge": _font(22),
        "meta": _font(22),
        "footer": _font(22),
    }

    _draw_header(draw, fonts, date)

    margin_x = 58
    top = 205
    bottom = 96
    gap = 18
    count = len(card_list)
    card_h = int((HEIGHT - top - bottom - gap * (count - 1)) / max(count, 1))
    card_h = max(122, min(card_h, 160))

    y = top
    for index, card in enumerate(card_list, start=1):
        _draw_card(draw, card, index, margin_x, y, WIDTH - margin_x * 2, card_h, fonts)
        y += card_h + gap

    footer = "只展示评分最高的精选卡片 · 完整内容见今日 draft"
    _draw_text(draw, (margin_x, HEIGHT - 58), footer, fonts["footer"], "#64748b")
    return image


def _draw_header(draw: ImageDraw.ImageDraw, fonts: dict[str, ImageFont.FreeTypeFont], date: str) -> None:
    header_h = 168
    for y in range(header_h):
        ratio = y / max(header_h - 1, 1)
        left = _mix_rgb((49, 46, 129), (190, 24, 93), ratio)
        right = _mix_rgb((190, 24, 93), (249, 115, 22), ratio)
        color = _mix_rgb(left, right, y / header_h)
        draw.line([(0, y), (WIDTH, y)], fill=color)

    _draw_text(draw, (58, 38), "信先行 · 今日AI精选", fonts["brand"], "#ffffff")
    _draw_text(draw, (60, 108), date, fonts["date"], "#ffedd5")
    _draw_text(draw, (WIDTH - 288, 111), "教程 / AI变现 / 效率技巧", fonts["meta"], "#ffffff")


def _draw_card(
    draw: ImageDraw.ImageDraw,
    card: ShareCard,
    index: int,
    x: int,
    y: int,
    w: int,
    h: int,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    radius = 24
    draw.rounded_rectangle((x + 4, y + 6, x + w + 4, y + h + 6), radius=radius, fill="#e2e8f0")
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill="#ffffff", outline="#e5e7eb", width=2)

    content_x = x + 32
    content_y = y + 24
    index_text = f"{index:02d}"
    _draw_text(draw, (content_x, content_y + 2), index_text, fonts["meta"], "#94a3b8")

    label = TYPE_LABELS.get(card.signal_type, card.signal_type)
    fg, bg = TYPE_COLORS.get(card.signal_type, ("#475569", "#e2e8f0"))
    badge_w = _text_width(draw, label, fonts["badge"]) + 34
    badge_h = 36
    badge_x = x + w - badge_w - 28
    badge_y = content_y
    draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=18, fill=bg)
    _draw_text(draw, (badge_x + 17, badge_y + 4), label, fonts["badge"], fg)

    title_x = content_x + 58
    title_w = badge_x - title_x - 18
    title_lines = _wrap_text(draw, card.title, fonts["title"], title_w, max_lines=1)
    title_y = content_y
    for line in title_lines:
        _draw_text(draw, (title_x, title_y), line, fonts["title"], "#0f172a")
        title_y += 39

    intro_y = title_y + 8
    intro_lines = _wrap_text(draw, card.intro, fonts["intro"], w - 64, max_lines=2)
    for line in intro_lines:
        _draw_text(draw, (content_x, intro_y), line, fonts["intro"], "#475569")
        intro_y += 31


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
    max_lines: int,
) -> list[str]:
    text = _clean_text(text)
    lines: list[str] = []
    current = ""

    for char in text:
        trial = current + char
        if _text_width(draw, trial, font) <= max_width:
            current = trial
            continue

        if current:
            lines.append(current)
            current = char.lstrip()
        else:
            lines.append(char)
            current = ""

        if len(lines) == max_lines:
            break

    if current and len(lines) < max_lines:
        lines.append(current)

    if len(lines) > max_lines:
        lines = lines[:max_lines]

    if len("".join(lines)) < len(text) and lines:
        lines[-1] = _ellipsize(draw, lines[-1], font, max_width)

    return lines or [""]


def _ellipsize(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    suffix = "..."
    while text and _text_width(draw, text + suffix, font) > max_width:
        text = text[:-1]
    return (text.rstrip() + suffix) if text else suffix


def _draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    draw.text(xy, text, font=font, fill=fill)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _mix_rgb(a: tuple[int, int, int], b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * ratio) for i in range(3))


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _date_from_path(path: Path) -> str | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    return match.group(1) if match else None
