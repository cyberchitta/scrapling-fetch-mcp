[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/cyberchitta-scrapling-fetch-mcp-badge.jpg)](https://mseep.ai/app/cyberchitta-scrapling-fetch-mcp)

# Scrapling Fetch MCP

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/scrapling-fetch-mcp.svg)](https://pypi.org/project/scrapling-fetch-mcp/)

An MCP server that helps AI assistants access text content from websites that implement bot detection, bridging the gap between what you can see in your browser and what the AI can access.

## Intended Use

This tool is optimized for low-volume retrieval of documentation and reference materials (text/HTML only) from websites that implement bot detection. It has not been designed or tested for general-purpose site scraping or data harvesting.

> **Note**: This project was developed in collaboration with Claude Sonnet 3.7, using [LLM Context](https://github.com/cyberchitta/llm-context.py).

## Installation

1. Requirements:
   - Python 3.10+
   - [uv](https://github.com/astral-sh/uv) package manager

2. Install dependencies and the tool:
```bash
uv tool install scrapling
scrapling install
uv tool install scrapling-fetch-mcp
```

## Setup with Claude

Add this configuration to your Claude client's MCP server configuration:

```json
{
  "mcpServers": {
    "Cyber-Chitta": {
      "command": "uvx",
      "args": ["scrapling-fetch-mcp"]
    }
  }
}
```

## Available Tools

This package provides two distinct tools:

1. **s-fetch-page**: Retrieves complete web pages with pagination support
2. **s-fetch-pattern**: Extracts content matching regex patterns with surrounding context

## Example Usage

### Fetching a Complete Page

```
Human: Please fetch and summarize the documentation at https://example.com/docs

Claude: I'll help you with that. Let me fetch the documentation.

<mcp:function_calls>
<mcp:invoke name="s-fetch-page">
<mcp:parameter name="url">https://example.com/docs</mcp:parameter>
<mcp:parameter name="mode">basic</mcp:parameter>
</mcp:invoke>
</mcp:function_calls>

Based on the documentation I retrieved, here's a summary...
```

### Extracting Specific Content with Pattern Matching

```
Human: Please find all mentions of "API keys" on the documentation page.

Claude: I'll search for that specific information.

<mcp:function_calls>
<mcp:invoke name="s-fetch-pattern">
<mcp:parameter name="url">https://example.com/docs</mcp:parameter>
<mcp:parameter name="mode">basic</mcp:parameter>
<mcp:parameter name="search_pattern">API\s+keys?</mcp:parameter>
<mcp:parameter name="context_chars">150</mcp:parameter>
</mcp:invoke>
</mcp:function_calls>

I found several mentions of API keys in the documentation:
...
```

## Functionality Options

- **Protection Levels**:
  - `basic`: Fast retrieval (1-2 seconds) but lower success with heavily protected sites
  - `stealth`: Balanced protection (3-8 seconds) that works with most sites
  - `max-stealth`: Maximum protection (10+ seconds) for heavily protected sites

- **Content Targeting Options**:
  - **s-fetch-page**: Retrieve entire pages with pagination support (using `start_index` and `max_length`)
  - **s-fetch-pattern**: Extract specific content using regular expressions (with `search_pattern` and `context_chars`)
    - Results include position information for follow-up queries with `s-fetch-page`

## Tips for Best Results

- Start with `basic` mode and only escalate to higher protection levels if needed
- For large documents, use the pagination parameters with `s-fetch-page`
- Use `s-fetch-pattern` when looking for specific information on large pages
- The AI will automatically adjust its approach based on the site's protection level

## Limitations

- **Designed only for text content**: Specifically for documentation, articles, and reference materials
- Not designed for high-volume scraping or data harvesting
- May not work with sites requiring authentication
- Performance varies by site complexity

## License

Apache 2
