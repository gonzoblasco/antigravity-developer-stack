---
name: tailwind-patterns
description: Use when designing UI, writing CSS, or configuring styles. Keywords: tailwind, css, styling, ui, design system, oklch.
---

# Tailwind CSS Best Practices (v4.1)

> **Goal**: Create modern, performant, and maintainable styles using Tailwind CSS v4 native features.

## 1. The v4 "Iron Laws" (ALWAYS FOLLOW)

1.  **CSS-First Config**: NEVER create `tailwind.config.js` for new projects. Use `@theme { ... }` in your CSS file.
2.  **No PostCSS needed**: Trust the Oxide engine. It handles imports and nesting natively.
3.  **OKLCH Colors**: Always use `oklch()` for custom colors. It is the new standard for digital color.
4.  **No `@apply`**: Avoid `@apply` in CSS files unless wrapping a 3rd party library. Extract to React/Vue components instead.

## 2. v4.1 Feature Mandates

When the user asks for these features, use the **Native v4.1 Utilities**, not plugins or hacks:

| Feature             | Legacy / Hack (REJECT)        | v4.1 Native (USE)                          |
| ------------------- | ----------------------------- | ------------------------------------------ |
| **Text Shadow**     | `drop-shadow`, custom plugins | `text-shadow-sm`, `text-shadow-blue-500`   |
| **Masking**         | `style="mask-image:..."`      | `mask-linear`, `mask-radial`               |
| **Coloured Shadow** | `shadow-[rgba...]`            | `drop-shadow-indigo-500`, `shadow-red-500` |

## 3. Layout & Responsivity

- **Container Queries First**: If a component is reusable, use `@container` on the parent and `@md:` on the child. DO NOT use viewport breakpoints (`md:`) for internal component logic.
- **Mobile-First**: Never use `sm:` to define the default state. Default is mobile.
  - ❌ `sm:w-full md:w-1/2`
  - ✅ `w-full md:w-1/2`

## 4. Anti-Patterns to Correct

If you see these, refactor them immediately:

- **Hex Codes**: `bg-[#1da1f2]` -> Define semantic `--color-brand` in `@theme`.
- **Arbitrary Values**: `p-[13px]` -> Use the closest scale `p-3` (0.75rem) or `p-3.5` (0.875rem).
- **String Interpolation**: `` `bg-${color}-500` `` -> Full class names `bg-red-500` (so Oxide can detect them).

## Documentation Index

- **[Architecture & v4.1 Features](references/v4-architecture.md)**: Config, Performance, detailed feature list.
- **[Layout Patterns](references/modern-layout.md)**: Flex, Grid, Bento, Container Queries.
- **[Design Tokens](references/design-tokens.md)**: Typography, Colors, Animation.
