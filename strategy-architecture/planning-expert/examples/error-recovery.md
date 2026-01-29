# Example: Error Recovery Pattern

When something fails, **DON'T hide it**.

## Before (Anti-Pattern)

```
Action: Read config.json
Error: File not found
Action: Read config.json  # Silent retry
Action: Read config.json  # Another retry -> Infinite loop
```

## After (Correct Pattern)

```
Action: Read config.json
Error: File not found

# Update task_plan.md
## Errors Encountered
- config.json not found → Will create default config.

Action: Write config.json (default config)
Action: Read config.json
Success!
```
