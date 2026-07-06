---
layout: default
title: Configuration Guide
---

# Configuration Guide

信先行 is configured through two files: a `.env` file for API keys and a `data/config.json` file for sources, AI provider, and filtering options.

## AI Providers

Configure which AI model scores and summarizes your content.

`api_key_env` is always an environment variable name, not the API key value.
Store secrets in `.env` or your shell environment, then point `api_key_env` at
that variable:

```bash
OPENAI_API_KEY=sk-your-key
GOOGLE_API_KEY=your-gemini-key
```

When 信先行 starts, environment variables have priority because
`data/config.json` does not store the secret. For local VS Code runs, create
`.env` in the repository root and launch 信先行 from that same root directory.

Common API key variable names:

| Provider | `api_key_env` value |
| --- | --- |
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` |
| Gemini | `GOOGLE_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| Aliyun DashScope | `DASHSCOPE_API_KEY` |
| Doubao | `DOUBAO_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |

**Anthropic Claude**:

```json
{
  "ai": {
    "provider": "anthropic",
    "model": "claude-sonnet-4.5-20250929",
    "api_key_env": "ANTHROPIC_API_KEY",
    "throttle_sec": 0
  }
}
```

**OpenAI**:

```json
{
  "ai": {
    "provider": "openai",
    "model": "gpt-4",
    "api_key_env": "OPENAI_API_KEY",
    "throttle_sec": 0
  }
}
```

**Gemini**:

```json
{
  "ai": {
    "provider": "gemini",
    "model": "gemini-2.0-flash",
    "api_key_env": "GOOGLE_API_KEY",
    "throttle_sec": 0
  }
}
```

**Azure OpenAI**:

```json
{
  "ai": {
    "provider": "azure",
    "model": "gpt-4o-production",
    "api_key_env": "AZURE_OPENAI_API_KEY",
    "azure_endpoint_env": "AZURE_OPENAI_ENDPOINT",
    "api_version": "2024-10-21",
    "throttle_sec": 0
  }
}
```

Set `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in your `.env`. The `model` field should be your Azure deployment name, not just the base model family name.

**MiniMax**:

```json
{
  "ai": {
    "provider": "minimax",
    "model": "MiniMax-M3",
    "api_key_env": "MINIMAX_API_KEY",
    "throttle_sec": 0
  }
}
```

Available models: `MiniMax-M3`, `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`

**Aliyun DashScope** (OpenAI-compatible):

```json
{
  "ai": {
    "provider": "ali",
    "model": "qwen-plus",
    "api_key_env": "DASHSCOPE_API_KEY",
    "throttle_sec": 0
  }
}
```

