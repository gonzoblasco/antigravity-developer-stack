---
name: testing-patterns
description: Jest testing patterns, factory functions, mocking strategies, and TDD workflow. Use when writing unit tests, creating test factories, or following TDD red-green-refactor cycle.
---

# Testing Patterns and Utilities

## Testing Philosophy

- **Test-Driven Development (TDD):** Write failing test FIRST -> Implement minimal code -> Refactor.
- **Behavior-Driven:** Test behavior (what it does), not implementation (how it works). Focus on user-observable outcomes.
- **Factory Pattern:** Always use factories for data/props to keep tests DRY and resilient to schema changes.

## Test Utilities

### Custom Render Function

Wrap components with required providers (Theme, Auth, etc.) in a custom render function.

- [View Example: Custom Render](examples/render-utils.tsx)

```typescript
// Usage
renderWithTheme(<MyComponent />);
```

## Factory Pattern

### Component Props & Data Factories

Create flexible factory functions that provide sensible defaults but allow overrides. This prevents brittle tests that break when a new required field is added.

- [View Example: Factories](examples/factories.ts)

```typescript
// Usage
const user = getMockUser({ role: "admin" });
const props = getMockMyComponentProps({ title: "Custom" });
```

## Mocking Patterns

### Mocking Modules & Hooks

Use `jest.mock` to isolate the unit under test. Use `jest.requireMock` to access the mock in your test for assertions or setup.

- [View Example: Mocking Modules & Hooks](examples/mocking.ts)

```typescript
// Usage
const mockLogEvent = jest.requireMock("utils/analytics").Analytics.logEvent;
expect(mockLogEvent).toHaveBeenCalled();
```

## Test Structure & Queries

Organize tests with `describe` blocks. Use `beforeEach` to clear mocks.

- **Query Priority:** `getByText/Role` (user visible) > `getByTestId` (implementation detail).
- **Async:** Use `waitFor` for async updates.
- **User Interaction:** Use `fireEvent` to simulate user actions.

- [View Example: User Interaction Test](examples/user-interaction.test.tsx)

## Best Practices

1.  **Always use factory functions** for props and data.
2.  **Test behavior, not implementation**.
3.  **Use descriptive test names**.
4.  **Keep tests focused** - one behavior per test.

> [!WARNING]
> Avoid common anti-patterns like testing mock calls instead of side effects.
> [Read more: Anti-Patterns](references/anti-patterns.md)

## Integration with Other Skills

- **react-ui-patterns**: Test all UI states (loading, error, empty, success).
- **systematic-debugging**: Write a test that reproduces the bug before fixing it.
