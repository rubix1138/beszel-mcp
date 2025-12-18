# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Errors

**Problem:** `Failed to authenticate with PocketBase`

**Solutions:**
1. Verify your `BESZEL_URL` is correct and accessible
2. Check that `BESZEL_EMAIL` and `BESZEL_PASSWORD` are correct
3. Ensure the admin account exists in PocketBase
4. Try accessing the PocketBase admin UI directly at `http://your-url/_/`

### Connection Errors

**Problem:** `Connection refused` or `Timeout`

**Solutions:**
1. Verify Beszel/PocketBase is running
2. Check firewall settings
3. Ensure the URL includes the correct protocol (http/https)
4. Test connection with curl: `curl http://localhost:8090/api/health`

### No Data Returned

**Problem:** Empty results when listing systems or containers

**Solutions:**
1. Verify data exists in PocketBase admin UI
2. Check authentication - some collections may require admin access
3. Try without filters first to ensure basic connectivity works
4. Review PocketBase logs for authorization issues

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'mcp'`

**Solutions:**
1. Ensure you've installed the package: `pip install -e .`
2. Activate your virtual environment: `source venv/bin/activate`
3. Verify MCP is installed: `pip list | grep mcp`
4. Try reinstalling: `pip install --force-reinstall mcp`

### Filter Syntax Errors

**Problem:** Invalid filter string errors

**Solutions:**
1. Use single quotes for string values: `name = 'value'`
2. Use proper operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, `~` (contains)
3. Combine with `&&` (AND) or `||` (OR)
4. Example: `status = 'active' && cpu > 80`

### Time Range Queries

**Problem:** No results for time range queries

**Solutions:**
1. Use ISO 8601 format: `2024-12-15T10:00:00Z`
2. Ensure timezone is specified (Z for UTC)
3. Check that the time range makes sense (start before end)
4. Verify data exists in that time range

## Debugging Tips

### Enable Debug Logging

Add to your environment:
```bash
export PYTHONUNBUFFERED=1
export MCP_DEBUG=1
```

### Test PocketBase Connectivity

```bash
# Test health endpoint
curl http://localhost:8090/api/health

# Test collections (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8090/api/collections/systems/records
```

### Verify Environment Variables

```bash
echo $BESZEL_URL
echo $BESZEL_EMAIL
# Don't echo password in production!
```

### Check PocketBase Collections

Log into the PocketBase admin UI and verify:
1. Collections exist: systems, system_stats, containers, container_stats, alerts, alerts_history
2. Records exist in the collections
3. Your admin user has access to these collections

### Test the MCP Server Directly

```bash
# In one terminal, start the server with debug output
python -m beszel_mcp

# The server should wait for input on stdin
# Send a test message (this is just for verification)
```

## Getting Help

If you continue to have issues:

1. Check the [Beszel documentation](https://github.com/henrygd/beszel)
2. Review [PocketBase API docs](https://pocketbase.io/docs)
3. Check the [MCP specification](https://spec.modelcontextprotocol.io/)
4. Open an issue with:
   - Your environment (OS, Python version)
   - Steps to reproduce
   - Error messages
   - Relevant configuration (without sensitive data)

## Performance Considerations

### Large Result Sets

If you have many records:
1. Use pagination (`page` and `per_page` parameters)
2. Apply filters to reduce result size
3. Use specific time ranges for stats queries
4. Consider increasing `per_page` for batch operations (max usually 500)

### Rate Limiting

PocketBase may have rate limits. If you encounter issues:
1. Add delays between requests
2. Use batch operations when possible
3. Cache results when appropriate
4. Reduce polling frequency

## Security Notes

### Credentials Storage

Never commit credentials to version control:
- Use environment variables
- Use a `.env` file (and add it to `.gitignore`)
- Use a secrets manager in production
- Rotate credentials regularly

### Network Security

In production:
- Use HTTPS for PocketBase connection
- Restrict PocketBase access to trusted networks
- Use authentication for all requests
- Consider using API tokens instead of password auth

### MCP Server Security

- Run the MCP server with minimal privileges
- Validate all input parameters
- Monitor for unusual activity
- Keep dependencies updated
