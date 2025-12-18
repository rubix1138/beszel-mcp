# Running Beszel MCP - All Methods Compared

Quick comparison of different ways to run the Beszel MCP server.

## Method Comparison

| Method | Speed | Setup | Best For |
|--------|-------|-------|----------|
| `uv run` | ⚡⚡⚡ | Instant | Development, Quick testing |
| `uvx` | ⚡⚡⚡ | None | Claude Desktop, Production |
| `pip + venv` | ⚡ | Manual | Traditional workflows |
| `Docker` | ⚡⚡ | Complex | Containers, Cloud |

## 1. uv run (Recommended for Dev)

**Fastest for development - no installation needed!**

```bash
cd /path/to/beszel-mcp
export BESZEL_URL="http://localhost:8090"
uv run beszel-mcp
```

**Pros:**
- ⚡ Instant - no `pip install` step
- 🎯 No virtual env activation
- 🔄 Automatic dependency management
- 🚀 10-100x faster than pip

**Cons:**
- Requires uv installed

**Best for:** Daily development, testing changes

## 2. uvx (Recommended for Claude Desktop)

**Best for Claude Desktop integration**

```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/beszel-mcp", "beszel-mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090"
      }
    }
  }
}
```

**Pros:**
- ⚡ Fast startup
- 🔒 Isolated dependencies
- 🎯 No global installation
- 🔄 Auto-updates possible

**Cons:**
- Requires absolute path

**Best for:** Claude Desktop, production use

## 3. Traditional pip + venv

**Most compatible, works everywhere**

```bash
cd /path/to/beszel-mcp
python -m venv venv
source venv/bin/activate
pip install -e .
beszel-mcp
```

**Pros:**
- ✅ Works on all systems
- 📦 Standard Python workflow
- 🔧 Full control

**Cons:**
- 🐌 Slower installation (10-30 seconds vs 1-3)
- 📝 Manual venv activation
- 🔄 Manual dependency updates

**Best for:** Systems without uv, corporate environments

## 4. Global Installation

```bash
# With pip
pip install /path/to/beszel-mcp

# With uv
uv tool install /path/to/beszel-mcp

# Then run from anywhere
beszel-mcp
```

**Pros:**
- 🌍 Available globally
- 📍 No path needed

**Cons:**
- ⚠️ Pollutes global Python
- 🔄 Harder to update
- 💥 Potential conflicts

**Best for:** Personal single-user systems

## 5. Docker

```dockerfile
FROM python:3.11-slim
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"
WORKDIR /app
COPY . .
RUN uv sync
CMD ["uv", "run", "beszel-mcp"]
```

**Pros:**
- 📦 Fully isolated
- ☁️ Cloud-ready
- 🔒 Reproducible

**Cons:**
- 🐳 Requires Docker
- 💾 Larger footprint
- 🔧 More complex setup

**Best for:** Containers, Kubernetes, cloud deployments

## Speed Comparison

Installing FastMCP + httpx:

```bash
# pip (traditional)
time pip install fastmcp httpx
# → 15-30 seconds

# uv
time uv pip install fastmcp httpx
# → 1-3 seconds

# uv run (no install needed!)
time uv run beszel-mcp
# → Instant after first run
```

## Recommendation by Use Case

### Daily Development
```bash
uv run beszel-mcp
```
**Why:** Instant, no setup, no venv activation

### Claude Desktop
```json
"command": "uvx",
"args": ["--from", "/path/to/beszel-mcp", "beszel-mcp"]
```
**Why:** Reliable, isolated, fast startup

### CI/CD Pipeline
```yaml
- run: uv sync
- run: uv run pytest
```
**Why:** Fast, reproducible, cacheable

### Production Server
```bash
uv tool install /path/to/beszel-mcp
# Or systemd with uv run
```
**Why:** Stable, managed, logged

### Corporate/Restricted Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```
**Why:** Standard, no special tools needed

## Configuration Files

### For uv (recommended)

**pyproject.toml** already includes:
```toml
[project.scripts]
beszel-mcp = "beszel_mcp.__main__:main"

[tool.uv]
dev-dependencies = ["pytest>=8.0.0", "pytest-asyncio>=0.23.0"]
```

### Environment Variables (all methods)

```bash
export BESZEL_URL="http://localhost:8090"
export BESZEL_EMAIL="admin@example.com"
export BESZEL_PASSWORD="password"
```

Or create `.env`:
```env
BESZEL_URL=http://localhost:8090
BESZEL_EMAIL=admin@example.com
BESZEL_PASSWORD=password
```

## Quick Decision Tree

```
Need it for Claude Desktop?
├─ Yes → Use uvx (Method 2)
└─ No
   ├─ Developing/Testing?
   │  ├─ Have uv? → Use uv run (Method 1)
   │  └─ No uv? → Use pip+venv (Method 3)
   └─ Production?
      ├─ Docker/K8s? → Use Docker (Method 5)
      ├─ Systemd? → Use uv run with service
      └─ Simple? → Global install (Method 4)
```

## Summary

**For most users:** Start with `uv run` for development and `uvx` for Claude Desktop.

**Installation time:**
- uv: 10 seconds total (once)
- pip: 30-60 seconds every time

**Running time:**
- uv run: Instant (after first run)
- traditional: Instant (after venv activation)

**Winner: uv** for speed, simplicity, and modern Python workflows! ⚡
