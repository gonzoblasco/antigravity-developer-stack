# NestJS Patterns & Solutions

## Common Patterns

### Module Organization

```typescript
// Feature module pattern
@Module({
  imports: [CommonModule, DatabaseModule],
  controllers: [FeatureController],
  providers: [FeatureService, FeatureRepository],
  exports: [FeatureService], // Export for other modules
})
export class FeatureModule {}
```

### Custom Decorator Pattern

```typescript
// Combine multiple decorators
export const Auth = (...roles: Role[]) =>
  applyDecorators(UseGuards(JwtAuthGuard, RolesGuard), Roles(...roles));
```

### Testing Pattern

```typescript
// Comprehensive test setup
beforeEach(async () => {
  const module = await Test.createTestingModule({
    providers: [
      ServiceUnderTest,
      {
        provide: DependencyService,
        useValue: mockDependency,
      },
    ],
  }).compile();

  service = module.get<ServiceUnderTest>(ServiceUnderTest);
});
```

### Exception Filter Pattern

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    // Custom error handling
  }
}
```

## Quick Reference

### Dependency Injection Tokens

```typescript
// Custom provider token
export const CONFIG_OPTIONS = Symbol('CONFIG_OPTIONS');

// Usage in module
@Module({
  providers: [
    {
      provide: CONFIG_OPTIONS,
      useValue: { apiUrl: 'https://api.example.com' }
    }
  ]
})
```

### Global Module Pattern

```typescript
@Global()
@Module({
  providers: [GlobalService],
  exports: [GlobalService],
  // ...
})
export class GlobalModule {}
```

### Dynamic Module Pattern

```typescript
@Module({})
export class ConfigModule {
  static forRoot(options: ConfigOptions): DynamicModule {
    return {
      module: ConfigModule,
      providers: [
        {
          provide: "CONFIG_OPTIONS",
          useValue: options,
        },
      ],
    };
  }
}
```
