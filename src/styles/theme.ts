import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    primary: {
      50: '#e5f5ff',
      100: '#b8e0ff',
      200: '#8ac5ff',
      300: '#5caaff',
      400: '#2e90ff',
      500: '#0077ff',
      600: '#005fd9',
      700: '#0047b3',
      800: '#00308c',
      900: '#001a66',
    },
  },
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  components: {
    Button: {
      variants: {
        primary: {
          bg: 'primary.500',
          color: 'white',
          _hover: {
            bg: 'primary.600',
          },
        },
      },
    },
  },
});

export default theme;