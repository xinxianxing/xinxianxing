#!/usr/bin/env python3
"""Local smoke check for Xinxianxing MCP integration."""

from __future__ import annotations

import asyncio
import json

from src.mcp.xinxianxing_adapter import resolve_xinxianxing_path
from src.mcp.server import xx_get_metrics
from src.mcp.service import XinxianxingPipelineService


async def _main() -> None:
    xinxianxing_path = resolve_xinxianxing_path()
    service = XinxianxingPipelineService()
    validation = await service.validate_config(
        xinxianxing_path=str(xinxianxing_path),
        check_env=False,
    )
    metrics = xx_get_metrics()

    payload = {
        "ok": True,
        "xinxianxing_path": str(xinxianxing_path),
        "config_path": validation["config_path"],
        "enabled_sources": validation["enabled_sources"],
        "languages": validation["ai"]["languages"],
        "metrics_ok": metrics["ok"],
        "metrics_tool": metrics["tool"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
