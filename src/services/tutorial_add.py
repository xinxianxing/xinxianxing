"""Interactive CLI for adding curated tutorial drafts."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from src.services.tutorials import (
    TUTORIAL_CATEGORIES,
    TUTORIAL_FIELD_LABELS,
    TUTORIAL_SECTION_FIELDS,
    write_tutorial_draft,
)


ROOT = Path(__file__).resolve().parents[2]
DRAFTS_DIR = ROOT / "data/tutorials/drafts"


def main() -> None:
    print("信先行教程库录入")
    print("按提示填写字段；多行内容单独输入一个 . 结束。\n")

    values = {
        "title": prompt_text("教程标题", required=True),
        "category": prompt_category(),
        "summary": prompt_text("一句话说明", required=True),
        "audience": prompt_text("适合谁", required=True),
        "source_author": prompt_text("原作者", required=False),
        "source_url": prompt_text("原帖链接", required=True),
        "is_member_only": prompt_bool("是否会员内容", default=True),
        "updated_at": prompt_text("更新时间", default=date.today().isoformat(), required=True),
    }

    for field in TUTORIAL_SECTION_FIELDS:
        values[field] = prompt_multiline(TUTORIAL_FIELD_LABELS[field])

    path = write_tutorial_draft(values, DRAFTS_DIR)
    print(f"\n已生成教程草稿：{path}")
    print("确认后手动移动到 data/tutorials/published/，网站构建时只读取 published。")


def prompt_text(label: str, default: str | None = None, required: bool = False) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{label}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if value or not required:
            return value
        print("这个字段必填。")


def prompt_category() -> str:
    print("分类：")
    for index, category in enumerate(TUTORIAL_CATEGORIES, start=1):
        print(f"  {index}. {category}")
    while True:
        value = input("请选择分类序号 [1]: ").strip() or "1"
        if value.isdigit():
            index = int(value)
            if 1 <= index <= len(TUTORIAL_CATEGORIES):
                return TUTORIAL_CATEGORIES[index - 1]
        if value in TUTORIAL_CATEGORIES:
            return value
        print("请输入有效分类序号。")


def prompt_bool(label: str, default: bool) -> bool:
    default_hint = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} [{default_hint}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes", "true", "1", "是"}:
            return True
        if value in {"n", "no", "false", "0", "否"}:
            return False
        print("请输入 y 或 n。")


def prompt_multiline(label: str) -> str:
    print(f"{label}：")
    print("  可输入多行，单独输入 . 结束。")
    lines: list[str] = []
    while True:
        line = input("> ")
        if line == ".":
            break
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


if __name__ == "__main__":
    main()
