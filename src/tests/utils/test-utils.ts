import { render, RenderOptions } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from '@tanstack/react-router';
import theme from '../../styles/theme';

const queryClient = new QueryClient();

const AllProviders = ({ children }: { children: React.ReactNode }) => (
  <ChakraProvider theme={theme}>
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{children}</MemoryRouter>
    </QueryClientProvider>
  </ChakraProvider>
);

const customRender = (ui: React.ReactElement, options?: RenderOptions) =>
  render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };