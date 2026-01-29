// --- Mocking Modules ---

// Mock entire module
jest.mock('utils/analytics');

// Mock with factory function
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// Access mock in test
const mockLogEvent = jest.requireMock('utils/analytics').Analytics.logEvent;


// --- Mocking GraphQL Hooks ---

jest.mock('./GetItems.generated', () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock(
  './GetItems.generated'
).useGetItemsQuery as jest.Mock;

// Usage in test
/*
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
*/
