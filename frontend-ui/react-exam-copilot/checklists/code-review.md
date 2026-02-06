# Code Review Checklist

## Architecture

- [ ] Componentes con responsabilidad única
- [ ] Separación clara: UI / lógica / data
- [ ] Custom hooks para lógica reutilizable
- [ ] Props interface bien definida
- [ ] Composición sobre herencia

## TypeScript

- [ ] Sin `any` (usar `unknown` si necesario)
- [ ] Tipos exportados para reutilización
- [ ] Generics donde aumenten flexibilidad
- [ ] Discriminated unions para estados
- [ ] `as const` para literales

```typescript
// ✅ Good: discriminated union
type State =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: User[] }
  | { status: "error"; error: Error };

// ❌ Bad: optional everything
type State = {
  status: string;
  data?: User[];
  error?: Error;
};
```

## Error Handling

- [ ] Error boundaries en secciones críticas
- [ ] try/catch en async operations
- [ ] Errores con mensajes útiles para usuarios
- [ ] Logging de errores para debugging

## Naming Conventions

- [ ] Componentes: PascalCase
- [ ] Hooks: use\* prefix
- [ ] Handlers: handle\* prefix
- [ ] Booleans: is*, has*, should\*
- [ ] Constants: UPPER_SNAKE_CASE

## Code Smells 🚩

```typescript
// ❌ Props drilling profundo
<A><B><C><D prop={x} /></C></B></A>
// ✅ Context o composition

// ❌ useEffect como "componentDidUpdate"
useEffect(() => { doSomething(); }, [dep1, dep2, dep3, dep4]);
// ✅ Revisar si es derived state o necesita refactor

// ❌ Index como key
{items.map((item, i) => <Item key={i} />)}
// ✅ ID estable
{items.map(item => <Item key={item.id} />)}

// ❌ Boolean props negadas
<Button notDisabled />
// ✅ Positivas
<Button enabled />
```

## Testing Readiness

- [ ] Funciones puras extraídas para unit tests
- [ ] Data-testid en elementos clave
- [ ] Estados fáciles de mockear
- [ ] Side effects aislados en hooks

## DX (Developer Experience)

- [ ] Imports ordenados y agrupados
- [ ] Archivos <300 líneas
- [ ] Funciones <50 líneas
- [ ] Comentarios solo donde el "por qué" no es obvio
- [ ] README con setup y decisiones

## Before Committing

1. `npm run lint` sin errores
2. `npm run typecheck` sin errores
3. `npm run test` pasando
4. Self-review del diff
5. Descripción clara del PR
