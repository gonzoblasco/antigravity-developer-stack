# Anti-Patterns & Sharp Edges

## Anti-Patterns

### ❌ Unbounded Autonomy

**Problem**: Agent makes unlimited decisions without human oversight

**Symptoms**:

- Unexpected file deletions
- Runaway API costs
- Unintended side effects

**Solution**:

- Set hard limits on iterations
- Implement cost caps
- Require approval for risky operations

---

### ❌ Trusting Agent Outputs

**Problem**: Assuming agent actions are always correct

**Symptoms**:

- Silent data corruption
- Propagating errors through workflow
- False confidence in results

**Solution**:

- Validate against ground truth
- Use approval flows for critical operations
- Implement verification steps

---

### ❌ General-Purpose Autonomy

**Problem**: One agent for everything

**Symptoms**:

- Poor performance on specialized tasks
- Inconsistent behavior
- Hard to debug

**Solution**:

- Build specialized agents for focused domains
- Use routing to select appropriate agent
- Keep scope narrow

---

### ❌ No Error Logging

**Problem**: Can't debug failures

**Symptoms**:

- "It just stopped working"
- No visibility into agent decisions
- Unable to reproduce issues

**Solution**:

- Structured logging for every tool call
- Log reasoning, not just actions
- Include timestamps and context

---

## Sharp Edges

| Issue                                       | Severity | Solution                                   |
| ------------------------------------------- | -------- | ------------------------------------------ |
| Compounding error rates destroy reliability | Critical | Reduce step count, simplify tasks          |
| Runaway costs in production                 | Critical | Set hard cost limits on iterations         |
| Agents making dangerous operations          | Critical | Least privilege principle, approval flows  |
| Hallucinating tool outputs                  | High     | Validate against ground truth              |
| Hidden network/API failures                 | High     | Build robust API clients with retries      |
| Context window overflow                     | Medium   | Track context usage, summarize when needed |
| Difficult debugging                         | Medium   | Structured logging of all decisions        |

## The Compounding Error Problem

> **Every extra decision multiplies failure probability.**

| Steps | Success Rate @ 95%/step | Success Rate @ 90%/step |
| ----- | ----------------------- | ----------------------- |
| 1     | 95%                     | 90%                     |
| 5     | 77%                     | 59%                     |
| 10    | 60%                     | 35%                     |
| 20    | 36%                     | 12%                     |

**Mitigation strategies**:

1. Minimize number of steps
2. Maximize reliability per step
3. Add checkpoints for recovery
4. Use human-in-the-loop for critical decisions

## Production Reliability Patterns

```python
class ReliableAgent:
    """Production-ready agent with safety features"""

    def __init__(self, max_iterations=50, max_cost_usd=1.0):
        self.max_iterations = max_iterations
        self.max_cost = max_cost_usd
        self.current_cost = 0.0
        self.logger = StructuredLogger()

    def run(self, task: str) -> str:
        for i in range(self.max_iterations):
            # Check cost limit
            if self.current_cost >= self.max_cost:
                self.logger.error("Cost limit exceeded")
                return "Stopped: cost limit exceeded"

            try:
                result = self._execute_step(task)
                self.logger.info("Step completed", step=i, result=result)

                if result.is_complete:
                    return result.output

            except Exception as e:
                self.logger.error("Step failed", step=i, error=str(e))
                # Decide: retry, skip, or abort
                if self._should_abort(e):
                    return f"Aborted: {str(e)}"

        return "Max iterations reached"
```
