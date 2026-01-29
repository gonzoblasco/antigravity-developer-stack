# Context Management

## Context Injection Patterns (@-mention)

````python
import os
import requests
from html2text import html_to_markdown

class ContextManager:
    """Manage context provided to the agent"""

    def __init__(self):
        self.context = []

    def add_file(self, path: str) -> None:
        """@file - Add file contents to context"""
        with open(path, 'r') as f:
            content = f.read()

        self.context.append({
            "type": "file",
            "path": path,
            "content": content
        })

    def add_folder(self, path: str, max_files: int = 20) -> None:
        """@folder - Add all files in folder"""
        file_count = 0
        for root, dirs, files in os.walk(path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file_count >= max_files:
                    return
                file_path = os.path.join(root, file)
                self.add_file(file_path)
                file_count += 1

    def add_url(self, url: str) -> None:
        """@url - Fetch and add URL content"""
        response = requests.get(url)
        content = html_to_markdown(response.text)

        self.context.append({
            "type": "url",
            "url": url,
            "content": content
        })

    def add_selection(self, text: str, source: str) -> None:
        """@selection - Add selected text"""
        self.context.append({
            "type": "selection",
            "source": source,
            "content": text
        })

    def get_context_prompt(self) -> str:
        """Format context for LLM prompt"""
        parts = []
        for item in self.context:
            if item["type"] == "file":
                parts.append(f"File: {item['path']}\n```\n{item['content']}\n```")
            elif item["type"] == "url":
                parts.append(f"URL: {item['url']}\n{item['content']}")
            elif item["type"] == "selection":
                parts.append(f"Selection from {item['source']}:\n{item['content']}")

        return "\n\n---\n\n".join(parts)

    def estimate_tokens(self) -> int:
        """Estimate token count (rough: 4 chars = 1 token)"""
        total_chars = sum(len(item.get("content", "")) for item in self.context)
        return total_chars // 4
````

## Context Window Management

```python
class ContextWindowManager:
    """Manage context to avoid overflow"""

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        self.context_manager = ContextManager()

    def add_with_limit(self, item: dict) -> bool:
        """Add item if within token limit"""
        current = self.context_manager.estimate_tokens()
        item_tokens = len(item.get("content", "")) // 4

        if current + item_tokens > self.max_tokens:
            return False

        self.context_manager.context.append(item)
        return True

    def summarize_if_needed(self, llm) -> None:
        """Summarize context if approaching limit"""
        if self.context_manager.estimate_tokens() > self.max_tokens * 0.8:
            # Summarize older context
            summary = llm.summarize(self.context_manager.get_context_prompt())
            self.context_manager.context = [{
                "type": "summary",
                "content": summary
            }]
```

## Multi-Model Architecture

```python
class MultiModelAgent:
    """Use different models for different purposes"""

    def __init__(self):
        self.models = {
            "fast": "gpt-3.5-turbo",      # Quick decisions
            "smart": "gpt-4-turbo",        # Complex reasoning
            "code": "claude-3-sonnet",      # Code generation
        }

    def select_model(self, task_type: str) -> str:
        if task_type == "planning":
            return self.models["fast"]
        elif task_type == "analysis":
            return self.models["smart"]
        elif task_type == "code":
            return self.models["code"]
        return self.models["smart"]
```
