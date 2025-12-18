# Quick Start Guide

Get up and running with the Beszel MCP server in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- A running Beszel instance with PocketBase backend
- Admin credentials for PocketBase

## Installation

### Step 1: Clone or Download

```bash
cd /path/to/beszel-mcp
```

### Step 2: Install Dependencies

**Option A: Using uv (Recommended, Fast)**
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Or just run without installing
uv run beszel-mcp
```

**Option B: Using the setup script**
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Prepare the package for development

### Step 3: Configure Environment

Create a `.env` file or export environment variables:

```bash
export BESZEL_URL="http://localhost:8090"
export BESZEL_EMAIL="admin@example.com"
export BESZEL_PASSWORD="your-secure-password"
```

Or create a `.env` file:

```env
BESZEL_URL=http://localhost:8090
BESZEL_EMAIL=admin@example.com
BESZEL_PASSWORD=your-secure-password
```

## Testing the Server

### Quick Test

**With uv (no activation needed):**
```bash
uv run beszel-mcp
# or
uv run python -m beszel_mcp
```

**With traditional venv:**
```bash
source venv/bin/activate
python -m beszel_mcp
```

The server will start and wait for MCP protocol messages on stdin.

You can also use FastMCP's dev mode for testing:

```bash
uv run fastmcp dev src/beszel_mcp/server.py
# or
fastmcp dev src/beszel_mcp/server.py
```

This will start an interactive development server.

### With Claude Desktop

1. Locate your Claude Desktop config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the Beszel MCP server configuration:

**Using uvx (Recommended):**
```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/beszel-mcp", "beszel-mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-secure-password"
      }
    }
  }
}
```

**Or using Python:**
```json
{
  "mcpServers": {
    "beszel": {
      "command": "python",
      "args": ["-m", "beszel_mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-secure-password"
      }
    }
  }
}
```

**Note:** Replace `/absolute/path/to/beszel-mcp` with your actual project path. Find it with `pwd` in the project directory.

3. Restart Claude Desktop

4. The Beszel tools should now appear in Claude!

## First Queries

Try these example queries in Claude:

### List Systems
```
Show me all the systems being monitored by Beszel
```

### Check System Stats
```
What are the current CPU and memory stats for my systems?
```

### View Alerts
```
Show me any recent alerts
```

### Container Information
```
List all containers and their status
```

## Example Use Cases

### Monitoring Dashboard
```
Give me a summary of:
1. Total number of systems
2. Any systems with high CPU usage (>80%)
3. Recent alerts in the last hour
4. Top 5 containers by resource usage
```

### Performance Analysis
```
Show me the CPU and memory trends for system abc123 over the last 24 hours
```

### Alert Investigation
```
What alerts were triggered yesterday? Show me the details including which systems were affected.
```

### Capacity Planning
```
Which systems have the highest average CPU usage over the last week?
```

## Verify Installation

Check that everything is working:

```bash
# Activate virtual environment
source venv/bin/activate

# Check Python version
python --version

# Check installed packages
pip list | grep -E "(fastmcp|httpx)"

# Try importing the package
python -c "from beszel_mcp import __version__; print(__version__)"

# Test the server in dev mode
fastmcp dev src/beszel_mcp/server.py

# Run tests (optional)
pytest
```

## Next Steps

- Read the [API Reference](docs/API_REFERENCE.md) to understand available data
- Check out [Example Queries](examples/queries.md) for more ideas
- Review [Troubleshooting Guide](docs/TROUBLESHOOTING.md) if you encounter issues
- Customize filters and queries for your specific monitoring needs

## Common First-Time Issues

### Can't connect to Beszel
- Verify Beszel is running: `curl http://localhost:8090/api/health`
- Check the URL in your config

### Authentication fails
- Verify credentials in PocketBase admin UI
- Ensure you're using an admin account

### No data returned
- Check that systems are actually reporting to Beszel
- Verify data exists in the PocketBase admin UI at `http://localhost:8090/_/`

### Server won't start
- Make sure virtual environment is activated
- Run `./setup.sh` again to reinstall dependencies
- Check Python version: `python --version` (must be 3.10+)

## Getting Help

If you need help:
1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review the [README](README.md) for detailed documentation
3. Look at the [examples](examples/) directory
4. Check the Beszel and PocketBase documentation

Happy monitoring! 🚀
