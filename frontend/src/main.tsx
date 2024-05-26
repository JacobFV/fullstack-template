import { ChakraProvider } from "@chakra-ui/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { RouterProvider, createRouter } from "@tanstack/react-router"
import ReactDOM from "react-dom/client"
import { routeTree } from "./routeTree.gen"

import { StrictMode } from "react"
import { OpenAPI } from "./client"
import theme from "./theme"

OpenAPI.BASE = import.meta.env.VITE_API_URL
OpenAPI.TOKEN = async () => {
  return localStorage.getItem("access_token") || ""
}

const queryClient = new QueryClient()

const router = createRouter({ routeTree })
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ChakraProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ChakraProvider>
  </StrictMode>,
)

// import React from 'react';
// import ReactDOM from 'react-dom';
// import { ChakraProvider } from '@chakra-ui/react';
// import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
// import { ReactRouter } from '@tanstack/react-router';
// import theme from './styles/theme';
// import App from './App';
// import ErrorBoundary from './components/ErrorBoundary';

// const queryClient = new QueryClient();

// ReactDOM.render(
//   <React.StrictMode>
//     <ChakraProvider theme={theme}>
//       <QueryClientProvider client={queryClient}>
//         <ReactRouter>
//           <ErrorBoundary fallback={<div>Something went wrong.</div>}>
//             <App />
//           </ErrorBoundary>
//         </ReactRouter>
//       </QueryClientProvider>
//     </ChakraProvider>
//   </React.StrictMode>,
//   document.getElementById('root')
// );