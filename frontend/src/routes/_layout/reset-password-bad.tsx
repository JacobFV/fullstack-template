import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input, Text } from '@chakra-ui/react';
import { Link as RouterLink, useNavigate, useSearch } from '@tanstack/react-router';
import { useMutation } from '@tanstack/react-query';
import { resetPassword } from '../../services/api';

const ResetPassword: React.FC = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const search = useSearch();
  const token = search.token as string;

  const { mutate: resetPasswordMutation, isLoading, error } = useMutation(resetPassword, {
    onSuccess: () => {
      navigate('/login');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    resetPasswordMutation({ token, password });
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Reset Password
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="password" mb={4}>
          <FormLabel>New Password</FormLabel>
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </FormControl>
        <FormControl id="confirmPassword" mb={8}>
          <FormLabel>Confirm Password</FormLabel>
          <Input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </FormControl>
        {error && (
          <Text color="red.500" mb={4}>
            {error.message}
          </Text>
        )}
        <Button type="submit" colorScheme="blue" size="lg" width="full" isLoading={isLoading}>
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