"""CLI for enabling a file-backed channel."""

from __future__ import annotations

import argparse

from dotenv import load_dotenv
from rich.console import Console

from .channel_registry import check_channel, write_channel_file


console = Console()


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Enable a 信先行 channel")
    parser.add_argument("--channel-id", required=True)
    args = parser.parse_args()

    result = check_channel(args.channel_id, for_enable=True)
    channel = result.channel
    if channel is None:
        console.print(f"[red]{result.errors[0] if result.errors else '频道不存在'}[/red]")
        raise SystemExit(1)
    if result.errors or result.missing_secrets:
        console.print(f"[red]频道未通过启用检查：{channel.channel_name}[/red]")
        for item in result.errors + result.missing_secrets:
            console.print(f"- {item}")
        raise SystemExit(1)

    channel.active = True
    path = write_channel_file(channel)
    console.print(f"[green]已启用频道：{channel.channel_name}[/green]")
    console.print(f"配置文件：{path}")


if __name__ == "__main__":
    main()
