# Core Backend Patterns

## Controller with BaseController Pattern

All controllers should extend a base class for consistency in response formatting and error handling.

```typescript
export class BaseController {
  protected handleSuccess(res: Response, data: any, statusCode = 200) {
    res.status(statusCode).json({ success: true, data });
  }

  protected handleError(error: unknown, res: Response, context: string) {
    Sentry.captureException(error, { extra: { context } });

    if (error instanceof ApiError) {
      return res.status(error.statusCode).json({
        success: false,
        error: error.message,
      });
    }

    res.status(500).json({
      success: false,
      error: "Internal server error",
    });
  }
}

export class UserController extends BaseController {
  constructor(private userService: UserService) {
    super();
  }

  async getById(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.findById(req.params.id);
      this.handleSuccess(res, user);
    } catch (error) {
      this.handleError(error, res, "UserController.getById");
    }
  }
}
```

## Service Layer (Business Logic)

Services contain all business rules and should be framework-agnostic (no `req`/`res`).

```typescript
export class UserService {
  constructor(private userRepository: UserRepository) {}

  async createUser(data: CreateUserDto): Promise<User> {
    // Business validation
    const existingUser = await this.userRepository.findByEmail(data.email);
    if (existingUser) {
      throw new ApiError(409, "Email already exists");
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 10);

    // Create user
    const user = await this.userRepository.create({
      ...data,
      password: hashedPassword,
    });

    // Send welcome email (background job)
    await emailQueue.add({ type: "welcome", userId: user.id });

    return user;
  }
}
```

## Centralized Error Handling

Use custom error classes and centralized error middleware.

```typescript
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true,
  ) {
    super(message);
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

// Error middleware (Express)
export function errorHandler(
  error: Error,
  request: Request,
  res: Response,
  next: NextFunction,
) {
  // Log to Sentry
  Sentry.captureException(error);

  if (error instanceof ApiError) {
    return res.status(error.statusCode).json({
      success: false,
      error: error.message,
    });
  }

  if (error instanceof z.ZodError) {
    return res.status(400).json({
      success: false,
      error: "Validation failed",
      details: error.errors,
    });
  }

  // Unknown error
  console.error("Unexpected error:", error);
  res.status(500).json({
    success: false,
    error: "Internal server error",
  });
}
```

## Input Validation with Zod

Validate ALL inputs at system boundaries (controllers).

```typescript
import { z } from "zod";

const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(100),
});

export async function createUser(req: Request, res: Response) {
  try {
    // Validate input
    const validated = createUserSchema.parse(req.body);

    // Continue with validated data
    const user = await userService.create(validated);

    res.status(201).json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: "Validation failed",
        details: error.errors,
      });
    }
    throw error;
  }
}
```
