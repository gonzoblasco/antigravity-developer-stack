# Performance Checklist

## Rendering Optimization

- [ ] `React.memo` en componentes que reciben props estables
- [ ] `useMemo` para cálculos costosos
- [ ] `useCallback` para funciones pasadas a children memorizados
- [ ] Keys estables y únicas en listas
- [ ] Evitar objetos/arrays inline en props

## State Management

- [ ] Estado lo más cerca posible de donde se usa
- [ ] Contextos separados por dominio (evitar re-renders globales)
- [ ] State splitting cuando parte del estado cambia frecuentemente

## Data Fetching

- [ ] Caching de requests (React Query, SWR)
- [ ] Deduplicación de requests idénticos
- [ ] Prefetching de datos predecibles
- [ ] Pagination/infinite scroll para listas largas

## Code Splitting

```typescript
// Lazy loading de rutas
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Con fallback
<Suspense fallback={<Skeleton />}>
  <Dashboard />
</Suspense>
```

## Bundle Optimization

- [ ] Tree shaking funcionando (imports específicos)
- [ ] Dynamic imports para código no crítico
- [ ] Análisis de bundle size (`webpack-bundle-analyzer`)
- [ ] Dependencias pesadas evaluadas

## Images & Assets

- [ ] Lazy loading de imágenes (`loading="lazy"`)
- [ ] Formatos modernos (WebP, AVIF)
- [ ] Tamaños responsivos (`srcset`)
- [ ] Sprites/inline SVG para iconos

## Lists & Tables

- [ ] Virtualización para >100 items (`react-window`, `react-virtual`)
- [ ] Pagination server-side cuando posible
- [ ] Skeleton loaders durante fetch

## Measuring

```typescript
// React DevTools Profiler
// Performance tab Chrome DevTools
// Lighthouse Performance audit

// Custom profiling
const ProfiledComponent = React.memo(function Component() {
  useEffect(() => {
    performance.mark("component-mounted");
  }, []);
});
```

## Red Flags 🚩

- Re-renders en cada keystroke
- Listas largas sin virtualización
- Fetching en cada render
- Context que cambia muy frecuentemente
- Bundle >500KB inicial
