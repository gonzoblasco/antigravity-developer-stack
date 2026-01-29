# agent-tool-builder

Comprehensive skill for designing AI agent tools following best practices.

## Overview

This skill guides you through creating well-designed tools for AI agents, focusing on JSON Schema design, clear descriptions, structured error handling, and the MCP standard.

**Core Insight:** The LLM never sees your code - only the schema and description. Make them crystal clear.

## Quick Start

1. **Read** [SKILL.md](SKILL.md) for comprehensive guidance
2. **Use** scripts to validate and generate:
   ```bash
   python scripts/validate_tool_schema.py your_tool.json
   python scripts/generate_tool_template.py --name my_tool --type mcp --params "query:string"
   ```
3. **Reference** templates and checklists as you build
4. **Deep dive** into references for advanced topics

## What's Included

### Core Documentation

- **[SKILL.md](SKILL.md)** - Main skill (814 lines)
- **[walkthrough.md](walkthrough.md)** - Complete rewrite process documentation
- **[implementation_plan.md](implementation_plan.md)** - TDD planning
- **[task.md](task.md)** - Process tracking

### Practical Tools

- **[validate_tool_schema.py](scripts/validate_tool_schema.py)** - Validate schemas against best practices
- **[generate_tool_template.py](scripts/generate_tool_template.py)** - Generate boilerplate code

### Templates & Checklists

- **[mcp-tool-template.py](assets/templates/mcp-tool-template.py)** - Complete MCP tool template
- **[tool-schema-template.json](assets/templates/tool-schema-template.json)** - JSON Schema template
- **[tool-quality-checklist.md](assets/checklists/tool-quality-checklist.md)** - Quality review checklist
- **[tool-design-decisions.md](assets/decision-trees/tool-design-decisions.md)** - Decision flowcharts

### Deep Dives

- **[json-schema-deep-dive.md](references/json-schema-deep-dive.md)** - Advanced JSON Schema patterns
- **[mcp-standard-guide.md](references/mcp-standard-guide.md)** - MCP implementation guide
- **[error-handling-patterns.md](references/error-handling-patterns.md)** - Error handling strategies

## Usage Examples

### Validate a Tool Schema

```bash
python scripts/validate_tool_schema.py my_tool_schema.json
```

Output:

```
✅ Schema is valid and follows all best practices!
```

or

```
❌ ERRORS (must fix):
  - Parameter 'query' missing description

⚠️  WARNINGS (should fix):
  - Description is too short (15 words, minimum 20)

💡 SUGGESTIONS (nice to have):
  - Add examples for complex parameter 'filters'
```

### Generate a New Tool

```bash
python scripts/generate_tool_template.py \
  --name search_documents \
  --type mcp \
  --params "query:string,limit:integer,filters:object"
```

Generates complete boilerplate with schema, code, and description template.

## Key Principles

1. **LLM sees schema + description, not code** → Make them crystal clear
2. **Description > Implementation** → A vague tool with perfect code will fail
3. **Errors should guide recovery** → Not just report failures
4. **Be specific with types** → Enums, constraints, examples
5. **Test against real scenarios** → Happy path + edge cases + errors

## Structure

```
agent-tool-builder/
├── SKILL.md                  # Core content (814 lines)
├── README.md                 # This file
├── walkthrough.md            # Process documentation
├── implementation_plan.md    # TDD planning
├── task.md                   # Tracking
│
├── scripts/                  # Validation & generation tools
│   ├── validate_tool_schema.py
│   └── generate_tool_template.py
│
├── assets/
│   ├── templates/            # Code & schema templates
│   ├── checklists/           # Quality checklists
│   └── decision-trees/       # Decision flowcharts
│
└── references/               # Deep dive documentation
    ├── json-schema-deep-dive.md
    ├── mcp-standard-guide.md
    └── error-handling-patterns.md
```

## Related Skills

- **`mcp-builder`** - For designing complete MCP servers
- **`autonomous-agent-expert`** - For agent loops and tool integration patterns
- **`backend-expert`** - For implementing tools in Node.js/Express
- **`prompt-mastery`** - For optimizing tool descriptions and prompts

## Meta Note

This skill **exemplifies its own principles**:

- The validation script returns structured errors (what it teaches)
- Templates demonstrate best practices (progressive disclosure)
- Scripts have clear descriptions and error handling (meta-recursive)

A skill about tool design that uses tools to teach tool design. 🪞

---

**Remember:** Every tool you design is a contract between the LLM and the world. Make it clear, make it specific, make it helpful.
