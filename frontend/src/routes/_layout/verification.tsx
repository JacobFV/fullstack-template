import React, { useState, useRef } from 'react';
import { Box, Heading, Text, FormControl, FormLabel, Input, Button, Flex, Progress } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { useMutation } from '@tanstack/react-query';
import { initiateVerification, completeVerification } from '../../services/api';
import Webcam from 'react-webcam';
import { useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { type UserPublic, UsersService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

export const Route = createFileRoute("/_layout/verification")({
  component: Verification,
})
type VerificationFormData = {
  fullName: string;
  documentType: string;
  documentNumber: string;
  expirationDate: string;
};

function Verification() {
  const [step, setStep] = useState(1);
  const [progress, setProgress] = useState(0);
  const { register, handleSubmit, formState: { errors } } = useForm<VerificationFormData>();
  const initiateVerificationMutation = useMutation(initiateVerification);
  const completeVerificationMutation = useMutation(completeVerification);
  const webcamRef = useRef<Webcam>(null);

  const onSubmit = (data: VerificationFormData) => {
    initiateVerificationMutation.mutate(data, {
      onSuccess: () => {
        setStep(2);
      },
    });
  };

  const handleCapture = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      // Send the captured image to the backend via WebSocket
      const socket = new WebSocket('ws://localhost:8000/face_image_match_detection/ws/1');
      socket.onopen = () => {
        socket.send(imageSrc);
      };
      socket.onmessage = (event) => {
        console.log('Received message:', event.data);
        setProgress(100);
        setTimeout(() => {
          setStep(3);
        }, 1000);
      };
    }
  };

  const handleComplete = () => {
    completeVerificationMutation.mutate(undefined, {
      onSuccess: () => {
        setStep(4);
      },
    });
  };

  return (
    <Box maxW="container.lg" mx="auto" py={8}>
      <Heading as="h1" size="xl" mb={8}>
        Verification
      </Heading>
      {step === 1 && (
        <Box>
          <Heading as="h2" size="lg" mb={4}>
            Step 1: Personal Information
          </Heading>
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormControl id="fullName" mb={4}>
              <FormLabel>Full Name</FormLabel>
              <Input type="text" {...register('fullName', { required: 'Full name is required' })} />
              {errors.fullName && <Text color="red.500">{errors.fullName.message}</Text>}
            </FormControl>
            <FormControl id="documentType" mb={4}>
              <FormLabel>Document Type</FormLabel>
              <Input type="text" {...register('documentType', { required: 'Document type is required' })} />
              {errors.documentType && <Text color="red.500">{errors.documentType.message}</Text>}
            </FormControl>
            <FormControl id="documentNumber" mb={4}>
              <FormLabel>Document Number</FormLabel>
              <Input type="text" {...register('documentNumber', { required: 'Document number is required' })} />
              {errors.documentNumber && <Text color="red.500">{errors.documentNumber.message}</Text>}
            </FormControl>
            <FormControl id="expirationDate" mb={4}>
              <FormLabel>Expiration Date</FormLabel>
              <Input type="date" {...register('expirationDate', { required: 'Expiration date is required' })} />
              {errors.expirationDate && <Text color="red.500">{errors.expirationDate.message}</Text>}
            </FormControl>
            <Button type="submit" colorScheme="blue" isLoading={initiateVerificationMutation.isLoading}>
              Next
            </Button>
          </form>
        </Box>
      )}
      {step === 2 && (
        <Box>
          <Heading as="h2" size="lg" mb={4}>
            Step 2: Capture Photo
          </Heading>
          <Flex justify="center" align="center" direction="column">
            <Box borderWidth={2} borderRadius="md" p={4} mb={4}>
              <Webcam ref={webcamRef} />
            </Box>
            <Button onClick={handleCapture} colorScheme="blue">
              Capture
            </Button>
          </Flex>
          <Progress value={progress} mt={8} />
        </Box>
      )}
      {step === 3 && (
        <Box>
          <Heading as="h2" size="lg" mb={4}>
            Step 3: Complete Verification
          </Heading>
          <Text mb={4}>Please review the captured information and submit for verification.</Text>
          <Button onClick={handleComplete} colorScheme="blue" isLoading={completeVerificationMutation.isLoading}>
            Complete Verification
          </Button>
        </Box>
      )}
      {step === 4 && (
        <Box>
          <Heading as="h2" size="lg" mb={4}>
            Verification Complete
          </Heading>
          <Text mb={4}>Thank you for completing the verification process. Your information has been submitted successfully.</Text>
          <Button onClick={() => setStep(1)}>Start Over</Button>
        </Box>
      )}
    </Box>
  );
};

export default Verification;