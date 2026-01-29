# Tool Design Decision Trees

Flowcharts to guide key decisions when designing AI agent tools.

---

## Decision 1: One Tool or Multiple?

```mermaid
graph TD
    A[Designing Tool Functionality] --> B{Share same<br/>core entity?}

    B -->|Yes| C{Different actions<br/>on entity?}
    B -->|No| D[Separate Tools]

    C -->|Yes| E{Can use<br/>optional params?}
    C -->|No| F[Separate Tools]

    E -->|Yes| G[One Tool with<br/>Optional Params]
    E -->|No| H{Actions often<br/>used together?}

    H -->|Yes| G
    H -->|No| F

    style G fill:#90EE90
    style D fill:#FFB6C1
    style F fill:#FFB6C1
```

**Examples:**

- ✅ **One tool:** `get_user(user_id?, email?, username?)` - Same entity, flexible params
- ❌ **Separate:** `search_products()` vs `create_order()` - Different entities

---

## Decision 2: Tool vs Resource vs Prompt?

```mermaid
graph TD
    A[Designing Functionality] --> B{Requires<br/>computation?}

    B -->|Yes| C{Dynamic per<br/>request?}
    B -->|No| D{Static or<br/>semi-static data?}

    C -->|Yes| E[Tool]
    C -->|No| F[Resource]

    D -->|Yes| F
    D -->|No| G{Guiding LLM<br/>behavior?}

    G -->|Yes| H[Prompt Template]
    G -->|No| F

    style E fill:#87CEEB
    style F fill:#DDA0DD
    style H fill:#F0E68C
```

**Examples:**

- **Tool:** `search_documents(query)` - Dynamic computation
- **Resource:** `schema://database-schema` - Semi-static data
- **Prompt:** `analyze-code` - Behavior template

---

## Decision 3: Validation Level?

```mermaid
graph TD
    A[Defining Parameter] --> B{Critical for<br/>correctness?}

    B -->|Yes| C[Schema + Runtime<br/>Validation]
    B -->|No| D{Performance<br/>impact?}

    C --> E[Add detailed<br/>error messages]

    D -->|High| F[Schema Only]
    D -->|Low| G{Complex<br/>validation?}

    G -->|Yes| C
    G -->|No| F

    style C fill:#FFB6C1
    style F fill:#90EE90
    style E fill:#FFB6C1
```

**When to add runtime validation:**

- Cross-field dependencies
- Business logic rules
- Security checks (SQL injection, etc.)
- Format validation beyond JSON Schema

**When schema is enough:**

- Simple type checking
- Basic constraints (min/max)
- Enum validation

---

## Decision 4: Parameter Count?

```mermaid
graph TD
    A[Adding Parameters] --> B{How many<br/>total params?}

    B -->|1-3| C[Good]
    B -->|4-6| D{Can group<br/>related params?}
    B -->|7+| E[Too Many]

    D -->|Yes| F[Group into<br/>object param]
    D -->|No| G{Can have<br/>sensible defaults?}

    E --> H[Consider:<br/>Split into<br/>multiple tools]

    G -->|Yes| I[Make optional<br/>with defaults]
    G -->|No| H

    F --> C
    I --> C

    style C fill:#90EE90
    style E fill:#FF6347
    style H fill:#FFB6C1
```

**Rules of thumb:**

- **1-3 params:** Ideal, easy to understand
- **4-6 params:** OK if most have defaults
- **7+ params:** Likely doing too much, consider splitting

**Example refactoring:**

```diff
- search(query, category, min_price, max_price, sort_by, sort_order, page)
+ search(query, filters: {category, price_range}, pagination: {sort, page})
```

---

## Decision 5: Sync or Async?

```mermaid
graph TD
    A[Implementing Tool] --> B{Execution time<br/>predictable?}

    B -->|Yes| C{Usually < 2s?}
    B -->|No| D[Async with<br/>Job Status]

    C -->|Yes| E[Synchronous]
    C -->|No| F{Can stream<br/>results?}

    F -->|Yes| G[Streaming Tool]
    F -->|No| D

    D --> H[Return job_id<br/>immediately]
    H --> I[Provide separate<br/>get_status tool]

    style E fill:#90EE90
    style G fill:#87CEEB
    style D fill:#DDA0DD
```

