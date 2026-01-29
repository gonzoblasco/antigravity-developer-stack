---
name: frontend-dev-guidelines
description: Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend code.
---

# Frontend Development Guidelines

## Purpose

Comprehensive guide for modern React development, emphasizing Suspense-based data fetching, lazy loading, proper file organization, and performance optimization.

## When to Use This Skill

- Creating new components or pages
- Building new features
- Fetching data with TanStack Query
- Setting up routing with TanStack Router
- Styling components with MUI v7
- Performance optimization
- Organizing frontend code
- TypeScript best practices

---

## Quick Actions

### 📋 Checklists

- **[New Component Checklist](checklists/new-component.md)** - Use when creating a new UI component.
- **[New Feature Checklist](checklists/new-feature.md)** - Use when starting a new feature domain.

### ⚡ Cheatsheets

- **[Component Templates](cheatsheets/templates.md)** - Copy-paste modern component structure.
- **[Imports & Aliases](cheatsheets/imports.md)** - Common imports and path aliases.
- **[File Structure Reference](cheatsheets/quick-reference.md)** - Where to put files.

---

## 📚 Topic Guides

| Type          | Resource                                                  |
| ------------- | --------------------------------------------------------- |
| **Patterns**  | [Component Patterns](resources/component-patterns.md)     |
| **Data**      | [Data Fetching (Suspense)](resources/data-fetching.md)    |
| **Structure** | [File Organization](resources/file-organization.md)       |
| **UI**        | [Styling Guide (MUI)](resources/styling-guide.md)         |
| **Routing**   | [Routing Guide](resources/routing-guide.md)               |
| **UX**        | [Loading & Errors](resources/loading-and-error-states.md) |
| **Perf**      | [Performance Optimization](resources/performance.md)      |
| **Types**     | [TypeScript Standards](resources/typescript-standards.md) |
| **Misc**      | [Common Patterns](resources/common-patterns.md)           |
| **Full Code** | [Complete Examples](resources/complete-examples.md)       |

---

## Core Principles

1. **Lazy Load Everything Heavy**: Routes, DataGrid, charts, editors
2. **Suspense for Loading**: Use SuspenseLoader, not early returns
3. **useSuspenseQuery**: Primary data fetching pattern for new code
4. **Features are Organized**: api/, components/, hooks/, helpers/ subdirs
5. **Styles Based on Size**: <100 inline, >100 separate
6. **Import Aliases**: Use @/, ~types, ~components, ~features
7. **No Early Returns**: Prevents layout shift
8. **useMuiSnackbar**: For all user notifications

## Related Skills

- **error-tracking**: Error tracking with Sentry
- **backend-dev-guidelines**: Backend API patterns
