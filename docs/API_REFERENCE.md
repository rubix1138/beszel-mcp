# Beszel API Collections Reference

This document describes the PocketBase collections used by Beszel for reference when using the MCP server.

## Collections

### systems
Stores information about monitored systems.

**Common Fields:**
- `id` - Unique system identifier
- `name` - System name
- `host` - Hostname or IP address
- `status` - System status (e.g., "active", "inactive")
- `created` - Creation timestamp
- `updated` - Last update timestamp

### system_stats
Time-series statistics for systems.

**Common Fields:**
- `id` - Record ID
- `system` - Reference to system ID
- `cpu` - CPU usage percentage
- `memory` - Memory usage
- `disk` - Disk usage
- `network_in` - Network input
- `network_out` - Network output
- `created` - Timestamp of the stat record

### containers
Information about Docker containers.

**Common Fields:**
- `id` - Container ID
- `name` - Container name
- `system` - Reference to system ID
- `image` - Container image
- `status` - Container status
- `created` - Creation timestamp
- `updated` - Last update timestamp

### container_stats
Time-series statistics for containers.

**Common Fields:**
- `id` - Record ID
- `container` - Reference to container ID
- `cpu` - CPU usage
- `memory` - Memory usage
- `network_in` - Network input
- `network_out` - Network output
- `created` - Timestamp

### alerts
Alert configuration and rules.

**Common Fields:**
- `id` - Alert ID
- `name` - Alert name
- `type` - Alert type (e.g., "cpu", "memory", "disk")
- `threshold` - Threshold value
- `system` - Reference to system ID (optional)
- `container` - Reference to container ID (optional)
- `enabled` - Whether the alert is active
- `created` - Creation timestamp

### alerts_history
Historical record of triggered alerts.

**Common Fields:**
- `id` - History record ID
- `alert` - Reference to alert ID
- `system` - Reference to system ID
- `container` - Reference to container ID (optional)
- `value` - The value that triggered the alert
- `message` - Alert message
- `triggered` - When the alert was triggered
- `resolved` - When the alert was resolved (if applicable)
- `created` - Record creation timestamp

## Filter Examples

### Systems
```
# Active systems
filter="status = 'active'"

# Systems with name containing 'prod'
filter="name ~ 'prod'"

# Systems created after a date
filter="created >= '2024-01-01'"
```

### Statistics
```
# High CPU usage
filter="cpu > 80"

# Stats for specific system in time range
filter="system = 'SYSTEM_ID' && created >= '2024-01-01' && created <= '2024-01-31'"

# Recent stats (last hour)
filter="created >= '2024-12-15T10:00:00Z'"
```

### Alerts
```
# Enabled alerts
filter="enabled = true"

# CPU alerts
filter="type = 'cpu'"

# Alerts for specific system
filter="system = 'SYSTEM_ID'"
```

### Alert History
```
# Recent alerts
filter="created >= '2024-12-15'"

# Unresolved alerts
filter="resolved = null"

# Alerts for specific system
filter="system = 'SYSTEM_ID'"
```

## Sort Examples

```
# Most recent first
sort="-created"

# Oldest first
sort="created"

# By name alphabetically
sort="name"

# By CPU usage descending
sort="-cpu"

# Multiple fields
sort="-cpu,name"
```
