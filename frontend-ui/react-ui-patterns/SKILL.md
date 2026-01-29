---
name: react-ui-patterns
description: Modern React UI patterns for loading states, error handling, performance optimization, and data fetching. Use when building UI components, handling async data, or managing UI states. Keywords: react, loading, error handling, clean code, ui patterns, performance, skeleton, spinner.
---

# React UI Patterns

## Core Principles

1. **Never show stale UI** - Loading spinners only when actually loading.
2. **Always surface errors** - Users must know when something fails.
3. **Optimistic updates** - Make the UI feel instant.
4. **Performance First** - Don't block the main thread.
5. **Graceful degradation** - Partial data is better than no data.

## Loading State Patterns

> [!TIP]
> **The Golden Rule**: Show loading indicator ONLY when there's no data to display.

- **[Examples: Correct vs Wrong Loading Patterns](examples/loading-states.tsx)**
- **[Detailed Guide: Skeleton vs Spinner](examples/loading-states.tsx)**

### Decision Tree

1. **Error?** → Show Error State (with Retry).
2. **Loading AND No Data?** → Show Loading Indicator.
3. **Data Exists?** → Show Content (even if refreshing).

## Error Handling Patterns

> [!IMPORTANT]
> **CRITICAL**: Never swallow errors silently.

- **[Examples: Error Handling Hierarchy & Reusable Component](examples/error-handling.tsx)**

### Strategy

1. **Field Level**: Validation errors inline.
2. **Toast**: Transient/Recoverable errors.
3. **Banner**: Persistent but partial functionality.
4. **Full Screen**: Catastrophic failure.

## Performance Optimization

> [!NOTE]
> Optimization adds complexity. Measure first.

- **[Full Guide: React Performance Optimization](references/performance-optimization.md)**

### Quick Wins

- Use `React.memo` for pure components (lists, UI kits).
- **VIRTUALIZE** long lists (`react-window`).
- Use `useCallback` for functions passed to memoized children.
- Use `useTransition` for non-urgent state updates (avoid UI freezing).

## Button State Patterns

**CRITICAL: Always disable triggers during async operations.**

```tsx
// CORRECT - Button disabled while loading
<Button
  disabled={isSubmitting} // Prevent double-tap
  isLoading={isSubmitting} // Feedback
  onClick={handleSubmit}
>
  Submit
</Button>
```

## Empty States

Every list/collection MUST have an empty state.

```tsx
// CORRECT - Explicit empty state
return (
  <FlatList
    data={items}
    ListEmptyComponent={
      <EmptyState
        title="No items"
        description="Create one to get started"
        action={<CreateButton />}
      />
    }
  />
);
```

## Checklist

Before completing any UI component:

**UI States:**

- [ ] Error state handled and shown to user?
- [ ] Loading state shown ONLY when no data exists (no flash)?
- [ ] Empty state provided for collections?
- [ ] Buttons disabled during async operations?

**Performance:**

- [ ] Are list keys stable?
- [ ] Are heavy lists virtualized?
- [ ] Is `console.log` removed?

## Integration with Other Skills

- **graphql-schema**: Use mutation patterns with proper error handling.
- **testing-patterns**: Test all UI states (loading, error, empty, success).
- **formik-patterns**: Apply form submission patterns.
