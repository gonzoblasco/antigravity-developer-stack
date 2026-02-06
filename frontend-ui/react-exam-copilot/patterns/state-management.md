# State Management Patterns

> Patrones para manejar estado local, compartido y global

## Reducer Pattern

Estado complejo con acciones tipadas.

```typescript
// Tipos
type Todo = { id: string; text: string; completed: boolean };

type TodoAction =
  | { type: "ADD"; payload: { text: string } }
  | { type: "TOGGLE"; payload: { id: string } }
  | { type: "DELETE"; payload: { id: string } }
  | { type: "CLEAR_COMPLETED" };

// Reducer
function todoReducer(state: Todo[], action: TodoAction): Todo[] {
  switch (action.type) {
    case "ADD":
      return [
        ...state,
        {
          id: crypto.randomUUID(),
          text: action.payload.text,
          completed: false,
        },
      ];
    case "TOGGLE":
      return state.map((todo) =>
        todo.id === action.payload.id
          ? { ...todo, completed: !todo.completed }
          : todo,
      );
    case "DELETE":
      return state.filter((todo) => todo.id !== action.payload.id);
    case "CLEAR_COMPLETED":
      return state.filter((todo) => !todo.completed);
    default:
      return state;
  }
}

// Uso
const [todos, dispatch] = useReducer(todoReducer, []);
dispatch({ type: "ADD", payload: { text: "Learn React" } });
```

## Context + Reducer

Estado global tipado y escalable.

```typescript
// types.ts
interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'LOGOUT' };

// context.tsx
const AuthContext = createContext<{
  state: AuthState;
  dispatch: Dispatch<AuthAction>;
} | null>(null);

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { user: action.payload, isLoading: false, error: null };
    case 'LOGIN_ERROR':
      return { user: null, isLoading: false, error: action.payload };
    case 'LOGOUT':
      return { user: null, isLoading: false, error: null };
    default:
      return state;
  }
}

function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isLoading: false,
    error: null,
  });

  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

// Actions helper (opcional)
function useAuthActions() {
  const { dispatch } = useAuth();

  const login = async (credentials: Credentials) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const user = await api.login(credentials);
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR', payload: error.message });
    }
  };

  const logout = () => dispatch({ type: 'LOGOUT' });

  return { login, logout };
}
```

## State Machine Pattern

Para flujos con estados discretos.

```typescript
type FormStatus = "idle" | "validating" | "submitting" | "success" | "error";

interface FormState {
  status: FormStatus;
  values: Record<string, string>;
  errors: Record<string, string>;
  submitError: string | null;
}

type FormAction =
  | { type: "CHANGE"; field: string; value: string }
  | { type: "VALIDATE" }
  | { type: "VALIDATION_ERROR"; errors: Record<string, string> }
  | { type: "SUBMIT" }
  | { type: "SUBMIT_SUCCESS" }
  | { type: "SUBMIT_ERROR"; error: string };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case "CHANGE":
      // Solo permitido en 'idle' o 'error'
      if (state.status !== "idle" && state.status !== "error") return state;
      return {
        ...state,
        status: "idle",
        values: { ...state.values, [action.field]: action.value },
        errors: { ...state.errors, [action.field]: "" },
      };
    case "VALIDATE":
      return { ...state, status: "validating" };
    case "VALIDATION_ERROR":
      return { ...state, status: "error", errors: action.errors };
    case "SUBMIT":
      // Solo permitido después de validación exitosa
      if (state.status !== "validating") return state;
      return { ...state, status: "submitting" };
    case "SUBMIT_SUCCESS":
      return { ...state, status: "success" };
    case "SUBMIT_ERROR":
      return { ...state, status: "error", submitError: action.error };
    default:
      return state;
  }
}
```

## Derived State

Calcular valores derivados, no duplicar estado.

```typescript
// ❌ MAL: Estado duplicado
const [items, setItems] = useState<Item[]>([]);
const [filteredItems, setFilteredItems] = useState<Item[]>([]); // Duplicado!
const [totalPrice, setTotalPrice] = useState(0); // Duplicado!

// ✅ BIEN: Estado derivado
const [items, setItems] = useState<Item[]>([]);
const [filter, setFilter] = useState("");

// Derivados con useMemo si el cálculo es costoso
const filteredItems = useMemo(
  () => items.filter((item) => item.name.includes(filter)),
  [items, filter],
);

const totalPrice = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items],
);
```

## State Colocation

Mantener estado cerca de donde se usa.

```typescript
// ❌ MAL: Estado global innecesario
function App() {
  const [searchQuery, setSearchQuery] = useState(''); // ¿Por qué aquí?
  return <SearchPage query={searchQuery} onQueryChange={setSearchQuery} />;
}

// ✅ BIEN: Estado local
function SearchPage() {
  const [searchQuery, setSearchQuery] = useState(''); // Donde se usa
  return (
    <>
      <SearchInput value={searchQuery} onChange={setSearchQuery} />
      <SearchResults query={searchQuery} />
    </>
  );
}
```

## Lifting State Up

Cuando dos componentes necesitan compartir estado.

```typescript
// Antes: estados separados
function TemperatureInput({ scale }: { scale: 'C' | 'F' }) {
  const [temperature, setTemperature] = useState('');
  // No puede sincronizar con el otro input
}

// Después: estado elevado
function Calculator() {
  const [temperature, setTemperature] = useState('');
  const [scale, setScale] = useState<'C' | 'F'>('C');

  const celsius = scale === 'F' ? tryConvert(temperature, toCelsius) : temperature;
  const fahrenheit = scale === 'C' ? tryConvert(temperature, toFahrenheit) : temperature;

  return (
    <>
      <TemperatureInput
        scale="C"
        value={celsius}
        onChange={(value) => { setTemperature(value); setScale('C'); }}
      />
      <TemperatureInput
        scale="F"
        value={fahrenheit}
        onChange={(value) => { setTemperature(value); setScale('F'); }}
      />
    </>
  );
}
```
