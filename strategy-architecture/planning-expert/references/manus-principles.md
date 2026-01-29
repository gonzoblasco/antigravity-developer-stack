# Manus Principles

This skill is based on context engineering principles from Manus, the AI agent company.

## The 6 Manus Principles

### Principle 1: Design Around KV-Cache

Keep prompt prefixes STABLE. Single-token changes invalidate the cache. NO timestamps in system prompts. Use deterministic serialization.

### Principle 2: Mask, Don't Remove

Don't dynamically remove tools. Use logit masking. Use consistent action prefixes (e.g., `browser_`, `shell_`, `file_`).

### Principle 3: Filesystem as External Memory

> "Markdown is my 'working memory' on disk."

- **Context Window** = RAM (volatile, limited)
- **Filesystem** = Disk (persistent, unlimited)
- Keep pointers (URLs, paths) even if content is dropped.

### Principle 4: Manipulate Attention Through Recitation

Push the global plan into the model's recent attention span by re-reading `task_plan.md` before decisions. This prevents the "lost in the middle" effect.

### Principle 5: Leave the Wrong Turns In

Failed actions with stack traces help the model update beliefs and reduce mistake repetition. Error recovery is a primary signal of agentic behavior.

### Principle 6: Don't Get Few-Shotted

Introduce controlled variation in phrasings to prevent drift and hallucination caused by repetitive action-observation pairs.
