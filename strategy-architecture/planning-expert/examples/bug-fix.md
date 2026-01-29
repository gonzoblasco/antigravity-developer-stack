# Example: Bug Fix Task

**Request**: "Fix the login bug in the authentication module."

## task_plan.md (Execution State)

```markdown
# Task Plan: Fix Login Bug

## Phases

- [x] Phase 1: Understand the bug report ✓
- [x] Phase 2: Locate relevant code ✓
- [/] Phase 3: Identify root cause (CURRENT)
- [ ] Phase 4: Implement fix

## Errors Encountered

| Error                                                | Attempt | Resolution                        |
| ---------------------------------------------------- | ------- | --------------------------------- |
| TypeError: Cannot read property 'token' of undefined | 1       | Found user object wasn't awaited. |

## Status

**Currently in Phase 3** - Found root cause, preparing fix.
```

## Key Insight

The agent uses the "Errors Encountered" table to document the fix path, ensuring that if the fix doesn't work, it has a record of what was already attempted.
