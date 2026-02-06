# Custom Hooks Patterns

> Patrones para extraer y reutilizar lógica con custom hooks

## useDebounce

Debounce de valores para búsquedas, inputs, etc.

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Uso
const searchTerm = useDebounce(inputValue, 300);
```

## useLocalStorage

Persistir estado en localStorage con sync automático.

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error("Error saving to localStorage:", error);
    }
  };

  return [storedValue, setValue] as const;
}
```

## useToggle

Boolean toggle simple.

```typescript
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
}

// Uso
const modal = useToggle();
<button onClick={modal.toggle}>Toggle</button>
{modal.value && <Modal onClose={modal.setFalse} />}
```

## usePrevious

Acceder al valor anterior de una variable.

```typescript
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Uso: detectar cambios
const prevCount = usePrevious(count);
if (prevCount !== undefined && prevCount !== count) {
  console.log(`Changed from ${prevCount} to ${count}`);
}
```

## useOnClickOutside

Detectar clicks fuera de un elemento (dropdowns, modals).

```typescript
function useOnClickOutside<T extends HTMLElement>(
  ref: RefObject<T>,
  handler: (event: MouseEvent | TouchEvent) => void,
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      handler(event);
    };

    document.addEventListener("mousedown", listener);
    document.addEventListener("touchstart", listener);

    return () => {
      document.removeEventListener("mousedown", listener);
      document.removeEventListener("touchstart", listener);
    };
  }, [ref, handler]);
}
```

## useMediaQuery

Responsive design con hooks.

```typescript
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(
    () => window.matchMedia(query).matches,
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handler = (event: MediaQueryListEvent) => setMatches(event.matches);

    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

// Uso
const isMobile = useMediaQuery("(max-width: 768px)");
```

## useAsync

Manejo genérico de operaciones async.

```typescript
type AsyncState<T> =
  | { status: "idle"; data: null; error: null }
  | { status: "pending"; data: null; error: null }
  | { status: "success"; data: T; error: null }
  | { status: "error"; data: null; error: Error };

function useAsync<T>(asyncFn: () => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    status: "idle",
    data: null,
    error: null,
  });

  useEffect(() => {
    setState({ status: "pending", data: null, error: null });

    asyncFn()
      .then((data) => setState({ status: "success", data, error: null }))
      .catch((error) => setState({ status: "error", data: null, error }));
  }, deps);

  return state;
}
```
