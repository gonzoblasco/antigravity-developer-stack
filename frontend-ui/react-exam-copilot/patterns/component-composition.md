# Component Composition Patterns

> Patrones avanzados para componentes flexibles y reutilizables

## Compound Components

Componentes que trabajan juntos compartiendo estado implícito.

```typescript
// context interno
const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (tab: string) => void;
} | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) throw new Error('useTabs must be used within Tabs');
  return context;
}

// Componente padre
function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-componentes
Tabs.List = function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
};

// Uso
<Tabs defaultTab="tab1">
  <Tabs.List>
    <Tabs.Tab id="tab1">First</Tabs.Tab>
    <Tabs.Tab id="tab2">Second</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="tab1">Content 1</Tabs.Panel>
  <Tabs.Panel id="tab2">Content 2</Tabs.Panel>
</Tabs>
```

## Render Props

Compartir lógica via función como children.

```typescript
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({
  children
}: {
  children: (position: MousePosition) => ReactNode
}) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return <>{children(position)}</>;
}

// Uso
<MouseTracker>
  {({ x, y }) => <div>Mouse at: {x}, {y}</div>}
</MouseTracker>
```

## Controlled vs Uncontrolled

Patrón para componentes que pueden ser ambos.

```typescript
interface InputProps {
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
}

function Input({ value, defaultValue = '', onChange }: InputProps) {
  // Estado interno solo si no es controlado
  const [internalValue, setInternalValue] = useState(defaultValue);

  // Determinar si es controlado
  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }
    onChange?.(newValue);
  };

  return <input value={currentValue} onChange={handleChange} />;
}

// Uso controlado
<Input value={name} onChange={setName} />

// Uso no controlado
<Input defaultValue="initial" onChange={console.log} />
```

## Slots Pattern

Componentes con "ranuras" para contenido personalizado.

```typescript
interface CardProps {
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
}

function Card({ children, header, footer }: CardProps) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Uso
<Card
  header={<h2>Title</h2>}
  footer={<button>Submit</button>}
>
  Main content here
</Card>
```

## Polymorphic Components

Componentes que cambian su elemento base.

```typescript
type PolymorphicProps<E extends ElementType> = {
  as?: E;
  children: ReactNode;
} & ComponentPropsWithoutRef<E>;

function Box<E extends ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Uso
<Box>Default div</Box>
<Box as="section">As section</Box>
<Box as="a" href="/home">As link</Box>
<Box as={Link} to="/about">As React Router Link</Box>
```

## Provider Pattern

Encapsular providers múltiples.

```typescript
function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <ToastProvider>
            {children}
          </ToastProvider>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

// En App.tsx
function App() {
  return (
    <AppProviders>
      <Router />
    </AppProviders>
  );
}
```
