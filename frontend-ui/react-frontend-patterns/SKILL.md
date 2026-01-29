---
name: react-frontend-patterns
description: Use when writing React applications, designing components, managing state, or optimizing performance. Keywords: react, hooks, state, patterns, frontend, components, nextjs, performance.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# React & Frontend Patterns

> **Central Hub for React Best Practices**
>
> This skill provides guidelines for building production-ready React applications. It is designed to be **modular**: read specific reference files for deep dives.

---

## 📚 Quick Reference

### 1. [Component Patterns](references/component-patterns.md)

- **Design Rules**: "Props down, events up", composition over inheritance.
- **Composition**: Compound components, Render props (legacy/niche).
- **TypeScript**: Proper typing for props and children.

### 2. [State Management](references/state-management.md)

- **Selection**: When to use `useState` vs Context vs Zustand vs React Query.
- **Custom Hooks**: Logic reuse patterns (`useToggle`, `useDebounce`).
- **Forms**: Controlled components vs libraries.

### 3. [Performance](references/performance.md)

- **Optimization**: Measure first, then optimize.
- **Techniques**: React Compiler, Memoization (`useMemo`, `useCallback`), Virtualization.
- **Code Splitting**: `React.lazy`, `Suspense`.

### 4. [React 19 & Next.js](references/react-19-features.md)

- **New Hooks**: `useActionState`, `useOptimistic`, `use`.
- **Server Components**: Architecture and data fetching patterns.
- **Next.js**: [Next.js specific patterns](references/nextjs.md).

### 5. [Quality Assurance](references/testing-accessibility.md)

- **Testing**: Unit vs Integration vs E2E.
- **Accessibility**: Semantic HTML, Keyboard navigation.
- **Error Handling**: Error Boundaries.

---

## 🧩 Code Examples

Don't reinvent the wheel. Copy these patterns:

- **[Custom Hooks](examples/custom-hooks.ts)**: `useToggle`, `useDebounce`.
- **[Complex Form](examples/complex-form.tsx)**: Controlled form with validation.
- **[Composition](examples/advanced-composition.tsx)**: Compound components & Render props.
- **[State Reducer](examples/state-patterns.tsx)**: Context + useReducer pattern.

---

## 🚫 Common Anti-Patterns

| ❌ Anti-Pattern                             | ✅ Solution                                            |
| :------------------------------------------ | :----------------------------------------------------- |
| **Prop Drilling** (passing props 3+ levels) | Use **Composition** or **Context**.                    |
| **Giant Components** (> 200 lines)          | Split into **smaller, focused components**.            |
| **`useEffect` chaining**                    | Use **derived state** or **event handlers**.           |
| **Premature Optimization**                  | **Profile** first. Most code doesn't need memoization. |
| **Index as Key** (`key={index}`)            | Use **stable unique IDs**.                             |
| **Storing Props in State**                  | Use props directly or derive state.                    |
| **Fetching in `useEffect` (client)**        | Use **React Query** or **SWR**.                        |

---

## 💡 Quick Tips

1.  **Readability > Cleverness**: Clear code is better than short code.
2.  **Colocation**: Keep styles, tests, and types close to the component.
3.  **Automatic Batching**: React 18+ batches updates automatically. You rarely need to batch manually.
4.  **Strict Mode**: Always develop with Strict Mode enabled to catch bugs early.
