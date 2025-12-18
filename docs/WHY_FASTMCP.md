# Why FastMCP?

This document explains why we use FastMCP and how it simplifies MCP server development.

## The Problem with Raw MCP SDK

The raw MCP SDK is powerful but requires significant boilerplate:

```python
# OLD WAY: Low-level MCP SDK (verbose)
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("beszel-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_systems",
            description="List all monitored systems in Beszel...",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "Page number",
                        "default": 1,
                    },
                    "per_page": {
                        "type": "number",
                        "description": "Results per page",
                        "default": 50,
                    },
                    # ... more properties
                },
            },
        ),
        # ... more tools
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "list_systems":
        result = await client.get_list(
            collection="systems",
            page=arguments.get("page", 1),
            per_page=arguments.get("per_page", 50),
            # ...
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "list_containers":
        # ... more elif branches
```

**Problems:**
- 🔴 Lots of boilerplate for tool definitions
- 🔴 Manual JSON schema writing
- 🔴 Complex if/elif chains for routing
- 🔴 Manual response formatting
- 🔴 Verbose type definitions
- 🔴 Error-prone string matching

## The FastMCP Solution

FastMCP provides a high-level, decorator-based API:

```python
# NEW WAY: FastMCP (clean and simple)
from fastmcp import FastMCP

mcp = FastMCP("beszel-mcp")

@mcp.tool()
async def list_systems(
    page: int = 1,
    per_page: int = 50,
    filter: Optional[str] = None,
    sort: Optional[str] = None,
) -> dict:
    """List all monitored systems in Beszel.
    
    Args:
        page: Page number (default: 1)
        per_page: Number of results per page (default: 50)
        filter: PocketBase filter string
        sort: Sort order
    
    Returns:
        Dictionary containing paginated list of systems
    """
    client = get_client()
    await ensure_authenticated(client)
    
    return await client.get_list(
        collection="systems",
        page=page,
        per_page=per_page,
        filter=filter,
        sort=sort,
    )

# That's it! No manual schema, no routing, no response formatting!
```

**Benefits:**
- ✅ Clean decorator-based API
- ✅ Automatic JSON schema generation from type hints
- ✅ Direct return values (no manual TextContent wrapping)
- ✅ Docstrings become tool descriptions
- ✅ Type safety with Python types
- ✅ Less code = fewer bugs

## Feature Comparison

| Feature | Raw MCP SDK | FastMCP |
|---------|-------------|---------|
| Lines of code (for 6 tools) | ~300 | ~120 |
| Tool definition | Manual JSON Schema | Type hints + decorators |
| Routing | Manual if/elif | Automatic |
| Response formatting | Manual TextContent | Automatic |
| Documentation | Separate strings | From docstrings |
| Type safety | Limited | Full Python typing |
| Learning curve | Steep | Gentle |

## Code Reduction

**Before (Raw MCP SDK):**
- `server.py`: ~280 lines
- Boilerplate: ~60%
- Business logic: ~40%

**After (FastMCP):**
- `server.py`: ~180 lines
- Boilerplate: ~20%
- Business logic: ~80%

**Result: 35% less code, much more readable!**

## What FastMCP Does For You

### 1. Automatic Schema Generation

```python
# You write:
async def query_system_stats(
    system_id: str,
    start_time: Optional[str] = None,
    page: int = 1,
) -> dict:
    """Query statistics for a system."""
    pass

# FastMCP generates:
# {
#   "type": "object",
#   "properties": {
#     "system_id": {"type": "string"},
#     "start_time": {"type": "string"},
#     "page": {"type": "integer", "default": 1}
#   },
#   "required": ["system_id"]
# }
```

### 2. Automatic Routing

```python
# You write:
@mcp.tool()
async def list_systems(): pass

@mcp.tool()
async def list_containers(): pass

# FastMCP automatically routes:
# - Call to "list_systems" → list_systems()
# - Call to "list_containers" → list_containers()
```

### 3. Automatic Response Handling

```python
# You write:
return {"items": [...], "total": 42}

# FastMCP converts to:
# [TextContent(type="text", text='{"items": [...], "total": 42}')]
```

### 4. Error Handling

```python
# You write:
raise ValueError("System not found")

# FastMCP converts to proper MCP error response automatically
```

## Developer Experience

### Raw MCP SDK
```python
# Define tool (verbose)
Tool(name="...", description="...", inputSchema={...})

# Implement handler (string matching)
if name == "my_tool":
    # Extract args
    arg1 = arguments.get("arg1")
    arg2 = arguments.get("arg2", default)
    
    # Call logic
    result = await do_something(arg1, arg2)
    
    # Format response
    return [TextContent(type="text", text=json.dumps(result))]
```

### FastMCP
```python
# Everything in one place!
@mcp.tool()
async def my_tool(arg1: str, arg2: int = 42) -> dict:
    """Does something cool."""
    return await do_something(arg1, arg2)
```

## Running the Server

### Raw MCP SDK
```python
async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### FastMCP
```python
if __name__ == "__main__":
    mcp.run()  # That's it!
```

## Additional FastMCP Features

### Development Mode
```bash
# Interactive testing
fastmcp dev src/beszel_mcp/server.py
```

### Built-in CLI
```bash
# Run production
fastmcp run src/beszel_mcp/server.py

# Install as tool
fastmcp install src/beszel_mcp/server.py
```

### Hot Reloading
```bash
# Auto-restart on code changes
fastmcp dev --reload src/beszel_mcp/server.py
```

## Conclusion

FastMCP is to MCP what Flask is to WSGI - a high-level framework that handles the boring parts so you can focus on your application logic. 

**Use FastMCP when:**
- ✅ You want to build MCP servers quickly
- ✅ You prefer clean, readable code
- ✅ You want automatic schema generation
- ✅ You value developer experience
- ✅ You're building a new MCP server

**Use raw MCP SDK when:**
- ⚠️ You need fine-grained control over every detail
- ⚠️ You're extending an existing low-level implementation
- ⚠️ You need features not yet in FastMCP

For 99% of use cases, **FastMCP is the better choice**.
