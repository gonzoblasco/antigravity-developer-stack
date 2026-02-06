# Form Patterns

> Patrones para formularios robustos y accesibles

## Controlled Form

Formulario con estado controlado completo.

```typescript
interface FormData {
  email: string;
  password: string;
  remember: boolean;
}

interface FormErrors {
  email?: string;
  password?: string;
}

function LoginForm() {
  const [data, setData] = useState<FormData>({
    email: '',
    password: '',
    remember: false,
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    // Limpiar error al editar
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!data.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(data.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!data.password) {
      newErrors.password = 'Password is required';
    } else if (data.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await api.login(data);
    } catch (error) {
      setErrors({ email: 'Invalid credentials' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={data.email}
          onChange={handleChange}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && <span id="email-error" role="alert">{errors.email}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={data.password}
          onChange={handleChange}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && <span id="password-error" role="alert">{errors.password}</span>}
      </div>

      <div>
        <input
          id="remember"
          name="remember"
          type="checkbox"
          checked={data.remember}
          onChange={handleChange}
        />
        <label htmlFor="remember">Remember me</label>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log In'}
      </button>
    </form>
  );
}
```

## Custom Form Hook

Hook reutilizable para formularios.

```typescript
function useForm<T extends Record<string, any>>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>,
) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = useCallback(
    (
      e: ChangeEvent<
        HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
      >,
    ) => {
      const { name, value, type } = e.target;
      const newValue =
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value;

      setValues((prev) => ({ ...prev, [name]: newValue }));
    },
    [],
  );

  const handleBlur = useCallback(
    (
      e: FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>,
    ) => {
      const { name } = e.target;
      setTouched((prev) => ({ ...prev, [name]: true }));

      // Validate single field
      const fieldErrors = validate(values);
      if (fieldErrors[name as keyof T]) {
        setErrors((prev) => ({
          ...prev,
          [name]: fieldErrors[name as keyof T],
        }));
      } else {
        setErrors((prev) => {
          const { [name as keyof T]: _, ...rest } = prev;
          return rest as typeof prev;
        });
      }
    },
    [values, validate],
  );

  const handleSubmit = useCallback(
    (onSubmit: (values: T) => void | Promise<void>) => {
      return async (e: FormEvent) => {
        e.preventDefault();

        // Touch all fields
        const allTouched = Object.keys(values).reduce(
          (acc, key) => ({ ...acc, [key]: true }),
          {} as Record<keyof T, boolean>,
        );
        setTouched(allTouched);

        // Validate all
        const validationErrors = validate(values);
        setErrors(validationErrors);

        if (Object.keys(validationErrors).length === 0) {
          await onSubmit(values);
        }
      };
    },
    [values, validate],
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  }, [initialValues]);

  const getFieldProps = (name: keyof T) => ({
    name,
    value: values[name],
    onChange: handleChange,
    onBlur: handleBlur,
    "aria-invalid": touched[name] && !!errors[name],
    "aria-describedby": errors[name] ? `${String(name)}-error` : undefined,
  });

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    getFieldProps,
    isValid: Object.keys(errors).length === 0,
  };
}
```

## Multi-Step Form

Wizard pattern para formularios largos.

```typescript
interface StepProps {
  data: FormData;
  updateData: (updates: Partial<FormData>) => void;
  next: () => void;
  back: () => void;
}

function MultiStepForm() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState<FormData>(initialData);

  const updateData = (updates: Partial<FormData>) => {
    setData(prev => ({ ...prev, ...updates }));
  };

  const next = () => setStep(prev => prev + 1);
  const back = () => setStep(prev => prev - 1);

  const steps = [
    { component: PersonalInfo, title: 'Personal Info' },
    { component: ContactInfo, title: 'Contact' },
    { component: Review, title: 'Review' },
  ];

  const CurrentStep = steps[step].component;

  return (
    <div>
      {/* Progress indicator */}
      <nav aria-label="Form progress">
        <ol>
          {steps.map((s, i) => (
            <li
              key={s.title}
              aria-current={i === step ? 'step' : undefined}
              className={i <= step ? 'completed' : ''}
            >
              {s.title}
            </li>
          ))}
        </ol>
      </nav>

      {/* Current step */}
      <CurrentStep
        data={data}
        updateData={updateData}
        next={next}
        back={back}
      />
    </div>
  );
}
```

## Field Array Pattern

Para campos dinámicos (agregar/quitar items).

```typescript
function useFieldArray<T>(initialItems: T[] = []) {
  const [items, setItems] = useState(initialItems);

  const append = (item: T) => setItems(prev => [...prev, item]);

  const remove = (index: number) => {
    setItems(prev => prev.filter((_, i) => i !== index));
  };

  const update = (index: number, item: T) => {
    setItems(prev => prev.map((existing, i) =>
      i === index ? item : existing
    ));
  };

  const move = (from: number, to: number) => {
    setItems(prev => {
      const result = [...prev];
      const [removed] = result.splice(from, 1);
      result.splice(to, 0, removed);
      return result;
    });
  };

  return { items, append, remove, update, move };
}

// Uso
function PhoneNumbers() {
  const { items, append, remove } = useFieldArray<string>(['']);

  return (
    <fieldset>
      <legend>Phone Numbers</legend>
      {items.map((phone, index) => (
        <div key={index}>
          <input
            value={phone}
            onChange={(e) => update(index, e.target.value)}
            aria-label={`Phone number ${index + 1}`}
          />
          <button
            type="button"
            onClick={() => remove(index)}
            aria-label={`Remove phone ${index + 1}`}
          >
            Remove
          </button>
        </div>
      ))}
      <button type="button" onClick={() => append('')}>
        Add Phone
      </button>
    </fieldset>
  );
}
```

## Debounced Validation

Validar mientras escribe sin bloquear.

```typescript
function useDebouncedValidation<T>(
  value: T,
  validate: (value: T) => Promise<string | null>,
  delay = 300,
) {
  const [error, setError] = useState<string | null>(null);
  const [isValidating, setIsValidating] = useState(false);

  useEffect(() => {
    setIsValidating(true);

    const timer = setTimeout(async () => {
      const result = await validate(value);
      setError(result);
      setIsValidating(false);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, validate, delay]);

  return { error, isValidating };
}

// Uso: validar username disponibilidad
const { error, isValidating } = useDebouncedValidation(
  username,
  async (value) => {
    if (!value) return "Username required";
    const available = await api.checkUsername(value);
    return available ? null : "Username taken";
  },
);
```
