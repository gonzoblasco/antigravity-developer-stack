---
name: react-migration-16-to-19
description: Use cuando necesites migrar una aplicación de React 16/17/18 a React 19. Keywords: react migration, upgrade react, legacy react, react 19 upgrade.
---

# React Migration: 16 → 19

Guía de orquestación para migrar aplicaciones React legacy de forma segura e incremental.

> [!CAUTION]
> **IRON LAW**: NUNCA saltes directamente de v16 a v19. La migración DEBE ser secuencial: 16 → 17 → 18.3 → 19.

## Fase 1: Preparación (16 → 17)

El objetivo es habilitar el nuevo JSX transform y eliminar dependencias viejas.

1.  Actualizar `react` y `react-dom` a 17.x.
2.  Habilitar `runtime: 'automatic'` en Babel/TS.
3.  **Verificar**: Tests deben pasar.

## Fase 2: Concurrent Mode Ready (17 → 18.3)

Preparar la app para concurrencia y limpiar APIs deprecadas.

1.  Actualizar a **React 18.3** (versión puente con warnings críticos).
2.  Migrar `ReactDOM.render` a `createRoot`.
3.  Resolver TODOS los warnings de consola.

> [!TIP]
> Usa [Detection Patterns](references/detection-patterns.md) para encontrar código legacy con grep.

## Fase 3: Limpieza de APIs Legacy

Antes de pasar a v19, debes eliminar APIs que dejarán de existir.

Consulta [Breaking Changes Reference](references/breaking-changes.md) para detalles de migración en:

- PropTypes (Eliminado)
- DefaultProps en funciones (Eliminado)
- String Refs (Eliminado)
- Legacy Context (Eliminado)

## Fase 4: React 19 Upgrade

Finalmente, actualiza a la versión estable.

1.  Actualizar paquetes a v19.
2.  Ejecutar codemods oficiales.
3.  Implementar nuevo manejo de errores si es necesario.

Ver [React 19 Features](references/react-19-features.md) para nuevas capacidades como `useActionState` y `useOptimistic`.

## Verificación Final

- [ ] **Unit Tests**: Sin regresiones.
- [ ] **Console**: Libre de warnings.
- [ ] **Build**: Producción compila sin errores.

---

**Recursos:**

- [Breaking Changes Detallados](references/breaking-changes.md)
- [Patrones de Búsqueda (Grep)](references/detection-patterns.md)
- [Nuevas Features React 19](references/react-19-features.md)
