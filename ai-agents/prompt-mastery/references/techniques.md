# Key Techniques

## Few-Shot Examples

Include 2-5 diverse examples that demonstrate desired behavior:

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

**Best practices:**

- Show diverse examples covering edge cases
- Match example difficulty to expected inputs
- Use consistent formatting across examples
- Include negative examples when helpful
- Balance token usage vs accuracy (more examples = better but costlier)

## Chain-of-Thought Prompting

Request step-by-step reasoning before final answer. Improves accuracy on analytical tasks by 30-50%.

```markdown
Analyze this bug report and determine root cause.

Think step by step:

1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

## Progressive Disclosure

Start simple, add complexity only when needed:

1. **Level 1 - Direct**: "Summarize this article"
2. **Level 2 - Constrained**: "Summarize in 3 bullet points, focusing on key findings"
3. **Level 3 - Reasoning**: "Read this article, identify the main findings, then summarize in 3 bullets"
4. **Level 4 - Examples**: Include 2-3 example summaries with input-output pairs

## Template Systems

Build reusable structures for consistency:

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

# Usage
prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\\n2. XSS risks\\n3. Authentication"
)
```
