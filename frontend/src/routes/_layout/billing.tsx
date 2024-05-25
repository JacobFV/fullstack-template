import React from 'react';
import { Box, Heading, Text, Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { getBillingData } from '../../services/api';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/billing")({
  component: Billing,
})
function Billing() {
  const { data: billingData, isLoading, error } = useQuery(['billingData'], getBillingData);

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (error) {
    return <Text>Error: {error.message}</Text>;
  }

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Billing
      </Heading>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Billing History
        </Heading>
        <Table>
          <Thead>
            <Tr>
              <Th>Date</Th>
              <Th>Amount</Th>
              <Th>Status</Th>
            </Tr>
          </Thead>
          <Tbody>
            {billingData.history.map((item) => (
              <Tr key={item.id}>
                <Td>{item.date}</Td>
                <Td>{item.amount}</Td>
                <Td>{item.status}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          Billing Information
        </Heading>
        <Text>Current Plan: {billingData.currentPlan}</Text>
        <Text>Next Billing Date: {billingData.nextBillingDate}</Text>
      </Box>
    </Box>
  );
};

export default Billing;