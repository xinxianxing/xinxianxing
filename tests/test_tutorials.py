from __future__ import annotations

import json

from src.services.tutorials import (
    TUTORIAL_CATEGORIES,
    build_tutorial_markdown,
    load_access_codes,
    load_tutorials,
    write_tutorial_draft,
)


def test_load_tutorials_reads_frontmatter_and_sections(tmp_path):
    tutorial = tmp_path / "sample.md"
    tutorial.write_text(
        """---
title: "样例教程"
category: "AI副业赚钱"
summary: "一句话简介"
audience: "适合普通创作者"
source_author: "作者"
source_url: "https://example.com/post"
is_member_only: true
updated_at: "2026-07-07"
---

## source_summary

原帖核心观点。

## steps

1. 第一步
2. 第二步
""",
        encoding="utf-8",
    )

    tutorials = load_tutorials(tmp_path)

    assert len(tutorials) == 1
    assert tutorials[0].title == "样例教程"
    assert tutorials[0].category == "AI副业赚钱"
    assert tutorials[0].is_member_only is True
    assert tutorials[0].steps == "1. 第一步\n2. 第二步"


def test_write_tutorial_draft_round_trips(tmp_path):
    path = write_tutorial_draft(
        {
            "title": "测试教程",
            "category": TUTORIAL_CATEGORIES[0],
            "summary": "简介",
            "audience": "运营",
            "source_author": "作者",
            "source_url": "https://example.com",
            "is_member_only": False,
            "updated_at": "2026-07-07",
            "steps": "1. 做第一步",
        },
        tmp_path,
    )

    assert path.exists()
    tutorials = load_tutorials(tmp_path)
    assert tutorials[0].title == "测试教程"
    assert tutorials[0].is_member_only is False
    assert tutorials[0].steps == "1. 做第一步"


def test_build_tutorial_markdown_defaults_unknown_category():
    markdown = build_tutorial_markdown({"title": "测试", "category": "不存在"})

    assert 'category: "AI自动化"' in markdown


def test_load_access_codes_accepts_codes_object(tmp_path):
    path = tmp_path / "codes.json"
    path.write_text(json.dumps({"codes": [" A ", "", "B"]}), encoding="utf-8")

    assert load_access_codes(path) == ["A", "B"]
