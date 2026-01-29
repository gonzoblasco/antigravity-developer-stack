# Data Access Patterns

## Repository Pattern

Repositories abstract database access, providing a single source of truth for queries and decoupling the service layer from the ORM.

```typescript
export interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User>;
  delete(id: string): Promise<void>;
}

export class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserDto): Promise<User> {
    return this.prisma.user.create({ data });
  }
}
```

## Database Optimization

### Preventing N+1 Queries

```typescript
// ❌ BAD: N+1 query problem
const markets = await getMarkets();
for (const market of markets) {
  market.creator = await getUser(market.creator_id); // N queries!
}

// ✅ GOOD: Batch fetch (Application level)
const markets = await getMarkets();
const creatorIds = markets.map((m) => m.creator_id);
const creators = await getUsers(creatorIds); // 1 query
const creatorMap = new Map(creators.map((c) => [c.id, c]));

markets.forEach((market) => {
  market.creator = creatorMap.get(market.creator_id);
});

// ✅ BETTER: Join query (Database level)
const markets = await prisma.market.findMany({
  include: { creator: true }, // SQL JOIN - single query
});
```

## Caching with Redis

Implement the Cache-Aside pattern to reduce database load.

```typescript
class CachedUserRepository implements UserRepository {
  constructor(
    private baseRepo: UserRepository,
    private redis: RedisClient,
  ) {}

  async findById(id: string): Promise<User | null> {
    // Check cache first
    const cached = await this.redis.get(`user:${id}`);
    if (cached) {
      return JSON.parse(cached);
    }

    // Cache miss - fetch from database
    const user = await this.baseRepo.findById(id);

    if (user) {
      // Cache for 5 minutes
      await this.redis.setex(`user:${id}`, 300, JSON.stringify(user));
    }

    return user;
  }

  async invalidateCache(id: string): Promise<void> {
    await this.redis.del(`user:${id}`);
  }
}
```
