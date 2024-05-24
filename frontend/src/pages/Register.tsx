import React from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const Register: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle registration form submission
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Register
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="name" mb={4}>
          <FormLabel>Name</FormLabel>
          <Input type="text" />
        </FormControl>
        <FormControl id="email" mb={4}>
          <FormLabel>Email address</FormLabel>
          <Input type="email" />
        </FormControl>
        <FormControl id="password" mb={8}>
          <FormLabel>Password</FormLabel>
          <Input type="password" />
        </FormControl>
        <Button type="submit" colorScheme="blue" size="lg" width="full">
          Register
        </Button>
      </form>
      <Box mt={8}>
        Already have an account? <RouterLink to="/login">Login</RouterLink>
      </Box>
    </Box>
  );
};

export default Register;