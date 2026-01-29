# --- 2.1 ReAct Pattern (Reasoning + Acting) ---

REACT_PROMPT = """
You are an AI assistant that can use tools to answer questions.

Available tools:
{tools_description}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(arguments)]
Observation: [tool result - this will be filled in]
... (repeat Thought/Action/Observation as needed)
Thought: I have enough information to answer
Final Answer: [your final response]

Question: {question}
"""

class ReActAgent:
    def __init__(self, tools: list, llm):
        self.tools = {t.name: t for t in tools}
        self.llm = llm
        self.max_iterations = 10

    def _format_tools(self):
        return "\n".join([f"{name}: {t.description}" for name, t in self.tools.items()])

    def _extract_final_answer(self, response): return response.split("Final Answer:")[-1].strip()
    def _parse_action(self, response): return "tool_name", {} 
    def _execute_tool(self, action): return "tool_output"

    def run(self, question: str) -> str:
        prompt = REACT_PROMPT.format(
            tools_description=self._format_tools(),
            question=question
        )

        for _ in range(self.max_iterations):
            response = self.llm.generate(prompt)

            if "Final Answer:" in response:
                return self._extract_final_answer(response)

            action = self._parse_action(response)
            observation = self._execute_tool(action)
            prompt += f"\nObservation: {observation}\n"

        return "Max iterations reached"

# --- 2.2 Function Calling Pattern ---

# Define tools as functions with schemas
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }
]

class FunctionCallingAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def _execute_tool(self, name, args): return "result"

    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]

        while True:
            response = self.llm.chat(
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(
                        tool_call.name,
                        tool_call.arguments
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                return response.content

# --- 2.3 Plan-and-Execute Pattern ---

class PlanAndExecuteAgent:
    """
    1. Create a plan (list of steps)
    2. Execute each step
    3. Replan if needed
    """
    def __init__(self, planner, executor, synthesizer):
        self.planner = planner
        self.executor = executor
        self.synthesizer = synthesizer

    def _needs_replan(self, task, results): return False

    def run(self, task: str) -> str:
        # Planning phase
        plan = self.planner.create_plan(task)
        # Returns: ["Step 1: ...", "Step 2: ...", ...]

        results = []
        for step in plan:
            # Execute each step
            result = self.executor.execute(step, context=results)
            results.append(result)

            # Check if replan needed
            if self._needs_replan(task, results):
                new_plan = self.planner.replan(
                    task,
                    completed=results,
                    remaining=plan[len(results):]
                )
                plan = new_plan

        # Synthesize final answer
        return self.synthesizer.summarize(task, results)

# --- 2.4 Multi-Agent Collaboration ---

# Mock classes for Multi-Agent
class ResearchAgent: pass
class AnalystAgent: pass
class WriterAgent: pass
class CriticAgent: 
    def review(self, results): return type('Critique', (), {'needs_revision': False})()
class CoordinatorAgent:
    def decompose(self, task): return []
    def synthesize(self, results): return "Final result"

class AgentTeam:
    """
    Specialized agents collaborating on complex tasks
    """

    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
            "critic": CriticAgent()
        }
        self.coordinator = CoordinatorAgent()
    
    def solve_with_feedback(self, task, results, critique): return "Revised result"

    def solve(self, task: str) -> str:
        # Coordinator assigns subtasks
        assignments = self.coordinator.decompose(task)

        results = {}
        for assignment in assignments:
            agent = self.agents[assignment.agent]
            result = agent.execute(
                assignment.subtask,
                context=results
            )
            results[assignment.id] = result

        # Critic reviews
        critique = self.agents["critic"].review(results)

        if critique.needs_revision:
            # Iterate with feedback
            return self.solve_with_feedback(task, results, critique)

        return self.coordinator.synthesize(results)
