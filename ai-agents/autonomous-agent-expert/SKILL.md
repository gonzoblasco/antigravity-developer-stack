---
name: autonomous-agent-expert
description: "Use when building AI agents, designing tool APIs, implementing permission systems, creating autonomous coding assistants, or working with ReAct/Plan-Execute patterns. Keywords: agent loop, tool design, permission system, sandbox, human-in-the-loop, compounding errors, agent reliability."
---

# Autonomous Agent Expert

**Role**: AI Agent Architect & Production Reliability Specialist

> [!IMPORTANT]
> **Core insight**: Autonomy is earned, not granted. Start with heavily constrained agents that do one thing reliably. Add autonomy only as you prove reliability.

## Philosophy

**Guardrails before capabilities, logging before optimization, reliability before features.**

## Core Principles

1. **Compounding Errors Kill Agents** - 95% success per step = 60% by step 10
2. **Constrain First, Expand Later** - Narrow scope = higher reliability
3. **Human-in-the-Loop by Default** - Approval for risky operations
4. **Sandbox Everything** - Isolation prevents catastrophic failures
5. **Log Everything** - Debugging autonomous systems requires complete audit trails

---

## Quick Start: ReAct Agent

The most common production pattern - alternating reasoning and action:

```python
class ReActAgent:
    def run(self, task: str) -> str:
        for i in range(self.max_iterations):
            # Think: Get LLM response
            response = self.llm.chat(messages=self.history, tools=self.tools)

            # Act: Execute tool if requested
            if response.tool_calls:
                for call in response.tool_calls:
                    result = self._execute_tool(call)
                    self.history.append({"role": "tool", "content": result})
            else:
                return response.content  # Done

        return "Max iterations reached"
```

**Full implementation**: See [react-pattern.md](references/react-pattern.md)

---

## Agent Architecture Patterns

| Pattern          | Best For                               | Reference                                                     |
| ---------------- | -------------------------------------- | ------------------------------------------------------------- |
| **ReAct**        | General-purpose, exploratory tasks     | [react-pattern.md](references/react-pattern.md)               |
| **Plan-Execute** | Complex multi-step, predictable tasks  | [plan-execute-pattern.md](references/plan-execute-pattern.md) |
| **Reflection**   | Quality-critical, iterative refinement | [reflection-pattern.md](references/reflection-pattern.md)     |

---

## Tool Design

Essential tools for coding agents:

| Category     | Tools                            | Risk   |
| ------------ | -------------------------------- | ------ |
| **Read**     | read_file, search_code, list_dir | Low    |
| **Write**    | write_file, edit_file            | Medium |
| **Execute**  | run_command, send_input          | High   |
| **External** | search_web, open_browser         | Medium |

**Full patterns**: See [tool-design.md](references/tool-design.md)

---

## Permission & Safety

```python
class PermissionLevel(Enum):
    AUTO = "auto"          # Fully automatic (read operations)
    ASK_ONCE = "ask_once"  # Ask once per session (write operations)
    ASK_EACH = "ask_each"  # Ask every time (execute operations)
    NEVER = "never"        # Never allow (dangerous operations)
```

**Full implementation**: See [permission-patterns.md](references/permission-patterns.md)

---

## Best Practices Checklist

### Agent Design

- [ ] Clear task decomposition
- [ ] Appropriate tool granularity
- [ ] Error handling at each step
- [ ] Max iterations limit
- [ ] Cost limits set

### Safety

- [ ] Permission system implemented
- [ ] Dangerous operations blocked
- [ ] Sandbox for untrusted code
- [ ] Audit logging enabled
- [ ] Human-in-the-loop for high-risk actions

### UX

- [ ] Progress updates provided
- [ ] Explanation of actions
- [ ] Undo/rollback available

---

## Key Insights

> **Every extra decision multiplies failure probability.** A 95% success rate per step compounds to 60% by step 10. Minimize steps, maximize reliability per step.

> **The best agents are boring.** They do one thing reliably rather than many things impressively.

> **Guardrails before capabilities.** Permission systems, sandboxing, and logging should be built before adding autonomous features.

---

## Anti-Patterns & Sharp Edges

| Issue                   | Severity | Solution                        |
| ----------------------- | -------- | ------------------------------- |
| Compounding error rates | Critical | Reduce steps, simplify tasks    |
| Runaway costs           | Critical | Set hard cost limits            |
| Dangerous operations    | Critical | Approval flows, least privilege |
| Hallucinating outputs   | High     | Validate against ground truth   |

**Full details**: See [anti-patterns.md](references/anti-patterns.md)

---

## Related Skills

Works well with: `agent-tool-builder`, `browser-automation-expert`, `mcp-builder`, `prompt-mastery`

---

## References

**Internal**:

- [react-pattern.md](references/react-pattern.md) - ReAct Agent Loop
- [plan-execute-pattern.md](references/plan-execute-pattern.md) - Plan-Execute Pattern
- [reflection-pattern.md](references/reflection-pattern.md) - Reflection Pattern
- [tool-design.md](references/tool-design.md) - Tool Design Patterns
- [permission-patterns.md](references/permission-patterns.md) - Permission & Safety
- [context-management.md](references/context-management.md) - Context Management
- [anti-patterns.md](references/anti-patterns.md) - Anti-Patterns & Sharp Edges

**External**:

- [Cline](https://github.com/cline/cline) - Autonomous coding agent
- [LangGraph](https://python.langchain.com/docs/langgraph) - Agent framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - Tool standardization
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use) - Function calling guide
