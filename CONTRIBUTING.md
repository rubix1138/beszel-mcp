# Contributing to Beszel MCP Server

Thank you for your interest in contributing to the Beszel MCP Server! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/beszel-mcp.git`
3. Run the setup script: `./setup.sh`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites
- Python 3.10 or higher
- A running Beszel instance for testing
- Git

### Environment Setup

```bash
# Run the setup script
./setup.sh

# Activate the virtual environment
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

### Environment Variables

Create a `.env` file for testing:

```env
BESZEL_URL=http://localhost:8090
BESZEL_EMAIL=admin@example.com
BESZEL_PASSWORD=your-test-password
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function arguments and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Example

```python
async def get_system_stats(
    system_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict[str, Any]:
    """Get statistics for a specific system.
    
    Args:
        system_id: The ID of the system
        start_time: Optional start time in ISO 8601 format
        end_time: Optional end time in ISO 8601 format
        
    Returns:
        Dictionary containing system statistics
        
    Raises:
        ValueError: If system_id is invalid
        Exception: If the API request fails
    """
    # Implementation here
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=beszel_mcp

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_authenticate
```

### Writing Tests

- Write tests for all new functionality
- Use pytest fixtures for common setup
- Mock external dependencies (HTTP calls, etc.)
- Test both success and error cases
- Aim for high test coverage

### Example Test

```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_list_systems(client):
    """Test listing systems."""
    with patch.object(client.client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "test"}]
        }
        mock_get.return_value = mock_response
        
        result = await client.get_list("systems")
        assert len(result["items"]) == 1
```

## Adding New Features

### Adding a New Tool

1. Add the tool definition in `server.py` in the `list_tools()` function
2. Implement the tool handler in `call_tool()`
3. Add client methods in `pocketbase_client.py` if needed
4. Write tests for the new functionality
5. Update documentation

Example:

```python
# In list_tools()
Tool(
    name="my_new_tool",
    description="Description of what the tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description",
            },
        },
        "required": ["param1"],
    },
)

# In call_tool()
elif name == "my_new_tool":
    result = await client.my_new_method(arguments["param1"])
```

### Extending the PocketBase Client

When adding new client methods:

1. Add async method to `PocketBaseClient` class
2. Use type hints
3. Add proper error handling
4. Write docstrings
5. Write tests

## Documentation

### Updating Documentation

When adding features or making changes:

1. Update README.md with new capabilities
2. Add examples to `examples/queries.md`
3. Update API_REFERENCE.md if adding new collections
4. Add troubleshooting tips if relevant
5. Update CHANGELOG.md

### Documentation Style

- Use clear, concise language
- Provide code examples
- Include both simple and complex use cases
- Document limitations and known issues

## Pull Request Process

1. **Create a branch**: Use a descriptive name like `feature/add-system-management` or `fix/authentication-error`

2. **Make your changes**: 
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation

3. **Test thoroughly**:
   ```bash
   pytest
   # Test manually with a real Beszel instance
   python -m beszel_mcp
   ```

4. **Commit your changes**:
   - Use clear commit messages
   - Reference issues if applicable
   - Keep commits focused and atomic

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide a clear description of changes
   - Link to related issues
   - Describe testing performed
   - List any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] CHANGELOG.md updated
```

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs
- Beszel/PocketBase version

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Example of how it would work
- Any implementation ideas

## Code Review

All contributions will be reviewed. Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Build and publish to PyPI (maintainers only)

## Questions?

- Check existing documentation
- Look at existing code for examples
- Ask questions in issues or discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
