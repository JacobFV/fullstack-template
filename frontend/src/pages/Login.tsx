import React from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const Login: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login form submission
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Login
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="email" mb={4}>
          <FormLabel>Email address</FormLabel>
          <Input type="email" />
        </FormControl>
        <FormControl id="password" mb={8}>
          <FormLabel>Password</FormLabel>
          <Input type="password" />
        </FormControl>
        <Button type="submit" colorScheme="blue" size="lg" width="full">
          Login
        </Button>
      </form>
      <Box mt={8}>
        <RouterLink to="/forgot-password">Forgot password?</RouterLink>
      </Box>
      <Box mt={4}>
        Don't have an account? <RouterLink to="/register">Register</RouterLink>
      </Box>
    </Box>
  );
};

export default Login;