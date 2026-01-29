# Error Handling Patterns

Advanced error handling strategies for AI agent tools that help LLMs recover gracefully.

## Table of Contents

1. [Error Taxonomy](#error-taxonomy)
2. [Error Structure Templates](#error-structure-templates)
3. [Recovery Strategies](#recovery-strategies)
4. [Common Error Scenarios](#common-error-scenarios)
5. [Testing Error Handling](#testing-error-handling)

---

## Error Taxonomy

### User Errors (Recoverable)

**Characteristics:**

- Caused by invalid input
- LLM can fix and retry
- Clear path to resolution

**Examples:**

- Validation errors
- Missing required parameters
- Format errors
- Out-of-range values

**Response Strategy:** Detailed feedback + specific suggestions

### System Errors (Retry-able)

**Characteristics:**

- Temporary failures
- Not caused by user input
- May succeed on retry

**Examples:**

- Service unavailable
- Network timeouts
- Database connection lost
- Rate limit exceeded

**Response Strategy:** Indicate retry-ability + wait time

### Business Logic Errors (Contextual)

**Characteristics:**

- Valid request, invalid state
- Context-dependent
- May require different action

**Examples:**

- Resource not found
- Permission denied
- Duplicate entry
- Invalid state transition

**Response Strategy:** Explain context + suggest alternatives

### Fatal Errors (Non-recoverable)

**Characteristics:**

- Cannot be fixed by LLM
- Requires human intervention
- System-level issues

**Examples:**

- Configuration missing
- Critical service down
- Corrupted data
- Authentication failure

**Response Strategy:** Clear explanation + escalation path

---

## Error Structure Templates

### Base Error Structure

```json
{
  "error": {
    "type": "error_category",
    "message": "Human-readable explanation",
    "code": "MACHINE_READABLE_CODE",
    "details": {},
    "suggestions": [],
    "metadata": {}
  }
}
```

### Validation Error

```json
{
  "error": {
    "type": "validation_error",
    "message": "Field 'email' must be a valid email address",
    "code": "INVALID_EMAIL_FORMAT",
    "field": "email",
    "provided_value": "notanemail",
    "constraint": "Must match format: user@example.com",
    "suggestions": [
      "Provide email in format: user@example.com",
      "Example: john.doe@company.com",
      "Ensure @ symbol and domain are present"
    ]
  }
}
```

**When to use:**

- Input doesn't match schema
- Business rule violated
- Format incorrect

### Not Found Error

```json
{
  "error": {
    "type": "not_found",
    "message": "User with ID 'user_123' does not exist",
    "code": "USER_NOT_FOUND",
    "resource_type": "user",
    "resource_id": "user_123",
    "suggestions": [
      "Verify the user ID is correct",
      "Use list_users() to see available users",
      "Check if user was recently deleted"
    ],
    "alternatives": {
      "similar_ids": ["user_124", "user_125"],
      "list_tool": "list_users"
    }
  }
}
```

**When to use:**

- Resource doesn't exist
- ID not found
- Query returned no results

### Permission Error

```json
{
  "error": {
    "type": "permission_denied",
    "message": "User lacks 'admin' role required for this operation",
    "code": "INSUFFICIENT_PERMISSIONS",
    "required_permission": "admin",
    "current_permissions": ["user", "viewer"],
    "suggestions": [
      "Request admin access from an administrator",
      "Use a different user account with admin role",
      "Try a read-only operation instead"
    ],
    "escalation": {
      "contact": "admin@example.com",
      "self_service_url": "https://app.example.com/request-access"
    }
  }
}
```

**When to use:**

- Insufficient permissions
- Role requirement not met
- Access denied

### Service Error (Retry-able)

```json
{
  "error": {
    "type": "service_unavailable",
    "message": "Search service timed out after 30s",
    "code": "SERVICE_TIMEOUT",
    "service_name": "elasticsearch",
    "retry": true,
    "retry_after_seconds": 60,
    "suggestions": [
      "Wait 60 seconds and retry the same request",
      "If problem persists after 3 retries, report the issue",
      "Try a simpler query in the meantime"
    ],
    "status_url": "https://status.example.com"
  }
}
```

**When to use:**

- External service down
- Timeout occurred
- Temporary failure
- Rate limit hit

### Rate Limit Error

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "API rate limit exceeded: 100 requests per hour",
    "code": "RATE_LIMIT_EXCEEDED",
    "limit": 100,
    "period": "hour",
    "current_usage": 100,
    "reset_at": "2024-01-15T11:00:00Z",
    "retry_after_seconds": 1800,
    "suggestions": [
      "Wait until 2024-01-15T11:00:00Z for limit reset",
      "Upgrade to a higher tier for increased limits",
      "Batch requests to use fewer API calls"
    ]
  }
}
```

**When to use:**

- Rate limit hit
- Quota exceeded
- Throttling active

---

## Recovery Strategies

### Strategy 1: Immediate Retry

**For:** Transient network errors, temporary unavailability

```python
def with_retry(func, max_attempts=3):
    """Retry with exponential backoff"""
    for attempt in range(max_attempts):
        try:
            return func()
        except TransientError as e:
            if attempt == max_attempts - 1:
                return {
                    "error": {
                        "type": "service_unavailable",
                        "message": f"Failed after {max_attempts} attempts: {str(e)}",
                        "retry": False,
                        "suggestions": [
                            "Service may be experiencing issues",
                            "Try again in a few minutes",
                            "Check service status page"
                        ]
                    }
                }

            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
```

### Strategy 2: Graceful Degradation

**For:** Non-critical failures, optional enhancements

```python
def search_with_enrichment(query: str) -> dict:
    """Search with optional metadata enrichment"""
    # Core search (critical)
    results = search_index(query)

    # Enrichment (nice-to-have)
    try:
        enriched = add_metadata(results)
        return {
            "results": enriched,
            "enriched": True
        }
    except MetadataServiceError:
        # Return basic results rather than failing
        return {
            "results": results,
            "enriched": False,
            "warning": "Metadata service unavailable, returned basic results"
        }
```

### Strategy 3: Alternative Paths

**For:** Resource not found, permission denied

```python
def get_user(user_id: str) -> dict:
    """Get user with fallback to search"""
    user = db.find_by_id(user_id)

    if not user:
        # Suggest alternative
        similar = db.search_users(user_id, limit=5)

        return {
            "error": {
                "type": "not_found",
                "message": f"User '{user_id}' not found",
                "suggestions": [
                    "Verify the user ID",
                    "Try searching by email or username instead"
                ],
                "alternatives": {
                    "similar_users": [
                        {"id": u.id, "email": u.email}
                        for u in similar
                    ],
                    "search_tool": "search_users"
                }
            }
        }

    return {"user": user}
```

### Strategy 4: Partial Success

**For:** Batch operations, multi-step workflows

```python
def batch_create_users(users: list) -> dict:
    """Create multiple users, report partial failures"""
    successes = []
    failures = []

    for user_data in users:
        try:
            user = create_user(user_data)
            successes.append({
                "email": user_data["email"],
                "user_id": user.id
            })
        except Exception as e:
            failures.append({
                "email": user_data["email"],
                "error": str(e),
                "suggestion": "Fix this entry and retry individually"
            })

    if failures and not successes:
        # Total failure
        return {
            "error": {
                "type": "batch_operation_failed",
                "message": "All user creations failed",
                "failures": failures
            }
        }

    # Partial or full success
    return {
        "successes": successes,
        "failures": failures if failures else None,
        "total": len(users),
        "success_count": len(successes),
        "failure_count": len(failures)
    }
```

---

## Common Error Scenarios

### Scenario 1: Empty Required Field

```python
def search(query: str) -> dict:
    if not query or not query.strip():
        return {
            "error": {
                "type": "validation_error",
                "field": "query",
                "message": "Query cannot be empty",
                "provided_value": query,
                "suggestions": [
                    "Provide a non-empty search query",
                    "Example: 'machine learning best practices'",
                    "Query must be 1-500 characters"
                ]
            }
        }
```

### Scenario 2: Invalid Enum Value

```python
def set_priority(task_id: str, priority: str) -> dict:
    valid_priorities = ["low", "medium", "high", "urgent"]

    if priority not in valid_priorities:
        return {
            "error": {
                "type": "validation_error",
                "field": "priority",
                "message": f"Priority '{priority}' is invalid",
                "provided_value": priority,
                "constraint": f"Must be one of: {', '.join(valid_priorities)}",
                "suggestions": [
                    f"Use one of the allowed values: {', '.join(valid_priorities)}",
                    "Default is 'medium' if not specified"
                ]
            }
        }
```

### Scenario 3: Duplicate Entry

```python
def create_project(name: str) -> dict:
    if project_exists(name):
        existing = get_project_by_name(name)

        return {
            "error": {
                "type": "duplicate_entry",
                "message": f"Project '{name}' already exists",
                "existing_resource": {
                    "id": existing.id,
                    "name": existing.name,
                    "created_at": existing.created_at
                },
                "suggestions": [
                    f"Use existing project ID: {existing.id}",
                    "Choose a different project name",
                    "Update existing project instead of creating new one"
                ],
                "alternatives": {
                    "update_tool": "update_project",
                    "get_tool": "get_project"
                }
            }
        }
```

### Scenario 4: Dependency Missing

```python
def deploy_service(service_id: str) -> dict:
    service = get_service(service_id)

    # Check dependencies
    missing_deps = []
    for dep in service.dependencies:
        if not is_deployed(dep):
            missing_deps.append(dep)

    if missing_deps:
        return {
            "error": {
                "type": "dependency_not_met",
                "message": f"Cannot deploy '{service_id}': dependencies not deployed",
                "missing_dependencies": missing_deps,
                "suggestions": [
                    f"Deploy dependencies first: {', '.join(missing_deps)}",
                    "Use deploy_with_dependencies() to auto-deploy deps",
                    "Check dependency status with get_deployment_status()"
                ],
                "recovery_steps": [
                    f"1. Deploy each dependency: {', '.join(missing_deps)}",
                    f"2. Retry deploying '{service_id}'"
                ]
            }
        }
```

### Scenario 5: State Transition Invalid

```python
def transition_order(order_id: str, new_status: str) -> dict:
    order = get_order(order_id)

    # Valid transitions
    valid_transitions = {
        "pending": ["processing", "cancelled"],
        "processing": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": []
    }

    if new_status not in valid_transitions.get(order.status, []):
        return {
            "error": {
                "type": "invalid_state_transition",
                "message": f"Cannot transition from '{order.status}' to '{new_status}'",
                "current_state": order.status,
                "requested_state": new_status,
                "allowed_transitions": valid_transitions[order.status],
                "suggestions": [
                    f"From '{order.status}', you can transition to: {', '.join(valid_transitions[order.status])}",
                    "Check order status before attempting transition",
                    "Use get_order() to see current state"
                ]
            }
        }
```

---

## Testing Error Handling

### Test Matrix

| Scenario      | Input              | Expected Error Type   | Key in Suggestion            |
| ------------- | ------------------ | --------------------- | ---------------------------- |
| Empty query   | `query=""`         | `validation_error`    | "Provide non-empty"          |
| Invalid enum  | `priority="super"` | `validation_error`    | "Use one of: low, medium..." |
| Not found     | `user_id="fake"`   | `not_found`           | "Verify ID"                  |
| Duplicate     | `name="existing"`  | `duplicate_entry`     | "Choose different name"      |
| No permission | `role="user"`      | `permission_denied`   | "Request admin access"       |
| Service down  | Simulate timeout   | `service_unavailable` | "Wait Xs and retry"          |
| Rate limit    | 101st request      | `rate_limit_exceeded` | "Wait until reset"           |

### Test Example

```python
def test_empty_query_error():
    """Test that empty query returns helpful error"""
    result = search_docs(query="")

    assert "error" in result
    assert result["error"]["type"] == "validation_error"
    assert result["error"]["field"] == "query"
    assert "empty" in result["error"]["message"].lower()
    assert len(result["error"]["suggestions"]) > 0
    assert any("example" in s.lower() for s in result["error"]["suggestions"])
```

---

## Best Practices Checklist

- [ ] Every error has a `type` and `message`
- [ ] Validation errors include `field` name
- [ ] All errors have `suggestions` array (min 2 suggestions)
- [ ] Retry-able errors indicate `retry_after_seconds`
- [ ] Not found errors suggest alternatives
- [ ] Messages are specific, not generic
- [ ] Suggestions are actionable
- [ ] No sensitive data in error messages
- [ ] Error types are consistent across tools
- [ ] Test each error scenario

---

## Anti-Patterns

❌ **Generic errors:**

```json
{ "error": "Something went wrong" }
```

❌ **No suggestions:**

```json
{ "error": { "type": "invalid", "message": "Bad input" } }
```

❌ **Exposing internals:**

```json
{ "error": "SQL error: table users does not exist" }
```

✅ **Good error:**

```json
{
  "error": {
    "type": "validation_error",
    "message": "Email format is invalid",
    "field": "email",
    "provided_value": "notanemail",
    "suggestions": [
      "Use format: user@example.com",
      "Example: john.doe@company.com"
    ]
  }
}
```

---

## Summary

**Good error handling:**

1. ✅ Categorizes errors correctly
2. ✅ Provides specific messages
3. ✅ Includes actionable suggestions
4. ✅ Indicates retry-ability
5. ✅ Suggests alternatives
6. ✅ Helps LLM recover

**Goal:** Every error should move the LLM closer to success, not just report failure.
