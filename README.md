# scrapling-fetch-mcp

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/scrapling-fetch-mcp.svg)](https://pypi.org/project/scrapling-fetch-mcp/)

An MCP server and Claude Code skill that help AI assistants access text content from websites that implement bot detection, bridging the gap between what you can see in your browser and what the AI can access.

## Intended Use

This tool is optimized for low-volume retrieval of documentation and reference materials (text/HTML only) from websites that implement bot detection. It has not been designed or tested for general-purpose site scraping or data harvesting.

> **Note**: This project was developed in collaboration with Claude Sonnets 3.7 and 4.5, using [LLM Context](https://github.com/cyberchitta/llm-context.py).

## Installation

### Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Install

```bash
# Install scrapling-fetch-mcp
uv tool install git+https://github.com/cyberchitta/scrapling-fetch-mcp

# Install browser binaries (REQUIRED - large downloads)
uvx --from git+https://github.com/cyberchitta/scrapling-fetch-mcp scrapling install
```

**Important**: The browser installation downloads hundreds of MB of data and must complete before first use. If the MCP server times out on first use, the browsers may still be installing in the background. Wait a few minutes and try again.

## Setup with Claude Desktop

Add this configuration to your Claude Desktop MCP settings:

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

After updating the config, restart Claude Desktop.

## What It Does

This MCP server provides two tools that Claude can use automatically when you ask it to fetch web content:

- **Page fetching**: Retrieves complete web pages with support for pagination
- **Pattern extraction**: Finds and extracts specific content using regex patterns

The AI decides which tool to use based on your request. You just ask naturally:

```
"Can you fetch the docs at https://example.com/api"
"Find all mentions of 'authentication' on that page"
"Get me the installation instructions from their homepage"
```

## Protection Modes

The tools support three levels of bot detection bypass:

- **basic**: Fast (1-2s), works for most sites
- **stealth**: Moderate (3-8s), handles more protection
- **max-stealth**: Maximum (10+s), for heavily protected sites

Claude automatically starts with `basic` mode and escalates if needed.

## Tips for Best Results

- Just ask naturally - Claude handles the technical details
- For large pages, Claude can page through content automatically
- For specific searches, mention what you're looking for and Claude will use pattern matching
- The metadata returned helps Claude decide whether to page or search

## Limitations

- Designed for text content only (documentation, articles, references)
- Not for high-volume scraping or data harvesting
- May not work with sites requiring authentication
- Performance varies by site complexity and protection level

## Claude Code Skill

This repo also ships as a Claude Code skill with a `/s-fetch` slash command that fetches URLs directly via scrapling. The skill requires the MCP server to be installed first (it reuses the same scrapling environment).

Install from within Claude Code:

```
/skills install github:cyberchitta/scrapling-fetch-mcp
```

Once installed, Claude will use `/s-fetch` automatically when you ask it to fetch a URL from a bot-protected site. You can also invoke it directly as `/s-fetch <url>` with an optional mode (`basic`, `stealth`, `max-stealth`) and format (`markdown`, `html`).

## License

Apache 2.0