Use the [DashScope compatible-mode](https://help.aliyun.com/zh/dashscope/developer-reference/use-dashscope-by-calling-openai-api) endpoint. Set `DASHSCOPE_API_KEY` in your `.env`. Optional: set `base_url` to override the default `https://dashscope.aliyuncs.com/compatible-mode/v1`.

**Ollama**:

```json
{
  "ai": {
    "provider": "ollama",
    "model": "llama3.1",
    "api_key_env": "",
    "base_url": "http://192.168.1.10:11434",
    "throttle_sec": 0
  }
}
```

Omit `base_url` to use the default `http://localhost:11434/v1`.
For remote Ollama servers, set `ai.base_url` in `data/config.json` or set
`XINXIANXING_OLLAMA_BASE_URL` in `.env`. `OLLAMA_BASE_URL` and `OLLAMA_HOST` are
also recognized. If the value omits `/v1`, 信先行 appends it automatically
for Ollama's OpenAI-compatible endpoint.

### AI throttling

If your model has a strict per-minute request cap, you can slow the scorer down in `data/config.json`:

```json
{
  "ai": {
    "throttle_sec": 4.5
  }
}
```

- `throttle_sec`: Pause between scored items in seconds. Default is `0`.
- `4.5` is a reasonable starting point for free-tier models capped around 15 requests per minute.
- Set it back to `0` if you have enough throughput headroom and want maximum speed.

### AI Concurrency

By default, AI scoring and enrichment run one item at a time. If your API endpoint supports concurrent requests, you can increase throughput:

```json
{
  "ai": {
    "analysis_concurrency": 4,
    "enrichment_concurrency": 2
  }
}
```

- `analysis_concurrency`: Number of items scored in parallel. Default is `1`.
- `enrichment_concurrency`: Number of high-scoring items enriched in parallel. Default is `1`.
- Both values are clamped to a minimum of `1`.
- Preserve the existing retry behavior per item.
- Result ordering is preserved regardless of concurrency.
- If you also use `throttle_sec`, each concurrent task sleeps independently after finishing an item.

**Custom Base URL** (for proxies):

```json
{
  "ai": {
    "provider": "anthropic",
    "base_url": "https://your-proxy.com/v1",
    ...
  }
}
```

For OpenAI-compatible gateways, 信先行 sends `temperature` by default. If a newer reasoning-style model rejects that parameter with an error such as `temperature is deprecated for this model`, 信先行 retries once without it and remembers that capability for later requests.

## Information Sources

All sources are configured under the top-level `sources` key in `config.json`.

### GitHub

```json
{
  "sources": {
    "github": [
      {
        "type": "user_events",
        "username": "gvanrossum",
        "enabled": true
      },
      {
        "type": "repo_releases",
        "owner": "python",
        "repo": "cpython",
        "enabled": true
      }
    ]
  }
}
```

### Hacker News

```json
{
  "sources": {
    "hackernews": {
      "enabled": true,
      "fetch_top_stories": 30,
      "min_score": 100
    }
  }
}
```

### RSS Feeds

```json
{
  "sources": {
    "rss": [
      {
        "name": "Blog Name",
        "url": "https://example.com/feed.xml",
        "enabled": true,
        "category": "ai-ml"
      }
    ]
  }
}
```

### Reddit

Reddit scraping is free and does not require API keys. Subreddit posts and comments prefer `old.reddit.com`; JSON and RSS endpoints are used as fallbacks when needed.

```json
{
  "sources": {
    "reddit": {
      "enabled": true,
      "fetch_comments": 5,
      "subreddits": [
        {
          "subreddit": "MachineLearning",
          "sort": "hot",
          "fetch_limit": 25,
          "min_score": 10
        }
      ],
      "users": [
        {
          "username": "spez",
          "sort": "new",
          "fetch_limit": 10
        }
      ]
    }
  }
}
```

### Telegram

Telegram scraping uses the public web preview at `https://t.me/s/<channel>`, so no API key is required. Only public channels are supported.

```json
{
  "sources": {
    "telegram": {
      "enabled": true,
      "channels": [
        {
          "channel": "zaihuapd",
          "enabled": true,
          "fetch_limit": 20
        }
      ]
    }
  }
}
```

- `enabled` — enable or disable Telegram fetching globally
- `channels` — list of public Telegram channels to monitor
- `channel` — Telegram channel username only, without `@` or the full `https://t.me/` URL
- `fetch_limit` — maximum number of recent messages to inspect per channel per run (default: `20`)

### Twitter

Requires an [Apify](https://apify.com) account. Set `APIFY_TOKEN` in your `.env` file. The free tier includes $5/month of credit, enough for roughly 20,000 tweets.

```json
{
  "sources": {
    "twitter": {
      "enabled": true,
      "mode": "apify",
      "users": ["karpathy", "ylecun"],
      "search_queries": [
        "(AI OR ChatGPT OR Claude OR Cursor OR DeepSeek OR 大模型 OR 提示词 OR 自动化 OR 副业) lang:zh -filter:replies min_faves:50"
      ],
      "search_sort": "Top",
      "search_limit": 100,
      "fetch_limit": 20,
      "fetch_reply_text": false,
      "max_replies_per_tweet": 3,
      "max_tweets_to_expand": 10,
      "reply_min_likes": 5,
      "apify_token_env": "APIFY_TOKEN",
      "actor_id": "altimis~scweet"
    }
  }
}
```

- `mode` — `apify` uses Apify, `playwright` uses local browser cookies
- `users` — Twitter screen names to monitor, without the `@` prefix
- `search_queries` — raw Twitter/X advanced search queries. Use this for topic feeds such as Chinese AI/productivity trends.
- `search_sort` — Apify search ordering, usually `Top` for hot-topic discovery or `Latest` for fresh monitoring
- `search_limit` — maximum search tweets requested per query. The actor may enforce a minimum run size.
- `fetch_limit` — maximum profile tweets requested per run. The actor may enforce a minimum run size.
- `fetch_reply_text` — when `true`, fetch actual reply bodies for important tweets and append them under `--- Top Comments ---` so the AI can factor in community discussion. Disabled by default.
- `max_replies_per_tweet` — maximum reply lines to append per tweet (default: 3)
- `max_tweets_to_expand` — cap on how many tweets get reply expansion per run, to control Apify credit usage (default: 10)
- `reply_min_likes` — only include replies with at least this many likes (default: 0)

Example Chinese hot-topic query:

```text
(AI OR ChatGPT OR Claude OR Cursor OR DeepSeek OR 大模型 OR 提示词 OR 自动化 OR 副业) lang:zh -filter:replies min_faves:50
```

The scraper uses the `altimis/scweet` actor by default. You can override it with `actor_id` if needed.

### OpenBB Financial News

OpenBB is useful when you want equity or macro news from providers such as yfinance, Benzinga, FMP, Intrinio, Tiingo, SEC, or Federal Reserve through one SDK.

Install the optional dependency before enabling the source:

```bash
uv sync --extra openbb
```

If your platform struggles to build transitive dependencies, prefer:

```bash
uv pip install --only-binary=:all: openbb openbb-benzinga
```

```json
{
  "sources": {
    "openbb": {
      "enabled": true,
      "watchlists": [
        {
          "name": "megacaps",
          "enabled": true,
          "provider": "yfinance",
          "fetch_limit": 20,
          "category": "equities",
          "symbols": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        }
      ]
    }
  }
}
```

- `enabled` — enable or disable the OpenBB source globally
- `watchlists` — list of named ticker groups; each watchlist becomes one `news.company()` call per run
- `name` — label shown in 信先行 metadata and selection breakdowns
- `provider` — OpenBB provider name such as `yfinance` or `benzinga`
- `fetch_limit` — maximum news rows requested for that watchlist
- `category` — optional tag stored on fetched items
- `symbols` — ticker symbols to fetch together; group symbols by provider to keep requests efficient

OpenBB provider credentials are handled by the OpenBB SDK itself, using its own environment variables or user settings. 信先行 does not pass those secrets through `data/config.json`.

### OSS Insight (Trending GitHub Repos)

Pulls top star-gain repositories from the [OSS Insight](https://ossinsight.io) public API, which aggregates GitHub WatchEvents. Useful for surfacing repos that are gaining stars right now without needing to scrape GitHub Trending or query BigQuery.

```json
{
  "sources": {
    "ossinsight": {
      "enabled": true,
      "period": "past_24_hours",
      "languages": ["All", "Python", "TypeScript"],
      "keywords": [],
      "min_stars": 10,
      "max_items": 30
    }
  }
}
```

- `period` — time window for star-gain ranking. Supported: `past_24_hours`, `past_28_days`. (`past_7_days` is currently broken upstream.)
- `languages` — primary language buckets to query. Use `"All"` for the full ranking, or any GitHub language label such as `"Python"`, `"TypeScript"`, `"Rust"`, `"Jupyter Notebook"`. The scraper fans out one request per language and merges results.
- `keywords` — optional case-insensitive substrings matched against `description`, `collection_names`, and `repo_name`. Only repos containing at least one keyword pass through. Leave empty to ingest everything trending.
- `min_stars` — drop repos with fewer than this many stars gained in the period.
- `max_items` — final cap after merging and sorting by `stars_gained` descending.

No API key is required.

## Filtering

Content is scored 0-10:

- **9-10**: Groundbreaking - Major breakthroughs, paradigm shifts
- **7-8**: High Value - Important developments, deep technical content
- **5-6**: Interesting - Worth knowing but not urgent
- **3-4**: Low Priority - Generic or routine content
- **0-2**: Noise - Spam, off-topic, or trivial

```json
{
  "filtering": {
    "ai_score_threshold": 7.0,
    "time_window_hours": 24,
    "max_items": 20,
    "category_groups": {
      "ai": {
        "name": "AI / Machine Learning",
        "limit": 5,
        "categories": ["ai-news", "ai-tools", "machine-learning", "llm"]
      },
      "finance": {
        "name": "Finance",
        "limit": 5,
        "categories": ["finance", "equities", "crypto"]
      }
    },
    "default_group": "other",
    "default_group_limit": 3
  }
}
```

- `ai_score_threshold`: Only include content scoring >= this value
- `time_window_hours`: Fetch content from last N hours
- `max_items`: Optional final cap after all group limits are applied
- `category_groups`: Optional map of quota groups. Each group requires a positive
  `limit` and a non-empty `categories` list. Items within each group are kept by
  AI score, highest first.
- `category_groups.*.name`: Optional display name used in run logs
- `default_group`: Group key for items whose category does not match any
  configured group. Default is `other`.
- `default_group_limit`: Optional positive limit for unmatched items. If omitted,
  unmatched items are unlimited except for `max_items`.

Balanced digest filtering runs after AI score threshold filtering and topic
deduplication, but before enrichment. This reduces enrichment calls to only the
items that can appear in the final digest.

Group matching uses the source category stored in `ContentItem.metadata.category`.
RSS sources expose this through `sources.rss[].category`, and OpenBB watchlists
through `sources.openbb.watchlists[].category`. Sources without a category enter
the default group.

If the same category appears in multiple groups, 信先行 logs a warning and uses
the first group in configuration order. Omitting both `category_groups` and
`max_items` preserves the previous filtering behavior.

## Environment Variable Substitution

Any string value in `data/config.json` supports `${VAR_NAME}` syntax. Variables are expanded at runtime from the environment (including values loaded from `.env`). This lets you keep secrets, tenant-specific endpoints, and private URLs out of the checked-in JSON file.

Example:

```json
{
  "ai": {
    "base_url": "${XINXIANXING_AI_BASE_URL}"
  },
  "sources": {
    "rss": [
      {
        "name": "LWN.net",
        "url": "https://lwn.net/headlines/full_text?key=${LWN_KEY}",
        "enabled": true
      }
    ]
  },
  "webhook": {
    "url_env": "XINXIANXING_WEBHOOK_URL",
    "headers": "Authorization: Bearer ${XINXIANXING_WEBHOOK_TOKEN}"
  }
}
```

- `${NAME}` is replaced only when `NAME` is a valid identifier like `LWN_KEY` or `XINXIANXING_AI_BASE_URL`.
- Unset variables are left as `${NAME}` instead of becoming an empty string, so configuration mistakes fail loudly downstream.
- Expansion is recursive through dicts, lists, and tuples; non-string values are left unchanged.

## Email Subscription

Email delivery is optional and disabled unless `email.enabled` is `true`. 信先行 uses SMTP to send daily summaries and IMAP to check subscribe/unsubscribe requests.

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "smtp_username": null,
    "imap_enabled": true,
    "imap_server": "imap.qq.com",
    "imap_port": 993,
    "email_address": "xxx@qq.com",
    "password_env": "EMAIL_PASSWORD",
    "sender_name": "信先行 Daily",
    "subscribe_keyword": "SUBSCRIBE",
    "unsubscribe_keyword": "UNSUBSCRIBE"
  }
}
```

- `enabled`: Turns email subscription handling and daily email delivery on or off.
- `smtp_server` / `smtp_port`: SMTP server used to send emails.
- `smtp_username`: Optional SMTP login username. If omitted, 信先行 uses `email_address`.
- `imap_enabled`: Turns IMAP subscribe/unsubscribe checks on or off. Set it to `false` for send-only SMTP providers.
- `imap_server` / `imap_port`: IMAP server used to scan incoming subscription requests when `imap_enabled` is `true`.
- `email_address`: Sender account and mailbox checked for subscription requests.
- `password_env`: Environment variable containing the email password or app password. Defaults to `EMAIL_PASSWORD`.
- `sender_name`: Display name shown in sent emails.
- `subscribe_keyword` / `unsubscribe_keyword`: Keywords 信先行 looks for in incoming email subjects.

Resend SMTP example:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.resend.com",
    "smtp_port": 465,
    "smtp_username": "resend",
    "password_env": "RESEND_API_KEY",
    "imap_enabled": false,
    "imap_server": "",
    "imap_port": 993,
    "email_address": "noreply@example.com",
    "sender_name": "信先行 Daily"
  }
}
```

Set `RESEND_API_KEY` in `.env`. Recipients are loaded from `data/subscribers.json`.

## Webhook Notification

Webhook notification is optional and disabled unless `webhook.enabled` is `true`. 信先行 can call Feishu/Lark, DingTalk, Slack, Discord, or any custom webhook endpoint when the pipeline succeeds or fails.

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "XINXIANXING_WEBHOOK_URL",
    "paid_feishu_url": "",
    "delivery": "summary",
    "overview_position": "first",
    "platform": "generic",
    "layout": "markdown",
    "fallback_layout": "markdown",
    "languages": null,
    "request_body": {
      "text": "#{message_title}\n#{summary}"
    },
    "headers": ""
  }
}
```

- `enabled`: Turns webhook delivery on or off. The default is `false`.
- `url_env`: Environment variable that contains the webhook URL. For example, set `XINXIANXING_WEBHOOK_URL=https://...` in `.env`.
- `paid_feishu_url`: Optional direct Feishu/Lark bot URL for the paid-user channel. Leave it blank to skip paid delivery without affecting the public webhook.
- `delivery`: Controls how messages are sent. Use `summary` for one full message, or `summary_and_items` for one overview message followed by one message per selected item.
- `overview_position`: Controls where the overview is sent in `summary_and_items` mode. Use `first` for the traditional order, or `last` to send item details in reverse and keep the overview as the newest chat message.
- `platform`: Optional webhook platform hint. Use `generic` by default, or `feishu` / `lark` to enable platform-specific card rendering.
- `layout`: Controls the message layout. Use `markdown` for templated Markdown delivery, or `collapsible` with `platform: "feishu"` / `"lark"` for a single Feishu Card JSON 2.0 message with each item in a collapsed panel.
- `fallback_layout`: Reserved fallback layout for unsupported platform/layout combinations. The current safe fallback is `markdown`.
- `languages`: Optional webhook-only language filter. Use `["zh"]` or `["en"]` to send only selected languages; use `null` or omit it to send all configured `ai.languages`.
- `request_body`: Optional request body. If empty, 信先行 sends a `GET` request. If provided, 信先行 sends a `POST` request.
- `headers`: Optional custom headers, one `Key: Value` pair per line.

