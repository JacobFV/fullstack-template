import React from 'react';
import { Box, Flex, Link } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from '@tanstack/react-router';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <Box as="nav" bg="gray.100" py={4}>
      <Flex justify="space-between" align="center" maxW="container.lg" mx="auto">
        <Link as={RouterLink} to="/" fontWeight="bold">
          GOTCHA
        </Link>
        <Flex>
          <Link
            as={RouterLink}
            to="/account"
            ml={4}
            fontWeight={location.pathname === '/account' ? 'bold' : 'normal'}
          >
            Account
          </Link>
          <Link
            as={RouterLink}
            to="/playground"
            ml={4}
            fontWeight={location.pathname === '/playground' ? 'bold' : 'normal'}
          >
            Playground
          </Link>
          <Link
            as={RouterLink}
            to="/docs"
            ml={4}
            fontWeight={location.pathname === '/docs' ? 'bold' : 'normal'}
          >
            Documentation
          </Link>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navigation;