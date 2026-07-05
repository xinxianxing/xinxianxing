from pathlib import Path

from PIL import Image
import pytest

from src.services.share_image import generate_share_image, parse_action_cards, render_share_image


SAMPLE_DRAFT = """# 信先行实用卡片 - 2026-07-02

<section class="action-card" data-card-id="one" markdown="1">
<a id="item-1"></a>
## [低分内容](https://example.com/one)

**栏目分类**: `NEWS`

**一句话简介**: 这条内容不太适合普通人实践。

**实用度评分**: Score: 4.0 / 10

</section>

<section class="action-card" data-card-id="two" markdown="1">
<a id="item-2"></a>
## [提示词工作流](https://example.com/two)

**栏目分类**: `TUTORIAL`

**一句话简介**: 用固定步骤把提示词从单句升级为可复用工作流。

**实用度评分**: Score: 8.0 / 10

</section>
"""


def test_parse_action_cards_sorts_by_score():
    cards = parse_action_cards(SAMPLE_DRAFT)

    assert [card.title for card in cards] == ["提示词工作流", "低分内容"]
    assert cards[0].signal_type == "TUTORIAL"
    assert cards[0].intro.startswith("用固定步骤")


def test_parse_action_cards_skips_incomplete_cards_and_defaults_type():
    draft = """
<section class="action-card" markdown="1">
## [没有简介](https://example.com/missing-intro)

**栏目分类**: `TUTORIAL`

</section>

<section class="action-card" markdown="1">
## [默认分类](https://example.com/default-type)

**一句话简介**: 没有栏目分类时应默认按 NEWS 处理。

**实用度评分**: Score: 8..0 / 10

</section>
"""

    cards = parse_action_cards(draft)

    assert len(cards) == 1
    assert cards[0].title == "默认分类"
    assert cards[0].signal_type == "NEWS"
    assert cards[0].score is None


def test_generate_share_image_writes_png(tmp_path: Path):
    draft = tmp_path / "xinxianxing-2026-07-02-zh.md"
    draft.write_text(SAMPLE_DRAFT, encoding="utf-8")

    image_path = generate_share_image(draft, tmp_path / "share_images", date="2026-07-02")

    assert image_path.name == "2026-07-02-share.png"
    with Image.open(image_path) as image:
        assert image.size == (1080, 1440)


def test_generate_share_image_uses_date_from_draft_filename(tmp_path: Path):
    draft = tmp_path / "xinxianxing-2026-07-03-zh.md"
    draft.write_text(SAMPLE_DRAFT, encoding="utf-8")

    image_path = generate_share_image(draft, tmp_path / "share_images")

    assert image_path.name == "2026-07-03-share.png"


def test_generate_share_image_raises_when_draft_has_no_cards(tmp_path: Path):
    draft = tmp_path / "xinxianxing-2026-07-04-zh.md"
    draft.write_text("# 空草稿\n\n暂无内容", encoding="utf-8")

    with pytest.raises(ValueError, match="No Action Cards found"):
        generate_share_image(draft, tmp_path / "share_images")


def test_render_share_image_handles_empty_card_iterable():
    image = render_share_image([], "2026-07-05")

    assert image.size == (1080, 1440)
