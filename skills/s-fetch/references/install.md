# Installing scrapling-fetch-mcp

Run once on a machine that doesn't yet have `scrapling-fetch-mcp`
installed. The main SKILL.md points here when the fetch command fails
because the tool is missing.

**1. Install the tool:**

```bash
uv tool install git+https://github.com/cyberchitta/scrapling-fetch-mcp
```

**2. Install browser binaries** (large download, may take a few minutes):

```bash
"$(uv tool dir)/scrapling-fetch-mcp/bin/scrapling" install
```

**3. Verify:**

```bash
[ -x "$(uv tool dir)/scrapling-fetch-mcp/bin/python3" ] && echo ok
```

Report success and continue with whatever the user originally asked for.

## Updating later

To upgrade the tool to the latest commit on `main`:

```bash
uv tool upgrade scrapling-fetch-mcp
```

The skill files (`SKILL.md`, `references/`) don't auto-update — re-run
the `cp -r` from the README's install section to refresh them.
