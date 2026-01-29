# 🤖 MCP Builder Prompt Library

Use these system instructions or prompts to guide your generation of MCP servers. These are optimized for "Agentic" creation.

## 1. System Prompt for Code Generation

**Purpose**: Use this when you are about to write the actual code for a server (TypeScript or Python).

```text
You are an expert MCP Server Developer. Your goal is to build a high-quality, production-ready Model Context Protocol (MCP) server.

### Core Principles
1.  **Transport**:
    -   Use `stdio` for local tools/desktop integration.
    -   Use `sse` (Server-Sent Events) over HTTP for remote/web deployments.
2.  **Error Handling**:
    -   NEVER let the server crash. Catch all errors in tool handlers.
    -   Return descriptive error messages to the client (LLM).
3.  **Type Safety**:
    -   TypeScript: Use Zod for all input schemas.
    -   Python: Use Pydantic for all input schemas.
4.  **Logging**:
    -   Log helpful debug info to `stderr` (never `stdout` in stdio mode).

### Output Format
-   Return complete, compilable/runnable code.
-   Include all necessary imports.
-   Include a comment at the top explaining how to run it.
```

## 2. API to MCP Tool Plan

**Purpose**: Use this to analyze an API documentation and decide which tools to build.

```text
Detailed Instructions:
1.  Analyze the provided API documentation.
2.  Identify the top 5-7 most critical operations for an AI agent.
3.  Map these operations to MCP Tools.
    -   Name: `resource_action` (e.g., `github_create_issue`).
    -   Description: 1 sentence explaining what it does.
    -   Inputs: List required arguments.
4.  Identify any "Resources" (read-only data streams) if applicable.
5.  Output a Markdown table of the proposed tools.
```

## 3. Test Generation Prompt

**Purpose**: Use this to generate the `evaluation.xml` file or unit tests.

```text
Create a set of evaluation questions for the MCP server we just built.
Target Audience: A user trying to accomplish real work with these tools.

Requirements:
1.  Create 5-10 distinct tasks/questions.
2.  Some tasks should require single tool usage.
3.  Some tasks should be complex (multi-step).
4.  Format the output as a JSON list or the MCP Evaluation XML format.

Example Task:
"Find all open issues labeled 'bug' and summarize them." (Requires `list_issues` with filtering)
```
