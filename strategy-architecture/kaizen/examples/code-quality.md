# Kaizen Code Examples

This reference documents the code patterns (Good vs Bad) for the Kaizen skill.

## 1. Continuous Improvement (Iterative Refinement)

### <Good> Iterative Approach

```typescript
// Iteration 1: Make it work
const calculateTotal = (items: Item[]) => {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
};

// Iteration 2: Make it clear (refactor)
const calculateTotal = (items: Item[]): number => {
  return items.reduce((total, item) => {
    return total + item.price * item.quantity;
  }, 0);
};

// Iteration 3: Make it robust (add validation)
const calculateTotal = (items: Item[]): number => {
  if (!items?.length) return 0;

  return items.reduce((total, item) => {
    if (item.price < 0 || item.quantity < 0) {
      throw new Error("Price and quantity must be non-negative");
    }
    return total + item.price * item.quantity;
  }, 0);
};
```

Each step is complete, tested, and working.

### <Bad> Big Bang Approach

```typescript
// Trying to do everything at once
const calculateTotal = (items: Item[]): number => {
  // Validate, optimize, add features, handle edge cases all together
  if (!items?.length) return 0;
  const validItems = items.filter(item => {
    if (item.price < 0) throw new Error('Negative price');
    if (item.quantity < 0) throw new Error('Negative quantity');
    return item.quantity > 0; // Also filtering zero quantities
  });
  // Plus caching, plus logging, plus currency conversion...
  return validItems.reduce(...); // Too many concerns at once
};
```

Overwhelming, error-prone, hard to verify.

## 2. Poka-Yoke (Error Proofing)

### Type System Error Proofing

<Good>
```typescript
// Error: string status can be any value
type OrderBad = {
  status: string; // Can be "pending", "PENDING", "pnding", anything!
  total: number;
};

// Good: Only valid states possible
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
status: OrderStatus;
total: number;
};

// Better: States with associated data
type Order =
| { status: 'pending'; createdAt: Date }
| { status: 'processing'; startedAt: Date; estimatedCompletion: Date }
| { status: 'shipped'; trackingNumber: string; shippedAt: Date }
| { status: 'delivered'; deliveredAt: Date; signature: string };

// Now impossible to have shipped without trackingNumber

````
</Good>

<Good>
```typescript
// Make invalid states unrepresentable
type NonEmptyArray<T> = [T, ...T[]];

const firstItem = <T>(items: NonEmptyArray<T>): T => {
  return items[0]; // Always safe, never undefined!
};

// Caller must prove array is non-empty
const items: number[] = [1, 2, 3];
if (items.length > 0) {
  firstItem(items as NonEmptyArray<number>); // Safe
}
````

</Good>

### Validation Error Proofing

<Good>
```typescript
// Error: Validation after use
const processPayment = (amount: number) => {
  const fee = amount * 0.03; // Used before validation!
  if (amount <= 0) throw new Error('Invalid amount');
  // ...
};

// Good: Validate immediately
const processPayment = (amount: number) => {
if (amount <= 0) {
throw new Error('Payment amount must be positive');
}
if (amount > 10000) {
throw new Error('Payment exceeds maximum allowed');
}

const fee = amount \* 0.03;
// ... now safe to use
};

// Better: Validation at boundary with branded type
type PositiveNumber = number & { readonly \_\_brand: 'PositiveNumber' };

const validatePositive = (n: number): PositiveNumber => {
if (n <= 0) throw new Error('Must be positive');
return n as PositiveNumber;
};

const processPayment = (amount: PositiveNumber) => {
// amount is guaranteed positive, no need to check
const fee = amount \* 0.03;
};

// Validate at system boundary
const handlePaymentRequest = (req: Request) => {
const amount = validatePositive(req.body.amount); // Validate once
processPayment(amount); // Use everywhere safely
};

````
</Good>

### Guards and Preconditions
<Good>
```typescript
// Early returns prevent deeply nested code
const processUser = (user: User | null) => {
  if (!user) {
    logger.error('User not found');
    return;
  }

  if (!user.email) {
    logger.error('User email missing');
    return;
  }

  if (!user.isActive) {
    logger.info('User inactive, skipping');
    return;
  }

  // Main logic here, guaranteed user is valid and active
  sendEmail(user.email, 'Welcome!');
};
````

</Good>

### Configuration Error Proofing

