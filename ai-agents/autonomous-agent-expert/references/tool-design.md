# Tool Design Patterns

## Essential Coding Agent Tools

```python
CODING_AGENT_TOOLS = {
    # File operations
    "read_file": "Read file contents",
    "write_file": "Create or overwrite a file",
    "edit_file": "Make targeted edits to a file",
    "list_directory": "List files and folders",
    "search_files": "Search for files by pattern",

    # Code understanding
    "search_code": "Search for code patterns (grep)",
    "get_definition": "Find function/class definition",
    "get_references": "Find all references to a symbol",

    # Terminal
    "run_command": "Execute a shell command",
    "read_output": "Read command output",
    "send_input": "Send input to running command",

    # Browser (optional)
    "open_browser": "Open URL in browser",
    "click_element": "Click on page element",
    "type_text": "Type text into input",
    "screenshot": "Capture screenshot",

    # Context
    "ask_user": "Ask the user a question",
    "search_web": "Search the web for information"
}
```

## Tool Schema Design

```python
from dataclasses import dataclass
from typing import Any
import json

@dataclass
class ToolResult:
    success: bool
    output: str = ""
    error: str | None = None


class Tool:
    """Base class for agent tools"""

    name: str
    description: str

    @property
    def schema(self) -> dict:
        """JSON Schema for the tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self._get_parameters(),
                "required": self._get_required()
            }
        }

    def _get_parameters(self) -> dict:
        """Override to define parameters"""
        return {}

    def _get_required(self) -> list:
        """Override to define required params"""
        return []

    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool and return result"""
        raise NotImplementedError


class ReadFileTool(Tool):
    """Example: Read file contents"""

    name = "read_file"
    description = "Read the contents of a file"

    def _get_parameters(self) -> dict:
        return {
            "path": {
                "type": "string",
                "description": "Absolute path to the file"
            },
            "start_line": {
                "type": "integer",
                "description": "Start line (1-indexed, optional)"
            },
            "end_line": {
                "type": "integer",
                "description": "End line (1-indexed, optional)"
            }
        }

    def _get_required(self) -> list:
        return ["path"]

    def execute(self, path: str, start_line: int = None, end_line: int = None) -> ToolResult:
        try:
            with open(path, 'r') as f:
                lines = f.readlines()

            if start_line and end_line:
                lines = lines[start_line-1:end_line]

            return ToolResult(success=True, output=''.join(lines))
        except Exception as e:
            return ToolResult(success=False, error=str(e))
```

## Tool Design Principles

1. **Single Responsibility**: Each tool does one thing well
2. **Clear Parameters**: Use descriptive names and types
3. **Structured Output**: Return consistent ToolResult format
4. **Error Handling**: Always catch and report errors
5. **Idempotency**: Prefer tools that can be safely retried

## Common Tool Categories

| Category | Examples                         | Risk Level |
| -------- | -------------------------------- | ---------- |
| Read     | read_file, search_code, list_dir | Low        |
| Write    | write_file, edit_file            | Medium     |
| Execute  | run_command, send_input          | High       |
| External | search_web, open_browser         | Medium     |
| User     | ask_user, notify_user            | Low        |
