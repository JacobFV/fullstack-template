import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input, Text } from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from '@tanstack/react-router';
import { useMutation } from '@tanstack/react-query';
import { login } from '../../services/api';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const { mutate: loginMutation, isLoading, error } = useMutation(login, {
    onSuccess: () => {
      navigate('/account');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loginMutation({ email, password });
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Login
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="email" mb={4}>
          <FormLabel>Email address</FormLabel>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </FormControl>
        <FormControl id="password" mb={8}>
          <FormLabel>Password</FormLabel>
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </FormControl>
        {error && (
          <Text color="red.500" mb={4}>
            {error.message}
          </Text>
        )}
        <Button type="submit" colorScheme="blue" size="lg" width="full" isLoading={isLoading}>
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