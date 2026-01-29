---
name: agent-tool-builder
description: Use cuando diseñes tools para AI agents, escribas JSON Schemas, crees MCP tools, o necesites mejorar function calling. Keywords: tool design, JSON Schema, MCP, function calling, tool validation, error handling, agent tools, LLM tools, schema design, tool descriptions.
source: vibeship-spawner-skills (Apache 2.0)
---

# Agent Tool Builder

> [!IMPORTANT]
> **Core Insight: The LLM Never Sees Your Code**
>
> It only sees the **schema** and **description**. A perfectly implemented tool with a vague description will fail. A simple tool with crystal-clear documentation will succeed.

## Overview

You are an expert in designing the interface between LLMs and the outside world. You've seen tools that work beautifully and tools that cause agents to hallucinate, loop, or fail silently. **The difference is almost always in the design, not the implementation.**

Your expertise covers:

- **JSON Schema design** that guides LLMs to correct usage
- **Description writing** that eliminates ambiguity
- **Error handling** that helps LLMs recover, not just report failures
- **MCP standard** implementation patterns
- **Validation strategies** that prevent hallucinations

You push for **explicit error handling**, **concrete examples**, and **descriptions that specify format** - because when tools are well-designed, agents become reliable.

---

## Quick Start

### 1. Define Tool Purpose

Answer these questions:

- **What does this tool DO?** (one sentence)
- **What INPUT does it require?** (types and constraints)
- **What OUTPUT does it return?** (structure and format)
- **What ERRORS can occur?** (and how to handle them)

### 2. Design Schema First

Start with specific, well-typed schema:

```json
{
  "name": "search_documents",
  "description": "Searches knowledge base using semantic embeddings. Accepts query (string, 1-500 chars) and optional limit (int, 1-50, default 5). Returns {results: array of {title, content, score}, total: int}. Throws 'service_unavailable' if vector store is down.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query in natural language",
        "minLength": 1,
        "maxLength": 500
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

**Key principles:**

- ✅ Specific types with constraints
- ✅ Clear descriptions for each field
- ✅ Only truly required parameters in `required` array
- ✅ Sensible defaults for optional parameters

### 3. Write LLM-Friendly Description

Use this template:

```
[ACTION] [WHAT] using [METHOD].
Accepts [INPUT with constraints].
Returns [OUTPUT structure].
Throws [ERROR_TYPE] if [CONDITION].
```

**Example:**
"Searches knowledge base using semantic embeddings. Accepts query (string, 1-500 chars) and limit (int, 1-50, default 5). Returns {results: array of {title, content, score}, total: int}. Throws 'service_unavailable' if vector store is down."

→ **For complete templates and examples:** [description-writing-guide.md](references/description-writing-guide.md)

### 4. Structure Error Responses

Return errors that help LLM recover:

```json
{
  "error": {
    "type": "validation_error",
    "message": "Query cannot be empty",
    "field": "query",
    "suggestions": [
      "Provide a non-empty search query",
      "Example: 'machine learning best practices'"
    ]
  }
}
```

---

## Tool Schema Design

**Core principles:**

- Use **specific types** (integer vs number, string with enum)
- Add **constraints** (min/max, length, format, pattern)
- Use **enum** for finite choices (status, priority, format)
- Keep **nesting shallow** (< 3 levels)
- Only **required** what's truly needed

**Example:**

```json
{
  "priority": {
    "type": "string",
    "enum": ["low", "medium", "high"],
    "description": "Task priority"
  },
  "query": {
    "type": "string",
    "minLength": 1,
    "maxLength": 500,
    "description": "Search query"
  }
}
```

→ **For advanced patterns, examples, performance tips:** [json-schema-deep-dive.md](references/json-schema-deep-dive.md)

---

## Description Writing

**Template:** `[ACTION] [WHAT] using [METHOD]. Accepts [INPUT]. Returns [OUTPUT]. Throws [ERROR] if [CONDITION].`

**Example:**
"Validates user config against JSON schema. Accepts config (object) and schema_id (string). Returns {valid: boolean, errors: array}. Throws 'schema_not_found' if schema_id doesn't exist."

→ **For complete templates, 20+ examples, patterns:** [description-writing-guide.md](references/description-writing-guide.md)

---

## MCP Tool Patterns

### Basic MCP Tool (FastMCP)

```python
from fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def search_docs(query: str, limit: int = 10) -> dict:
    """
    Searches documentation using full-text search.

    Accepts query (string, 1-500 chars) and limit (int, 1-50).
    Returns {results: array of {title, content, score}, total: int}.
    Throws 'service_unavailable' if search is down.
    """
    # Implementation
    return {"results": [...], "total": 42}
```

### Tool vs Resource vs Prompt

**Use Tool when:**

- Performing actions
- Dynamic computation needed
- Parameters vary per request

**Use Resource when:**

- Static/semi-static data
- Schemas, docs, configs
- Read-only access

**Use Prompt when:**

- Pre-built templates
- Guiding LLM behavior
- Standardizing patterns

→ **For MCP server architecture, stateful tools, streaming:** [mcp-standard-guide.md](references/mcp-standard-guide.md)

---

## Error Handling

### Structured Error Format

```json
{
  "error": {
    "type": "validation_error",
    "message": "Field 'email' must be valid email",
    "field": "email",
    "provided_value": "notanemail",
    "suggestions": [
      "Use format: user@example.com",
      "Example: john.doe@company.com"
    ]
  }
}
```

### Error Types

- **validation_error**: User can fix input
- **not_found**: Resource doesn't exist
- **permission_denied**: Insufficient permissions
- **service_unavailable**: Temporary failure (retry-able)
- **rate_limit_exceeded**: Quota hit

### LLM-Friendly Messages

❌ **Bad:** "Invalid input"

✅ **Good:** "Field 'email' must match format: user@example.com. Provided value 'notanemail' is invalid."

**Key elements:**

- What's wrong
- What was provided
- How to fix it
- Example of correct format

→ **For error taxonomy, recovery strategies, testing:** [error-handling-patterns.md](references/error-handling-patterns.md)

---

## Validation Patterns

### Layer 1: JSON Schema Validation

Built-in type and constraint checking:

```json
{
  "query": {
    "type": "string",
    "minLength": 1,
    "maxLength": 500
  }
}
```

### Layer 2: Runtime Validation

Business logic and complex rules:

```python
def search_docs(query: str) -> dict:
    # Check for SQL injection
    if contains_forbidden_chars(query):
        return {
            "error": {
                "type": "validation_error",
                "message": "Query contains forbidden characters",
                "suggestions": ["Remove special SQL characters"]
            }
        }
