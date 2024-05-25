import React from 'react';
import { Box, Heading, Text } from '@chakra-ui/react';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/privacy-policy")({
  component: PrivacyPolicy,
})
function PrivacyPolicy() {
  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Privacy Policy
      </Heading>
      <Text mb={4}>
        At GOTCHA, we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy outlines how we collect, use, and safeguard the data you provide to us when using our identity verification services.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        Information We Collect
      </Heading>
      <Text mb={4}>
        When you use our identity verification services, we may collect the following information:
        <ul>
          <li>Full name</li>
          <li>Email address</li>
          <li>Phone number</li>
          <li>Date of birth</li>
          <li>Government-issued identification documents (e.g., passport, driver's license)</li>
          <li>Biometric data (e.g., facial images, fingerprints)</li>
        </ul>
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        How We Use Your Information
      </Heading>
      <Text mb={4}>
        We use the information we collect to provide and improve our identity verification services, ensure the security of our platform, and comply with legal and regulatory requirements. Specifically, we may use your information for the following purposes:
        <ul>
          <li>Verify your identity and prevent fraudulent activities</li>
          <li>Communicate with you about our services and respond to your inquiries</li>
          <li>Analyze and improve our services and user experience</li>
          <li>Enforce our terms of service and other policies</li>
        </ul>
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        Data Security
      </Heading>
      <Text mb={4}>
        We take the security of your personal information seriously and implement appropriate technical and organizational measures to protect your data from unauthorized access, alteration, disclosure, or destruction. We use industry-standard encryption technologies to safeguard your sensitive information during transmission and storage.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        Data Retention
      </Heading>
      <Text mb={4}>
        We retain your personal information only for as long as necessary to fulfill the purposes for which it was collected, comply with legal obligations, resolve disputes, and enforce our agreements. Once the retention period expires, we securely delete or anonymize your data.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        Third-Party Disclosure
      </Heading>
      <Text mb={4}>
        We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this Privacy Policy. We may share your information with trusted third-party service providers who assist us in operating our services, subject to confidentiality obligations.
      </Text>
      <Heading as="h2" size="lg" mb={4}>
        Your Rights
      </Heading>
      <Text mb={4}>
        You have the right to access, update, and delete your personal information. If you wish to exercise any of these rights or have any questions or concerns about our Privacy Policy, please contact us at privacy@gotcha.com.
      </Text>
      <Text>
        By using our identity verification services, you acknowledge that you have read and understood this Privacy Policy and agree to the collection, use, and storage of your personal information as described herein.
      </Text>
    </Box>
  );
};

export default PrivacyPolicy;