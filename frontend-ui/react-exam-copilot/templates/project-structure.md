# Project Structure Template

> Estructuras de carpetas recomendadas según complejidad

## Small Challenge (< 5 componentes)

```
src/
├── components/
│   ├── Button.tsx
│   ├── Card.tsx
│   └── index.ts
├── hooks/
│   └── useDebounce.ts
├── types/
│   └── index.ts
├── App.tsx
├── App.css
└── main.tsx
```

## Medium Challenge (5-15 componentes)

```
src/
├── components/           # Componentes UI reutilizables
│   ├── ui/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.module.css
│   │   │   └── index.ts
│   │   └── Input/
│   └── layout/
│       ├── Header.tsx
│       └── Footer.tsx
│
├── features/             # Módulos por feature
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── index.ts
│   └── products/
│       ├── components/
│       ├── hooks/
│       └── index.ts
│
├── hooks/                # Hooks globales
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
│
├── services/             # API y servicios externos
│   ├── api.ts
│   └── auth.ts
│
├── types/                # Types globales
│   └── index.ts
│
├── utils/                # Funciones helper
│   └── formatters.ts
│
├── App.tsx
└── main.tsx
```

## Large Challenge (con routing)

```
src/
├── app/                  # Setup de app
│   ├── App.tsx
│   ├── providers.tsx     # Todos los providers
│   └── router.tsx        # Configuración de rutas
│
├── components/           # Componentes compartidos
│   ├── ui/               # Primitivos de UI
│   ├── layout/           # Layout components
│   └── common/           # Otros compartidos
│
├── features/             # Feature modules (auto-contenidos)
│   ├── auth/
│   │   ├── api/          # API calls del feature
│   │   ├── components/   # Componentes del feature
│   │   ├── hooks/        # Hooks del feature
│   │   ├── types/        # Types del feature
│   │   └── index.ts      # Exports públicos
│   │
│   └── dashboard/
│       └── ...
│
├── pages/                # Page components (solo routing)
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   └── DashboardPage.tsx
│
├── hooks/                # Hooks globales
├── services/             # Servicios globales
├── stores/               # Estado global (si aplica)
├── types/                # Types globales
├── utils/                # Utilidades
│
└── main.tsx
```

## Convenciones de Archivos

```typescript
// Component file: PascalCase
Button.tsx;
UserProfile.tsx;

// Hook file: camelCase con "use" prefix
useDebounce.ts;
useAuth.ts;

// Utility file: camelCase
formatDate.ts;
validators.ts;

// Type file: camelCase o PascalCase según contenido
types.ts; // Múltiples types
User.ts; // Un type principal

// Test file: mismo nombre + .test
Button.test.tsx;
useDebounce.test.ts;

// Style file: mismo nombre + .module.css
Button.module.css;
```

## Index Files (Barrel Exports)

```typescript
// components/ui/index.ts
export { Button } from "./Button";
export { Input } from "./Input";
export { Card } from "./Card";

// Uso
import { Button, Input, Card } from "@/components/ui";
```

## Paths Aliases (tsconfig.json)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/features/*": ["src/features/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/utils/*": ["src/utils/*"]
    }
  }
}
```