When `request_body` is a JSON object or array, 信先行 renders placeholders and serializes it as JSON. When it is a string, 信先行 renders it directly and detects JSON if the rendered string is valid JSON.

### Delivery Modes And Layouts

`delivery` controls how many webhook messages 信先行 sends:

- `summary`: Sends one message containing the full daily summary. This is simple, but some chat platforms may reject long messages.
- `summary_and_items`: Sends one overview message plus one message per selected item. In each item message, `#{summary}` contains only that item's Markdown body. This is useful for platforms that reject or truncate long messages.

`layout` controls how each message is rendered:

- `markdown`: Uses your `request_body` template for each message. This is the default and works with generic webhooks, DingTalk, Slack, Discord, Feishu, and Lark.
- `collapsible`: Currently supported for `platform: "feishu"` or `"lark"`. 信先行 ignores `request_body` and builds one Feishu/Lark Card JSON 2.0 message with each item in a collapsed panel.

For platforms without a platform-specific layout, keep `layout: "markdown"` and choose the message count with `delivery`.

Example `summary_and_items` Markdown delivery config:

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "XINXIANXING_WEBHOOK_URL",
    "delivery": "summary_and_items",
    "overview_position": "last",
    "platform": "generic",
    "layout": "markdown",
    "request_body": {
      "text": "#{message_title}\n\n#{summary?limit=3000&split=---}"
    }
  }
}
```

With `summary_and_items`, 信先行 sends one overview plus one message per selected item. `overview_position: "last"` sends item messages first and keeps the overview as the newest chat message; omit it or set `"first"` to send the overview first.

### Webhook Templates

Available variables:

| Variable | Description |
|----------|-------------|
| `#{date}` | Report date, for example `2026-04-24` |
| `#{language}` | Language code, such as `en` or `zh` |
| `#{important_items}` | Number of items that passed the score threshold |
| `#{all_items}` | Total number of fetched items |
| `#{result}` | `success` or `failed` |
| `#{timestamp}` | Unix timestamp |
| `#{message_title}` | Message title, such as the daily title, overview title, or item title |
| `#{message_kind}` | Message kind: `summary`, `overview`, `item`, `failure`, or `manual` |
| `#{summary}` | Message Markdown. In `summary_and_items` mode this is the overview or one item body, depending on the message |

