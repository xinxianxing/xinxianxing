# Xinxianxing MCP

Xinxianxing includes a built-in MCP server that exposes the native Xinxianxing pipeline as staged tools and read-only resources.

The MCP layer does not reimplement Xinxianxing business logic. It reuses the existing fetch, score, filter, enrich, and summarize modules from the main codebase.

## Tools

| Tool | Description |
| --- | --- |
| `xx_validate_config` | Validate Xinxianxing config and required environment variables |
| `xx_fetch_items` | Fetch and deduplicate content into the `raw` stage |
| `xx_score_items` | Score items from a stage into `scored` |
| `xx_filter_items` | Filter scored items into `filtered` |
| `xx_enrich_items` | Enrich filtered items into `enriched` |
| `xx_generate_summary` | Generate markdown from a stage |
| `xx_run_pipeline` | Run fetch -> score -> filter -> enrich -> summarize |
| `xx_list_runs` | List recent run artifacts |
| `xx_get_run_meta` | Read metadata for a run |
| `xx_get_run_stage` | Read items from a run stage |
| `xx_get_run_summary` | Read a generated summary |
| `xx_get_metrics` | Read in-memory server metrics |

## Resources

- `xinxianxing://server/info`
- `xinxianxing://metrics`
- `xinxianxing://runs`
- `xinxianxing://runs/{run_id}/meta`
- `xinxianxing://runs/{run_id}/items/{stage}`
- `xinxianxing://runs/{run_id}/summary/{language}`
- `xinxianxing://config/effective`

## Install and Start

```bash
uv sync
uv run xinxianxing-mcp
```

The server runs over stdio and is intended to be launched by an MCP client.

## Run Artifacts

Each run writes artifacts under `data/mcp-runs/<run_id>/`:

- `meta.json`
- `raw_items.json`
- `scored_items.json`
- `filtered_items.json`
- `enriched_items.json`
- `summary-<lang>.md`

## Design Principles

1. Keep Xinxianxing as the single source of business logic.
2. Preserve staged re-entry so a run can continue from intermediate artifacts.
3. Default to no extra side effects unless explicitly requested.

## Client Setup

See [integration.md](integration.md).
