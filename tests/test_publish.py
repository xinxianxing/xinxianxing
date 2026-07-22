from __future__ import annotations

import pytest

from src.services.publish import daily_draft_path, publish_draft, published_post_path


def _write_draft(tmp_path, run_date: str = "2026-07-22", language: str = "zh"):
    path = daily_draft_path(tmp_path, run_date, language)
    path.parent.mkdir(parents=True)
    path.write_text("---\ntitle: Reviewed draft\n---\n\n# Content\n", encoding="utf-8")
    return path


def test_publish_draft_copies_reviewed_markdown_without_removing_source(tmp_path):
    source = _write_draft(tmp_path)

    result = publish_draft("2026-07-22", root=tmp_path)

    destination = published_post_path(tmp_path, "2026-07-22", "zh")
    assert result.source == source
    assert result.destination == destination
    assert result.published is True
    assert source.exists()
    assert destination.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


def test_publish_draft_dry_run_does_not_write(tmp_path):
    _write_draft(tmp_path)

    result = publish_draft("2026-07-22", root=tmp_path, dry_run=True)

    assert result.published is False
    assert not result.destination.exists()


def test_publish_draft_refuses_to_replace_existing_post_without_force(tmp_path):
    _write_draft(tmp_path)
    destination = published_post_path(tmp_path, "2026-07-22", "zh")
    destination.parent.mkdir(parents=True)
    destination.write_text("old", encoding="utf-8")

    with pytest.raises(FileExistsError, match="Use --force"):
        publish_draft("2026-07-22", root=tmp_path)


def test_publish_draft_reports_missing_or_invalid_date(tmp_path):
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        publish_draft("2026/07/22", root=tmp_path)

    with pytest.raises(FileNotFoundError, match="Reviewed draft not found"):
        publish_draft("2026-07-22", root=tmp_path)