**Synchronous:** Fast operations (< 2s)

- Database queries
- API calls
- Simple computations

**Async with jobs:** Long operations (> 5s)

- File processing
- Batch operations
- External service calls

**Streaming:** Progressive results

- Large dataset processing
- Real-time updates
- Chat/generation tasks

---

## Decision 6: Error Granularity?

```mermaid
graph TD
    A[Handling Errors] --> B{Multiple failure<br/>modes?}

    B -->|No| C[Single error type]
    B -->|Yes| D{LLM needs to<br/>handle differently?}

    D -->|Yes| E[Specific error types<br/>per failure mode]
    D -->|No| F{Field-level<br/>validation?}

    E --> G[Add recovery<br/>suggestions per type]

    F -->|Yes| H[Include field name<br/>in error]
    F -->|No| C

    H --> I[Add field-specific<br/>suggestions]

    style E fill:#FFB6C1
    style H fill:#FFB6C1
    style C fill:#90EE90
```

**Error type examples:**

```python
{
  "validation_error": "User can fix input",
  "not_found": "Try different ID or list available",
  "service_unavailable": "Retry after delay",
  "permission_denied": "Check auth or request access"
}
```

**Each type should have:**

- Clear message
- Specific suggestions
- Retry guidance (if applicable)

---

## Decision 7: When to Use Enums?

```mermaid
graph TD
    A[Defining String Param] --> B{Finite set<br/>of values?}

    B -->|No| C[String with<br/>pattern/constraints]
    B -->|Yes| D{All values<br/>known now?}

    D -->|No| E[String with<br/>examples]
    D -->|Yes| F{How many<br/>options?}

    F -->|2-20| G[Use Enum]
    F -->|20-50| H{Will LLM<br/>remember all?}
    F -->|50+| I[String with<br/>validation]

    H -->|Yes| G
    H -->|No| I

    style G fill:#90EE90
    style C fill:#87CEEB
    style E fill:#87CEEB
    style I fill:#87CEEB
```

**Use enum when:**

- ✅ Values are finite and known
- ✅ 2-20 options (sweet spot)
- ✅ Values won't change frequently
- ✅ Examples: status, mode, format, priority

**Don't use enum when:**

- ❌ User-generated content
- ❌ Extensible lists
- ❌ High cardinality (50+ options)
- ❌ Examples: names, messages, search queries

---

## Decision 8: MCP vs Simple Function?

```mermaid
graph TD
    A[Implementing Tool] --> B{Need external<br/>integration?}

    B -->|Yes| C{Multiple tools<br/>in suite?}
    B -->|No| D[Simple Function]

    C -->|Yes| E[MCP Server]
    C -->|No| F{Stateful<br/>operations?}

    F -->|Yes| E
    F -->|No| G{Need<br/>resources/prompts?}

    G -->|Yes| E
    G -->|No| D

    E --> H[Use FastMCP or<br/>MCP SDK]

    style E fill:#DDA0DD
    style D fill:#90EE90
```

**MCP Server when:**

- Multiple related tools
- Need resources (schemas, docs)
- Need prompt templates
- Stateful operations
- External service integration

**Simple Function when:**

- Single, standalone tool
- No state needed
- Internal operations only
- Quick prototyping

---

## Quick Decision Matrix

| Question                        | Answer | Recommendation                 |
| ------------------------------- | ------ | ------------------------------ |
| Same entity, different actions? | Yes    | One tool with optional params  |
| Need dynamic computation?       | Yes    | Tool (not Resource)            |
| Operation takes > 5s?           | Yes    | Async with job tracking        |
| 7+ parameters?                  | Yes    | Consider splitting or grouping |
| Finite values (2-20)?           | Yes    | Use enum                       |
| Multiple related tools?         | Yes    | MCP Server                     |
| Critical for security?          | Yes    | Schema + runtime validation    |
| Field-level errors?             | Yes    | Include field name in error    |

---

## Usage Tips

1. **Start simple:** Begin with synchronous, single-tool approach
2. **Iterate based on usage:** Add complexity only when needed
3. **Test with LLM:** Decisions should make sense to the LLM, not just developers
4. **Follow patterns:** Consistency across tools reduces token usage
5. **Document decisions:** Explain why you chose specific approach

**Remember:** Good tool design makes the agent's job easier, not harder.
