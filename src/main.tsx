import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider } from '@chakra-ui/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactRouter } from '@tanstack/react-router';
import theme from './styles/theme';
import App from './App';

const queryClient = new QueryClient();

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <ReactRouter>
          <App />
        </ReactRouter>
      </QueryClientProvider>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById('root')
);