When `delivery` is `summary_and_items`, item messages also include:

| Variable | Description |
|----------|-------------|
| `#{item_index}` | 1-based item number |
| `#{item_count}` | Total number of item messages |
| `#{item_title}` | Current item title |
| `#{item_url}` | Current item URL |
| `#{item_score}` | Current item AI score |

For webhook delivery, 信先行 flattens HTML disclosure blocks such as `<details><summary>...</summary>` in `#{summary}` into plain Markdown link lists. This makes the generated summary easier to render in chat products. Saved Markdown files, GitHub Pages, and email content are unchanged.

When `paid_feishu_url` is configured, 信先行 also sends a separate paid-channel Feishu card after the public webhook. The public webhook sends only the title, category, score, and site link for each selected item. The paid channel receives all score-qualified items for the day, but still keeps the Feishu message concise: title, category, score, one short intro, and a link to the full site content. If the URL is blank or invalid, paid delivery is skipped and the public webhook continues normally.

Use `#{key?limit=N&split=DELIM}` to truncate long values by splitting on `DELIM` and keeping segments until the total character count reaches `N`.

```text
#{summary?limit=3000&split=---}
```

### DingTalk

In DingTalk, create a custom group robot and use a custom keyword such as `信先行`. The keyword must appear in the body content.

