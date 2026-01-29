# Permission & Safety Patterns

## Permission Levels

```python
from enum import Enum

class PermissionLevel(Enum):
    AUTO = "auto"          # Fully automatic
    ASK_ONCE = "ask_once"  # Ask once per session
    ASK_EACH = "ask_each"  # Ask every time
    NEVER = "never"        # Never allow


PERMISSION_CONFIG = {
    # Low risk - can auto-approve
    "read_file": PermissionLevel.AUTO,
    "list_directory": PermissionLevel.AUTO,
    "search_code": PermissionLevel.AUTO,

    # Medium risk - ask once
    "write_file": PermissionLevel.ASK_ONCE,
    "edit_file": PermissionLevel.ASK_ONCE,

    # High risk - ask each time
    "run_command": PermissionLevel.ASK_EACH,
    "delete_file": PermissionLevel.ASK_EACH,

    # Dangerous - never auto-approve
    "sudo_command": PermissionLevel.NEVER,
    "format_disk": PermissionLevel.NEVER
}
```

## Permission Manager

```python
class PermissionManager:
    def __init__(self, config: dict[str, PermissionLevel]):
        self.config = config
        self.session_approvals = set()  # Tools approved this session

    def check_permission(self, tool_name: str, context: dict) -> bool:
        """Check if tool execution is allowed"""
        level = self.config.get(tool_name, PermissionLevel.ASK_EACH)

        if level == PermissionLevel.AUTO:
            return True

        if level == PermissionLevel.NEVER:
            return False

        if level == PermissionLevel.ASK_ONCE:
            if tool_name in self.session_approvals:
                return True
            approved = self._ask_user(tool_name, context)
            if approved:
                self.session_approvals.add(tool_name)
            return approved

        # ASK_EACH
        return self._ask_user(tool_name, context)

    def _ask_user(self, tool_name: str, context: dict) -> bool:
        """Prompt user for approval"""
        print(f"Agent wants to execute: {tool_name}")
        print(f"Context: {context}")
        response = input("Allow? (y/n): ")
        return response.lower() == 'y'
```

## Sandboxed Execution

```python
import os
import subprocess

class SandboxedExecution:
    """Execute code/commands in isolated environment"""

    def __init__(self, workspace_dir: str):
        self.workspace = workspace_dir
        self.allowed_commands = ["npm", "python", "node", "git", "ls", "cat"]

    def validate_path(self, path: str) -> bool:
        """Ensure path is within workspace"""
        real_path = os.path.realpath(path)
        workspace_real = os.path.realpath(self.workspace)
        return real_path.startswith(workspace_real)

    def validate_command(self, command: str) -> bool:
        """Check if command is allowed"""
        cmd_parts = command.split()
        if not cmd_parts:
            return False
        return cmd_parts[0] in self.allowed_commands

    def execute_sandboxed(self, command: str) -> ToolResult:
        if not self.validate_command(command):
            return ToolResult(success=False, error="Command not allowed")

        # Execute in isolated environment
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace,
            capture_output=True,
            timeout=30,
            env={
                **os.environ,
                "HOME": self.workspace,  # Isolate home directory
            }
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.decode(),
            error=result.stderr.decode() if result.returncode != 0 else None
        )
```

## Security Checklist

- [ ] Permission system implemented for all tools
- [ ] Dangerous operations require explicit approval
- [ ] Path traversal attacks prevented
- [ ] Command injection attacks prevented
- [ ] Sandbox isolation for untrusted code
- [ ] Timeout limits on all operations
- [ ] Audit logging for all tool executions
