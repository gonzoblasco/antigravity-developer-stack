# Breaking Changes: React 16 → 19

Detalle de los principales cambios que rompen compatibilidad y cómo migrarlos.

## 1. JSX Transform (Obligatorio)

| Antes                                       | Después                          |
| ------------------------------------------- | -------------------------------- |
| `import React from 'react'` en cada archivo | Ya no necesario                  |
| Babel preset `@babel/preset-react` legacy   | Habilitar `runtime: 'automatic'` |

**Configuración Babel:**

```json
{
  "presets": [["@babel/preset-react", { "runtime": "automatic" }]]
}
```

## 2. PropTypes (Eliminado)

| React 16-18                   | React 19                    |
| ----------------------------- | --------------------------- |
| `Component.propTypes = {...}` | ❌ Silenciosamente ignorado |
| Validación en runtime         | Usar TypeScript             |

**Migración:**

```tsx
// ❌ ANTES (React 16)
import PropTypes from "prop-types";

function Button({ label, onClick }) {
  return <button onClick={onClick}>{label}</button>;
}
Button.propTypes = {
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func,
};

// ✅ DESPUÉS (React 19 + TypeScript)
interface ButtonProps {
  label: string;
  onClick?: () => void;
}

function Button({ label, onClick }: ButtonProps) {
  return <button onClick={onClick}>{label}</button>;
}
```

## 3. DefaultProps para Funciones (Eliminado)

| React 16-18                      | React 19                     |
| -------------------------------- | ---------------------------- |
| `Component.defaultProps = {...}` | ❌ No soportado en funciones |
| Class components                 | ✅ Sigue funcionando         |

**Migración:**

```tsx
// ❌ ANTES
function Greeting({ name }) {
  return <h1>Hello, {name}</h1>;
}
Greeting.defaultProps = { name: "Guest" };

// ✅ DESPUÉS (ES6 defaults)
function Greeting({ name = "Guest" }) {
  return <h1>Hello, {name}</h1>;
}
```

## 4. Refs como Props Regulares

| React 16-18               | React 19                    |
| ------------------------- | --------------------------- |
| `forwardRef()` requerido  | `ref` es prop normal        |
| `element.ref`             | ❌ Usar `element.props.ref` |
| String refs `ref="myRef"` | ❌ Eliminado completamente  |

**Migración String Refs:**

```tsx
// ❌ ANTES (String Refs - Legacy)
class MyComponent extends React.Component {
  componentDidMount() {
    this.refs.myInput.focus();
  }
  render() {
    return <input ref="myInput" />;
  }
}

// ✅ DESPUÉS (Callback Refs o createRef)
class MyComponent extends React.Component {
  inputRef = React.createRef();

  componentDidMount() {
    this.inputRef.current?.focus();
  }
  render() {
    return <input ref={this.inputRef} />;
  }
}
```

## 5. Context API Legacy (Eliminado)

| Eliminado           | Usar en cambio       |
| ------------------- | -------------------- |
| `contextTypes`      | `static contextType` |
| `getChildContext()` | `Context.Provider`   |
| `childContextTypes` | `useContext()` hook  |

**Migración:**

```tsx
// ❌ ANTES (Legacy Context)
class Parent extends React.Component {
  getChildContext() {
    return { theme: "dark" };
  }
}
Parent.childContextTypes = {
  theme: PropTypes.string,
};

// ✅ DESPUÉS (Modern Context)
const ThemeContext = React.createContext("light");

function Parent({ children }) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>;
}
```

## 6. ReactDOM.render (Deprecado)

| React 16-17          | React 18+               |
| -------------------- | ----------------------- |
| `ReactDOM.render()`  | `createRoot().render()` |
| `ReactDOM.hydrate()` | `hydrateRoot()`         |

**Migración:**

```tsx
// ❌ ANTES
import ReactDOM from "react-dom";
ReactDOM.render(<App />, document.getElementById("root"));

// ✅ DESPUÉS
import { createRoot } from "react-dom/client";
const root = createRoot(document.getElementById("root")!);
root.render(<App />);
```
