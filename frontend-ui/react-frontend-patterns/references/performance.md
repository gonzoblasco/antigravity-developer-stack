# Performance Optimization

## Strategy

1.  **Measure First**: Don't optimize prematurely. Use React DevTools Profiler.
2.  **Identify Bottlenecks**: Look for wasted renders or expensive calculations.
3.  **Apply Fixes**: Memoize, virtualize, or split code.

## Techniques

### 1. Memoization (Pre-React 19 / Compiler)

If not using React Compiler:

- `useMemo`: For expensive calculations.
- `useCallback`: For stable function references passed to optimized children.
- `React.memo`: To prevent re-renders of pure components when props haven't changed.

### 2. Code Splitting & Lazy Loading

Break your main bundle into smaller chunks.

```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))

<Suspense fallback={<Spinner />}>
  <HeavyChart />
</Suspense>
```

### 3. Virtualization

For long lists (100+ items), render only what's visible.

Recommended library: `@tanstack/react-virtual`.

### 4. Next.js Specifics

- **Server Components**: Move non-interactive UI to Server Components to reduce client JS bundle.
- **Image Optimization**: Use `next/image` to prevent layout shift and serve optimized formats.
