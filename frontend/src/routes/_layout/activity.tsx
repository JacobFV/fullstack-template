import React from 'react';
import { Box, Heading, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { getVerificationHistory } from '../../services/api';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/activity")({
  component: Activity,
})

function Activity() {
  const { data: verificationHistory, isLoading, error } = useQuery(['verificationHistory'], getVerificationHistory);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Activity
      </Heading>
      <Table>
        <Thead>
          <Tr>
            <Th>Date</Th>
            <Th>Verification ID</Th>
            <Th>Status</Th>
          </Tr>
        </Thead>
        <Tbody>
          {verificationHistory.map((item) => (
            <Tr key={item.id}>
              <Td>{item.date}</Td>
              <Td>{item.verificationId}</Td>
              <Td>{item.status}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default Activity;