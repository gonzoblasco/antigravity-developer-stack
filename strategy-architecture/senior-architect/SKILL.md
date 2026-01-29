---
name: senior-architect
description: Use when designing system architecture, making technical decisions, creating architecture diagrams, or evaluating tech stacks. Keywords: architecture, system design, diagram, tech stack, scalability, trade-offs.
---

# Senior Architect

Comprehensive toolkit for designing scalable systems, documenting architecture, and analyzing dependencies.

## Capabilities

### 1. Architecture Diagram Generator

Generates Mermaid JS diagrams from your codebase structure.

```bash
python scripts/architecture_diagram_generator.py <project-path> --output diagram.mmd
```

### 2. Dependency Analyzer

Analyzes project dependencies (package.json, requirements.txt) and reports metrics.

```bash
python scripts/dependency_analyzer.py <project-path> --json
```

### 3. Project Architect (Linter)

Checks project health against architectural best practices (README, Dockerfile, Gitignore existence, etc.).

```bash
python scripts/project_architect.py <target-path>
```

## Reference Documentation

- [Architecture Patterns](references/architecture_patterns.md)
- [System Design Workflows](references/system_design_workflows.md)
- [Tech Decision Guide](references/tech_decision_guide.md)

## Tech Stack Coverage

- **Languages:** TypeScript, JavaScript, Python, Go
- **Frontend:** React, Next.js, React Native
- **Backend:** Node.js, Express, GraphQL
- **Database:** PostgreSQL, Supabase
- **DevOps:** Docker, Kubernetes

## Development Workflow

1. **Analyze**: Run `project_architect.py` to assess current state.
2. **Visualize**: Run `architecture_diagram_generator.py` to see the structure.
3. **Plan**: Use `references/` guides to make decisions.
