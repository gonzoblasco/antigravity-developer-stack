# MCP Standard Guide

Extended guide for implementing Model Context Protocol (MCP) tools following best practices.

> [!NOTE]
> For comprehensive MCP server creation (not just tools), see the `mcp-builder` skill.
> This guide focuses on tool-level patterns within MCP.

## Table of Contents

1. [MCP Architecture Overview](#mcp-architecture-overview)
2. [Tool Implementation Patterns](#tool-implementation-patterns)
3. [Resources vs Tools](#resources-vs-tools)
4. [Stateful Tools](#stateful-tools)
5. [Streaming Responses](#streaming-responses)
6. [Authentication & Security](#authentication--security)

---

## MCP Architecture Overview

### The Three MCP Primitives

```
┌─────────────────┐
│  MCP Server     │
├─────────────────┤
│  Tools          │ ← Function calling (dynamic)
│  Resources      │ ← Data access (static/semi-static)
│  Prompts        │ ← Behavior templates
└─────────────────┘
```

**When to use each:**

- **Tools:** Actions, computations, anything dynamic
- **Resources:** Schemas, docs, configs (read-only data)
- **Prompts:** Pre-built prompt templates for common tasks

---

## Tool Implementation Patterns

### Basic Tool (FastMCP)

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_docs(query: str, limit: int = 10) -> dict:
    """
    Searches documentation using full-text search.

    Accepts query (string, 1-500 chars) and limit (int, 1-50, default 10).
    Returns {results: array of {title, content, score}, total: int}.
    Throws 'service_unavailable' if search index is down.
    """
    # Implementation
    return {"results": [...], "total": 42}
```

### Tool with Complex Input (MCP SDK - TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({
  name: "my-tools",
  version: "1.0.0",
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "analyze_code",
      description:
        "Analyzes code for issues. Accepts code (string), language (enum), and optional rules (array). Returns {issues: array of {line, severity, message}}.",
      inputSchema: {
        type: "object",
        properties: {
          code: {
            type: "string",
            description: "Code to analyze",
          },
          language: {
            type: "string",
            enum: ["python", "javascript", "typescript"],
            description: "Programming language",
          },
          rules: {
            type: "array",
            items: { type: "string" },
            description: "Optional lint rules to apply",
            default: [],
          },
        },
        required: ["code", "language"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "analyze_code") {
    const { code, language, rules = [] } = request.params.arguments;

    // Implementation
    const issues = analyzecode(code, language, rules);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ issues }),
        },
      ],
    };
  }
});
```

### Tool with Validation

```python
from fastmcp import FastMCP, MCPError

mcp = FastMCP("validated-tools")

@mcp.tool()
def create_user(
    email: str,
    role: str = "user",
    metadata: dict = None
) -> dict:
    """
    Creates a new user account.

    Accepts email (string, valid email format), role (enum: admin|user, default user),
    and optional metadata (object).
    Returns {user_id: string, created_at: string}.
    Throws 'invalid_email' if email format is wrong, 'duplicate_email' if already exists.
    """

    # Validation beyond JSON Schema
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        raise MCPError(
            "invalid_email",
            f"Email '{email}' is not valid. Use format: user@example.com"
        )

    if role not in ["admin", "user"]:
        raise MCPError(
            "invalid_role",
            f"Role '{role}' is invalid. Allowed: admin, user"
        )

    # Check for duplicates
    if user_exists(email):
        raise MCPError(
            "duplicate_email",
            f"User with email '{email}' already exists. Use a different email or update existing user."
        )

    # Create user
    user = create_user_in_db(email, role, metadata or {})

    return {
        "user_id": user.id,
        "created_at": user.created_at.isoformat()
    }
```

---

## Resources vs Tools

### When to Use Resources

Resources are for **static or semi-static data** that doesn't require computation per request:

```python
@mcp.resource("schema://database")
def get_database_schema() -> str:
    """Database schema in JSON format"""
    return json.dumps({
        "tables": {
            "users": {
                "columns": ["id", "email", "created_at"]
            }
        }
    })

@mcp.resource("docs://api/v1")
def get_api_docs() -> str:
    """API documentation"""
    return open("api_docs.md").read()
```

**Advantages:**

- Lower latency (can be cached)
- No parameters needed
- Perfect for schemas, configs, docs

### When to Use Tools

Tools are for **dynamic operations** that require input:

```python
@mcp.tool()
def query_database(sql: str) -> dict:
    """Execute SQL query dynamically"""
    return {"results": execute_sql(sql)}
```

### Hybrid Pattern: Resource + Tool

```python
# Resource: Static schema for reference
@mcp.resource("schema://users")
def user_schema():
    return """
    User Schema:
    - id: string (UUID)
    - email: string
    - role: enum (admin|user)
    """

# Tool: Dynamic query
@mcp.tool()
def query_users(filters: dict) -> dict:
    """Query users table using the schema from schema://users"""
    return {"users": [...]}
```

LLM can reference the resource to understand structure, then use the tool for dynamic queries.

---

## Stateful Tools

### Problem: Tools are Stateless

Each tool call is independent - no shared state by default.

### Solution 1: External State Store

```python
import redis

redis_client = redis.Redis()

@mcp.tool()
def start_workflow(workflow_id: str) -> dict:
    """Starts a multi-step workflow"""
    redis_client.set(f"workflow:{workflow_id}", json.dumps({
        "status": "started",
        "step": 1,
        "created_at": datetime.now().isoformat()
    }))
    return {"workflow_id": workflow_id, "status": "started"}

@mcp.tool()
def continue_workflow(workflow_id: str, data: dict) -> dict:
    """Continues workflow to next step"""
    state = json.loads(redis_client.get(f"workflow:{workflow_id}"))
    state["step"] += 1
    state["data"] = data
    redis_client.set(f"workflow:{workflow_id}", json.dumps(state))
    return state
```

### Solution 2: Session-Based State (MCP 1.0+)

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("stateful-server")

@mcp.tool()
def init_session(context: Context) -> dict:
    """Initialize persistent session"""
    context.session["user_id"] = generate_id()
    context.session["created_at"] = datetime.now()
    return {"session_id": context.session["user_id"]}

@mcp.tool()
def add_to_cart(item_id: str, context: Context) -> dict:
    """Add item to cart (persists across calls)"""
    if "cart" not in context.session:
        context.session["cart"] = []

    context.session["cart"].append(item_id)
    return {"cart": context.session["cart"]}
```

---

## Streaming Responses

### When to Stream

- Large datasets (> 100 items)
- Progressive results (search as you type)
- Long-running operations (live updates)
- Real-time data (logs, metrics)

### Streaming Pattern (FastMCP)

```python
@mcp.tool()
async def search_large_dataset(query: str) -> dict:
    """
    Searches large dataset with streaming results.

    Returns results progressively as they're found.
    """
    async def stream_results():
        for batch in search_in_batches(query, batch_size=10):
            yield {
                "batch": batch,
                "has_more": True
            }

        yield {"has_more": False}

    return stream_results()
```

### Streaming with Progress Updates

```python
@mcp.tool()
async def process_large_file(file_url: str) -> dict:
    """
    Processes large file with progress updates.
    """
    total_lines = count_lines(file_url)

    async def process_with_progress():
        processed = 0

        for chunk in read_chunks(file_url):
            result = process_chunk(chunk)
            processed += len(chunk)

            yield {
                "progress": processed / total_lines,
                "processed_lines": processed,
                "total_lines": total_lines,
                "current_result": result
            }

        yield {"complete": True}

    return process_with_progress()
```

---

## Authentication & Security

### API Key Authentication

```python
from fastmcp import FastMCP, Context, MCPError

mcp = FastMCP("secure-server")

def verify_api_key(api_key: str) -> bool:
    """Verify API key against database"""
    return api_key in get_valid_keys()

@mcp.tool()
def protected_operation(
    data: dict,
    api_key: str,
    context: Context
) -> dict:
    """
    Performs protected operation requiring API key.

    Accepts data (object) and api_key (string).
    Throws 'unauthorized' if API key is invalid.
    """
    if not verify_api_key(api_key):
        raise MCPError(
            "unauthorized",
            "Invalid API key. Obtain a valid key from the admin panel."
        )

    # Perform operation
    return {"status": "success"}
```

### OAuth2 Pattern

```python
@mcp.tool()
def oauth_protected_call(
    access_token: str,
    resource_id: str
) -> dict:
    """
    Calls external API with OAuth2 token.

    Accepts access_token (string) and resource_id (string).
    Throws 'token_expired' if token needs refresh, 'unauthorized' if token invalid.
    """
    import requests

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"https://api.example.com/{resource_id}", headers=headers)

    if response.status_code == 401:
        # Check if expired vs invalid
        if "expired" in response.text.lower():
            raise MCPError(
                "token_expired",
                "Access token expired. Refresh token and retry.",
                {"retry_with_refresh": True}
            )
        else:
            raise MCPError(
                "unauthorized",
                "Access token is invalid. Re-authenticate to get new token."
            )

    return response.json()
```

### Rate Limiting

```python
from fastmcp import FastMCP
import time

# Simple in-memory rate limiter
rate_limits = {}

@mcp.tool()
def rate_limited_search(query: str, user_id: str) -> dict:
    """
    Search with rate limiting (10 requests per minute per user).

    Throws 'rate_limit_exceeded' if user exceeds limit.
    """
    now = time.time()
    minute_ago = now - 60

    # Clean old entries
    if user_id in rate_limits:
        rate_limits[user_id] = [t for t in rate_limits[user_id] if t > minute_ago]
    else:
        rate_limits[user_id] = []

    # Check limit
    if len(rate_limits[user_id]) >= 10:
        raise MCPError(
            "rate_limit_exceeded",
            f"Rate limit exceeded. You can make 10 requests per minute. Try again in {60 - (now - rate_limits[user_id][0]):.0f} seconds."
        )

    # Record this request
    rate_limits[user_id].append(now)

    # Perform search
    return {"results": [...]}
```

---

## Best Practices Summary

### Tool Design

1. ✅ Clear, complete descriptions
2. ✅ Specific input/output schemas
3. ✅ Structured error responses
4. ✅ Validation beyond JSON Schema
5. ✅ Examples for complex types

### Performance

1. ✅ Use resources for static data
2. ✅ Stream large responses
3. ✅ Cache when possible
4. ✅ Set reasonable timeouts

### Security

1. ✅ Validate all inputs (never trust LLM output)
2. ✅ Use authentication for sensitive operations
3. ✅ Rate limit to prevent abuse
4. ✅ Sanitize outputs (no sensitive data leaks)
5. ✅ Log operations for audit trail

### State Management

1. ✅ Use external store (Redis, DB) for persistence
2. ✅ Session state for user-specific data
3. ✅ Include workflow IDs for multi-step operations
4. ✅ Provide status checking tools for async operations

---

## Further Reading

- [MCP Official Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP SDK (TypeScript)](https://github.com/modelcontextprotocol/typescript-sdk)
- **`mcp-builder` skill** - For complete MCP server architecture
