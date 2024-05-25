import React from 'react';
import { Box, Heading, Text } from '@chakra-ui/react';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/terms-of-service")({
  component: TermsOfService,
})
function TermsOfService() {
  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Terms of Service
      </Heading>
      <Text mb={4}>
        Welcome to GOTCHA, an identity verification platform. By accessing or using our services, you agree to be bound by these Terms of Service ("Terms") and our Privacy Policy. If you do not agree to these Terms, please do not use our services.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        1. Service Description
      </Heading>
      <Text mb={4}>
        GOTCHA provides identity verification services to businesses and individuals who require secure and reliable verification of user identities. Our services include collecting and verifying personal information, biometric data, and government-issued identification documents.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        2. User Responsibilities
      </Heading>
      <Text mb={4}>
        When using our services, you agree to:
        <ul>
          <li>Provide accurate, current, and complete information about yourself</li>
          <li>Maintain the confidentiality of your account credentials</li>
          <li>Use our services only for lawful purposes and in compliance with applicable laws and regulations</li>
          <li>Not attempt to circumvent our security measures or interfere with the proper functioning of our services</li>
        </ul>
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        3. Intellectual Property
      </Heading>
      <Text mb={4}>
        All intellectual property rights related to our services, including trademarks, logos, and copyrights, are the property of GOTCHA or its licensors. You may not use, reproduce, or distribute any of our intellectual property without our prior written consent.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        4. Limitation of Liability
      </Heading>
      <Text mb={4}>
        In no event shall GOTCHA be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or in connection with your use of our services. Our total liability to you for any claims under these Terms shall not exceed the amount paid by you for our services in the preceding twelve (12) months.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        5. Termination
      </Heading>
      <Text mb={4}>
        We reserve the right to suspend or terminate your access to our services at any time, without prior notice, for any reason, including if we reasonably believe you have violated these Terms or our Privacy Policy.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        6. Governing Law
      </Heading>
      <Text mb={4}>
        These Terms shall be governed by and construed in accordance with the laws of [Jurisdiction]. Any disputes arising under these Terms shall be subject to the exclusive jurisdiction of the courts located in [Jurisdiction].
      </Text>
      <Text>
        We may update these Terms from time to time. The most current version will always be available on our website. By continuing to use our services after any changes to these Terms, you agree to be bound by the revised Terms.
      </Text>
    </Box>
  );
};

export default TermsOfService;