import React from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const ResetPassword: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle reset password form submission
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Reset Password
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="password" mb={4}>
          <FormLabel>New Password</FormLabel>
          <Input type="password" />
        </FormControl>
        <FormControl id="confirmPassword" mb={8}>
          <FormLabel>Confirm Password</FormLabel>
          <Input type="password" />
        </FormControl>
        <Button type="submit" colorScheme="blue" size="lg" width="full">
          Reset Password
        </Button>
      </form>
      <Box mt={8}>
        <RouterLink to="/login">Back to Login</RouterLink>
      </Box>
    </Box>
  );
};

export default ResetPassword;