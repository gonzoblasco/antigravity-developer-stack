# Imports Cheatsheet

## Import Aliases Quick Reference

| Alias         | Resolves To      | Example                                                       |
| ------------- | ---------------- | ------------------------------------------------------------- |
| `@/`          | `src/`           | `import { apiClient } from '@/lib/apiClient'`                 |
| `~types`      | `src/types`      | `import type { User } from '~types/user'`                     |
| `~components` | `src/components` | `import { SuspenseLoader } from '~components/SuspenseLoader'` |
| `~features`   | `src/features`   | `import { authApi } from '~features/auth'`                    |

Defined in: [vite.config.ts](../../vite.config.ts) lines 180-185

## Common Imports Cheatsheet

```typescript
// React & Lazy Loading
import React, { useState, useCallback, useMemo } from "react";
const Heavy = React.lazy(() => import("./Heavy"));

// MUI Components
import { Box, Paper, Typography, Button, Grid } from "@mui/material";
import type { SxProps, Theme } from "@mui/material";

// TanStack Query (Suspense)
import { useSuspenseQuery, useQueryClient } from "@tanstack/react-query";

// TanStack Router
import { createFileRoute } from "@tanstack/react-router";

// Project Components
import { SuspenseLoader } from "~components/SuspenseLoader";

// Hooks
import { useAuth } from "@/hooks/useAuth";
import { useMuiSnackbar } from "@/hooks/useMuiSnackbar";

// Types
import type { Post } from "~types/post";
```
