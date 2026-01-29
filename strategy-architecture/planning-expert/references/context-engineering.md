# Context Engineering Strategies

Techniques utilized by advanced agents like Manus to manage large task contexts.

## Strategy 1: Context Reduction

- **Compaction**: Store raw tool content in the filesystem; keep only references/paths in the primary context for older results.
- **Summarization**: Apply when compaction reaches limits. Create standardized summary objects for stale tool results.

## Strategy 2: Context Isolation (Multi-Agent)

Use a Planner Agent to assign tasks to Executor Sub-Agents. This isolates context and prevents the main planner from being overwhelmed by execution details.

- **Hierarchical Planning**: Shift from a single monolithic `todo.md` to multiple sub-agents with their own local contexts.

## Strategy 3: Context Offloading

- **Atomic Tools**: Use a small set (<20) of focused functions.
- **Filesystem First**: Store all full results on disk immediately.
- **Searchable Memory**: Use tools like `glob` and `grep` to retrieve only what's needed when it's needed (Progressive Disclosure).
