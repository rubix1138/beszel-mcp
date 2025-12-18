# Beszel MCP Server - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Desktop / MCP Client              │
│                    (or other MCP-compatible client)             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ MCP Protocol (stdio)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      Beszel MCP Server                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              MCP Server (server.py)                     │  │
│  │                                                         │  │
│  │  • Tool Registration                                    │  │
│  │  • Request Handling                                     │  │
│  │  • Response Formatting                                  │  │
│  │  • Error Management                                     │  │
│  └────────────────────┬────────────────────────────────────┘  │
│                       │                                         │
│  ┌────────────────────▼────────────────────────────────────┐  │
│  │        PocketBase Client (pocketbase_client.py)         │  │
│  │                                                         │  │
│  │  • Authentication                                       │  │
│  │  • HTTP Request Management                              │  │
│  │  • Filter Building                                      │  │
│  │  • Response Parsing                                     │  │
│  └────────────────────┬────────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ HTTP/HTTPS
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                  PocketBase / Beszel Backend                    │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  systems    │  │container_    │  │  alerts_history    │   │
│  │             │  │  stats       │  │                    │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ containers  │  │ system_stats │  │     alerts         │   │
│  │             │  │              │  │                    │   │
│  └─────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. List Systems Flow

```
User Query: "Show me all systems"
         │
         ▼
┌─────────────────────┐
│  Claude interprets  │
│  and selects tool:  │
│  "list_systems"     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  MCP Server         │
│  call_tool()        │
│  receives request   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PocketBase Client  │
│  get_list()         │
│  builds request     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP GET Request   │
│  to PocketBase:     │
│  /api/collections/  │
│  systems/records    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PocketBase         │
│  returns JSON       │
│  with systems data  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  MCP Server formats │
│  response as        │
│  TextContent        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Claude displays    │
│  results to user    │
└─────────────────────┘
```

### 2. Query System Stats Flow

```
User Query: "Show CPU stats for system abc123 in last hour"
         │
         ▼
┌─────────────────────┐
│  Claude extracts:   │
│  - Tool: query_     │
│    system_stats     │
│  - system_id:       │
│    "abc123"         │
│  - time range       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  MCP Server         │
│  builds filter:     │
│  "system='abc123'   │
│  && created >=      │
│  '<timestamp>'"     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PocketBase Client  │
│  query_stats()      │
│  with filter        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP GET Request   │
│  with filter and    │
│  sort parameters    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PocketBase returns │
│  filtered stats     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Claude analyzes    │
│  and presents data  │
└─────────────────────┘
```

## Component Interactions

### MCP Server Tools

```
┌───────────────────────────────────────────────────────┐
│                  Available Tools                      │
├───────────────────────────────────────────────────────┤
│                                                       │
│  list_systems          ──▶  PocketBase: systems      │
│                                                       │
│  list_containers       ──▶  PocketBase: containers   │
│                                                       │
│  list_alerts           ──▶  PocketBase: alerts       │
│                                                       │
│  list_alert_history    ──▶  PocketBase:              │
│                             alerts_history            │
│                                                       │
│  query_system_stats    ──▶  PocketBase:              │
│                             system_stats              │
│                                                       │
│  query_container_stats ──▶  PocketBase:              │
│                             container_stats           │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Authentication Flow

```
┌──────────────┐
│  Server      │
│  Startup     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     Yes    ┌──────────────┐
│ Credentials  │───────────▶│ Authenticate │
│ Provided?    │            │ with         │
└──────┬───────┘            │ PocketBase   │
       │                    └──────┬───────┘
       │ No                        │
       │                           ▼
       │                    ┌──────────────┐
       │                    │ Store auth   │
       │                    │ token        │
       │                    └──────┬───────┘
       │                           │
       └───────────┬───────────────┘
                   │
                   ▼
            ┌──────────────┐
            │ Add token to │
            │ all requests │
            └──────────────┘
```

## Error Handling Flow

```
┌──────────────┐
│  User        │
│  Request     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  MCP Server  │
│  validates   │
└──────┬───────┘
       │
       ├─ Valid ────────────▶ Process
       │
       └─ Invalid ──▶ Return Error
                     TextContent
       
┌──────────────┐
│  HTTP        │
│  Request     │
└──────┬───────┘
       │
       ├─ Success ─────────▶ Parse & Return
       │
       ├─ 4xx Error ──▶ Authentication/
       │                  Permission Error
       │
       └─ 5xx Error ──▶ Server Error
                        with details
```

## Configuration Flow

```
┌────────────────────────┐
│  Environment Variables │
│  ┌──────────────────┐  │
│  │ BESZEL_URL       │  │
│  │ BESZEL_EMAIL     │  │
│  │ BESZEL_PASSWORD  │  │
│  └──────────────────┘  │
└───────────┬────────────┘
            │
            ▼
┌───────────────────────┐
│  get_client()         │
│  creates PocketBase   │
│  client instance      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Client singleton     │
│  reused for all       │
│  requests             │
└───────────────────────┘
```

## Deployment Architecture

### Local Development

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   Developer    │────▶│  Python venv   │────▶│   Local        │
│   Machine      │     │  with Beszel   │     │   Beszel       │
│                │     │  MCP Server    │     │   Instance     │
└────────────────┘     └────────────────┘     └────────────────┘
```

### Claude Desktop Integration

```
┌────────────────┐
│ Claude Desktop │
│                │
│  ┌──────────┐  │     ┌────────────────┐     ┌────────────────┐
│  │ Config   │──┼────▶│  Beszel MCP    │────▶│  Production    │
│  │ JSON     │  │     │  Server        │     │  Beszel        │
│  └──────────┘  │     │  (subprocess)  │     │  Server        │
└────────────────┘     └────────────────┘     └────────────────┘
```

### Production Setup

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  AI Assistant  │────▶│  Beszel MCP    │────▶│  Beszel        │
│  (Claude, etc) │     │  Server        │     │  + PocketBase  │
│                │     │  (systemd/     │     │  (Docker)      │
│                │     │   supervisor)  │     │                │
└────────────────┘     └────────────────┘     └────┬───────────┘
                                                    │
                                             ┌──────▼───────┐
                                             │  Monitored   │
                                             │  Systems &   │
                                             │  Containers  │
                                             └──────────────┘
```

## Key Design Principles

1. **Async First**: All I/O operations are async for performance
2. **Single Responsibility**: Each component has a clear purpose
3. **Error Resilience**: Comprehensive error handling at all levels
4. **Stateless**: Server maintains no state between requests
5. **Configurable**: Environment-based configuration
6. **Testable**: Mock-friendly design for testing
7. **Documented**: Clear documentation at all levels
8. **Extensible**: Easy to add new tools and features
