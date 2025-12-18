# Beszel MCP Server - Project Summary

## Overview

A complete Model Context Protocol (MCP) server implementation for the Beszel system monitoring tool. This server enables AI assistants like Claude to interact with Beszel's monitoring data through natural language queries.

## Project Structure

```
beszel-mcp/
├── src/beszel_mcp/          # Main package source code
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point for running as module
│   ├── server.py            # MCP server implementation
│   └── pocketbase_client.py # PocketBase API client
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_client.py       # PocketBase client tests
├── docs/                    # Documentation
│   ├── QUICKSTART.md        # Quick start guide
│   ├── API_REFERENCE.md     # PocketBase collections reference
│   └── TROUBLESHOOTING.md   # Common issues and solutions
├── examples/                # Example configurations and queries
│   ├── config.json          # Example Claude Desktop config
│   └── queries.md           # Example queries
├── pyproject.toml           # Project metadata and dependencies
├── setup.sh                 # Development setup script
├── pytest.ini               # Pytest configuration
├── README.md                # Main documentation
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```

## Core Components

### 1. PocketBase Client (`pocketbase_client.py`)

A comprehensive async client for interacting with PocketBase:
- Authentication with admin credentials
- Record listing with pagination
- Filtering and sorting support
- Time-range query builder
- Proper error handling

Key Methods:
- `authenticate()` - Admin authentication
- `get_list()` - Paginated record listing
- `get_one()` - Single record retrieval
- `query_stats()` - Statistics queries
- `build_time_filter()` - Time-range filter builder

### 2. MCP Server (`server.py`)

Implements the Model Context Protocol:
- Tool registration and listing
- Request handling
- Response formatting
- Error management
- Environment configuration

### 3. Available Tools

Six powerful tools for monitoring:

1. **list_systems**
   - List all monitored systems
   - Supports filtering by name, status, etc.
   - Pagination and sorting

2. **list_containers**
   - List all Docker containers
   - Filter by system, status, image
   - Detailed container information

3. **list_alerts**
   - View alert configurations
   - Filter by type, threshold, status
   - See notification settings

4. **list_alert_history**
   - Historical alert records
   - Track triggered and resolved alerts
   - Time-based filtering

5. **query_system_stats**
   - Time-series system statistics
   - CPU, memory, disk, network metrics
   - Custom time ranges

6. **query_container_stats**
   - Container resource usage over time
   - CPU, memory, network stats
   - Performance trend analysis

## Key Features

### Filtering
Uses PocketBase's powerful filter syntax:
```
name ~ 'prod'                    # Contains
status = 'active'                # Exact match
cpu > 80                         # Comparison
created >= '2024-01-01'          # Date range
(cpu > 80 || memory > 90)        # Complex logic
```

### Sorting
Flexible sorting options:
```
-created     # Descending by creation date
name         # Ascending by name
-cpu,name    # Multiple fields
```

### Pagination
Handle large datasets efficiently:
- Configurable page size
- Page navigation
- Total count information

### Time Ranges
Query statistics for specific periods:
- ISO 8601 timestamp format
- Start and end time filtering
- Historical data analysis

## Integration

### Claude Desktop

Add to `claude_desktop_config.json`:
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

### Environment Variables

Required:
- `BESZEL_URL` - PocketBase instance URL

Optional (for authenticated access):
- `BESZEL_EMAIL` - Admin email
- `BESZEL_PASSWORD` - Admin password

## Technology Stack

- **Python 3.10+** - Core language
- **FastMCP** - High-level MCP framework (simpler than raw MCP SDK)
- **httpx** - Async HTTP client
- **pytest** - Testing framework

## Use Cases

### System Monitoring
- Check system health and status
- Monitor resource usage
- Track performance trends
- Identify bottlenecks

### Container Management
- View running containers
- Monitor container resources
- Analyze container performance
- Track container lifecycle

### Alert Management
- Review alert configurations
- Check triggered alerts
- Investigate alert patterns
- Plan alert improvements

### Capacity Planning
- Analyze historical trends
- Identify peak usage times
- Forecast resource needs
- Plan infrastructure scaling

### Troubleshooting
- Diagnose performance issues
- Correlate alerts with metrics
- Review system history
- Identify root causes

## Example Queries

### Basic Monitoring
```
"Show me all systems and their current status"
"What containers are running on system abc123?"
"Are there any active alerts?"
```

### Performance Analysis
```
"Show me CPU trends for system xyz over the last 24 hours"
"Which systems had high memory usage yesterday?"
"What's the average CPU usage across all systems?"
```

### Alert Investigation
```
"What alerts were triggered in the last hour?"
"Show me all unresolved alerts"
"Which systems triggered the most alerts this week?"
```

### Capacity Planning
```
"Which systems are approaching 80% CPU usage?"
"Show me disk usage trends for the last month"
"What's the growth rate of container resource usage?"
```

## Development Workflow

1. **Setup**: Run `./setup.sh`
2. **Develop**: Edit code in `src/beszel_mcp/`
3. **Test**: Run `pytest`
4. **Document**: Update relevant docs
5. **Commit**: Follow contribution guidelines

## Testing

Comprehensive test suite:
- Unit tests for PocketBase client
- Mock HTTP interactions
- Async test support with pytest-asyncio
- Coverage reporting

Run tests:
```bash
pytest                           # All tests
pytest --cov=beszel_mcp         # With coverage
pytest tests/test_client.py     # Specific file
```

## Documentation

Complete documentation set:
- **README.md** - Main documentation
- **QUICKSTART.md** - Fast setup guide
- **API_REFERENCE.md** - PocketBase collections
- **TROUBLESHOOTING.md** - Common issues
- **CONTRIBUTING.md** - Development guide
- **examples/** - Sample configurations

## Best Practices

### Security
- Use environment variables for credentials
- Never commit sensitive data
- Use HTTPS in production
- Rotate credentials regularly

### Performance
- Use pagination for large result sets
- Apply filters to reduce data transfer
- Use specific time ranges for stats
- Cache results when appropriate

### Reliability
- Proper error handling
- Informative error messages
- Connection retry logic
- Timeout configuration

## Future Enhancements

Potential additions:
- Real-time monitoring with WebSocket support
- Advanced analytics and aggregations
- Alert management (create, update, delete)
- System and container management tools
- Reporting and dashboard generation
- Export functionality
- Batch operations
- Webhook integration

## Support

- Documentation in `docs/` directory
- Examples in `examples/` directory
- Issue tracker for bug reports
- Discussions for questions

## License

MIT License - see LICENSE file for details

## Quick Commands

```bash
# Setup
./setup.sh

# Run server
python -m beszel_mcp

# Run tests
pytest

# Install for development
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

## Summary

The Beszel MCP Server provides a complete, production-ready integration between AI assistants and the Beszel monitoring system. With comprehensive documentation, robust error handling, and extensive testing, it enables natural language queries for system monitoring, container management, and performance analysis.
