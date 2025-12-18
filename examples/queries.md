# Example Queries for Beszel MCP Server

## List all systems
```
Can you list all the systems being monitored?
```

## List systems with filtering
```
Show me all systems that have 'prod' in their name
```
Uses filter: `name ~ 'prod'`

## Query system statistics
```
Show me the CPU and memory stats for system abc123 for the last 24 hours
```

## List recent alerts
```
What alerts have been triggered in the last hour?
```
Uses filter: `created >= '2024-12-15T10:00:00Z'`

## List containers on a specific system
```
Show me all containers running on system xyz789
```
Uses filter: `system = 'xyz789'`

## Query container statistics
```
Get the resource usage for container def456 over the past week
```

## Complex filtering examples

### High CPU usage
Filter: `cpu > 80 && status = 'active'`

### Memory alerts
Filter: `type = 'memory' && triggered = true`

### Date range
Filter: `created >= '2024-01-01' && created <= '2024-12-31'`

### Multiple conditions
Filter: `(cpu > 80 || memory > 90) && name ~ 'server'`

## Sorting examples

### Most recent first
Sort: `-created`

### Oldest first
Sort: `created`

### By name
Sort: `name`

### Multiple fields
Sort: `-cpu,name`
