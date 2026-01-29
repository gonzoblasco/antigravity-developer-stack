# ReAct Agent Pattern

**Alternating reasoning and action** - The most common production pattern for autonomous agents.

## How It Works

1. **Think**: LLM analyzes context and decides next action
2. **Act**: Execute the chosen tool
3. **Observe**: Add result to history
4. **Repeat**: Until task complete or max iterations

## Implementation

```python
class ReActAgent:
    def __init__(self, llm, tools, max_iterations=50):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.history = []

    def run(self, task: str) -> str:
        self.history.append({"role": "user", "content": task})

        for i in range(self.max_iterations):
            # Think: Get LLM response with tool options
            response = self.llm.chat(
                messages=self.history,
                tools=self._format_tools(),
                tool_choice="auto"
            )

            # Decide: Check if agent wants to use a tool
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    # Act: Execute the tool
                    result = self._execute_tool(tool_call)

                    # Observe: Add result to history
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                # No more tool calls = task complete
                return response.content

        return "Max iterations reached"

    def _format_tools(self) -> list:
        """Format tools for LLM API"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    def _execute_tool(self, tool_call) -> str:
        """Execute a tool and return result"""
        tool = self.tools.get(tool_call.function.name)
        if not tool:
            return f"Unknown tool: {tool_call.function.name}"

        try:
            args = json.loads(tool_call.function.arguments)
            return tool.execute(**args)
        except Exception as e:
            return f"Tool error: {str(e)}"
```

## When to Use

- **General-purpose agents** that need flexibility
- **Exploratory tasks** where next steps depend on results
- **Interactive workflows** with user feedback

## Tradeoffs

| Pros                        | Cons                   |
| --------------------------- | ---------------------- |
| Flexible, adapts to results | Can get stuck in loops |
| Easy to understand          | No upfront planning    |
| Good for exploration        | May miss optimal path  |
