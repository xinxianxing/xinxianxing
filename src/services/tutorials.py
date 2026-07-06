"""Utilities for the manually curated tutorial library."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


TUTORIAL_CATEGORIES = [
    "AI自动化",
    "AI副业赚钱",
    "电商运营",
    "独立站",
    "内容创作",
    "开源项目",
    "海外获客",
]

TUTORIAL_METADATA_FIELDS = [
    "title",
    "category",
    "summary",
    "audience",
    "source_author",
    "source_url",
    "is_member_only",
    "updated_at",
]

TUTORIAL_SECTION_FIELDS = [
    "source_summary",
    "steps",
    "tools",
    "prompt_template",
    "case_result",
    "alternatives",
    "cost_and_effect",
    "risk_notice",
]

TUTORIAL_FIELD_LABELS = {
    "title": "教程标题",
    "category": "分类",
    "summary": "一句话说明",
    "audience": "适合谁",
    "source_author": "原作者",
    "source_url": "原帖链接",
    "source_summary": "原帖核心观点",
    "steps": "中文步骤拆解",
    "tools": "使用工具",
    "prompt_template": "可复制Prompt",
    "case_result": "实操案例/实测结果",
    "alternatives": "国内可替代方案",
    "cost_and_effect": "成本与预计效果",
    "risk_notice": "风险和注意事项",
    "is_member_only": "是否会员内容",
    "updated_at": "更新时间",
}

SECTION_ALIASES = {
    field: field for field in TUTORIAL_SECTION_FIELDS
}
SECTION_ALIASES.update(
    {
        "原帖核心观点": "source_summary",
        "中文步骤拆解": "steps",
        "使用工具": "tools",
        "可复制Prompt": "prompt_template",
        "实操案例/实测结果": "case_result",
        "实操案例": "case_result",
        "实测结果": "case_result",
        "国内可替代方案": "alternatives",
        "成本与预计效果": "cost_and_effect",
        "风险和注意事项": "risk_notice",
    }
)


@dataclass(frozen=True)
class Tutorial:
    source: Path
    slug: str
    title: str
    category: str
    summary: str
    audience: str
    source_author: str
    source_url: str
    source_summary: str
    steps: str
    tools: str
    prompt_template: str
    case_result: str
    alternatives: str
    cost_and_effect: str
    risk_notice: str
    is_member_only: bool
    updated_at: str


def load_tutorials(directory: Path) -> list[Tutorial]:
    """Load published tutorial Markdown files from a directory."""

    if not directory.exists():
        return []

    tutorials: list[Tutorial] = []
    for path in sorted(directory.glob("*.md")):
        front, body = split_front_matter(path.read_text(encoding="utf-8"))
        sections = parse_sections(body)
        title = str(front.get("title") or path.stem).strip()
        category = normalize_category(str(front.get("category") or ""))
        values = {
            field: str(sections.get(field) or front.get(field) or "").strip()
            for field in TUTORIAL_SECTION_FIELDS
        }
        tutorials.append(
            Tutorial(
                source=path,
                slug=slug_from_path(path),
                title=title,
                category=category,
                summary=str(front.get("summary") or "").strip(),
                audience=str(front.get("audience") or "").strip(),
                source_author=str(front.get("source_author") or "").strip(),
                source_url=str(front.get("source_url") or "").strip(),
                source_summary=values["source_summary"],
                steps=values["steps"],
                tools=values["tools"],
                prompt_template=values["prompt_template"],
                case_result=values["case_result"],
                alternatives=values["alternatives"],
                cost_and_effect=values["cost_and_effect"],
                risk_notice=values["risk_notice"],
                is_member_only=parse_bool(front.get("is_member_only"), default=True),
                updated_at=str(front.get("updated_at") or "").strip(),
            )
        )

    tutorials.sort(key=lambda item: (item.updated_at, item.title), reverse=True)
    return tutorials


def load_access_codes(path: Path) -> list[str]:
    """Read simple tutorial unlock codes from a JSON file."""

    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    raw_codes: Any
    if isinstance(payload, dict):
        raw_codes = payload.get("codes", [])
    else:
        raw_codes = payload
    if not isinstance(raw_codes, list):
        return []
    return [str(code).strip() for code in raw_codes if str(code).strip()]


def write_tutorial_draft(values: dict[str, Any], drafts_dir: Path) -> Path:
    """Write a tutorial Markdown draft and return the created path."""

    drafts_dir.mkdir(parents=True, exist_ok=True)
    title = str(values.get("title") or "untitled").strip()
    slug = slugify(title)
    path = drafts_dir / f"{date.today().isoformat()}-{slug}.md"
    suffix = 2
    while path.exists():
        path = drafts_dir / f"{date.today().isoformat()}-{slug}-{suffix}.md"
        suffix += 1

    path.write_text(build_tutorial_markdown(values), encoding="utf-8")
    return path


def build_tutorial_markdown(values: dict[str, Any]) -> str:
    """Serialize tutorial values into Markdown with frontmatter and sections."""

    front = {
        "title": str(values.get("title") or "").strip(),
        "category": normalize_category(str(values.get("category") or "")),
        "summary": str(values.get("summary") or "").strip(),
        "audience": str(values.get("audience") or "").strip(),
        "source_author": str(values.get("source_author") or "").strip(),
        "source_url": str(values.get("source_url") or "").strip(),
        "is_member_only": parse_bool(values.get("is_member_only"), default=True),
        "updated_at": str(values.get("updated_at") or date.today().isoformat()).strip(),
    }
    sections = {
        field: str(values.get(field) or "").strip()
        for field in TUTORIAL_SECTION_FIELDS
    }

    front_lines = ["---"]
    for field in TUTORIAL_METADATA_FIELDS:
        value = front[field]
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = json.dumps(value, ensure_ascii=False)
        front_lines.append(f"{field}: {rendered}")
    front_lines.append("---")

    body_lines: list[str] = []
    for field in TUTORIAL_SECTION_FIELDS:
        body_lines.append(f"## {field}")
        body_lines.append("")
        body_lines.append(sections[field])
        body_lines.append("")
    return "\n".join(front_lines + [""] + body_lines).rstrip() + "\n"


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    front: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = parse_front_value(value.strip())
    return front, body


def parse_front_value(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    return value.strip("'")


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            label = heading.group(1).strip()
            current = SECTION_ALIASES.get(label, label)
            if current in TUTORIAL_SECTION_FIELDS:
                sections.setdefault(current, [])
            else:
                current = None
            continue
        if current:
            sections.setdefault(current, []).append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def normalize_category(value: str) -> str:
    cleaned = value.strip()
    if cleaned in TUTORIAL_CATEGORIES:
        return cleaned
    return TUTORIAL_CATEGORIES[0]


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "否"}:
        return False
    return default


def slug_from_path(path: Path) -> str:
    name = path.with_suffix("").name
    dated = re.match(r"\d{4}-\d{2}-\d{2}-(.+)", name)
    return dated.group(1) if dated else name


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    if slug:
        return slug[:72]
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"tutorial-{digest}"
