# Ejemplo Real: Migración E-commerce App

> Caso práctico completo de migración Redux → RTK → Zustand

---

## Contexto del Proyecto

**Stack inicial:**

- React 17
- Redux clásico (createStore)
- Redux Thunk
- 5 slices: auth, cart, products, orders, ui

**Problemas:**

- Bundle size: 45kb solo para state management
- Boilerplate excesivo: ~200 líneas por feature
- Bugs frecuentes por inmutabilidad manual

---

## Fase 1: Redux → RTK (Semana 1-2)

### Día 1: Setup y Primer Slice

```bash
# Instalar RTK
npm install @reduxjs/toolkit

# Detectar código legacy
grep -r "createStore" --include="*.ts" src/
```

### Día 2-3: Migrar Auth Slice

**Antes (auth/types.ts + actions.ts + reducer.ts = 89 líneas):**

```typescript
// types.ts
export const LOGIN_REQUEST = "auth/LOGIN_REQUEST";
export const LOGIN_SUCCESS = "auth/LOGIN_SUCCESS";
export const LOGIN_FAILURE = "auth/LOGIN_FAILURE";
export const LOGOUT = "auth/LOGOUT";

// actions.ts
export const loginRequest = () => ({ type: LOGIN_REQUEST });
export const loginSuccess = (user) => ({ type: LOGIN_SUCCESS, payload: user });
export const loginFailure = (error) => ({
  type: LOGIN_FAILURE,
  payload: error,
});
export const logout = () => ({ type: LOGOUT });

export const login = (credentials) => async (dispatch) => {
  dispatch(loginRequest());
  try {
    const user = await api.login(credentials);
    dispatch(loginSuccess(user));
  } catch (error) {
    dispatch(loginFailure(error.message));
  }
};

// reducer.ts
const initialState = { user: null, loading: false, error: null };

export default function authReducer(state = initialState, action) {
  switch (action.type) {
    case LOGIN_REQUEST:
      return { ...state, loading: true, error: null };
    case LOGIN_SUCCESS:
      return { ...state, loading: false, user: action.payload };
    case LOGIN_FAILURE:
      return { ...state, loading: false, error: action.payload };
    case LOGOUT:
      return initialState;
    default:
      return state;
  }
}
```

**Después (authSlice.ts = 35 líneas):**

```typescript
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

export const login = createAsyncThunk(
  "auth/login",
  async (credentials: Credentials, { rejectWithValue }) => {
    try {
      return await api.login(credentials);
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState: { user: null, loading: false, error: null } as AuthState,
  reducers: {
    logout: () => ({ user: null, loading: false, error: null }),
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
```

**Resultado: -60% líneas, +100% type safety**

### Día 4-7: Migrar Remaining Slices

- cart → cartSlice ✅
- products → productsSlice ✅
- orders → ordersSlice ✅
- ui → uiSlice ✅

### Día 8-10: Testing y Cleanup

```bash
# Verificar no quedan patterns legacy
grep -r "createStore\|combineReducers" src/
# Resultado esperado: 0 matches

# Correr test suite
npm test
```

---

## Fase 2: RTK → Zustand (Semana 3-4)

### Por qué migrar

| Métrica        | Con RTK | Con Zustand |
| -------------- | ------- | ----------- |
| Bundle size    | 18kb    | 4kb         |
| Líneas totales | 450     | 180         |
| Providers      | 1       | 0           |

### Slice por Slice

**Migrar UI primero (menos crítico):**

```typescript
// ❌ ANTES: uiSlice.ts (RTK)
import { createSlice } from "@reduxjs/toolkit";

const uiSlice = createSlice({
  name: "ui",
  initialState: { sidebarOpen: false, theme: "light" },
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setTheme: (state, action) => {
      state.theme = action.payload;
    },
  },
});

// ✅ DESPUÉS: useUIStore.ts (Zustand)
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UIStore {
  sidebarOpen: boolean;
  theme: "light" | "dark";
  toggleSidebar: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen: false,
      theme: "light",
      toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
    }),
    { name: "ui-storage" },
  ),
);
```

**Actualizar componentes:**

```tsx
// ❌ ANTES
import { useSelector, useDispatch } from "react-redux";
import { toggleSidebar } from "./uiSlice";

function Header() {
  const dispatch = useDispatch();
  const sidebarOpen = useSelector((s) => s.ui.sidebarOpen);

  return <button onClick={() => dispatch(toggleSidebar())}>Menu</button>;
}

// ✅ DESPUÉS
import { useUIStore } from "./useUIStore";

function Header() {
  const { sidebarOpen, toggleSidebar } = useUIStore();

  return <button onClick={toggleSidebar}>Menu</button>;
}
```

---

## Resultados Finales

| Métrica       | Antes | Después | Mejora |
| ------------- | ----- | ------- | ------ |
| Bundle size   | 45kb  | 4kb     | -91%   |
| Líneas código | 1200  | 280     | -77%   |
| Archivos      | 25    | 8       | -68%   |
| Providers     | 1     | 0       | -100%  |
| Tiempo render | 45ms  | 28ms    | -38%   |

---

## Lecciones Aprendidas

1. **Migrar slice por slice** - Nunca todo de una vez
2. **Empezar por el menos crítico** - UI antes que Auth
3. **Mantener tests pasando** - Después de cada slice
4. **Feature flags** - Para rollback rápido
5. **Documentar el mapeo** - Actions viejas → nuevas

---

## Timeline Real

```
Semana 1: RTK setup + 2 slices
Semana 2: 3 slices restantes + testing
Semana 3: Zustand UI + Cart
Semana 4: Auth + Products + Orders + cleanup
```

Total: **4 semanas, 0 downtime, 0 bugs en producción**
