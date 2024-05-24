import React from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const ForgotPassword: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle forgot password form submission
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Forgot Password
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="email" mb={8}>
          <FormLabel>Email address</FormLabel>
          <Input type="email" />
        </FormControl>
        <Button type="submit" colorScheme="blue" size="lg" width="full">
          Reset Password
        </Button>
      </form>
      <Box mt={8}>
        Remember your password? <RouterLink to="/login">Login</RouterLink>
      </Box>
    </Box>
  );
};

export default ForgotPassword;