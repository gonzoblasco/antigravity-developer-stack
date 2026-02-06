# README Template

> Template para documentar tu solución de challenge

````markdown
# [Nombre del Challenge]

> Breve descripción de lo que hace la aplicación

## Demo

[Link a demo desplegada si aplica]

![Screenshot](./screenshot.png)

## Stack

- React 18 + TypeScript
- [Estado]: Context / Zustand / Redux
- [Estilos]: CSS Modules / Tailwind / Styled Components
- [Testing]: Vitest + React Testing Library

## Cómo correr

​```bash

# Instalar dependencias

npm install

# Desarrollo

npm run dev

# Tests

npm run test

# Build

npm run build
​```

## Estructura del proyecto

​`
src/
├── components/     # Componentes reutilizables
├── features/       # Módulos por feature
├── hooks/          # Custom hooks
├── services/       # API calls
├── types/          # TypeScript types
└── utils/          # Helpers
​`

## Decisiones de arquitectura

### [Decisión 1: ej. State Management]

**Elegí:** Context + useReducer
**Razón:** La app es pequeña, no necesita estado global complejo
**Alternativa considerada:** Zustand - sería mi elección si creciera

### [Decisión 2: ej. Data Fetching]

**Elegí:** Custom hook con fetch
**Razón:** No quería agregar dependencias para un challenge simple
**Alternativa considerada:** React Query - lo usaría en producción

### [Decisión 3: ej. Estilos]

**Elegí:** CSS Modules
**Razón:** Scoping automático, sin configuración extra
**Alternativa considerada:** Tailwind - preferencia personal

## Trade-offs

| Trade-off             | Pro                | Contra                 |
| --------------------- | ------------------ | ---------------------- |
| Sin librería de forms | Menos dependencias | Más código boilerplate |
| Sin React Query       | Bundle más pequeño | Manejo manual de cache |

## Mejoras futuras

- [ ] Agregar más tests e2e
- [ ] Implementar lazy loading de rutas
- [ ] Agregar dark mode
- [ ] Internacionalización (i18n)

## Tiempo invertido

- Planificación: ~X min
- Implementación: ~X min
- Testing: ~X min
- Documentación: ~X min
- **Total:** ~X min
````
