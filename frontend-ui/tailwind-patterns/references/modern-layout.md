# Modern Layout & Responsive Design

> Patterns for Flexbox, Grid, and Container Queries.

## 1. Container Queries (v4 Native)

The preferred method for component-level responsivity.

| Type           | Responds To          | Syntax                |
| -------------- | -------------------- | --------------------- |
| **Breakpoint** | Viewport width       | `md:`, `lg:`          |
| **Container**  | Parent element width | `@container` + `@md:` |

### Usage Pattern

1. **Define**: Add `@container` to the parent wrapper.
2. **Respond**: Use `@sm:`, `@md:` on children (instead of `sm:`, `md:`).
3. **Name (Optional)**: `@container/card` to target specific parents.

## 2. Flexbox Patterns

| Pattern            | Classes                             |
| ------------------ | ----------------------------------- |
| Center (both axes) | `flex items-center justify-center`  |
| Vertical stack     | `flex flex-col gap-4`               |
| Horizontal row     | `flex gap-4`                        |
| Space between      | `flex justify-between items-center` |
| Wrap grid          | `flex flex-wrap gap-4`              |

## 3. Grid Patterns

| Pattern                   | Classes                                                          |
| ------------------------- | ---------------------------------------------------------------- |
| **Auto-fit (Responsive)** | `grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]`            |
| **Sidebar Layout**        | `grid grid-cols-[auto_1fr]`                                      |
| **Bento Grid**            | `grid grid-cols-3 grid-rows-2` using `col-span-*` / `row-span-*` |

> **Design Tip**: Prefer asymmetric "Bento" layouts over boring symmetric grids.

## 4. Responsive Best Practices

### Breakpoints

- `sm:` (640px)
- `md:` (768px)
- `lg:` (1024px)
- `xl:` (1280px)
- `2xl:` (1536px)

### Mobile-First Strategy

1. Write mobile styles **without prefix** (default).
2. Add prefixes (`md:`, `lg:`) only to **change** behavior for larger screens.
3. ❌ `sm:w-full md:w-1/2` (Redundant `sm:`).
4. ✅ `w-full md:w-1/2`.
