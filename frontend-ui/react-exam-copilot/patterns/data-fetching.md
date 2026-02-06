# Data Fetching Patterns

> Patrones para obtener, cachear y sincronizar datos

## Basic Fetch Hook

Implementación vanilla de data fetching.

```typescript
type FetchState<T> =
  | { status: "idle"; data: null; error: null }
  | { status: "loading"; data: null; error: null }
  | { status: "success"; data: T; error: null }
  | { status: "error"; data: null; error: Error };

function useFetch<T>(url: string): FetchState<T> & { refetch: () => void } {
  const [state, setState] = useState<FetchState<T>>({
    status: "idle",
    data: null,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState({ status: "loading", data: null, error: null });

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setState({ status: "success", data, error: null });
    } catch (error) {
      setState({ status: "error", data: null, error: error as Error });
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { ...state, refetch: fetchData };
}
```

## With Abort Controller

Cancelar requests cuando el componente se desmonta.

```typescript
function useFetchWithAbort<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        setIsLoading(true);
        const response = await fetch(url, { signal: controller.signal });
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();

    return () => controller.abort();
  }, [url]);

  return { data, error, isLoading };
}
```

## Paginated Data

Manejo de paginación.

```typescript
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

function usePaginatedData<T>(baseUrl: string, pageSize = 10) {
  const [page, setPage] = useState(1);
  const [allData, setAllData] = useState<T[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const url = `${baseUrl}?page=${page}&pageSize=${pageSize}`;

  useEffect(() => {
    async function fetchPage() {
      setIsLoading(true);
      const response = await fetch(url);
      const result: PaginatedResponse<T> = await response.json();

      setAllData((prev) => [...prev, ...result.data]);
      setHasMore(result.hasMore);
      setIsLoading(false);
    }

    fetchPage();
  }, [url]);

  const loadMore = () => {
    if (!isLoading && hasMore) {
      setPage((p) => p + 1);
    }
  };

  return { data: allData, isLoading, hasMore, loadMore };
}
```

## Infinite Scroll

Cargar más datos al hacer scroll.

```typescript
function useInfiniteScroll(
  loadMore: () => void,
  hasMore: boolean,
  isLoading: boolean
) {
  const observerRef = useRef<IntersectionObserver | null>(null);

  const lastElementRef = useCallback((node: HTMLElement | null) => {
    if (isLoading) return;

    if (observerRef.current) {
      observerRef.current.disconnect();
    }

    observerRef.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore) {
        loadMore();
      }
    });

    if (node) {
      observerRef.current.observe(node);
    }
  }, [isLoading, hasMore, loadMore]);

  return lastElementRef;
}

// Uso
function List() {
  const { data, isLoading, hasMore, loadMore } = usePaginatedData('/api/items');
  const lastRef = useInfiniteScroll(loadMore, hasMore, isLoading);

  return (
    <ul>
      {data.map((item, index) => (
        <li
          key={item.id}
          ref={index === data.length - 1 ? lastRef : null}
        >
          {item.name}
        </li>
      ))}
      {isLoading && <li>Loading...</li>}
    </ul>
  );
}
```

## Optimistic Updates

Actualizar UI antes de confirmar con servidor.

```typescript
function useOptimisticUpdate<T>(
  initialData: T,
  updateFn: (data: T) => Promise<T>,
) {
  const [data, setData] = useState(initialData);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const previousDataRef = useRef<T>(initialData);

  const update = async (newData: T) => {
    // Guardar estado anterior para rollback
    previousDataRef.current = data;

    // Actualización optimista
    setData(newData);
    setIsUpdating(true);
    setError(null);

    try {
      const confirmedData = await updateFn(newData);
      setData(confirmedData);
    } catch (err) {
      // Rollback on error
      setData(previousDataRef.current);
      setError(err as Error);
    } finally {
      setIsUpdating(false);
    }
  };

  return { data, update, isUpdating, error };
}
```

## Polling

Refetch periódico.

```typescript
function usePolling<T>(url: string, interval: number, enabled = true) {
  const [data, setData] = useState<T | null>(null);

  useEffect(() => {
    if (!enabled) return;

    const fetchData = async () => {
      const response = await fetch(url);
      const json = await response.json();
      setData(json);
    };

    fetchData(); // Initial fetch
    const id = setInterval(fetchData, interval);

    return () => clearInterval(id);
  }, [url, interval, enabled]);

  return data;
}

// Uso: polling cada 5 segundos
const notifications = usePolling("/api/notifications", 5000);
```
