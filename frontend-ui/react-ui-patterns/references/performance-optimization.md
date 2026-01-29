# React Performance Optimization Patterns

> [!IMPORTANT]
> Optimization is not free. It adds code complexity. Always measure before optimizing (Profile first!).

## 1. Render Optimization

### React.memo

Prevent re-renders of child components when props haven't changed.

**When to use:**

- Pure functional components that render often with same props.
- Big lists items.
- UI components (Buttons, Inputs) used everywhere.

```tsx
const ExpensiveComponent = React.memo(({ data, onClick }) => {
  // ... heavy rendering logic
  return <div onClick={onClick}>{data}</div>;
});

// CRITICAL: You MUST use useCallback for functions passed to memoized components!
// If you don't, the function reference changes on every render, breaking React.memo.
const Parent = () => {
  const handleClick = useCallback(() => {
    /*...*/
  }, []); // <--- Required

  return <ExpensiveComponent onClick={handleClick} />;
};
```

### useMemo & useCallback

- **useMemo**: Memoize _expensive calculations_.
- **useCallback**: Memoize _function references_ (essential for `React.memo` children).

```tsx
// Expensive Calculation
const filteredItems = useMemo(() => {
  return items.filter((item) => item.value > 1000).sort((a, b) => a.id - b.id);
}, [items]); // Only re-runs if items change

// Function Ref
const handleDelete = useCallback(
  (id: string) => {
    deleteItem(id);
  },
  [deleteItem],
); // Stable reference
```

## 2. List Virtualization

Rendering thousands of DOM nodes kills performance. Use virtualization to render only what's visible.

**Recommended Libraries:**

- `react-window` (Lightweight)
- `react-virtuoso` (Dynamic heights, easier API)

```tsx
import { FixedSizeList as List } from "react-window";

const Row = ({ index, style }) => <div style={style}>Row {index}</div>;

const Example = () => (
  <List height={150} itemCount={1000} itemSize={35} width={300}>
    {Row}
  </List>
);
```

## 3. Code Splitting & Lazy Loading

Break your bundle into smaller chunks.

```tsx
// 1. Lazy Import
const HeavyChart = React.lazy(() => import("./HeavyChart"));

// 2. Suspense Wrapper
const Dashboard = () => (
  <Suspense fallback={<Spinner />}>
    <HeavyChart />
  </Suspense>
);
```

## 4. Interaction Interaction (INP)

Avoid blocking the main thread during user interactions.

- Use startTransition to mark non-urgent updates.

```tsx
import { useState, useTransition } from "react";

const Search = () => {
  const [isPending, startTransition] = useTransition();
  const [input, setInput] = useState("");

  const handleChange = (e) => {
    // Urgent: Update input value immediately
    setInput(e.target.value);

    // Non-urgent: Filter list (can lag slightly)
    startTransition(() => {
      setFilter(e.target.value);
    });
  };
};
```

## Checklist

- [ ] Are keys in lists stable and unique? (No `index` as key if list changes)
- [ ] Is `React.memo` actually preventing renders? (Check with DevTools)
- [ ] Are heavy computations wrapped in `useMemo`?
- [ ] Are large lists virtualized?
- [ ] Are images optimized (WebP, lazy loading, correct size)?
