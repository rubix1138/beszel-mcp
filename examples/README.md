# Example Configuration Files

This directory contains example configuration files for integrating the Beszel MCP server with Claude Desktop and other MCP clients.

## config-uv.json (Recommended)

Configuration using uv/uvx for automatic dependency management:

```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/beszel-mcp", "beszel-mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-password-here"
      }
    }
  }
}
```

**Note:** Replace `/absolute/path/to/beszel-mcp` with the actual path to your project directory.

## config.json

Basic configuration using Python module:

```json
{
  "mcpServers": {
    "beszel": {
      "command": "python",
      "args": ["-m", "beszel_mcp"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-password-here"
      }
    }
  }
}
```

## config-uvx.json

Alternative configuration using uvx (recommended for easier dependency management):

```json
{
  "mcpServers": {
    "beszel": {
      "command": "uvx",
      "args": ["--from", ".", "fastmcp", "run", "src/beszel_mcp/server.py"],
      "env": {
        "BESZEL_URL": "http://localhost:8090",
        "BESZEL_EMAIL": "admin@example.com",
        "BESZEL_PASSWORD": "your-password-here"
      }
    }
  }
}
```

## Configuration Locations

### Claude Desktop

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Environment Variables

All configurations support these environment variables:

- `BESZEL_URL` (required): URL of your Beszel/PocketBase instance
- `BESZEL_EMAIL` (optional): Admin email for authentication
- `BESZEL_PASSWORD` (optional): Admin password for authentication

## Security Note

Never commit actual passwords to version control. Use placeholder values in example files and set actual credentials through:

1. Environment variables
2. Secret management tools
3. Secure configuration files (not in git)
