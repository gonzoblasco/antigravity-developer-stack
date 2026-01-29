---
name: supabase-postgres-best-practices
description: Use when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations. Keywords: postgres performance, optimize query, slow query, database schema, index strategy, RLS performance, supabase best practices, connection pooling.
license: MIT
metadata:
  author: supabase
  version: "2.0.0"
---

# Supabase Postgres Best Practices

**"The database is the bottleneck."** Prevent this cliché by applying these optimization rules.

This skill provides prioritized guidelines and **automated tools** to audit and optimize Postgres databases, specifically for Supabase environments.

## Quick Start (Automation)

Use the included scripts to instantly audit schemas and performance stats.

```bash
# 1. Audit a schema file for missing indexes, bad types, etc.
python scripts/audit_schema.py path/to/schema.sql

# 2. Check live performance metrics (run in SQL editor)
# See: scripts/pg_stat_check.sql
```

## When to Apply

- **Designing Schema**: "I'm creating a `users` table, what types should I use?" -> Uses `scripts/audit_schema.py`.
- **Slow Queries**: "Why is this JOIN slow?" -> Check Indexing (Category 1).
- **Production Issues**: "We're running out of connections." -> Check Connection Management (Category 2).
- **Security Check**: "Is my RLS secure and fast?" -> Check Security (Category 3).

## Rule Categories by Priority

| Priority | Category                 | Impact      | Prefix      |
| -------- | ------------------------ | ----------- | ----------- |
| 1        | Query Performance        | CRITICAL    | `query-`    |
| 2        | Connection Management    | CRITICAL    | `conn-`     |
| 3        | Security & RLS           | CRITICAL    | `security-` |
| 4        | Schema Design            | HIGH        | `schema-`   |
| 5        | Concurrency & Locking    | MEDIUM-HIGH | `lock-`     |
| 6        | Data Access Patterns     | MEDIUM      | `data-`     |
| 7        | Monitoring & Diagnostics | LOW-MEDIUM  | `monitor-`  |
| 8        | Advanced Features        | LOW         | `advanced-` |

## Reference Guide

Detailed rules are located in `references/`:

- **Queries**: `references/query-missing-indexes.md`, `references/query-index-types.md`...
- **Schema**: `references/schema-data-types.md`, `references/schema-primary-keys.md`...
- **Full Guide**: `references/AGENTS.md` (Compiled version)

## Common "Excuses" & Reality

| Agent Rationalization                    | Reality                            | Refutation                                                                                         |
| ---------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| "I'll add indexes later when it's slow." | Indexes on FKs are mandatory.      | "No. Missing FK indexes cause immediate locking issues on deletes. Add them now."                  |
| "VARCHAR(255) is standard."              | In Postgres, `TEXT` is better.     | "TEXT has no performance penalty and no arbitrary limits. Use TEXT."                               |
| "I'm using serial for IDs."              | `IDENTITY` is the modern standard. | "Use `GENERATED ALWAYS AS IDENTITY`. It's the SQL standard replacement for serial."                |
| "RLS is slow, I'll allow all."           | Insecure.                          | "RLS is fast if you index the columns used in the policy. Never disable security for performance." |
