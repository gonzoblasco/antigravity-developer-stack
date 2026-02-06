# Error Handling Patterns

> Patrones para manejar errores de forma robusta

## Error Boundary Class

Capturar errores en el árbol de componentes.

```typescript
interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log a servicio de errores
    console.error('Error caught:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}

// Fallback UI
function ErrorFallback({ error }: { error: Error | null }) {
  return (
    <div role="alert" className="error-fallback">
      <h2>Something went wrong</h2>
      {error && <pre>{error.message}</pre>}
      <button onClick={() => window.location.reload()}>
        Reload page
      </button>
    </div>
  );
}
```

## Error Boundary with Reset

Permitir retry sin recargar página.

```typescript
interface ErrorBoundaryWithResetProps {
  children: ReactNode;
  resetKeys?: unknown[];
}

class ErrorBoundaryWithReset extends Component<
  ErrorBoundaryWithResetProps,
  State
> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidUpdate(prevProps: ErrorBoundaryWithResetProps) {
    // Reset cuando cambian las keys
    if (
      this.state.hasError &&
      !shallowEqual(prevProps.resetKeys, this.props.resetKeys)
    ) {
      this.setState({ hasError: false, error: null });
    }
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallbackWithRetry
          error={this.state.error}
          onRetry={this.reset}
        />
      );
    }
    return this.props.children;
  }
}

// Uso
<ErrorBoundaryWithReset resetKeys={[userId]}>
  <UserProfile userId={userId} />
</ErrorBoundaryWithReset>
```

## Async Error Handling

Manejar errores en operaciones async.

```typescript
// Hook para manejar errores async
function useAsyncError() {
  const [, setError] = useState();

  return useCallback((error: Error) => {
    setError(() => {
      throw error; // Esto dispara el Error Boundary
    });
  }, []);
}

// Uso en componente
function DataComponent() {
  const throwError = useAsyncError();

  useEffect(() => {
    fetchData().then(setData).catch(throwError); // Propaga al Error Boundary
  }, []);
}
```

## Try-Catch Wrapper

Utility para async/await.

```typescript
type Result<T> =
  | { success: true; data: T; error: null }
  | { success: false; data: null; error: Error };

async function tryCatch<T>(promise: Promise<T>): Promise<Result<T>> {
  try {
    const data = await promise;
    return { success: true, data, error: null };
  } catch (error) {
    return { success: false, data: null, error: error as Error };
  }
}

// Uso
const result = await tryCatch(api.createUser(data));
if (!result.success) {
  console.error(result.error);
  return;
}
console.log(result.data);
```

## HTTP Error Handling

Wrapper para fetch con manejo de errores.

```typescript
class HttpError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data?: unknown,
  ) {
    super(`HTTP ${status}: ${statusText}`);
    this.name = "HttpError";
  }
}

async function fetchWithErrorHandling<T>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(url, options);

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new HttpError(response.status, response.statusText, data);
  }

  return response.json();
}

// Uso
try {
  const user = await fetchWithErrorHandling<User>("/api/user");
} catch (error) {
  if (error instanceof HttpError) {
    if (error.status === 401) {
      redirect("/login");
    } else if (error.status === 404) {
      setNotFound(true);
    }
  }
}
```

## Form Error Display Pattern

```typescript
function FormField({
  name,
  error,
  children
}: {
  name: string;
  error?: string;
  children: ReactNode;
}) {
  const errorId = `${name}-error`;

  return (
    <div className="form-field">
      {children}
      {error && (
        <span
          id={errorId}
          role="alert"
          className="error-message"
        >
          {error}
        </span>
      )}
    </div>
  );
}

// Uso con aria-describedby
<FormField name="email" error={errors.email}>
  <input
    name="email"
    aria-describedby={errors.email ? 'email-error' : undefined}
    aria-invalid={!!errors.email}
  />
</FormField>
```

## Toast/Notification Pattern

```typescript
interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
}

const ToastContext = createContext<{
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
} | null>(null);

function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = crypto.randomUUID();
    setToasts(prev => [...prev, { ...toast, id }]);

    // Auto-remove after 5s
    setTimeout(() => removeToast(id), 5000);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  );
}
```
