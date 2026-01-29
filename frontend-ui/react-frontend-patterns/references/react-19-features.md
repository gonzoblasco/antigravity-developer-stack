# React 19 Patterns

## New Hooks

| Hook               | Purpose                  |
| ------------------ | ------------------------ |
| **useActionState** | Form submission state    |
| **useOptimistic**  | Optimistic UI updates    |
| **use**            | Read resources in render |

## React Compiler

React 19 introduces the React Compiler, which largely automates memoization.

- **Automatic Memoization**: Components and hooks are memoized by default.
- **Pure Components**: Encourages writing pure components.
- **Less boilerplate**: Reduces the need for manual `useMemo` and `useCallback`.

## Server Actions

(If using Next.js or compatible framework)

Allows calling server-side functions directly from client components.

```typescript
// Server Action
async function createItem(formData: FormData) {
  'use server'
  await db.create(formData)
}

// Client Component
function Form() {
  return <form action={createItem}>...</form>
}
```
