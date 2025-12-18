# FastMCP Quick Reference

A cheat sheet for working with the Beszel MCP server using FastMCP.

## Installation

```bash
pip install fastmcp httpx
# or
pip install -e .
```

## Basic Server Structure

```python
from fastmcp import FastMCP

mcp = FastMCP("server-name")

@mcp.tool()
async def my_tool(param: str) -> dict:
    """Tool description."""
    return {"result": "data"}

if __name__ == "__main__":
    mcp.run()
```

## Running the Server

```bash
# Production
python -m beszel_mcp
fastmcp run src/beszel_mcp/server.py

# Development (with hot reload)
fastmcp dev src/beszel_mcp/server.py

# With environment variables
BESZEL_URL=http://localhost:8090 python -m beszel_mcp
```

## Tool Decorator

### Basic Tool
```python
@mcp.tool()
async def simple_tool() -> dict:
    """Does something simple."""
    return {"status": "ok"}
```

### Tool with Parameters
```python
@mcp.tool()
async def tool_with_params(
    required_param: str,
    optional_param: int = 42,
    another_optional: Optional[str] = None,
) -> dict:
    """Does something with parameters.
    
    Args:
        required_param: This is required
        optional_param: This has a default
        another_optional: This is optional
    """
    return {"result": required_param}
```

### Type Hints to JSON Schema

```python
# Python type hints
str              → {"type": "string"}
int              → {"type": "integer"}
float            → {"type": "number"}
bool             → {"type": "boolean"}
dict             → {"type": "object"}
list             → {"type": "array"}
Optional[str]    → {"type": "string"} (not required)
param: str = "x" → {"type": "string", "default": "x"}
```

## Available Tools in Beszel MCP

### list_systems
```python
await list_systems(
    page=1,
    per_page=50,
    filter="name ~ 'prod'",
    sort="-created"
)
```

### list_containers
```python
await list_containers(
    page=1,
    per_page=50,
    filter="status = 'running'",
    sort="name"
)
```

### list_alerts
```python
await list_alerts(
    page=1,
    per_page=50,
    filter="enabled = true"
)
```

### list_alert_history
```python
await list_alert_history(
    page=1,
    per_page=50,
    sort="-created"
)
```

### query_system_stats
```python
await query_system_stats(
    system_id="abc123",
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-02T00:00:00Z",
    page=1,
    per_page=100
)
```

### query_container_stats
```python
await query_container_stats(
    container_id="xyz789",
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-02T00:00:00Z"
)
```

## PocketBase Filter Syntax

```python
# Exact match
filter="name = 'server1'"

# Contains
filter="name ~ 'prod'"

# Comparison
filter="cpu > 80"
filter="memory <= 90"

# Boolean
filter="enabled = true"

# Logical operators
filter="cpu > 80 && status = 'active'"
filter="(cpu > 80 || memory > 90) && enabled = true"

# Date/time
filter="created >= '2024-01-01T00:00:00Z'"
filter="created >= '2024-01-01' && created <= '2024-12-31'"
```

## Common Patterns

### Authentication
```python
def get_client() -> PocketBaseClient:
    if pb_client is None:
        base_url = os.environ.get("BESZEL_URL")
        email = os.environ.get("BESZEL_EMAIL")
        password = os.environ.get("BESZEL_PASSWORD")
        pb_client = PocketBaseClient(base_url, email, password)
    return pb_client

async def ensure_authenticated(client: PocketBaseClient) -> None:
    if client.email and client.password and not client.token:
        await client.authenticate()
```

### Error Handling
```python
@mcp.tool()
async def safe_tool(param: str) -> dict:
    """Tool with error handling."""
    try:
        result = await do_something(param)
        return result
    except ValueError as e:
        return {"error": str(e), "status": "failed"}
    except Exception as e:
        return {"error": "Internal error", "details": str(e)}
```

### Building Filters
```python
def build_filter(system_id: str, start: str = None, end: str = None) -> str:
    filters = [f"system = '{system_id}'"]
    
    if start:
        filters.append(f"created >= '{start}'")
    if end:
        filters.append(f"created <= '{end}'")
    
    return " && ".join(filters)
```

## Environment Variables

```bash
# Required
export BESZEL_URL="http://localhost:8090"

# Optional (for authentication)
export BESZEL_EMAIL="admin@example.com"
export BESZEL_PASSWORD="your-password"
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "beszel": {
      "command": "python",
      "args": ["-m", "beszel_mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "password"
      }
    }
  }
}
```

## Debugging

```bash
# Enable debug output
export MCP_DEBUG=1
export PYTHONUNBUFFERED=1

# Run with debug
fastmcp dev src/beszel_mcp/server.py

# Test tool directly
python -c "
import asyncio
from beszel_mcp.server import list_systems
print(asyncio.run(list_systems()))
"
```

## Common Issues

### Import Error
```bash
# Fix: Install FastMCP
pip install fastmcp
```

### Connection Error
```bash
# Fix: Check Beszel is running
curl http://localhost:8090/api/health
```

### Authentication Error
```bash
# Fix: Verify credentials
export BESZEL_EMAIL="correct-email@example.com"
export BESZEL_PASSWORD="correct-password"
```

## Tips

1. **Use type hints** - They become JSON schemas automatically
2. **Write docstrings** - They become tool descriptions
3. **Return dicts** - FastMCP handles JSON conversion
4. **Use dev mode** - Hot reload speeds up development
5. **Test with curl** - Verify PocketBase directly first
6. **Check logs** - Enable debug output for troubleshooting

## Resources

- [FastMCP Docs](https://github.com/jlowin/fastmcp)
- [PocketBase API](https://pocketbase.io/docs/api-records/)
- [Beszel GitHub](https://github.com/henrygd/beszel)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
