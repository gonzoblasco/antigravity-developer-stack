# Error Protocols & Recovery

Guidelines for handling failures in an agentic loop.

## The 3-Strike Error Protocol

1.  **ATTEMPT 1: Diagnose & Fix**
    - Read error carefully.
    - Identify root cause.
    - Apply targeted fix.
2.  **ATTEMPT 2: Alternative Approach**
    - If the same error persists, try a different method.
    - Switch tools or libraries if applicable.
    - **NEVER repeat the exact same failing action.**
3.  **ATTEMPT 3: Broader Rethink**
    - Question assumptions.
    - Search for solutions or documentation.
    - Consider updating the global plan to reflect a new strategy.

**AFTER 3 FAILURES**: Escalate to the User. Explain what was tried, share the specific error, and ask for guidance.

## Failure Mutation Strategy

If an action fails, the next action must be different.

```python
if action_failed:
    next_action != same_action
```

Always track what you tried in `task_plan.md` to prevent infinite loops of the same mistake.

## Logging for Learning

Every error is a data point. Log them in the "Errors Encountered" table in `task_plan.md`:
| Error | Attempt | Resolution |
|-------|---------|------------|
| ... | 1 | ... |
