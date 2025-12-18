# Using Beszel MCP with uv

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager and resolver written in Rust. It's a great choice for running the Beszel MCP server.

## Why uv?

- ⚡ **Fast**: 10-100x faster than pip
- 🔒 **Reliable**: Lock files for reproducible installs
- 🎯 **Simple**: Handles virtual environments automatically
- 🚀 **Modern**: Built for Python 3.10+
- 📦 **Complete**: Package installation, resolution, and environment management

## Installation

### Install uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv

# With pipx
pipx install uv

# With Homebrew
brew install uv
```

### Install Beszel MCP

```bash
cd /path/to/beszel-mcp

# Install in development mode
uv pip install -e .

# Or install with all dependencies
uv sync
```

## Running the Server

### Quick Run (No Installation)

```bash
# Run directly without installing
uv run python -m beszel_mcp

# Or use the script entry point
uv run beszel-mcp
```

### With Environment Variables

```bash
# Set environment variables
export BESZEL_URL="http://localhost:8090"
export BESZEL_EMAIL="admin@example.com"
export BESZEL_PASSWORD="your-password"

# Run
uv run beszel-mcp
```

### One-liner with Environment

```bash
BESZEL_URL=http://localhost:8090 \
BESZEL_EMAIL=admin@example.com \
BESZEL_PASSWORD=password \
uv run beszel-mcp
```

## Development Workflow

### Create a Virtual Environment

```bash
# uv handles this automatically, but you can be explicit
uv venv

# Activate (optional, uv run doesn't require this)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
# Install project dependencies
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

# Or use sync (recommended)
uv sync
```

### Run Tests

```bash
# With uv
uv run pytest

# Or after activating venv
pytest
```

### Development Mode

```bash
# Run FastMCP dev server with hot reload
uv run fastmcp dev src/beszel_mcp/server.py
```

## Claude Desktop Integration

### Using uvx (Recommended)

`uvx` is uv's tool runner that handles dependencies automatically:

```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/beszel-mcp", "beszel-mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-password"
      }
    }
  }
}
```

**Important:** 
- Replace `/absolute/path/to/beszel-mcp` with your actual project path
- Use absolute paths (e.g., `/home/daniel/projects/beszel-mcp`)
- Don't use `~` or relative paths

### Find Your Absolute Path

```bash
# Linux/macOS
cd /path/to/beszel-mcp && pwd

# Windows (PowerShell)
cd C:\path\to\beszel-mcp; (Get-Location).Path
```

### Using uv run

Alternatively, use `uv run` with a wrapper script:

**create-wrapper.sh:**
```bash
#!/bin/bash
cd /absolute/path/to/beszel-mcp
exec uv run beszel-mcp
```

```json
{
  "mcpServers": {
    "beszel": {
      "command": "/path/to/create-wrapper.sh",
      "env": {
        "BESZEL_URL": "http://localhost:8090"
      }
    }
  }
}
```

## Lock Files

uv generates lock files for reproducible installations:

```bash
# Generate lock file
uv lock

# Update dependencies
uv lock --upgrade

# Install from lock file
uv sync
```

Commit `uv.lock` to version control for reproducibility!

## Common Commands

```bash
# Install package
uv pip install fastmcp

# Install with extras
uv pip install -e ".[dev]"

# Run script without installing
uv run python script.py

# Run command in project
uv run beszel-mcp

# Create virtual environment
uv venv

# Sync dependencies
uv sync

# Update dependencies
uv lock --upgrade
uv sync

# Run tests
uv run pytest

# Install from requirements
uv pip install -r requirements.txt

# List installed packages
uv pip list

# Show package info
uv pip show fastmcp
```

## Advantages Over pip

| Feature | pip | uv |
|---------|-----|-----|
| Speed | Baseline | 10-100x faster |
| Dependency resolution | Slow | Very fast |
| Lock files | No (pip-tools needed) | Built-in |
| Virtual envs | Manual | Automatic |
| Parallel downloads | No | Yes |
| Rust-based | No | Yes |
| Compatibility | Full | Full |

## Troubleshooting

### Command Not Found

```bash
# Make sure uv is in your PATH
which uv  # Linux/macOS
where uv  # Windows

# Reinstall if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Import Errors

```bash
# Ensure dependencies are installed
uv pip install -e .

# Or sync everything
uv sync
```

### uvx Can't Find Package

```bash
# Use absolute path with --from
uvx --from /absolute/path/to/project beszel-mcp

# Or install globally
uv tool install /path/to/beszel-mcp
```

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf .venv
uv venv
uv sync
```

## Performance Comparison

```bash
# Install FastMCP and dependencies

# With pip
time pip install fastmcp httpx
# Real: ~15-30 seconds

# With uv
time uv pip install fastmcp httpx
# Real: ~1-3 seconds

# 10x faster! ⚡
```

## Best Practices

1. **Use `uv sync`** for consistent installs
2. **Commit `uv.lock`** for reproducibility
3. **Use `uvx`** for running tools without installing
4. **Use `uv run`** during development
5. **Use absolute paths** in Claude Desktop config
6. **Update regularly**: `uv self update`

## Integration Examples

### Systemd Service (Linux)

```ini
[Unit]
Description=Beszel MCP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/beszel-mcp
Environment="BESZEL_URL=http://localhost:8090"
Environment="BESZEL_EMAIL=admin@example.com"
Environment="BESZEL_PASSWORD=password"
ExecStart=/home/your-user/.cargo/bin/uv run beszel-mcp
Restart=always

[Install]
WantedBy=multi-user.target
```

### Docker

```dockerfile
FROM python:3.11-slim

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app
COPY . .

# Install dependencies
RUN uv sync

# Run server
CMD ["uv", "run", "beszel-mcp"]
```

### GitHub Actions

```yaml
- name: Setup uv
  uses: astral-sh/setup-uv@v1
  
- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

## Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv Installation Guide](https://github.com/astral-sh/uv#installation)
- [Python Packaging with uv](https://github.com/astral-sh/uv/blob/main/PACKAGING.md)

## Summary

Using uv with Beszel MCP is simple:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run
cd beszel-mcp
uv run beszel-mcp

# Or for Claude Desktop, use uvx in config
# "command": "uvx",
# "args": ["--from", "/path/to/beszel-mcp", "beszel-mcp"]
```

That's it! Enjoy blazing-fast Python package management! ⚡
