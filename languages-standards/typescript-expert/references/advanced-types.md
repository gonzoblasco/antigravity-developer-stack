# Advanced Type System Expertise

## Type-Level Programming Patterns

### Branded Types for Domain Modeling

```typescript
// Create nominal types to prevent primitive obsession
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

// Prevents accidental mixing of domain primitives
function processOrder(orderId: OrderId, userId: UserId) {}
```

- Use for: Critical domain primitives, API boundaries, currency/units
- Resource: https://egghead.io/blog/using-branded-types-in-typescript

### Advanced Conditional Types

```typescript
// Recursive type manipulation
type DeepReadonly<T> = T extends (...args: any[]) => any
  ? T
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// Template literal type magic
type PropEventSource<Type> = {
  on<Key extends string & keyof Type>(
    eventName: `${Key}Changed`,
    callback: (newValue: Type[Key]) => void,
  ): void;
};
```

- Use for: Library APIs, type-safe event systems, compile-time validation
- Watch for: Type instantiation depth errors (limit recursion to 10 levels)

### Type Inference Techniques

```typescript
// Use 'satisfies' for constraint validation (TS 5.0+)
const config = {
  api: "https://api.example.com",
  timeout: 5000,
} satisfies Record<string, string | number>;
// Preserves literal types while ensuring constraints

// Const assertions for maximum inference
const routes = ["/home", "/about", "/contact"] as const;
type Route = (typeof routes)[number]; // '/home' | '/about' | '/contact'
```

### Recursive Types & Stack Depth

**"Excessive stack depth comparing types"**

- Cause: Circular or deeply recursive types
- Fix priority:
  1. Limit recursion depth with conditional types
  2. Use `interface` extends instead of type intersection
  3. Simplify generic constraints

```typescript
// Bad: Infinite recursion
type InfiniteArray<T> = T | InfiniteArray<T>[];

// Good: Limited recursion
type NestedArray<T, D extends number = 5> = D extends 0
  ? T
  : T | NestedArray<T, [-1, 0, 1, 2, 3, 4][D]>[];
```
