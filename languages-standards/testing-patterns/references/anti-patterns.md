# Testing Anti-Patterns

## Testing Mock Behavior Instead of Real Behavior

Avoid testing that the mock was called if the user cannot see the effect. Test the side effect (UI change) instead.

```typescript
// Bad - testing the mock
expect(mockFetchData).toHaveBeenCalled();

// Good - testing actual behavior
expect(screen.getByText("John Doe")).toBeTruthy();
```

## Not Using Factories

Hardcoding test data leads to brittle tests and duplication.

```typescript
// Bad - duplicated, inconsistent test data
it("test 1", () => {
  const user = { id: "1", name: "John", email: "john@test.com", role: "user" };
});
it("test 2", () => {
  const user = { id: "2", name: "Jane", email: "jane@test.com" }; // Missing role!
});

// Good - reusable factory
const user = getMockUser({ name: "Custom Name" });
```
