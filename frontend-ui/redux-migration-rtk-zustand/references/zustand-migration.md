# Fase 2: Redux Toolkit → Zustand

> Guía detallada de migración con ejemplos completos

---

## 1. ¿Por qué migrar de RTK a Zustand?

| Aspecto           | RTK                      | Zustand             |
| ----------------- | ------------------------ | ------------------- |
| Boilerplate       | Reducido pero existe     | Mínimo              |
| Bundle size       | ~11kb (sin RTK Query)    | ~1.2kb              |
| Provider          | Requerido (`<Provider>`) | No necesario        |
| DevTools          | Integrado                | Middleware opcional |
| Curva aprendizaje | Media                    | Baja                |
| TypeScript        | Bueno                    | Excelente           |
| Server components | Complejo                 | Simple              |

---

## 2. Migración de Store

```typescript
// ❌ ANTES (RTK)
// store.ts
import { configureStore } from '@reduxjs/toolkit';
import usersReducer from './usersSlice';

export const store = configureStore({
  reducer: {
    users: usersReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// App.tsx - Requiere Provider
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <MyComponent />
    </Provider>
  );
}

// ✅ DESPUÉS (Zustand)
// store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UsersStore {
  users: User[];
  loading: boolean;
  error: string | null;

  // Actions integradas en el store
  addUser: (user: User) => void;
  updateUser: (id: string, data: Partial<User>) => void;
  removeUser: (id: string) => void;
  fetchUsers: () => Promise<void>;
}

export const useUsersStore = create<UsersStore>()(
  devtools(
    persist(
      (set, get) => ({
        users: [],
        loading: false,
        error: null,

        addUser: (user) => set(
          (state) => ({ users: [...state.users, user] }),
          false,
          'addUser'
        ),

        updateUser: (id, data) => set(
          (state) => ({
            users: state.users.map(u =>
              u.id === id ? { ...u, ...data } : u
            ),
          }),
          false,
          'updateUser'
        ),

        removeUser: (id) => set(
          (state) => ({ users: state.users.filter(u => u.id !== id) }),
          false,
          'removeUser'
        ),

        fetchUsers: async () => {
          set({ loading: true, error: null }, false, 'fetchUsers/pending');
          try {
            const response = await api.getUsers();
            set({ users: response.data, loading: false }, false, 'fetchUsers/fulfilled');
          } catch (error) {
            set({
              error: error instanceof Error ? error.message : 'Error',
              loading: false
            }, false, 'fetchUsers/rejected');
          }
        },
      }),
      { name: 'users-storage' }
    ),
    { name: 'UsersStore' }
  )
);

// App.tsx - NO requiere Provider
function App() {
  return <MyComponent />; // ✅ Sin Provider wrapper
}
```

---

## 3. Migración de Hooks

```typescript
// ❌ ANTES (RTK)
import { useSelector, useDispatch } from 'react-redux';
import { selectUsers, selectLoading } from './usersSlice';
import { addUser, fetchUsers } from './usersSlice';

function UsersList() {
  const dispatch = useDispatch();
  const users = useSelector(selectUsers);
  const loading = useSelector(selectLoading);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  const handleAdd = (user: User) => {
    dispatch(addUser(user));
  };

  return (/* ... */);
}

// ✅ DESPUÉS (Zustand)
import { useUsersStore } from './store';

function UsersList() {
  // Selector con shallow comparison para optimizar re-renders
  const { users, loading, fetchUsers, addUser } = useUsersStore(
    (state) => ({
      users: state.users,
      loading: state.loading,
      fetchUsers: state.fetchUsers,
      addUser: state.addUser,
    })
  );

  // O selectores individuales (más eficiente)
  const users = useUsersStore((state) => state.users);
  const loading = useUsersStore((state) => state.loading);
  const addUser = useUsersStore((state) => state.addUser);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return (/* ... */);
}
```

---

## 4. Patrón de Slices en Zustand

Para stores grandes, usar slices:

```typescript
// slices/usersSlice.ts
import { StateCreator } from "zustand";

export interface UsersSlice {
  users: User[];
  addUser: (user: User) => void;
  removeUser: (id: string) => void;
}

export const createUsersSlice: StateCreator<
  UsersSlice & ProductsSlice, // Combinar con otros slices
  [],
  [],
  UsersSlice
> = (set) => ({
  users: [],
  addUser: (user) => set((state) => ({ users: [...state.users, user] })),
  removeUser: (id) =>
    set((state) => ({ users: state.users.filter((u) => u.id !== id) })),
});

// slices/productsSlice.ts
export interface ProductsSlice {
  products: Product[];
  addProduct: (product: Product) => void;
}

export const createProductsSlice: StateCreator<
  UsersSlice & ProductsSlice,
  [],
  [],
  ProductsSlice
> = (set) => ({
  products: [],
  addProduct: (product) =>
    set((state) => ({ products: [...state.products, product] })),
});

// store.ts
import { create } from "zustand";
import { createUsersSlice, UsersSlice } from "./slices/usersSlice";
import { createProductsSlice, ProductsSlice } from "./slices/productsSlice";

type StoreState = UsersSlice & ProductsSlice;

export const useStore = create<StoreState>()((...a) => ({
  ...createUsersSlice(...a),
  ...createProductsSlice(...a),
}));
```

---

## 5. RTK Query vs React Query + Zustand

| RTK Query                  | React Query + Zustand       |
| -------------------------- | --------------------------- |
| Todo en Redux              | Data fetching separado      |
| Cache integrado            | React Query cache + Zustand |
| Más boilerplate            | Separación de concerns      |
| Mejor para Redux existente | Mejor para proyectos nuevos |

**Recomendación**: Si usas RTK Query, considera migrar a **React Query + Zustand**. React Query maneja data fetching, Zustand maneja UI state.

---

## 6. Server Components (Next.js 13+)

```typescript
// Zustand es más simple con Server Components
// store.ts
import { create } from "zustand";

// Para SSR, usar createStore por request
import { createStore } from "zustand/vanilla";

const createUserStore = () =>
  createStore<UsersStore>((set) => ({
    // ...
  }));

// En Server Component
const store = createUserStore();
```

---

## 7. Rollback Strategy

Mantener compatibilidad durante la migración:

```typescript
// bridge.ts - Usar ambos stores temporalmente
import { useSelector } from "react-redux";
import { useUsersStore } from "./zustandStore";

// Hook de transición
export function useUsers() {
  const USE_ZUSTAND = process.env.NEXT_PUBLIC_USE_ZUSTAND === "true";

  const reduxUsers = useSelector((s) => s.users.users);
  const zustandUsers = useUsersStore((s) => s.users);

  return USE_ZUSTAND ? zustandUsers : reduxUsers;
}
```

---

## Checklist de Migración RTK → Zustand

- [ ] Instalar `zustand`
- [ ] Crear store Zustand equivalente
- [ ] Migrar estado y acciones
- [ ] Configurar middleware (devtools, persist)
- [ ] Crear custom hooks si necesario
- [ ] Actualizar componentes (eliminar useDispatch/useSelector)
- [ ] Eliminar Provider cuando todo esté migrado
- [ ] Ejecutar tests
- [ ] Eliminar dependencias RTK cuando esté completo
