---
name: s-fetch
description: Fetch a URL directly with scrapling's bot-detection bypass. Use when the user asks to fetch, curl, or scrape a URL from a bot-protected site.
argument-hint: <url> [basic|stealth|max-stealth] [html|markdown]
allowed-tools: [Bash]
version: 1.0.0
---

# s-fetch

Fetches a URL directly via scrapling, bypassing bot detection. Does not use the MCP server — runs scrapling inline.

## Arguments

$ARGUMENTS — parse as `<url> [mode] [format]`

- **url** (required)
- **mode** (optional, default `basic`): `basic` | `stealth` | `max-stealth`
- **format** (optional, default `markdown`): `markdown` | `html`

## Instructions

Run the following Bash command, substituting URL, MODE, and FORMAT with the parsed values:

```bash
uv run --isolated \
  --with 'scrapling[fetchers]>=0.4.7' \
  --with 'markdownify>=1.2.0' \
  --with 'beautifulsoup4>=4.14.2' \
  --with 'lxml>=6.0.2' \
  python3 - <<'PYEOF'
import asyncio
from contextlib import redirect_stdout
from os import devnull

async def fetch(url, mode):
    with open(devnull, "w") as null, redirect_stdout(null):
        from scrapling.fetchers import AsyncFetcher, StealthyFetcher
        if mode == "basic":
            return await AsyncFetcher.get(url, stealthy_headers=True)
        elif mode == "stealth":
            return await StealthyFetcher.async_fetch(url, headless=True, network_idle=True)
        elif mode == "max-stealth":
            return await StealthyFetcher.async_fetch(
                url, headless=True, block_webrtc=True,
                network_idle=True, disable_resources=False, block_images=False
            )
        else:
            raise ValueError(f"Unknown mode: {mode}")

url = "URL"
mode = "MODE"
fmt = "FORMAT"

page = asyncio.run(fetch(url, mode))
html = page.html_content

if fmt == "markdown":
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.extract()
    body = soup.find("body")
    print(md(str(body if body else soup)))
else:
    print(html)
PYEOF
```

If mode was not given and `basic` returns blocked or empty content, retry with `stealth`, then `max-stealth`.

## Mode guide

| Mode | Speed | Use when |
|------|-------|----------|
| `basic` | 1–2s | Most sites; curl-cffi with stealth headers |
| `stealth` | 3–8s | Sites that block basic; headless Chromium via patchright |
| `max-stealth` | 10s+ | Heavily protected sites; full browser fingerprint |
