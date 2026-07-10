"""CLI for sending a test message to a file-backed channel."""

from __future__ import annotations

import argparse
import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from rich.console import Console

from ..models import WebhookConfig
from .channel_registry import find_channel_file, runtime_channels_from_file_config
from .webhook import WebhookDeliveryError, WebhookNotifier, send_admin_notice


console = Console()


def _test_card(channel_name: str, destination_type: str) -> dict:
    content = "\n".join(
        [
            f"**频道**: {channel_name}",
            f"**目标**: {destination_type}",
            f"**测试时间**: {datetime.now(timezone.utc).isoformat()}",
            "",
            "这是一条信先行频道测试消息。收到这条消息，说明 webhook 配置可用。",
        ]
    )
    return {
        "msg_type": "interactive",
        "card": {
            "schema": "2.0",
            "config": {"wide_screen_mode": True, "update_multi": True},
            "header": {
                "title": {"tag": "plain_text", "content": "信先行频道测试"},
                "template": "blue",
            },
            "body": {"elements": [{"tag": "markdown", "content": content}]},
        },
    }


async def run_channel_test(channel_id: str) -> int:
    path, channel = find_channel_file(channel_id)
    if channel is None or path is None:
        console.print(f"[red]频道不存在：{channel_id}[/red]")
        return 1

    runtime_channels = runtime_channels_from_file_config(channel)
    notifier = WebhookNotifier(
        WebhookConfig(enabled=True, url_env=None, platform="generic", layout="markdown"),
        console=console,
        channels=runtime_channels,
    )
    configured = [
        runtime for runtime in runtime_channels if runtime.id in notifier.channel_webhook_urls
    ]
    if not configured:
        reason = "没有找到已配置的 webhook 环境变量"
        console.print(f"[red]{reason}[/red]")
        await send_admin_notice(
            os.getenv(channel.admin_webhook_secret_name),
            title="信先行频道测试失败",
            template="red",
            lines=[
                f"**频道**: {channel.channel_name} (`{channel.channel_id}`)",
                f"**失败原因**: {reason}",
            ],
        )
        return 1

    failures: list[str] = []
    sent = 0
    for runtime in configured:
        try:
            await notifier.notify_channel_feishu(
                runtime,
                _test_card(channel.channel_name, runtime.destination_type or "free"),
                raise_on_error=True,
            )
            sent += 1
            console.print(f"[green]测试推送成功：{runtime.id}[/green]")
        except WebhookDeliveryError as exc:
            failures.append(f"{runtime.id}: {exc}")
            console.print(f"[red]测试推送失败：{runtime.id}: {exc}[/red]")

    if failures:
        await send_admin_notice(
            os.getenv(channel.admin_webhook_secret_name),
            title="信先行频道测试失败",
            template="red",
            lines=[
                f"**频道**: {channel.channel_name} (`{channel.channel_id}`)",
                *[f"- {failure}" for failure in failures],
            ],
        )
        return 1

    await send_admin_notice(
        os.getenv(channel.admin_webhook_secret_name),
        title="信先行频道测试成功",
        template="green",
        lines=[
            f"**频道**: {channel.channel_name} (`{channel.channel_id}`)",
            f"**成功目标数**: {sent}",
        ],
    )
    return 0


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Send a test push for one channel")
    parser.add_argument("--channel-id", required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run_channel_test(args.channel_id)))


if __name__ == "__main__":
    main()
