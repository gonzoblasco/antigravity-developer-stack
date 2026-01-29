# Debugging Mastery & Error Patterns

## CLI Debugging Tools

```bash
# Debug TypeScript files directly (if tools installed)
command -v tsx >/dev/null 2>&1 && npx tsx --inspect src/file.ts
command -v ts-node >/dev/null 2>&1 && npx ts-node --inspect-brk src/file.ts

# Trace module resolution issues
npx tsc --traceResolution > resolution.log 2>&1
grep "Module resolution" resolution.log

# Debug type checking performance (use --incremental false for clean trace)
npx tsc --generateTrace trace --incremental false
# Analyze trace (if installed)
command -v @typescript/analyze-trace >/dev/null 2>&1 && npx @typescript/analyze-trace trace

# Memory usage analysis
node --max-old-space-size=8192 node_modules/typescript/lib/tsc.js
```

## Complex Error Patterns

### "The inferred type of X cannot be named"

- Cause: Missing type export or circular dependency
- Fix priority:
  1. Export the required type explicitly
  2. Use `ReturnType<typeof function>` helper
  3. Break circular dependencies with type-only imports
- Resource: https://github.com/microsoft/TypeScript/issues/47663

### Missing type declarations

- Quick fix with ambient declarations:

```typescript
// types/ambient.d.ts
declare module "some-untyped-package" {
  const value: unknown;
  export default value;
  export = value; // if CJS interop is needed
}
```

- For more details: [Declaration Files Guide](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html)

### Module Resolution Mysteries

- "Cannot find module" despite file existing:
  1. Check `moduleResolution` matches your bundler
  2. Verify `baseUrl` and `paths` alignment
  3. For monorepos: Ensure workspace protocol (workspace:\*)
  4. Try clearing cache: `rm -rf node_modules/.cache .tsbuildinfo`

### Path Mapping at Runtime

- TypeScript paths only work at compile time, not runtime
- Node.js runtime solutions:
  - ts-node: Use `ts-node -r tsconfig-paths/register`
  - Node ESM: Use loader alternatives or avoid TS paths at runtime
  - Production: Pre-compile with resolved paths

## Custom Error Classes

```typescript
// Proper error class with stack preservation
class DomainError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
  ) {
    super(message);
    this.name = "DomainError";
    Error.captureStackTrace(this, this.constructor);
  }
}
```
