# Quick Start with uv

Fast setup guide for running Beszel MCP with uv.

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Run

```bash
cd /path/to/beszel-mcp

# Set environment
export BESZEL_URL="http://localhost:8090"
export BESZEL_EMAIL="admin@example.com"
export BESZEL_PASSWORD="your-password"

# Run (no installation needed!)
uv run beszel-mcp
```

## For Claude Desktop

1. Find your absolute path:
```bash
cd /path/to/beszel-mcp && pwd
```

2. Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/from/step1", "beszel-mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "password"
      }
    }
  }
}
```

3. Restart Claude Desktop

Done! 🚀

## Common Commands

```bash
# Run without installing
uv run beszel-mcp

# Run dev mode
uv run fastmcp dev src/beszel_mcp/server.py

# Run tests
uv run pytest

# Install dependencies
uv sync

# Update dependencies
uv lock --upgrade && uv sync
```

## Why uv?

- ⚡ **10-100x faster** than pip
- 🎯 **No venv activation** needed
- 🔒 **Lock files** for reproducibility
- 📦 **All-in-one** package and environment manager

See [UV_GUIDE.md](UV_GUIDE.md) for details.
