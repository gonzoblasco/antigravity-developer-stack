# Plan-Execute Pattern

**Separate planning from execution** - Better for complex multi-step tasks that benefit from upfront planning.

## How It Works

1. **Plan**: Create complete plan before starting
2. **Execute**: Run each step sequentially
3. **Replan**: If step fails, create new plan

## Implementation

```python
class PlanExecuteAgent:
    def __init__(self, planner, executor):
        self.planner = planner
        self.executor = executor

    def run(self, task: str) -> str:
        # Phase 1: Planning
        plan = self.planner.create_plan(task)

        # Phase 2: Execution
        for step in plan.steps:
            result = self.executor.execute(step)

            if not result.success:
                # Replan on failure
                plan = self.planner.replan(
                    original_plan=plan,
                    failed_step=step,
                    error=result.error
                )

        return plan.final_result


class Planner:
    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, task: str) -> Plan:
        """Generate step-by-step plan"""
        response = self.llm.chat(
            messages=[{
                "role": "user",
                "content": f"""Create a step-by-step plan for: {task}

Return as JSON:
{{
    "steps": [
        {{"id": 1, "action": "...", "tool": "...", "args": {{}}}}
    ]
}}"""
            }]
        )
        return Plan.from_json(response.content)

    def replan(self, original_plan, failed_step, error) -> Plan:
        """Create new plan after failure"""
        return self.create_plan(
            f"Original task: {original_plan.task}\n"
            f"Failed at step {failed_step.id}: {error}\n"
            f"Create new plan from this point."
        )
```

## When to Use

- **Complex multi-step tasks** with clear milestones
- **Deterministic workflows** where steps are predictable
- **Tasks requiring coordination** of multiple tools

## Tradeoffs

| Pros                     | Cons                         |
| ------------------------ | ---------------------------- |
| Better for complex tasks | Replanning is expensive      |
| Clear progress tracking  | Less flexible to discoveries |
| Can estimate completion  | Initial plan may be wrong    |
