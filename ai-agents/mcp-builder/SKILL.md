---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

> [!IMPORTANT]
> **Core Principle**: The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks. Focus on **Tool Discoverability**, **Error Recovery**, and **Context Management**.

## 🚀 Quick Start

1.  **Scaffold**: Use the included script to start a new project instantly.
    ```bash
    ./scripts/scaffold.sh my-new-server
    ```
2.  **Plan**: Use the [Prompts Library](./reference/prompts.md) to generate your tool definitions.
3.  **Build**: Follow the language-specific guides below.
4.  **Evaluate**: You MUST create an evaluation set (10 questions) to verify your server.

---

## 📚 Resource Library

| Resource                                               | Description                                                          |
| :----------------------------------------------------- | :------------------------------------------------------------------- |
| **[🤖 Prompts Library](./reference/prompts.md)**       | **START HERE**. Copy-paste these prompts to generate code and tests. |
| [⚡ TypeScript Guide](./reference/node_mcp_server.md)  | Best for: Web-heavy, async, or JSON-centric services.                |
| [🐍 Python Guide](./reference/python_mcp_server.md)    | Best for: Data science, AI integration, or simple scripts.           |
| [📋 Best Practices](./reference/mcp_best_practices.md) | Naming conventions, error handling, and security.                    |
| [✅ Evaluation Guide](./reference/evaluation.md)       | How to prove your server actually works.                             |

---

## 🛠️ Step-by-Step Workflow

### Phase 1: Deep Research & Planning

**Do NOT write code yet.**

1.  **Analyze the API**: Read the documentation of the service you are integrating.
2.  **Select Tools**: Choose the top 5-7 most critical operations.
    - _Tip_: Use the "API to MCP Tool Plan" prompt in `reference/prompts.md`.
3.  **Define Schema**:
    - **TypeScript**: Plan your Zod schemas.
    - **Python**: Plan your Pydantic models.

### Phase 2: Implementation

> [!TIP]
> Use the "System Prompt for Code Generation" in `reference/prompts.md` to have an LLM write the boilerplate for you.

#### Core Checklist

- [ ] **Project Setup**: Use `scripts/scaffold.sh`.
- [ ] **Authentication**: flexible (Env vars preferred).
- [ ] **Error Handling**: NEVER crash. Catch errors and return a user-friendly message.
- [ ] **Logging**: Log to `stderr` only. `stdout` is reserved for the protocol.

### Phase 3: Review & Test

1.  **Build**: Ensure it compiles (`npm run build` or `python -m py_compile ...`).
2.  **Inspect**: Use the MCP Inspector.
    ```bash
    npx @modelcontextprotocol/inspector node build/index.js
    ```
3.  **Refine**: clear tool descriptions are critical for the LLM to understand _when_ to use a tool.

### Phase 4: Evaluation (Mandatory)

**You aren't done until you can prove it works.**

1.  Create `evaluation.xml` with 10 realistic questions.
2.  Run the evaluation script (see [Evaluation Guide](./reference/evaluation.md)).
3.  **Pass Criteria**: The LLM must be able to answer 8/10 questions correctly using your tools.

---

## 🧠 Expert Tips

### Best Practices

- **Tool Naming**: Use `service_action` (e.g., `github_create_issue`).
- **Descriptions**: Be verbose! "Creates a new issue" is bad. "Creates a new issue in the specified repository. Requires title and body. detailed_description is optional." is good.
- **Limit Output**: If a tool returns huge JSON, truncate it or offer pagination. Large context windows are expensive and slow.

### Common Pitfalls

1.  **Crashing on Error**: If a tool throws an unhandled exception, the connection dies. **Catch Everything.**
2.  **Console Logging**: `console.log` breaks JSON-RPC over stdio. Use `console.error` or a logging library that writes to stderr.
3.  **Sparse Descriptions**: If the LLM guesses parameters, your description is too vague.

---
