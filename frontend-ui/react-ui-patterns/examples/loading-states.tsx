
import React from 'react';

// ============================================================================
// THE GOLDEN RULE
// Show loading indicator ONLY when there's no data to display.
// ============================================================================

interface Data {
  items: string[];
}

interface ItemListProps {
  items: string[];
}

const ItemList = ({ items }: ItemListProps) => (
  <ul>{items.map(item => <li key={item}>{item}</li>)}</ul>
);

const EmptyState = () => <div>No items found</div>;
const LoadingState = () => <div>Loading...</div>;
const ErrorState = ({ error, onRetry }: { error: Error; onRetry: () => void }) => (
  <div>
    Error: {error.message}
    <button onClick={onRetry}>Retry</button>
  </div>
);

// Mock hook
const useGetItemsQuery = () => ({
  data: undefined as Data | undefined,
  loading: true,
  error: undefined as Error | undefined,
  refetch: () => {},
});

export const CorrectLoadingPattern = () => {
  // CORRECT - Only show loading when no data exists
  const { data, loading, error, refetch } = useGetItemsQuery();

  if (error) return <ErrorState error={error} onRetry={refetch} />;
  
  // Only show full page loader if we have NO data
  if (loading && !data) return <LoadingState />;
  
  // If we have data (even if stale/refetching), show it
  if (!data?.items.length) return <EmptyState />;

  return (
    <div>
       {loading && <span>Refreshing...</span>}
       <ItemList items={data.items} />
    </div>
  );
};

export const WrongLoadingPattern = () => {
  const { data, loading } = useGetItemsQuery();
  
  // WRONG - Shows spinner even when we have cached data
  // This causes the UI to flash/flicker on every refetch
  if (loading) return <LoadingState />; 
  
  return <ItemList items={data?.items || []} />;
};

// ============================================================================
// SKELETON VS SPINNER
// ============================================================================

/*
| Use Skeleton When   | Use Spinner When      |
|---------------------|-----------------------|
| Known content shape | Unknown content shape |
| List/card layouts   | Modal actions         |
| Initial page load   | Button submissions    |
| Content placeholders| Inline operations     |
*/
