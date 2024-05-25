import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Heading, Input, Text } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';
import { useMutation } from '@tanstack/react-query';
import { forgotPassword } from '../../services/api';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/forgot-password")({
  component: ForgotPassword,
})
function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const { mutate: forgotPasswordMutation, isLoading, error } = useMutation(forgotPassword, {
    onSuccess: () => {
      setSuccessMessage('Password reset email sent. Please check your inbox.');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    forgotPasswordMutation({ email });
  };

  return (
    <Box maxW="container.sm" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Forgot Password
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="email" mb={8}>
          <FormLabel>Email address</FormLabel>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </FormControl>
        {error && (
          <Text color="red.500" mb={4}>
            {error.message}
          </Text>
        )}
        {successMessage && (
          <Text color="green.500" mb={4}>
            {successMessage}
          </Text>
        )}
        <Button type="submit" colorScheme="blue" size="lg" width="full" isLoading={isLoading}>
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