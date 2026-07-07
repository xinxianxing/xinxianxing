from __future__ import annotations

import json
from datetime import datetime, timezone

from src.models import ContentItem, SourceType
from src.services.tutorials import (
    TUTORIAL_CATEGORIES,
    build_tutorial_markdown,
    load_access_codes,
    load_tutorials,
    write_tutorial_draft,
)
from src.services.tutorial_webapp import (
    form_values,
    infer_category,
    render_page,
    validate_values,
    values_from_imported_item,
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


def test_tutorial_webapp_form_values_parses_checkbox_and_multiline():
    values = form_values(
        {
            "title": ["网页录入教程"],
            "summary": ["一句话"],
            "category": ["内容创作"],
            "steps": ["1. 第一步\n2. 第二步"],
            "is_member_only": ["1"],
        }
    )

    assert values["title"] == "网页录入教程"
    assert values["category"] == "内容创作"
    assert values["steps"] == "1. 第一步\n2. 第二步"
    assert values["is_member_only"] is True


def test_tutorial_webapp_validation_requires_title_summary_category():
    values = form_values({"category": ["不存在"]})

    errors = validate_values(values)

    assert "教程标题 必填。" in errors
    assert "一句话说明 必填。" in errors
    assert "分类无效，请从下拉框选择。" in errors


def test_tutorial_webapp_render_page_contains_local_form():
    page = render_page(success="已保存到 data/tutorials/drafts/demo.md")

    assert "信先行教程录入" in page
    assert 'action="/import"' in page
    assert 'action="/tutorials"' in page
    assert "已保存到 data/tutorials/drafts/demo.md" in page


def test_tutorial_webapp_imported_item_prefills_form_values():
    item = ContentItem(
        id="manual:url:demo",
        source_type=SourceType.MANUAL,
        title="用 AI 自动化整理客户线索",
        url="https://example.com/ai-leads",
        content=(
            "这篇文章介绍如何用 AI 自动化整理客户线索，提高销售跟进效率。\n\n"
            "第一步是收集公开资料，第二步是用模型判断优先级。"
        ),
        author="example.com",
        published_at=datetime(2026, 7, 7, tzinfo=timezone.utc),
    )

    values = values_from_imported_item(item)

    assert values["title"] == "用 AI 自动化整理客户线索"
    assert values["category"] == "AI自动化"
    assert values["source_author"] == "example.com"
    assert values["source_url"] == "https://example.com/ai-leads"
    assert values["summary"] == "这篇文章介绍如何用 AI 自动化整理客户线索，提高销售跟进效率。"
    assert "自动采集原文" in str(values["source_summary"])
    assert "第一步是收集公开资料" in str(values["source_summary"])
    assert values["updated_at"] == "2026-07-07"


def test_tutorial_webapp_infer_category_uses_keywords():
    assert infer_category("Shopify 独立站转化优化", "") == "独立站"
    assert infer_category("短视频脚本批量生成", "") == "内容创作"
    assert infer_category("GitHub 开源项目运营", "") == "开源项目"
