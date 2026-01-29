# Reflection Pattern

**Self-evaluation and iterative improvement** - Agent critiques its own output and refines until satisfactory.

## How It Works

1. **Execute**: Generate initial result
2. **Reflect**: Critique the result
3. **Refine**: Incorporate feedback
4. **Repeat**: Until satisfactory or max attempts

## Implementation

```python
class ReflectiveAgent:
    def __init__(self, llm, max_attempts=3):
        self.llm = llm
        self.max_attempts = max_attempts

    def run_with_reflection(self, task: str) -> str:
        for attempt in range(self.max_attempts):
            # Execute
            result = self.execute(task)

            # Reflect
            critique = self.reflect(result)

            if critique.is_satisfactory:
                return result

            # Refine task with feedback
            task = self.refine_task(task, critique)

        return result  # Return best attempt

    def execute(self, task: str) -> str:
        """Generate result for task"""
        response = self.llm.chat([
            {"role": "user", "content": task}
        ])
        return response.content

    def reflect(self, result: str) -> Critique:
        """Evaluate the result"""
        response = self.llm.chat([
            {"role": "user", "content": f"""Evaluate this result:

{result}

Return JSON:
{{
    "is_satisfactory": true/false,
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1"]
}}"""}
        ])
        return Critique.from_json(response.content)

    def refine_task(self, original_task: str, critique: Critique) -> str:
        """Create refined task incorporating feedback"""
        return f"""{original_task}

Previous attempt had issues:
{chr(10).join(f'- {issue}' for issue in critique.issues)}

Suggestions:
{chr(10).join(f'- {s}' for s in critique.suggestions)}

Please address these issues."""
```

## When to Use

- **Quality-critical outputs** (code review, writing)
- **Tasks with clear success criteria**
- **Iterative refinement** workflows

## Tradeoffs

| Pros                       | Cons               |
| -------------------------- | ------------------ |
| Higher quality output      | Multiple LLM calls |
| Self-correcting            | Slower execution   |
| Works for subjective tasks | May over-refine    |
