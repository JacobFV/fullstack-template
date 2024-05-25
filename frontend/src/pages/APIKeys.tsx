import React from 'react';
import { Box, Heading, Text, Button, Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { getAPIKeys, createAPIKey, revokeAPIKey } from '../services/api';

const APIKeys: React.FC = () => {
  const { data: apiKeys, isLoading, error, refetch } = useQuery(['apiKeys'], getAPIKeys);
  const createMutation = useMutation(createAPIKey, {
    onSuccess: () => {
      refetch();
    },
  });
  const revokeMutation = useMutation(revokeAPIKey, {
    onSuccess: () => {
      refetch();
    },
  });

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (error) {
    return <Text>Error: {error.message}</Text>;
  }

  const handleCreateAPIKey = () => {
    createMutation.mutate();
  };

  const handleRevokeAPIKey = (keyId: string) => {
    revokeMutation.mutate(keyId);
  };

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        API Keys
      </Heading>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Your API Keys
        </Heading>
        <Table>
          <Thead>
            <Tr>
              <Th>Key</Th>
              <Th>Created At</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {apiKeys.map((key) => (
              <Tr key={key.id}>
                <Td>{key.key}</Td>
                <Td>{key.createdAt}</Td>
                <Td>
                  <Button size="sm" onClick={() => handleRevokeAPIKey(key.id)}>
                    Revoke
                  </Button>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          Create New API Key
        </Heading>
        <Button onClick={handleCreateAPIKey} isLoading={createMutation.isLoading}>
          Create API Key
        </Button>
      </Box>
    </Box>
  );
};

export default APIKeys;