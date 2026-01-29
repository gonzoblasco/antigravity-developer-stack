# Next.js Patterns

## Server vs Client Components

| Feature               | Server Components (Default)         | Client Components (`'use client'`)        |
| :-------------------- | :---------------------------------- | :---------------------------------------- |
| **Data Fetching**     | ✅ Async/Await                      | ❌ (Use `useEffect`, SWR, or React Query) |
| **Backend Resources** | ✅ Direct Access (DB, Files)        | ❌ No                                     |
| **Interactivity**     | ❌ No (No `onClick`, `onChange`)    | ✅ Yes                                    |
| **State/Effects**     | ❌ No (`useState`, `useEffect`)     | ✅ Yes                                    |
| **Browser APIs**      | ❌ No (No `window`, `localStorage`) | ✅ Yes                                    |

## Best Practices

1.  **Leaf Components**: Keep Client Components as leaves in the tree. Pass Server Components as children to Client Components.
2.  **Fetch on Server**: Fetch data in Server Components where possible to reduce waterfalls and client bundle size.
3.  **Route Handlers**: Use Route Handlers for API endpoints (`app/api/route.ts`).
4.  **Metadata**: Use the Metadata API for SEO.
