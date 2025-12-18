# Changelog

All notable changes to the Beszel MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-15

### Changed
- **BREAKING**: Switched from low-level MCP SDK to FastMCP for simpler, cleaner code
- Simplified server implementation using FastMCP decorators
- Reduced boilerplate code significantly
- Updated dependencies to use FastMCP

### Added
- Full uv package manager support
- Script entry point (`beszel-mcp` command)
- uv configuration in pyproject.toml
- Comprehensive uv documentation
- Example config for uvx
- uv setup instructions in README

### Improved
- Cleaner, more maintainable codebase
- Better type hints and documentation
- Simplified tool definitions using function decorators
- Faster installation and running with uv
- Better development workflow with uv

## [0.1.0] - 2025-12-15

### Added
- Initial release of Beszel MCP Server
- PocketBase client for interacting with Beszel backend
- Six core tools:
  - `list_systems` - List all monitored systems
  - `list_containers` - List all monitored containers
  - `list_alerts` - List configured alerts
  - `list_alert_history` - List alert history
  - `query_system_stats` - Query time-series statistics for systems
  - `query_container_stats` - Query time-series statistics for containers
- Support for PocketBase filtering and sorting
- Time-range filtering for statistics queries
- Authentication support for PocketBase admin accounts
- Comprehensive documentation:
  - README with full usage instructions
  - Quick Start guide
  - API reference for PocketBase collections
  - Troubleshooting guide
  - Example queries
- Test suite with pytest
- Development setup script
- Example configuration files
- MIT License

### Features
- Async/await support for efficient I/O operations
- Pagination support for large result sets
- Flexible filtering using PocketBase query syntax
- Sorting capabilities
- Error handling and informative error messages
- Environment variable configuration
- Compatible with Claude Desktop and other MCP clients

### Documentation
- Complete README with installation and usage instructions
- API reference documenting all Beszel collections
- Quick start guide for fast setup
- Troubleshooting guide for common issues
- Example queries for common use cases
- Claude Desktop integration examples

## [Unreleased]

### Planned
- Additional tools for system and container management
- Caching layer for improved performance
- Webhook support for alert notifications
- Dashboard generation capabilities
- Historical trend analysis tools
- Batch operations support
- Enhanced error reporting with suggestions
- Performance metrics and monitoring
- Support for custom PocketBase collections
- Export functionality for reports