```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "信先行 #{date} Daily",
    "text": "信先行 result: #{result}\n\n信先行 important items: #{important_items}/#{all_items}\n\n#{summary}"
  }
}
```

### Feishu / Lark

In Feishu or Lark, create a custom group robot and use a custom keyword such as `信先行`. The keyword must appear in the body content.

Use Card JSON 2.0 for Markdown rendering. The card must include `"schema": "2.0"` and put rich-text Markdown components under `card.body.elements`.

To keep the group chat compact while still allowing readers to browse the full briefing inside Feishu, use the collapsible layout:

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "XINXIANXING_WEBHOOK_URL",
    "platform": "feishu",
    "layout": "collapsible",
    "fallback_layout": "markdown",
    "languages": ["zh"]
  }
}
```

With this layout, 信先行 sends one interactive card containing the overview and one collapsed panel per selected item. Each panel keeps the group chat compact with the item title, category, score, and full-content link. The regular `request_body` template is ignored for this rendered card.

```json
{
  "msg_type": "interactive",
  "card": {
    "schema": "2.0",
    "config": {
      "wide_screen_mode": true
    },
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "#{message_title}"
      },
      "template": "blue"
    },
    "body": {
      "elements": [
        {
          "tag": "markdown",
          "content": "信先行 result: #{result}\n信先行 important items: #{important_items}/#{all_items}"
        },
        {
          "tag": "hr"
        },
        {
          "tag": "markdown",
          "content": "#{summary}"
        }
      ]
    }
  }
}
```

## GitHub Actions Daily Drafts

`.github/workflows/daily-summary.yml` runs once per day at 00:00 UTC, which is
08:00 in Asia/Shanghai. The workflow uses `data/config.github.json`, maps
runtime secrets from GitHub Actions Secrets, runs `uv run xinxianxing --hours 24`,
and commits only generated review artifacts:

- `data/drafts/`
- `docs/_drafts/`
- `data/share_images/`

The workflow explicitly checks that `publishing.auto_publish` is `false` and
fails if `docs/_posts/` is changed. Moving reviewed drafts into `docs/_posts/`
remains a manual publishing step.

Required GitHub Actions Secrets for the current configuration:

- `DEEPSEEK_API_KEY`: DeepSeek API key used by `ai.api_key_env`.
- `APIFY_TOKEN`: Apify API token used by the Twitter/X scraper.
- `XINXIANXING_WEBHOOK_URL`: Public Feishu/Lark bot webhook URL.

Optional:

- `XINXIANXING_PAID_FEISHU_URL`: Paid-channel Feishu/Lark bot webhook URL. If it is
  unset, the paid push is skipped and the public push still runs.

## Static Site

信先行 writes generated summaries to `data/summaries/` when `publishing.auto_publish` is `true`. By default, `auto_publish` is `false`, so generated Action Cards are saved for review in `data/drafts/` and copied to `docs/_drafts/`. When you manually approve a draft, move it into the configured publish location such as `docs/_posts/`.

To use GitHub Pages, enable Pages for the repository and run the scheduled workflow or trigger it manually. The generated site is built from the `docs/` directory.

### Manual URL Add

Use `xinxianxing-add` when you already have a useful public article or tweet URL and want to generate an Action Card without waiting for the scheduled scraper run:

```bash
uv run xinxianxing-add "https://example.com/article"
```

Optional flags:

- `--date YYYY-MM-DD`: Append to a specific draft date. Defaults to the current UTC day.
- `--lang zh`: Draft language. Defaults to `zh`.

The command fetches the public page, extracts readable text, reuses the existing Action Card prompt and AI analysis flow, then appends the card to the matching files under `data/drafts/` and `docs/_drafts/`. If the page requires login, blocks automated requests, has a non-page content type, times out, or contains too little readable text, the command exits with a clear error message and does not silently write an incomplete card.

### Share Images

After `uv run xinxianxing` finishes generating the daily draft, 信先行 automatically creates one 3:4 mobile share image from the highest-scoring Action Cards in the selected draft. The image is saved under:

```text
data/share_images/YYYY-MM-DD-share.png
```

The share image renderer reads the existing draft Markdown directly; it does not call AI again and does not publish to any third-party platform. If the draft is empty, missing Action Card sections, or the image cannot be written, the main run logs a warning and continues instead of failing the whole pipeline.

## MCP Server

信先行 includes an MCP server for AI assistants and MCP-compatible clients.

```bash
uv run xinxianxing-mcp
```

Available tools include `xx_validate_config`, `xx_fetch_items`, `xx_score_items`, `xx_filter_items`, `xx_enrich_items`, `xx_generate_summary`, and `xx_run_pipeline`.

See [`src/mcp/README.md`](../src/mcp/README.md) for the full tool reference and [`src/mcp/integration.md`](../src/mcp/integration.md) for client setup.
