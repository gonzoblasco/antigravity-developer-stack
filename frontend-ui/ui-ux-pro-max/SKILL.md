---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks. Actions: design, build, review, optimize. Searchable database with priority-based recommendations."
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide and search engine for web and mobile applications.

## Quick Start

1.  **Analyze Request**: Identify product type, style, industry, and stack.
2.  **Generate Design System** (Required):
    ```bash
    python3 .agent/skills/ui-ux-pro-max/scripts/search.py "query" --design-system -p "Project Name"
    ```
3.  **Refine & Implement**: Use detailed domain searches and stack guidelines.

## Usage

### 1. Design System Generation

This is the primary entry point. It searches all domains and applies reasoning rules.

```bash
# Example: Spa website
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness elegant" --design-system -p "Serenity"
```

### 2. Domain & Stack Search

Supplement the design system with specific queries.

```bash
# Domain example (ux, style, typography, color, charts, etc.)
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Stack example (html-tailwind, react, nextjs, etc.)
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "layout form" --stack html-tailwind
```

## References

- [Quality Standards & Checklists](references/quality-standards.md) (Accessibility, Rules, Pre-Delivery Checklist)
- [Search Guide](references/search-guide.md) (All Domains, Stacks, Workflows)

## Prerequisites

Ensure Python 3 is installed:

```bash
python3 --version
```
