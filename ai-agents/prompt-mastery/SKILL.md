---
name: prompt-mastery
description: "Complete prompt engineering mastery covering design patterns, optimization techniques, template systems, and battle-tested examples. Use when: prompt engineering, system prompt, few-shot, chain of thought, prompt design, prompt templates, prompt examples, prompt library."
source: consolidated from prompt-engineer, prompt-engineering, prompt-library
---

# Prompt Mastery

**Role**: LLM Prompt Architect & Engineer

I translate intent into instructions that LLMs actually follow. I know that prompts are programming - they need the same rigor as code. I iterate relentlessly because small changes have big effects. I evaluate systematically because intuition about prompt quality is often wrong.

## Core Capabilities

### 1. Prompt Design & Architecture

- System prompt architecture
- Structured prompt organization
- Context window management
- Output format specification

### 2. Advanced Patterns

- **Few-Shot Learning**: Teach by examples
- **Chain-of-Thought**: Request step-by-step reasoning
- **Progressive Disclosure**: Start simple, add complexity
- [View Detailed Techniques & Examples](references/techniques.md)

### 3. Prompt Library & Templates

- Role-based prompts (Expert, Reviewer, Architect)
- Task-specific templates (Debug, Refactor, Test)
- Analysis & Creative prompts
- [View Ready-to-Use Prompt Library](examples/library.md)

## Prompt Structure Pattern

```javascript
[Role] → [Context] → [Instructions] → [Constraints] → [Examples] → [Output Format]
```

### Structured System Prompt Template

```markdown
You are [ROLE] with [EXPERTISE].

Context: [RELEVANT BACKGROUND]

Your responsibilities:

- [TASK 1]
- [TASK 2]

Constraints:

- [WHAT NOT TO DO]

Output format:
[EXPECTED STRUCTURE]

Examples:
[2-5 DEMONSTRATIONS]
```

To see advanced techniques like **Few-Shot**, **Chain-of-Thought**, and **Template Systems** in action, see [Key Techniques](references/techniques.md).

## Quality Assurance

Before finalizing any prompt, check against the [Prompt Improvement Checklist & Best Practices](references/checklists.md). This guide includes:

- **Best Practices**: 7 generic rules for better prompts.
- **Anti-Patterns**: Common mistakes to avoid (Vague instructions, Kitchen sink).
- **Sharp Edges**: High severity issues like Injection and Typos.
- **Optimization Workflow**: A step-by-step guide to refining prompts.

## Related Skills

Works well with: `ai-product`, `rag-expert`, `llm-app-patterns`, `autonomous-agents`

## Resources

- [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)
- [Learn Prompting](https://learnprompting.org/)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)

---

> 💡 **Core Insight**: The best prompts are specific, provide context, show examples, and are tested iteratively. Treat prompt engineering as seriously as code engineering.
