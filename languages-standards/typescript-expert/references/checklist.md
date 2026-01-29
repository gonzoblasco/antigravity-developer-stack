# Code Review Checklist

When reviewing TypeScript/JavaScript code, focus on these domain-specific aspects:

### Type Safety

- [ ] No implicit `any` types (use `unknown` or proper types)
- [ ] Strict null checks enabled and properly handled
- [ ] Type assertions (`as`) justified and minimal
- [ ] Generic constraints properly defined
- [ ] Discriminated unions for error handling
- [ ] Return types explicitly declared for public APIs

### TypeScript Best Practices

- [ ] Prefer `interface` over `type` for object shapes (better error messages)
- [ ] Use const assertions for literal types
- [ ] Leverage type guards and predicates
- [ ] Avoid type gymnastics when simpler solution exists
- [ ] Template literal types used appropriately
- [ ] Branded types for domain primitives

### Performance Considerations

- [ ] Type complexity doesn't cause slow compilation
- [ ] No excessive type instantiation depth
- [ ] Avoid complex mapped types in hot paths
- [ ] Use `skipLibCheck: true` in tsconfig
- [ ] Project references configured for monorepos

### Module System

- [ ] Consistent import/export patterns
- [ ] No circular dependencies
- [ ] Proper use of barrel exports (avoid over-bundling)
- [ ] ESM/CJS compatibility handled correctly
- [ ] Dynamic imports for code splitting

### Error Handling Patterns

- [ ] Result types or discriminated unions for errors
- [ ] Custom error classes with proper inheritance
- [ ] Type-safe error boundaries
- [ ] Exhaustive switch cases with `never` type

### Code Organization

- [ ] Types co-located with implementation
- [ ] Shared types in dedicated modules
- [ ] Avoid global type augmentation when possible
- [ ] Proper use of declaration files (.d.ts)
