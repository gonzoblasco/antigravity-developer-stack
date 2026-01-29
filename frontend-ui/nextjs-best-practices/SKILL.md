---
name: nextjs-best-practices
description: Use when building or refactoring Next.js App Router applications. Keywords: nextjs, app router, server components, rsc, next.js.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Next.js Best Practices (App Router)

> **Golden Rule**: Server Components by default. Client Components only at the leaves.

## 1. The Iron Rules (Guardrails)

| IF you think...                                    | THEN remember...                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------- |
| "It's just a small component, I'll make it client" | **STOP.** Performance death by thousand cuts. Keep it server.           |
| "I need `useState` for data fetching"              | **WRONG.** Fetch in Server Component. Pass data as props.               |
| "I can't access `window` in Server Component"      | Correct. Move that specific logic to a Client Component leaf.           |
| "I'll wrap the whole app in a Context Provider"    | **AVOID.** Wrap only children who need it. Don't de-opt the whole tree. |

## 2. Server vs Client Decision Tree

1.  **Does it need interactivity?** (onClick, onChange, hooks)
    - YES -> [Client Component](templates/client-component.tsx)
2.  **Does it need to fetch data directly?** (DB, API)
    - YES -> [Server Component](templates/server-component.tsx)
3.  **Does it assume it's on the browser?** (localStorage, window)
    - YES -> [Client Component](templates/client-component.tsx)

**By Default:** Server Component.
**Opt-in:** Add `'use client'` at the VERY TOP of the file.

## 3. Data Fetching & Caching

- **Static (Default)**: `fetch('URL')`. Built once, cached forever.
- **Dynamic**: `fetch('URL', { cache: 'no-store' })`. Fetched on every request.
- **Revalidated**: `fetch('URL', { next: { revalidate: 60 } })`. Cached for 60s.

## 4. Project Structure (Standard)

```text
app/
├── (marketing)/      # Route Group (doesn't affect URL)
│   └── page.tsx
├── (dashboard)/
│   ├── layout.tsx    # Shared UI for dashboard
│   └── page.tsx
├── api/              # API Routes
│   └── route.ts      # [Route Handler Template](templates/route_handler.ts)
└── components/       # Colocated components
```

## 5. Metadata

**Never** hardcode `<head>`. Use the Metadata API.

```typescript
export const metadata = {
  title: "My Page",
  description: "Page description",
};
```

## 6. Anti-Patterns to Spot

- ❌ `useEffect` to fetch data on component mount (Use Server Component).
- ❌ importing server-only code (DB) into Client Components.
- ❌ deep prop drilling (Use RSC composition or deep Context only if necessary).
- ❌ huge `page.tsx` files (Break it down).

## 7. Templates

- [Server Component boilerplate](templates/server-component.tsx)
- [Client Component boilerplate](templates/client-component.tsx)
- [Route Handler boilerplate](templates/route_handler.ts)
