# scrapling-fetch-mcp

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/scrapling-fetch-mcp.svg)](https://pypi.org/project/scrapling-fetch-mcp/)

Helps AI assistants fetch content from bot-protected websites. Uses Scrapling (patchright + curl-cffi) to bypass anti-automation measures, returning clean HTML or Markdown.

> Optimized for low-volume retrieval of documentation and reference materials. Not designed for high-volume scraping or data harvesting.

**Requirements**: Python 3.10+, [uv](https://github.com/astral-sh/uv)

## Claude Code Skill

The easiest way to use this is as a Claude Code skill. Once installed, Claude will automatically fetch bot-protected URLs when you ask — no manual commands needed.

**Install into your project** (recommended — only loads in this project's context):

```bash
git clone --depth=1 https://github.com/cyberchitta/scrapling-fetch-mcp /tmp/scrapling-fetch-mcp
cp -r /tmp/scrapling-fetch-mcp/skills/s-fetch .claude/skills/
cp -r /tmp/scrapling-fetch-mcp/skills/s-fetch-setup .claude/skills/
rm -rf /tmp/scrapling-fetch-mcp
```

**Or install for all projects** (loads into context everywhere):

```bash
git clone --depth=1 https://github.com/cyberchitta/scrapling-fetch-mcp /tmp/scrapling-fetch-mcp
cp -r /tmp/scrapling-fetch-mcp/skills/s-fetch ~/.claude/skills/
cp -r /tmp/scrapling-fetch-mcp/skills/s-fetch-setup ~/.claude/skills/
rm -rf /tmp/scrapling-fetch-mcp
```

Then ask Claude to run `/s-fetch-setup` — it will install the tool and browser binaries (large download), then remove itself. After that, just ask naturally:

```
"Fetch the docs at https://example.com/api"
"Find all mentions of 'authentication' on that page"
"Get me the installation instructions from their homepage"
```

## Claude Desktop (MCP Server)

If you've already run `/s-fetch-setup`, the tool is installed — skip to the config below.

Otherwise install first:

```bash
uv tool install git+https://github.com/cyberchitta/scrapling-fetch-mcp
uvx --from git+https://github.com/cyberchitta/scrapling-fetch-mcp scrapling install
```

> **Note**: Browser installation downloads hundreds of MB and must complete before first use. If the server times out initially, wait a few minutes and try again.

Add this to your Claude Desktop MCP settings and restart:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scrapling-fetch": {
      "command": "uvx",
      "args": ["scrapling-fetch-mcp"]
    }
  }
}
```

## How It Works

Two tools, used automatically by Claude:

- **Page fetching** — retrieves complete pages with pagination support
- **Pattern extraction** — finds content matching a regex

Three protection levels, escalated automatically:

- **basic** — fast (1-2s), works for most sites
- **stealth** — moderate (3-8s), headless Chromium
- **max-stealth** — thorough (10s+), full browser fingerprint

## Limitations

- Text content only (documentation, articles, references)
- Not for high-volume scraping or sites requiring authentication
- Performance varies by site complexity and protection level

## License

Apache 2.0
