import React from 'react';
import { Box, Button, Heading, Text } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/home")({
  component: Home,
})
function Home() {
  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={4}>
        Welcome to GOTCHA
      </Heading>
      <Text fontSize="xl" mb={8}>
        The ultimate Graphical Online Turing test to Confirm Human Activity.
      </Text>
      <Button as={RouterLink} to="/playground" colorScheme="blue" size="lg">
        Try it out
      </Button>
    </Box>
  );
};

export default Home;