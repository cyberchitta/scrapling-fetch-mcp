---
name: s-fetch-setup
description: Install scrapling-fetch-mcp and its browser binaries. Run this once before using s-fetch. Removes itself after successful installation.
allowed-tools: [Bash]
---

# s-fetch-setup

Installs the scrapling-fetch-mcp tool and browser binaries required by the s-fetch skill.

## Instructions

Run the following steps in order:

**1. Install the tool:**

```bash
uv tool install git+https://github.com/cyberchitta/scrapling-fetch-mcp
```

**2. Install browser binaries** (large download, may take a few minutes):

```bash
"$(uv tool dir)/scrapling-fetch-mcp/bin/scrapling" install
```

**3. Remove this setup skill** (no longer needed):

```bash
rm -rf ~/.claude/skills/s-fetch-setup .claude/skills/s-fetch-setup
```

Report success and tell the user that s-fetch is ready to use.
