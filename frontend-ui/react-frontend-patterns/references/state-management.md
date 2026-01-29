# State Management & Hooks

## Hook Patterns

### When to Extract Hooks

| Pattern             | Extract When              |
| ------------------- | ------------------------- |
| **useLocalStorage** | Same storage logic needed |
| **useDebounce**     | Multiple debounced values |
| **useFetch**        | Repeated fetch patterns   |
| **useForm**         | Complex form state        |

### Hook Rules

1.  **Top Level Only**: Don't call hooks inside loops, conditions, or nested functions.
2.  **Same Order**: Hooks must run in the exact same order every render.
3.  **Naming**: Custom hooks must start with "use".
4.  **Effects**: Always clean up side effects (subscriptions, timers) in `useEffect`.

See examples in `examples/custom-hooks.ts`.

---

## State Management Selection

| Complexity         | Solution                          |
| ------------------ | --------------------------------- |
| **Simple**         | `useState`, `useReducer`          |
| **Shared local**   | React Context                     |
| **Server state**   | React Query (TanStack Query), SWR |
| **Complex global** | Zustand, Redux Toolkit            |

### State Placement

| Scope            | Where                  |
| ---------------- | ---------------------- |
| Single component | `useState`             |
| Parent-child     | Lift state up          |
| Subtree          | Context                |
| App-wide         | Global store (Zustand) |

### Context + Reducer Pattern

Ideal for complex local state that needs to be shared among a few components (e.g., a multi-step wizard, or a complex data grid).

See implementation in `examples/state-patterns.tsx`.

---

## Form Handling

For complex forms, use **React Hook Form**. For simple or specific custom forms, controlled components with Zod validation are a robust pattern.

See controlled form example in `examples/complex-form.tsx`.
