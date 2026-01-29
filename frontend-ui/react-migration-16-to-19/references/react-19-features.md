# React 19 Features & Error Handling

## Nuevos Hooks de React 19

| Hook             | Propósito                                   |
| ---------------- | ------------------------------------------- |
| `useActionState` | Estado de formularios/acciones              |
| `useOptimistic`  | Updates optimistas UI                       |
| `use`            | Leer recursos en render (promises, context) |
| `useFormStatus`  | Estado de form padre                        |

## Manejo de Errores

### Nuevas APIs

```tsx
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("root")!, {
  onUncaughtError: (error, errorInfo) => {
    // Errores no capturados por Error Boundaries
    console.error("Uncaught:", error, errorInfo.componentStack);
  },
  onCaughtError: (error, errorInfo) => {
    // Errores capturados por Error Boundaries
    console.error("Caught:", error, errorInfo.componentStack);
  },
});
```
