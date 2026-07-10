---
layout: default
title: Source Scrapers
---

# Source Scrapers

信先行 fetches content from multiple source types. All scrapers inherit from `BaseScraper`, share an async HTTP client, and implement a `fetch(since)` method that returns a list of `ContentItem` objects. Sources are fetched concurrently via `asyncio.gather`.

Every configured source can expose a stable `id` used by the `sources` field in
`config/channels/*.json` for multi-group routing. If an `id` is omitted, scrapers derive one from the
source type and name, such as `hackernews`, `twitter`, `reddit_artificial`, or
`rss_simon_willison`. Each fetched `ContentItem` stores this in
`metadata.source_id` and `metadata.source_ids`.

## Hacker News

**File**: `src/scrapers/hackernews.py`

Uses the [Firebase HN API](https://hacker-news.firebaseio.com/v0):

- `GET /topstories.json` — fetches top story IDs
- `GET /item/{id}.json` — fetches story/comment details

Stories and their comments are fetched concurrently. For each story, the top 5 comments are included (deleted/dead comments excluded, HTML stripped, truncated at 500 chars).

**Config** (`sources.hackernews`):

```json
{
  "id": "hackernews",
  "enabled": true,
  "fetch_top_stories": 30,
  "min_score": 100
}
```

- `fetch_top_stories` — number of top story IDs to fetch
- `min_score` — minimum HN points to include a story

**Extracted data**: title, URL (falls back to HN discussion URL), author, score, comment count, and top comment text.

## GitHub

**File**: `src/scrapers/github.py`

Uses the [GitHub REST API](https://api.github.com):

- `GET /users/{username}/events/public` — user activity events
- `GET /repos/{owner}/{repo}/releases` — repository releases

Two source types are supported:

- **`user_events`** — tracks push, create, release, public, and watch events for a user
- **`repo_releases`** — tracks new releases for a specific repository

**Config** (`sources.github`, list of entries):

```json
{
  "id": "github_torvalds",
  "type": "user_events",
  "username": "torvalds",
  "enabled": true
}
```

```json
{
  "id": "github_go_releases",
  "type": "repo_releases",
  "owner": "golang",
  "repo": "go",
  "enabled": true
}
```

**Authentication**: Set `GITHUB_TOKEN` in your environment for higher rate limits (5000 req/hr vs 60 without).

## RSS

**File**: `src/scrapers/rss.py`

Fetches any Atom/RSS feed using the `feedparser` library. Tries multiple date fields (`published`, `updated`, `created`) with fallback parsing.

**Config** (`sources.rss`, list of entries):

```json
{
  "id": "simon_willison",
  "name": "Simon Willison",
  "url": "https://simonwillison.net/atom/everything/",
  "enabled": true,
  "category": "ai-tools"
}
```

- `category` — optional tag for grouping (e.g., `"programming"`, `"microblog"`)

**Extracted data**: title, URL, author, content (from `summary`/`description`/`content` fields), feed name, category, and entry tags.

## Reddit

**File**: `src/scrapers/reddit.py`

Uses public, no-key Reddit endpoints. Subreddit listings and comments prefer `old.reddit.com` HTML because Reddit's unauthenticated JSON and RSS endpoints can intermittently block or fail:

- `GET https://old.reddit.com/r/{subreddit}/{sort}/` — subreddit posts
- `GET https://old.reddit.com/r/{subreddit}/comments/{post_id}/` — post comments
- `GET /r/{subreddit}/{sort}.json` — subreddit posts fallback
- `GET /user/{username}/submitted.json` — user submissions
- `GET /r/{subreddit}/comments/{post_id}.json` — post comments fallback
- `GET /r/{subreddit}/{sort}/.rss` — subreddit posts fallback when JSON is blocked

Subreddits and users are fetched concurrently. Comments are sorted by score, limited to the configured count, and exclude moderator-distinguished comments. Self-text is truncated at 1500 chars, comments at 500 chars.

**Config** (`sources.reddit`):

```json
{
  "enabled": true,
  "fetch_comments": 5,
  "subreddits": [
    {
      "id": "reddit_machinelearning",
      "subreddit": "MachineLearning",
      "sort": "hot",
      "fetch_limit": 25,
      "min_score": 10
    }
  ],
  "users": [
    {
      "id": "reddit_user_spez",
      "username": "spez",
      "sort": "new",
      "fetch_limit": 10
    }
  ]
}
```

- `sort` — `hot`, `new`, `top`, or `rising` (subreddits); `hot` or `new` (users)
- `time_filter` — for `top`/`rising` sorts: `hour`, `day`, `week`, `month`, `year`, `all`
- `min_score` — minimum post score (subreddits only)

**Rate limiting**: Detects HTTP 429 responses on JSON requests, reads the `Retry-After` header, waits, and retries once. Uses browser-like request headers for no-key public access.

**Extracted data**: title, URL, author, score, upvote ratio, comment count, subreddit, flair, self-text, and top comments.

## OpenBB

**File**: `src/scrapers/openbb.py`

Uses the [OpenBB Platform](https://www.openbb.co/platform) Python SDK via `obb.news.company()` to fetch company news for one or more ticker watchlists.

The scraper imports `openbb` lazily. If the optional dependency is not installed, 信先行 logs a warning and skips the source instead of failing the whole run.

**Config** (`sources.openbb`):

```json
{
  "enabled": true,
  "watchlists": [
    {
      "name": "megacaps",
      "symbols": ["AAPL", "MSFT", "NVDA"],
      "enabled": true,
      "provider": "yfinance",
      "fetch_limit": 20,
      "category": "equities"
    }
  ]
}
```

- `watchlists` — each enabled watchlist triggers one `news.company()` call per run
- `provider` — OpenBB provider name for that watchlist
- `symbols` — tickers fetched together for the same provider
- `fetch_limit` — maximum rows requested from the provider
- `category` — optional metadata tag stored on each item

Behavior:

- Wraps the synchronous OpenBB SDK in `asyncio.to_thread` so the event loop stays responsive
- Deduplicates duplicate news across watchlists by article URL
- Skips malformed rows, rows without URL/title/date, and items older than the current time window
- Keeps fetching other watchlists if one provider call fails

**Credentials**: provider-specific secrets are resolved by the OpenBB SDK from its own environment variables or settings file. 信先行 does not pass those values directly.

**Extracted data**: title, URL, author, published time, article body/excerpt, watchlist name, provider, category, and symbol list.

## Twitter

**File**: `src/scrapers/twitter.py`

Uses the [Apify](https://apify.com) platform to bypass Twitter's anti-scraping measures. The actor `altimis~scweet` is called via the Apify REST API.

Flow:
1. POST to `/v2/acts/{actor_id}/runs` to trigger a run
2. Poll `/v2/actor-runs/{run_id}` until status is `SUCCEEDED` or a terminal failure
3. GET `/v2/datasets/{dataset_id}/items` to retrieve results

**Config** (`sources.twitter`):

```json
{
  "id": "twitter",
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
  "actor_id": "altimis~scweet",
  "apify_token_env": "APIFY_TOKEN"
}
```

- `mode` — `apify` or `playwright`
- `users` — Twitter screen names to monitor, without the `@` prefix
- `search_queries` — raw Twitter/X advanced search queries. Use `lang:zh`, `min_faves`, `min_retweets`, and `-filter:replies` to approximate Chinese hot-topic discovery.
- `search_sort` — `Top` for hot-topic discovery, `Latest` for freshness
- `search_limit` — maximum search tweets requested per query
- `fetch_limit` — maximum profile tweets requested per run
- `fetch_reply_text` — when `true`, a second Apify run fetches reply bodies for each important tweet and appends them under `--- Top Comments ---` for AI analysis
- `max_replies_per_tweet` — maximum reply lines per tweet (sorted by engagement score)
- `max_tweets_to_expand` — cap on reply expansion runs per pipeline cycle, to control Apify credit usage
- `reply_min_likes` — minimum likes required for a reply to be included
- `actor_id` — Apify actor ID (default: `altimis~scweet`)
- `apify_token_env` — environment variable name containing the Apify API token

**Authentication**: Set `APIFY_TOKEN` in your `.env`. Get a token at [console.apify.com](https://console.apify.com/account/integrations).

**Modes**:
- Profile mode: configure `users` to follow specified bloggers.
- Search mode: configure `search_queries` to track Chinese AI/productivity hot topics.

**Extracted data**: tweet text, URL, author, publish time, likes, retweets, replies, views, source search query, and (optionally) reply-thread text appended under `--- Top Comments ---`.

Error handling:

- If `APIFY_TOKEN` is missing, the scraper logs a warning and skips Twitter instead of failing the whole run.
- If Apify rejects the run, returns malformed run data, times out, or the dataset cannot be parsed, the scraper logs the Apify error and returns the items that were successfully fetched from other runs.
- Logged Apify URLs redact the `token=...` query parameter so tokens do not leak into terminal output.

## Manual URL Add

**File**: `src/services/manual_add.py`

Manual URL ingestion is not a scheduled scraper, but it produces the same `ContentItem` and Action Card structure as automatic sources. Run it with:

```bash
uv run xinxianxing-add "https://example.com/article"
```

Flow:

1. Validate that the input is a full `http` or `https` URL.
2. Fetch the public page with browser-like headers and redirects enabled.
3. Reject login/blocked pages (`401`/`403`), non-page content types, timeouts, and HTTP errors with a clear `ManualAddError`.
4. Extract title, publication time, and readable body text from `article`, `main`, common content containers, or page body fallback.
5. Reject pages with too little readable text so image-only pages, login shells, and JavaScript-only pages are not silently added.
6. Reuse the existing AI Action Card generation path and append the result to the matching `data/drafts/`, `docs/_drafts/`, and `docs/drafts/` files.

Manual items use `source_type = "manual"` and metadata such as `feed_name = "Manual Add"`, `manual_url`, and `extracted_chars`.
