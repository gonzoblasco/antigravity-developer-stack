# Testing, Accessibility & Error Handling

## Testing Principles

| Level           | Focus                 | Tooling               |
| --------------- | --------------------- | --------------------- |
| **Unit**        | Pure functions, hooks | Vitest/Jest           |
| **Integration** | Component behavior    | React Testing Library |
| **E2E**         | User flows            | Playwright            |

**Priorities**:

1.  User-visible behavior (not implementation details).
2.  Edge cases (empty states, errors).
3.  Accessibility (keyboard nav, screen readers).

## Accessibility (a11y)

- **Semantic HTML**: Use `<button>`, `<nav>`, `<main>`, etc.
- **Keyboard Navigation**: Ensure all interactive elements are focusable and usable with a keyboard.
- **ARIA**: Use only when necessary. HTML is preferred.
  - `aria-expanded`, `aria-label`, `role="dialog"`.

## Error Handling

### Error Boundaries

Wrap parts of your application in Error Boundaries to prevent the entire app from crashing.

| Scope     | Placement              |
| --------- | ---------------------- |
| App-wide  | Root level             |
| Feature   | Route/feature level    |
| Component | Around risky component |

See `react-error-boundary` library for a robust implementation, or build a clear custom one.
