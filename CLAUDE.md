# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What it does

scrapling-fetch-mcp is an MCP server that helps AI assistants fetch web content from bot-protected sites. It exposes two tools (`s_fetch_page`, `s_fetch_pattern`) via FastMCP over stdio, using Scrapling (patchright + playwright + curl-cffi) to bypass anti-automation measures and returning HTML or Markdown.

It also ships as a Claude Code skill with a `/s-fetch` slash command that invokes scrapling directly via Bash (no MCP server required), installable from this repo.

## Commands

```bash
# Install dependencies
uv sync

# Install browser binaries (required once; large download)
uvx --from scrapling-fetch-mcp scrapling install

# Run MCP server
uv run scrapling-fetch-mcp

# Build
uv build
```

No test suite exists in this project.

## Skill structure

```
skills/s-fetch/SKILL.md      # /s-fetch slash command — invokes scrapling directly via Bash
```

Install: `/skills install github:cyberchitta/scrapling-fetch-mcp`

The skill uses `uv run --isolated --with scrapling[fetchers]` so it works in any directory without a local venv.

## Architecture

Request flow: `mcp.py` (FastMCP tool definitions) → `_fetcher.py` (content pipeline) → `_scrapling.py` (Scrapling dispatch) → returns `html_content`.

**`_scrapling.py`** — sole integration point with Scrapling. Maps the three fetch modes:
- `basic` — `AsyncFetcher.get` with stealthy headers (fastest, ~1-2s)
- `stealth` — `StealthyFetcher.async_fetch` headless+network_idle (~3-8s)
- `max-stealth` — same but with WebRTC blocked and resources/images not blocked (10s+)

Scrapling import is deferred inside `browse_url` with stdout redirected to `/dev/null` to suppress Scrapling's noisy startup output.

**`_fetcher.py`** — content pipeline: calls `browse_url`, optionally converts HTML→Markdown via `_markdownify.py`, applies pagination (`start_index`/`max_length`) or regex pattern extraction, and wraps everything in `METADATA: {json}\n\n[content]`. The metadata JSON includes `total_length`, `retrieved_length`, `is_truncated`, `percent_retrieved`, and optionally `start_index` / `match_count`.

Pattern extraction (`_search_content`) compiles the regex, merges overlapping context windows around matches, and delimits sections with `॥๛॥` followed by `[Position: start-end]` so callers can issue targeted follow-up `s_fetch_page` requests with specific `start_index` values.

**`_markdownify.py`** — `_CustomMarkdownify` subclass adapted from Microsoft markitdown. Strips `<script>`/`<style>` via BeautifulSoup before conversion, fixes heading newlines, URL-encodes link hrefs, and truncates `data:` image sources.

Entry point: `scrapling-fetch-mcp` CLI → `scrapling_fetch_mcp.mcp:run_server` → `mcp.run(transport="stdio")`.
