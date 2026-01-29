# Example: Feature Development

**Request**: "Add a dark mode toggle to the settings page."

## The 3-File Pattern in Action

### task_plan.md

```markdown
# Task Plan: Dark Mode Toggle

## Goal

Add functional dark mode toggle to settings.

## Phases

- [x] Phase 1: Research existing theme system ✓
- [x] Phase 2: Design implementation approach ✓
- [ ] Phase 3: Implement toggle component (CURRENT)
- [ ] Phase 4: Add theme switching logic

## Decisions Made

- Using CSS custom properties for theme.
- Storing preference in localStorage.
```

### findings.md

```markdown
# Findings: Dark Mode

## Files to Modify

1. src/styles/theme.ts - Add dark theme colors.
2. src/components/SettingsPage.tsx - Add toggle.
```
