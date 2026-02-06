# Component Templates

> Templates base para diferentes tipos de componentes

## Basic Functional Component

```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({
  children,
  variant = 'primary',
  disabled = false,
  onClick,
}: ButtonProps) {
  return (
    <button
      type="button"
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

## Component with Forwarded Ref

```typescript
import { forwardRef, type ComponentPropsWithoutRef } from 'react';

interface InputProps extends ComponentPropsWithoutRef<'input'> {
  label: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, error, id, ...props }, ref) {
    const inputId = id || label.toLowerCase().replace(/\s/g, '-');
    const errorId = `${inputId}-error`;

    return (
      <div className="input-wrapper">
        <label htmlFor={inputId}>{label}</label>
        <input
          ref={ref}
          id={inputId}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          {...props}
        />
        {error && (
          <span id={errorId} role="alert" className="error">
            {error}
          </span>
        )}
      </div>
    );
  }
);
```

## Component with Children Slots

```typescript
interface CardProps {
  children: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

export function Card({ children, header, footer, className = '' }: CardProps) {
  return (
    <article className={`card ${className}`}>
      {header && <header className="card-header">{header}</header>}
      <div className="card-body">{children}</div>
      {footer && <footer className="card-footer">{footer}</footer>}
    </article>
  );
}
```

## List Component with Empty State

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
  isLoading?: boolean;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items found',
  isLoading = false,
}: ListProps<T>) {
  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  if (items.length === 0) {
    return <div className="empty-state">{emptyMessage}</div>;
  }

  return (
    <ul className="list">
      {items.map((item, index) => (
        <li key={keyExtractor(item)} className="list-item">
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}
```

## Modal/Dialog Component

```typescript
import { useEffect, useRef } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      dialog.showModal();
    } else {
      dialog.close();
    }
  }, [isOpen]);

  // Close on backdrop click
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === dialogRef.current) {
      onClose();
    }
  };

  // Close on Escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <dialog
      ref={dialogRef}
      className="modal"
      onClick={handleBackdropClick}
      aria-labelledby="modal-title"
    >
      <div className="modal-content">
        <header className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button
            type="button"
            className="modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        </header>
        <div className="modal-body">{children}</div>
      </div>
    </dialog>
  );
}
```

## Data Display Component

```typescript
type AsyncState<T> =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: T };

interface AsyncDataProps<T> {
  state: AsyncState<T>;
  renderData: (data: T) => React.ReactNode;
  loadingComponent?: React.ReactNode;
  errorComponent?: (error: Error) => React.ReactNode;
}

export function AsyncData<T>({
  state,
  renderData,
  loadingComponent = <div>Loading...</div>,
  errorComponent = (error) => <div>Error: {error.message}</div>,
}: AsyncDataProps<T>) {
  switch (state.status) {
    case 'loading':
      return <>{loadingComponent}</>;
    case 'error':
      return <>{errorComponent(state.error)}</>;
    case 'success':
      return <>{renderData(state.data)}</>;
  }
}
```

## Page Component Template

```typescript
import { useDocumentTitle } from '@/hooks/useDocumentTitle';

export function DashboardPage() {
  useDocumentTitle('Dashboard | App Name');

  return (
    <main className="page dashboard-page">
      <header className="page-header">
        <h1>Dashboard</h1>
      </header>

      <section className="page-content">
        {/* Main content */}
      </section>
    </main>
  );
}
```
