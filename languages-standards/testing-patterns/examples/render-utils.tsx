import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};

// Usage Example:
// import { renderWithTheme } from 'utils/testUtils';
// import { screen } from '@testing-library/react-native';
// 
// it('should render component', () => {
//   renderWithTheme(<MyComponent />);
//   expect(screen.getByText('Hello')).toBeTruthy();
// });