<Good>
```typescript
// Error: Optional config with unsafe defaults
type ConfigBad = {
  apiKey?: string;
  timeout?: number;
};

const client = new APIClient({ timeout: 5000 }); // apiKey missing!

// Good: Required config, fails early
type Config = {
apiKey: string;
timeout: number;
};

const loadConfig = (): Config => {
const apiKey = process.env.API_KEY;
if (!apiKey) {
throw new Error('API_KEY environment variable required');
}

return {
apiKey,
timeout: 5000,
};
};

// App fails at startup if config invalid, not during request
const config = loadConfig();
const client = new APIClient(config);

````
</Good>

## 3. Standardized Work

### Following Patterns
<Good>
```typescript
// Existing codebase pattern for API clients
class UserAPIClient {
  async getUser(id: string): Promise<User> {
    return this.fetch(`/users/${id}`);
  }
}

// New code follows the same pattern
class OrderAPIClient {
  async getOrder(id: string): Promise<Order> {
    return this.fetch(`/orders/${id}`);
  }
}
````

</Good>

<Bad>
```typescript
// Existing pattern uses classes
class UserAPIClient { /* ... */ }

// New code introduces different pattern without discussion
const getOrder = async (id: string): Promise<Order> => {
// Breaking consistency "because I prefer functions"
};

````
</Bad>

### Error Handling Patterns
<Good>
```typescript
// Project standard: Result type for recoverable errors
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

// All services follow this pattern
const fetchUser = async (id: string): Promise<Result<User, Error>> => {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      return { ok: false, error: new Error('User not found') };
    }
    return { ok: true, value: user };
  } catch (err) {
    return { ok: false, error: err as Error };
  }
};

// Callers use consistent pattern
const result = await fetchUser('123');
if (!result.ok) {
  logger.error('Failed to fetch user', result.error);
  return;
}
const user = result.value; // Type-safe!
````

</Good>

### Documentation Standards

<Good>
```typescript
/**
 * Retries an async operation with exponential backoff.
 *
 * Why: Network requests fail temporarily; retrying improves reliability
 * When to use: External API calls, database operations
 * When not to use: User input validation, internal function calls
 *
 * @example
 * const result = await retry(
 *   () => fetch('https://api.example.com/data'),
 *   { maxAttempts: 3, baseDelay: 1000 }
 * );
 */
const retry = async <T>(
  operation: () => Promise<T>,
  options: RetryOptions
): Promise<T> => {
  // Implementation...
};
```
</Good>

## 4. Just-In-Time (JIT)

### YAGNI in Action

<Good>
```typescript
// Current requirement: Log errors to console
const logError = (error: Error) => {
  console.error(error.message);
};
```
</Good>

<Bad>
```typescript
// Over-engineered for "future needs"
interface LogTransport {
  write(level: LogLevel, message: string, meta?: LogMetadata): Promise<void>;
}

class ConsoleTransport implements LogTransport { /_... _/ }
class FileTransport implements LogTransport { /_ ... _/ }
class RemoteTransport implements LogTransport { /_ ..._/ }

class Logger {
private transports: LogTransport[] = [];
// ... 200 lines of code for "maybe we'll need it"
}

````
</Bad>

### Adding Complexity
<Good>
```typescript
// Start simple
const formatCurrency = (amount: number): string => {
  return `$${amount.toFixed(2)}`;
};

// Requirement evolves: support multiple currencies
const formatCurrency = (amount: number, currency: string): string => {
  const symbols = { USD: '$', EUR: '€', GBP: '£' };
  return `${symbols[currency]}${amount.toFixed(2)}`;
};

// Requirement evolves: support localization
const formatCurrency = (amount: number, locale: string): string => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: locale === 'en-US' ? 'USD' : 'EUR',
  }).format(amount);
};
````

</Good>

### Premature Abstraction

<Bad>
```typescript
// One use case, but building generic framework
abstract class BaseCRUDService<T> {
  abstract getAll(): Promise<T[]>;
  // ... building entire ORM for single table
}
```
</Bad>

<Good>
```typescript
// Simple functions for current needs
const getUsers = async (): Promise<User[]> => {
  return db.query('SELECT * FROM users');
};

const getUserById = async (id: string): Promise<User | null> => {
return db.query('SELECT \* FROM users WHERE id = $1', [id]);
};

// When pattern emerges across multiple entities, then abstract

````
</Good>

### Performance Optimization
<Good>
```typescript
// Current: Simple approach
const filterActiveUsers = (users: User[]): User[] => {
  return users.filter(user => user.isActive);
};

// Benchmark shows: 50ms for 1000 users (acceptable)
// ✓ Ship it, no optimization needed

// Later: After profiling shows this is bottleneck
// Then optimize with indexed lookup or caching
````

</Good>

<Bad>
```typescript
// Premature optimization
const filterActiveUsers = (users: User[]): User[] => {
  // "This might be slow, so let's cache and index"
  const cache = new WeakMap();
  const indexed = buildBTreeIndex(users, 'isActive');
  // 100 lines of optimization code
  // Adds complexity, harder to maintain
  // No evidence it was needed
};
```
</Bad>
