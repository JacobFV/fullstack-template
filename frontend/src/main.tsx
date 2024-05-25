import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider } from '@chakra-ui/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactRouter } from '@tanstack/react-router';
import theme from './styles/theme';
import App from './App';
import ErrorBoundary from './components/ErrorBoundary';

const queryClient = new QueryClient();

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <ReactRouter>
          <ErrorBoundary fallback={<div>Something went wrong.</div>}>
            <App />
          </ErrorBoundary>
        </ReactRouter>
      </QueryClientProvider>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById('root')
);