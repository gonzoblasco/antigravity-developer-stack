# Security Patterns

## Authentication Middleware (JWT)

Secure routes by verifying JWT tokens and attaching user context to the request.

```typescript
import jwt from "jsonwebtoken";

interface JWTPayload {
  userId: string;
  email: string;
  role: "admin" | "user";
}

export async function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const token = req.headers.authorization?.replace("Bearer ", "");

  if (!token) {
    return res.status(401).json({ error: "Missing authorization token" });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;

    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
}

// Usage
router.get("/profile", requireAuth, (req, res) => {
  // req.user is available
  res.json({ user: req.user });
});
```

## Rate Limiting

Protect your API from abuse with rate limiting.

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>();

  async checkLimit(
    identifier: string,
    maxRequests: number,
    windowMs: number,
  ): Promise<boolean> {
    const now = Date.now();
    const requests = this.requests.get(identifier) || [];

    // Remove old requests outside window
    const recentRequests = requests.filter((time) => now - time < windowMs);

    if (recentRequests.length >= maxRequests) {
      return false; // Rate limit exceeded
    }

    // Add current request
    recentRequests.push(now);
    this.requests.set(identifier, recentRequests);

    return true;
  }
}

const limiter = new RateLimiter();

export async function rateLimitMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const ip =
    req.headers["x-forwarded-for"] || req.socket.remoteAddress || "unknown";

  const allowed = await limiter.checkLimit(ip, 100, 60000); // 100 req/min

  if (!allowed) {
    return res.status(429).json({ error: "Rate limit exceeded" });
  }

  next();
}
```
