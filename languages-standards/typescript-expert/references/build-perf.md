# Build Performance & Tooling

## Performance Optimization Strategies

### Type Checking Performance

```bash
# Diagnose slow type checking
npx tsc --extendedDiagnostics --incremental false | grep -E "Check time|Files:|Lines:|Nodes:"

# Common fixes for "Type instantiation is excessively deep"
# 1. Replace type intersections with interfaces
# 2. Split large union types (>100 members)
# 3. Avoid circular generic constraints
# 4. Use type aliases to break recursion
```

### Build Performance Patterns

- Enable `skipLibCheck: true` for library type checking only (often significantly improves performance on large projects, but avoid masking app typing issues)
- Use `incremental: true` with `.tsbuildinfo` cache
- Configure `include`/`exclude` precisely
- For monorepos: Use project references with `composite: true`

## Monorepo Management

### Nx vs Turborepo Decision Matrix

- Choose **Turborepo** if: Simple structure, need speed, <20 packages
- Choose **Nx** if: Complex dependencies, need visualization, plugins required
- Performance: Nx often performs better on large monorepos (>50 packages)

### TypeScript Monorepo Configuration

```json
// Root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" },
    { "path": "./apps/web" }
  ],
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

## Biome vs ESLint

### Use Biome when:

- Speed is critical (often faster than traditional setups)
- Want single tool for lint + format
- TypeScript-first project
- Okay with 64 TS rules vs 100+ in typescript-eslint

### Stay with ESLint when:

- Need specific rules/plugins
- Have complex custom rules
- Working with Vue/Angular (limited Biome support)
- Need type-aware linting (Biome doesn't have this yet)

## Quick Decision Trees

### "Which tool should I use?"

```
Type checking only? → tsc
Type checking + linting speed critical? → Biome
Type checking + comprehensive linting? → ESLint + typescript-eslint
Type testing? → Vitest expectTypeOf
Build tool? → Project size <10 packages? Turborepo. Else? Nx
```

### "How do I fix this performance issue?"

```
Slow type checking? → skipLibCheck, incremental, project references
Slow builds? → Check bundler config, enable caching
Slow tests? → Vitest with threads, avoid type checking in tests
Slow language server? → Exclude node_modules, limit files in tsconfig
```