```

### Output Schema Definition

Document expected output in docstring:

```python
def search_docs(query: str) -> dict:
    """
    Returns:
        {
            "results": [{"title": str, "content": str, "score": float}],
            "total": int,
            "query_time_ms": int
        }
    """
```

---

## Anti-Patterns

### ❌ Vague Descriptions

**Problem:** "Processes data"

**Solution:** "Normalizes product prices to USD using current exchange rates. Accepts {amount: number, currency: string}. Returns {amount_usd: number, rate: number}."

### ❌ Silent Failures

**Problem:**

```python
try:
    return search(query)
except:
    return []  # LLM thinks "no results"
```

**Solution:**

```python
try:
    return {"results": search(query), "status": "success"}
except:
    return {
        "error": {
            "type": "service_unavailable",
            "message": "Search service is down",
            "retry": True,
            "suggestions": ["Wait 60s and retry"]
        }
    }
```

### ❌ Too Many Tools

**Problem:** Separate tools for `get_user_by_id`, `get_user_by_email`, `get_user_by_username`

**Solution:** One tool with flexible parameters:

```python
def get_user(user_id=None, email=None, username=None):
    """Provide exactly one of: user_id, email, username"""
```

### ❌ Generic Errors

**Problem:** "Error: Operation failed"

**Solution:** "Field 'category' has invalid value 'electronics'. Allowed: ['books', 'music', 'movies']. Use one of the allowed values."

### ❌ Missing Examples

**Problem:** Complex parameter without example

**Solution:**

```json
{
  "filter_expression": {
    "type": "string",
    "description": "SQL-like filter syntax",
    "examples": [
      "price > 100 AND category = 'electronics'",
      "created_at >= '2024-01-01'"
    ]
  }
}
```

---

## Practical Tools

### Scripts

- **`scripts/validate_tool_schema.py`** - Validate schemas against best practices
- **`scripts/generate_tool_template.py`** - Generate boilerplate for new tools

Usage:

```bash
python scripts/validate_tool_schema.py your_schema.json
python scripts/generate_tool_template.py --name my_tool --type mcp --params "query:string"
```

### Templates & Checklists

- **`assets/templates/mcp-tool-template.py`** - Complete MCP tool template
- **`assets/templates/tool-schema-template.json`** - JSON Schema template
- **`assets/checklists/tool-quality-checklist.md`** - Pre-deploy checklist
- **`assets/decision-trees/tool-design-decisions.md`** - Decision flowcharts

### Practical Examples

Progressive examples from simple to complete:

- **`examples/minimal_example.py`** - Simplest possible tool pattern (⭐ start here)
- **`examples/external_api_example.py`** - API calls, rate limits, retry patterns (⭐⭐)
- **`examples/manage_notes.py`** - Complete MCP CRUD tool with tests (⭐⭐⭐)
- **`examples/practical_example.md`** - Step-by-step walkthrough
- **`examples/manage_notes_schema.json`** - Validated JSON Schema

→ See [examples/README.md](examples/README.md) for usage instructions

---

## Deep Dives

For advanced topics, see these references:

### JSON Schema

- **Advanced types** (oneOf, allOf, anyOf)
- **Conditional schemas** (if/then/else)
- **Cross-field validation**
- **Performance optimization**
- **Pattern library** (pagination, filters, dates, etc.)

→ [json-schema-deep-dive.md](references/json-schema-deep-dive.md)

### MCP Implementation

- **MCP architecture** (Tools/Resources/Prompts)
- **Stateful tools** (session management)
- **Streaming responses**
- **Authentication & security**
- **Rate limiting**

→ [mcp-standard-guide.md](references/mcp-standard-guide.md)

### Error Handling

- **Error taxonomy** (User/System/Business/Fatal)
- **Recovery strategies**
- **Common scenarios** (10+ examples)
- **Testing patterns**

→ [error-handling-patterns.md](references/error-handling-patterns.md)

### Description Writing

- **Complete templates library**
- **20+ before/after examples**
- **Common mistakes**
- **Advanced patterns**

→ [description-writing-guide.md](references/description-writing-guide.md)

---

## Core Principles Summary

1. **LLM sees schema + description, not code** → Make them crystal clear
2. **Description > Implementation** → Vague description = failed tool
3. **Errors should guide recovery** → Not just report failures
4. **Be specific with types** → Enums, constraints, examples
5. **Test against real scenarios** → Happy path + edge cases + errors
6. **Progressive disclosure** → Quick Start here, deep dives in references

---

## Related Skills

- **`mcp-builder`** - For designing complete MCP servers
- **`autonomous-agent-expert`** - For agent loops and tool integration
- **`backend-expert`** - For implementing tools in Node.js/Express
- **`prompt-mastery`** - For optimizing tool descriptions

---

**Remember:** Every tool you design is a contract between the LLM and the world. Make it clear, make it specific, make it helpful.
