# Fase 1: Redux Clásico → Redux Toolkit

> Guía detallada de migración con ejemplos completos

---

## 1. Configuración del Store

| Redux Clásico              | Redux Toolkit                |
| -------------------------- | ---------------------------- |
| `createStore()`            | `configureStore()`           |
| `combineReducers()` manual | Automático con `reducer: {}` |
| Middleware manual          | Incluye thunk y devtools     |
| `compose()` para devtools  | Automático                   |

### Migración del Store

```typescript
// ❌ ANTES (Redux Clásico)
import { createStore, combineReducers, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";

const rootReducer = combineReducers({
  users: usersReducer,
  products: productsReducer,
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(thunk)),
);

// ✅ DESPUÉS (Redux Toolkit)
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: {
    users: usersReducer,
    products: productsReducer,
  },
  // thunk ya incluido, devtools automático
});
```

---

## 2. Migración de Reducers a Slices

| Redux Clásico                 | Redux Toolkit                   |
| ----------------------------- | ------------------------------- |
| Action types como constantes  | Generados automáticamente       |
| Action creators manuales      | Generados por `createSlice()`   |
| Switch statements             | Object con case reducers        |
| Spread operator inmutabilidad | Immer (mutación directa segura) |

### Ejemplo Completo

```typescript
// ❌ ANTES (Redux Clásico)
// types.js
export const ADD_USER = "users/ADD_USER";
export const UPDATE_USER = "users/UPDATE_USER";
export const REMOVE_USER = "users/REMOVE_USER";

// actions.js
export const addUser = (user) => ({ type: ADD_USER, payload: user });
export const updateUser = (id, data) => ({
  type: UPDATE_USER,
  payload: { id, ...data },
});
export const removeUser = (id) => ({ type: REMOVE_USER, payload: id });

// reducer.js
const initialState = { users: [], loading: false };

export default function usersReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_USER:
      return { ...state, users: [...state.users, action.payload] };
    case UPDATE_USER:
      return {
        ...state,
        users: state.users.map((u) =>
          u.id === action.payload.id ? { ...u, ...action.payload } : u,
        ),
      };
    case REMOVE_USER:
      return {
        ...state,
        users: state.users.filter((u) => u.id !== action.payload),
      };
    default:
      return state;
  }
}

// ✅ DESPUÉS (Redux Toolkit)
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: string;
  name: string;
  email: string;
}

interface UsersState {
  users: User[];
  loading: boolean;
}

const initialState: UsersState = { users: [], loading: false };

const usersSlice = createSlice({
  name: "users",
  initialState,
  reducers: {
    addUser: (state, action: PayloadAction<User>) => {
      // ✅ Immer permite "mutación" segura
      state.users.push(action.payload);
    },
    updateUser: (
      state,
      action: PayloadAction<Partial<User> & { id: string }>,
    ) => {
      const user = state.users.find((u) => u.id === action.payload.id);
      if (user) {
        Object.assign(user, action.payload);
      }
    },
    removeUser: (state, action: PayloadAction<string>) => {
      state.users = state.users.filter((u) => u.id !== action.payload);
    },
  },
});

export const { addUser, updateUser, removeUser } = usersSlice.actions;
export default usersSlice.reducer;
```

---

## 3. Migración de Async Actions (Thunks)

| Redux Clásico                  | Redux Toolkit                      |
| ------------------------------ | ---------------------------------- |
| Thunks manuales                | `createAsyncThunk()`               |
| Manejo manual de loading/error | `extraReducers` automático         |
| Try/catch en cada thunk        | Estados pending/fulfilled/rejected |

### Ejemplo Completo

```typescript
// ❌ ANTES (Thunk manual)
export const fetchUsers = () => async (dispatch) => {
  dispatch({ type: "users/FETCH_START" });
  try {
    const response = await api.getUsers();
    dispatch({ type: "users/FETCH_SUCCESS", payload: response.data });
  } catch (error) {
    dispatch({ type: "users/FETCH_ERROR", payload: error.message });
  }
};

// ✅ DESPUÉS (createAsyncThunk)
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

export const fetchUsers = createAsyncThunk(
  "users/fetchUsers",
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.getUsers();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  },
);

const usersSlice = createSlice({
  name: "users",
  initialState: { users: [], loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});
```

---

## 4. Migración de Selectors

```typescript
// ❌ ANTES (Selector básico)
const getUsers = (state) => state.users.users;
const getLoading = (state) => state.users.loading;

// ✅ DESPUÉS (con reselect integrado)
import { createSelector } from "@reduxjs/toolkit";

const selectUsersState = (state: RootState) => state.users;

export const selectUsers = createSelector(
  selectUsersState,
  (usersState) => usersState.users,
);

export const selectActiveUsers = createSelector(selectUsers, (users) =>
  users.filter((u) => u.active),
);
```

---

## Checklist de Migración Redux → RTK

- [ ] Instalar `@reduxjs/toolkit`
- [ ] Convertir store con `configureStore()`
- [ ] Identificar primer slice a migrar
- [ ] Crear slice con `createSlice()`
- [ ] Migrar action types y creators
- [ ] Migrar reducer con sintaxis Immer
- [ ] Migrar thunks a `createAsyncThunk()`
- [ ] Migrar selectors con `createSelector()`
- [ ] Actualizar imports en componentes
- [ ] Ejecutar tests
- [ ] Repetir con siguiente slice
