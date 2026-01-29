
import React from 'react';

// ============================================================================
// ERROR HANDLING HIERARCHY
// 1. Inline error (field-level) → Form validation errors
// 2. Toast notification → Recoverable errors, user can retry
// 3. Error banner → Page-level errors, data still partially usable
// 4. Full error screen → Unrecoverable, needs user action
// ============================================================================

// Mock toast
const toast = {
  success: (msg: any) => console.log('Success:', msg),
  error: (msg: any) => console.error('Error:', msg),
};

// Mock hook
const useCreateItemMutation = (options: any) => [
  async () => {}, 
  { loading: false }
];

export const CorrectErrorHandling = () => {
  // CORRECT - Error always surfaced to user
  const [createItem] = useCreateItemMutation({
    onCompleted: () => {
      toast.success({ title: 'Item created' });
    },
    onError: (error: Error) => {
      // Log for developer
      console.error('createItem failed:', error);
      // Show for user
      toast.error({ title: 'Failed to create item', description: error.message });
    },
  });

  return <button onClick={() => createItem()}>Create Item</button>;
};

export const WrongErrorHandling = () => {
  // WRONG - Error silently caught, user has no idea
  const [createItem] = useCreateItemMutation({
    onError: (error: Error) => {
      console.error(error); // User sees nothing!
    },
  });

  return <button onClick={() => createItem()}>Create Silent Fail</button>;
};

// ============================================================================
// REUSABLE ERROR COMPONENT
// ============================================================================

interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
  title?: string;
  className?: string;
}

export const ErrorState = ({ error, onRetry, title, className = '' }: ErrorStateProps) => (
  <div className={`p-4 border border-red-200 bg-red-50 rounded-lg ${className}`}>
    <div className="flex items-center gap-3 text-red-700">
      <span role="img" aria-label="error">⚠️</span>
      <h3 className="font-semibold">{title ?? 'Something went wrong'}</h3>
    </div>
    
    <p className="mt-2 text-sm text-red-600">{error.message}</p>
    
    {onRetry && (
      <button 
        onClick={onRetry}
        className="mt-3 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 rounded-md text-sm font-medium transition-colors"
      >
        Try Again
      </button>
    )}
  </div>
);
