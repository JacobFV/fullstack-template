import React from 'react';
import { Box, Flex, Link, Text } from '@chakra-ui/react';
import { Link as RouterLink } from '@tanstack/react-router';

const Footer: React.FC = () => {
  return (
    <Box as="footer" bg="gray.100" py={8}>
      <Flex justify="space-between" align="center" maxW="container.lg" mx="auto">
        <Text>&copy; {new Date().getFullYear()} GOTCHA. All rights reserved.</Text>
        <Flex>
          <Link as={RouterLink} to="/privacy-policy" ml={4}>
            Privacy Policy
          </Link>
          <Link as={RouterLink} to="/terms-of-service" ml={4}>
            Terms of Service
          </Link>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Footer;