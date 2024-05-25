import React from 'react';
import { Box, Heading, Text } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { getAccount } from '../../services/api';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/account")({
  component: Account,
})

function Account() {
  const { data: account, isLoading, error } = useQuery(['account'], getAccount);

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (error) {
    return <Text>Error: {error.message}</Text>;
  }

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Account
      </Heading>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Email Verification
        </Heading>
        {account.emailVerified ? (
          <Text>Your email is verified.</Text>
        ) : (
          <Text>Please verify your email address.</Text>
        )}
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Playground
        </Heading>
        <Text>Access the playground to test the verification system.</Text>
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Activity History
        </Heading>
        <Text>View your verification activity history.</Text>
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Billing
        </Heading>
        <Text>Manage your billing information and subscription.</Text>
      </Box>
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          API Keys
        </Heading>
        <Text>Generate and manage your API keys.</Text>
      </Box>
    </Box>
  );
};

export default Account;