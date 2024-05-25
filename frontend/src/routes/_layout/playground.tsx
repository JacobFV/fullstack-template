import React from 'react';
import { Box, Button, Heading, Text, FormControl, FormLabel, Input, Textarea } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { useQuery } from '@tanstack/react-query';
import { getPlaygroundData } from '../../services/api';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/playground")({
  component: Playground,
})
type FormData = {
  name: string;
  email: string;
  message: string;
};

function Playground() {
  const { data: playgroundData, isLoading, error } = useQuery(['playgroundData'], getPlaygroundData);
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();

  const onSubmit = (data: FormData) => {
    // Handle form submission
    console.log(data);
  };

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (error) {
    return <Text>Error: {error.message}</Text>;
  }

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Playground
      </Heading>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Embedded Form
        </Heading>
        <form onSubmit={handleSubmit(onSubmit)}>
          <FormControl id="name" mb={4}>
            <FormLabel>Name</FormLabel>
            <Input type="text" {...register('name', { required: 'Name is required' })} />
            {errors.name && <Text color="red.500">{errors.name.message}</Text>}
          </FormControl>
          <FormControl id="email" mb={4}>
            <FormLabel>Email</FormLabel>
            <Input type="email" {...register('email', { required: 'Email is required' })} />
            {errors.email && <Text color="red.500">{errors.email.message}</Text>}
          </FormControl>
          <FormControl id="message" mb={4}>
            <FormLabel>Message</FormLabel>
            <Textarea {...register('message', { required: 'Message is required' })} />
            {errors.message && <Text color="red.500">{errors.message.message}</Text>}
          </FormControl>
          <Button type="submit" colorScheme="blue">
            Submit
          </Button>
        </form>
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Playground Code
        </Heading>
        <Button onClick={() => navigator.clipboard.writeText(playgroundData.code)}>
          Copy Code
        </Button>
      </Box>
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          API Keys
        </Heading>
        <Text>Your API Key: {playgroundData.apiKey}</Text>
      </Box>
    </Box>
  );
};

export default Playground;