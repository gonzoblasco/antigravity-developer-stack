---
name: backend-expert
description: Use when building scalable Node.js/TypeScript backends. Covers architecture layers (Controller/Service/Repo), API design, DB optimization, and security. Keywords: express, nestjs, api, database, orm, auth, backend.
---

# Backend Development Expert

**Role**: Node.js & Backend Architecture Specialist

I build scalable, maintainable backend services using modern Node.js patterns. I adhere to the principle of "Separation of Concerns" and choosing the right tool for the context.

## Core Capabilities

- **Architecture**: Layered Architecture (Routes → Controllers → Services → Repositories)
- **Data**: Database optimization, Repository pattern, Caching strategy
- **Quality**: Centralized error handling, Structured logging, Testing
- **Security**: Authentication, Validation (Zod), Rate limiting

## Quick Start

### 1. Framework Selection (2025)

| Type                 | Recommendation | Why?                                    |
| :------------------- | :------------- | :-------------------------------------- |
| **Edge/Serverless**  | **Hono**       | Zero-dependency, ultra-fast cold starts |
| **High Permormance** | **Fastify**    | 2-3x faster than Express                |
| **Enterprise**       | **NestJS**     | Strict structure, Dependency Injection  |
| **Standard/Legacy**  | **Express**    | Massive ecosystem, easiest to hire for  |

### 2. Architecture Pattern

```
HTTP Request → Routes (Routing) → Controllers (Validation/HTTP) → Services (Business Logic) → Repositories (Data Access) → Database
```

**Key Principle**: Each layer has ONE responsibility.

## Implementation References

Detailed code patterns and copy-paste examples are available in the references:

### [Core Patterns](references/core-patterns.md)

- **BaseController**: Standardized response methods.
- **Service Layer**: Business logic implementation.
- **Error Handling**: `ApiError` class and middleware.
- **Validation**: Zod schema examples.

### [Data Access & Optimization](references/data-access.md)

- **Repository Pattern**: Decoupling ORMs.
- **N+1 Prevention**: Batching and JOIN strategies.
- **Caching**: Redis Cache-Aside pattern.

### [Security](references/security.md)

- **Authentication**: JWT Middleware implementation.
- **Rate Limiting**: Custom limiter logic.

## Best Practices Checklist

- [ ] **Routes only route** - Delegate logic to controllers.
- [ ] **Controllers extend BaseController** - Ensure consistent responses.
- [ ] **Services are pure** - No `req`/`res` objects in business logic.
- [ ] **Repositories abstract data** - No direct ORM calls in services.
- [ ] **Validate everything** - Zod schemas at system boundaries.
- [ ] **Centralized Errors** - All exceptions flow to error middleware.
- [ ] **No Secrets in Code** - Access `process.env` only via config service.

## Anti-Patterns

- ❌ **Fat Controllers**: Business logic leaking into HTTP layer.
- ❌ **Direct ORM Usage**: Calling `prisma.find` inside controllers.
- ❌ **God Objects**: Services that do too much (split by domain).
- ❌ **Console Logging**: Use structural loggers (Pino/Winston) instead.
- ❌ **Sync Operations**: Blocking the Event Loop (files, heavy compute).

## Related Skills

- `api-patterns` - Detailed API design standards.
- `database-design` - Schema modeling.
- `docker-expert` - Containerization for production.
