# Migration Guide: v0.1.0 to v0.2.0

## Overview

Version 0.2.0 is a major rewrite using FastMCP instead of the raw MCP SDK. This results in much simpler, cleaner code while maintaining 100% API compatibility.

## What Changed

### Dependencies

**Before (v0.1.0):**
```toml
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]
```

**After (v0.2.0):**
```toml
dependencies = [
    "fastmcp>=0.2.0",
    "httpx>=0.27.0",
]
```

### Code Structure

**Before:** ~280 lines with manual tool registration and routing  
**After:** ~235 lines with decorator-based tools

## Breaking Changes

### For End Users: ⚠️ NONE!

The API remains exactly the same:
- ✅ All 6 tools work identically
- ✅ Same parameters and return values
- ✅ Same configuration (environment variables)
- ✅ Same Claude Desktop integration

**You don't need to change anything in your configuration!**

### For Developers: If You Extended the Code

If you modified `server.py` or added custom tools, you'll need to adapt to the new FastMCP style:

#### Tool Definition

**Before:**
```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="my_tool",
            description="Does something",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "..."},
                },
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "my_tool":
        result = await do_something(arguments["param1"])
        return [TextContent(type="text", text=json.dumps(result))]
```

**After:**
```python
@mcp.tool()
async def my_tool(param1: str) -> dict:
    """Does something.
    
    Args:
        param1: Description of param1
    """
    return await do_something(param1)
```

Much simpler! ✨

## Migration Steps

### For End Users (No Code Changes)

1. Pull the latest code:
   ```bash
   cd /path/to/beszel-mcp
   git pull
   ```

2. Reinstall dependencies:
   ```bash
   ./setup.sh
   # or
   pip install -e .
   ```

3. Restart your MCP client (e.g., restart Claude Desktop)

That's it! Everything should work exactly as before.

### For Developers (With Custom Extensions)

1. Update dependencies:
   ```bash
   pip install fastmcp
   ```

2. Convert your custom tools to FastMCP decorators:
   - Change `@app.list_tools()` + `@app.call_tool()` to `@mcp.tool()`
   - Use type hints instead of JSON schemas
   - Return data directly instead of wrapping in TextContent
   - Move descriptions to docstrings

3. Test your changes:
   ```bash
   fastmcp dev src/beszel_mcp/server.py
   ```

## Benefits of Upgrading

- ✅ **Less code**: 16% reduction in lines of code
- ✅ **Cleaner**: No more boilerplate
- ✅ **Safer**: Type hints catch errors earlier
- ✅ **Easier**: Adding new tools is simpler
- ✅ **Better DX**: Dev mode with hot reloading

## Rollback (If Needed)

If you need to rollback to v0.1.0:

```bash
git checkout v0.1.0
pip install -e .
```

## Questions?

- Check the [Why FastMCP?](WHY_FASTMCP.md) guide for details
- Review the new [server.py](../src/beszel_mcp/server.py) for examples
- Open an issue if you encounter problems

## Timeline

- **v0.1.0**: Released December 15, 2025 (raw MCP SDK)
- **v0.2.0**: Released December 15, 2025 (FastMCP rewrite)

The migration is straightforward and brings significant improvements with no API changes! 🎉
