"""CLI for disabling a file-backed channel."""

from __future__ import annotations

import argparse
import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from rich.console import Console

from .channel_registry import find_channel_file, write_channel_file
from .webhook import send_admin_notice


console = Console()


async def _send_disable_notice(channel_id: str, channel_name: str) -> None:
    await send_admin_notice(
        os.getenv("HORIZON_ADMIN_WEBHOOK"),
        title="信先行频道已停用",
        template="yellow",
        lines=[
            f"**频道**: {channel_name} (`{channel_id}`)",
            f"**停用时间**: {datetime.now(timezone.utc).isoformat()}",
        ],
    )


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Disable a 信先行 channel")
    parser.add_argument("--channel-id", required=True)
    args = parser.parse_args()

    path, channel = find_channel_file(args.channel_id)
    if channel is None or path is None:
        console.print(f"[red]频道不存在：{args.channel_id}[/red]")
        raise SystemExit(1)

    channel.active = False
    saved_path = write_channel_file(channel)
    console.print(f"[green]已停用频道：{channel.channel_name}[/green]")
    console.print(f"配置文件：{saved_path}")
    asyncio.run(_send_disable_notice(channel.channel_id, channel.channel_name))


if __name__ == "__main__":
    main()
