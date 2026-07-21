"""Send a concise GitHub Actions failure alert to the admin Feishu webhook."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen


def main() -> None:
    webhook_url = os.getenv("XINXIANXING_ADMIN_WEBHOOK", "").strip()
    if not webhook_url:
        print("Admin webhook is not configured; skipping workflow failure alert.")
        return

    repository = os.getenv("GITHUB_REPOSITORY", "xinxianxing/xinxianxing")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    run_url = f"{server_url}/{repository}/actions/runs/{run_id}" if run_id else server_url
    generate_result = os.getenv("GENERATE_RESULT", "unknown")
    push_result = os.getenv("PUSH_RESULT", "unknown")

    payload = {
        "msg_type": "interactive",
        "card": {
            "schema": "2.0",
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "信先行自动化任务失败"},
                "template": "red",
            },
            "body": {
                "elements": [
                    {
                        "tag": "markdown",
                        "content": "\n".join(
                            [
                                f"**草稿生成**：{generate_result}",
                                f"**频道推送**：{push_result}",
                                f"[打开 GitHub Actions 日志]({run_url})",
                            ]
                        ),
                    }
                ]
            },
        },
    }
    request = Request(
        webhook_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"Unexpected status: {response.status}")
    except (OSError, RuntimeError, URLError) as exc:
        print(f"Unable to send admin failure alert: {exc}")
        raise SystemExit(1) from exc

    print("Admin failure alert sent.")


if __name__ == "__main__":
    main()
