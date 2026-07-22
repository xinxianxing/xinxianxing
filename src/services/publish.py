"""Explicitly publish one reviewed daily draft without enabling auto-publish."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from datetime import date as date_type
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class PublishResult:
    """Paths involved in publishing one reviewed daily issue."""

    source: Path
    destination: Path
    published: bool


def daily_draft_path(root: Path, run_date: str, language: str) -> Path:
    """Return the reviewed draft path for one date and language."""
    return root / "docs" / "_drafts" / f"{run_date}-summary-{language}.md"


def published_post_path(root: Path, run_date: str, language: str) -> Path:
    """Return the public post path for one date and language."""
    return root / "docs" / "_posts" / f"{run_date}-summary-{language}.md"


def publish_draft(
    run_date: str,
    language: str = "zh",
    *,
    root: Path = ROOT,
    force: bool = False,
    dry_run: bool = False,
) -> PublishResult:
    """Copy a reviewed draft into the public posts directory.

    This intentionally does not create a git commit, deploy a site, or delete
    the draft. Publishing remains an explicit human decision and the normal
    repository deployment workflow handles the site after the user commits.
    """
    try:
        date_type.fromisoformat(run_date)
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD, for example 2026-07-22") from exc

    language = language.strip().lower()
    if not language:
        raise ValueError("language is required")

    source = daily_draft_path(root, run_date, language)
    destination = published_post_path(root, run_date, language)
    if not source.exists():
        raise FileNotFoundError(f"Reviewed draft not found: {source}")
    if destination.exists() and not force:
        raise FileExistsError(
            f"Published post already exists: {destination}. Use --force to replace it."
        )

    if dry_run:
        return PublishResult(source=source, destination=destination, published=False)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return PublishResult(source=source, destination=destination, published=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy one reviewed 信先行 draft into docs/_posts for publication."
    )
    parser.add_argument("--date", required=True, help="Draft date in YYYY-MM-DD format")
    parser.add_argument("--language", "--lang", default="zh", help="Draft language (default: zh)")
    parser.add_argument("--dry-run", action="store_true", help="Show the target without writing")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing post for the same date and language",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        result = publish_draft(
            args.date,
            args.language,
            force=args.force,
            dry_run=args.dry_run,
        )
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        raise SystemExit(f"Publish cancelled: {exc}") from exc

    if not result.published:
        print(f"Ready to publish: {result.source} -> {result.destination}")
        return

    print(f"Published reviewed draft: {result.destination}")
    print("Next: commit and push this file; the Deploy Site workflow will update Cloudflare Pages.")
