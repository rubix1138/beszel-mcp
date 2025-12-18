"""Main entry point for the Beszel MCP server."""

from .server import mcp


def main():
    """Entry point for the beszel-mcp command."""
    mcp.run()


if __name__ == "__main__":
    main()
