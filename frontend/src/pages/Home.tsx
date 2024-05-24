import React from 'react';
import { Box, Button, Heading, Text } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const Home: React.FC = () => {
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