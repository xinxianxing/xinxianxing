"""CLI for validating file-backed channel configuration."""

from __future__ import annotations

import argparse

from dotenv import load_dotenv
from rich.console import Console

from .channel_registry import LEGACY_SECRET_ALIASES, check_channel


console = Console()


def print_check_result(channel_id: str) -> int:
    """Print check result. Returns process-style exit code."""
    result = check_channel(channel_id)
    channel_name = result.channel.channel_name if result.channel else channel_id
    console.print(f"频道：{channel_name}")
    console.print(f"状态：{result.status}")
    if result.path:
        console.print(f"配置文件：{result.path}")

    missing = result.errors + result.warnings + result.missing_secrets
    if missing:
        console.print("缺失配置：")
        for item in missing:
            console.print(f"- {item}")
            aliases = LEGACY_SECRET_ALIASES.get(item, ())
            if aliases:
                console.print(f"  可复用旧 Secret：{', '.join(aliases)}")
    else:
        console.print("[green]配置检查通过[/green]")

    return 0 if result.can_enable else 1


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Check a 信先行 channel config")
    parser.add_argument("--channel-id", required=True)
    args = parser.parse_args()
    raise SystemExit(print_check_result(args.channel_id))


if __name__ == "__main__":
    main()
