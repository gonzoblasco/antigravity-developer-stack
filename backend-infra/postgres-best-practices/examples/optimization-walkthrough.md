# Optimization Walkthrough

This example demonstrates how to use the `supabase-postgres-best-practices` skill to transform a naive schema into a production-ready one.

## 1. The Naive Schema ("Bad")

Found in `legacy_schema.sql`:

```sql
CREATE TABLE "Users" (
    "userId" serial PRIMARY KEY,
    "email" varchar(255),
    "created_at" timestamp
);

CREATE TABLE "Orders" (
    "id" uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    "user_id" int REFERENCES "Users"("userId"),
    "total" float
);
```

## 2. Running the Audit

We run the audit script:

```bash
python scripts/audit_schema.py legacy_schema.sql
```

**Output:**

```text
--- Primary Keys ---
⚠ Line 2: Usage of 'serial' detected. Prefer 'generated always as identity'.
⚠ Line 8: UUID Primary Key detected without v7 function. Ensure you are using v7...

--- Data Types ---
⚠ Line 3: 'varchar(n)' detected. Prefer 'text'...
⚠ Line 4: 'timestamp' (no tz) detected. Almost always prefer 'timestamptz'...

--- Indexes on Foreign Keys ---
⚠ Table 'Orders', Column 'user_id': Foreign Key appears unindexed...

--- Naming Conventions ---
⚠ Line 1: Mixed-case quoted identifier detected...
```

## 3. The Optimized Schema ("Good")

Applying the feedback:

```sql
create table users (
    id bigint generated always as identity primary key,
    email text,
    created_at timestamptz default now()
);

create table orders (
    id uuid default uuid_generate_v7() primary key, -- Assuming pg_uuidv7 extension
    user_id bigint references users(id) on delete cascade,
    total numeric(10, 2)
);

-- Crucial: Index the FK
create index orders_user_id_idx on orders(user_id);
```

**Re-running the audit returns:**

```text
--- Primary Keys ---
✓ No issues found
...
✓ No issues found
```
