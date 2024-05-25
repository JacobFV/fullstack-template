import React from 'react';
import { Box, Heading, Text, FormControl, FormLabel, Input, Button, AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { useQuery, useMutation } from '@tanstack/react-query';
import { getUserSettings, updateUserSettings, changePassword, exportData, deleteAccount } from '../services/api';

type UserInfoFormData = {
  name: string;
  email: string;
};

type ChangePasswordFormData = {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
};

const Settings: React.FC = () => {
  const { data: userSettings, isLoading, error } = useQuery(['userSettings'], getUserSettings);
  const { register: registerUserInfo, handleSubmit: handleSubmitUserInfo, formState: { errors: userInfoErrors } } = useForm<UserInfoFormData>();
  const { register: registerChangePassword, handleSubmit: handleSubmitChangePassword, formState: { errors: changePasswordErrors } } = useForm<ChangePasswordFormData>();
  const updateUserInfoMutation = useMutation(updateUserSettings);
  const changePasswordMutation = useMutation(changePassword);
  const exportDataMutation = useMutation(exportData);
  const deleteAccountMutation = useMutation(deleteAccount);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = React.useState(false);

  const onSubmitUserInfo = (data: UserInfoFormData) => {
    updateUserInfoMutation.mutate(data);
  };

  const onSubmitChangePassword = (data: ChangePasswordFormData) => {
    if (data.newPassword !== data.confirmPassword) {
      // Handle password mismatch error
      return;
    }
    changePasswordMutation.mutate(data);
  };

  const handleExportData = () => {
    exportDataMutation.mutate();
  };

  const handleDeleteAccount = () => {
    deleteAccountMutation.mutate();
  };

  const openDeleteDialog = () => {
    setIsDeleteDialogOpen(true);
  };

  const closeDeleteDialog = () => {
    setIsDeleteDialogOpen(false);
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
        Settings
      </Heading>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          User Information
        </Heading>
        <form onSubmit={handleSubmitUserInfo(onSubmitUserInfo)}>
          <FormControl id="name" mb={4}>
            <FormLabel>Name</FormLabel>
            <Input type="text" defaultValue={userSettings.name} {...registerUserInfo('name', { required: 'Name is required' })} />
            {userInfoErrors.name && <Text color="red.500">{userInfoErrors.name.message}</Text>}
          </FormControl>
          <FormControl id="email" mb={4}>
            <FormLabel>Email</FormLabel>
            <Input type="email" defaultValue={userSettings.email} {...registerUserInfo('email', { required: 'Email is required' })} />
            {userInfoErrors.email && <Text color="red.500">{userInfoErrors.email.message}</Text>}
          </FormControl>
          <Button type="submit" colorScheme="blue" isLoading={updateUserInfoMutation.isLoading}>
            Save Changes
          </Button>
        </form>
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Change Password
        </Heading>
        <form onSubmit={handleSubmitChangePassword(onSubmitChangePassword)}>
          <FormControl id="currentPassword" mb={4}>
            <FormLabel>Current Password</FormLabel>
            <Input type="password" {...registerChangePassword('currentPassword', { required: 'Current password is required' })} />
            {changePasswordErrors.currentPassword && <Text color="red.500">{changePasswordErrors.currentPassword.message}</Text>}
          </FormControl>
          <FormControl id="newPassword" mb={4}>
            <FormLabel>New Password</FormLabel>
            <Input type="password" {...registerChangePassword('newPassword', { required: 'New password is required' })} />
            {changePasswordErrors.newPassword && <Text color="red.500">{changePasswordErrors.newPassword.message}</Text>}
          </FormControl>
          <FormControl id="confirmPassword" mb={4}>
            <FormLabel>Confirm Password</FormLabel>
            <Input type="password" {...registerChangePassword('confirmPassword', { required: 'Confirm password is required' })} />
            {changePasswordErrors.confirmPassword && <Text color="red.500">{changePasswordErrors.confirmPassword.message}</Text>}
          </FormControl>
          <Button type="submit" colorScheme="blue" isLoading={changePasswordMutation.isLoading}>
            Change Password
          </Button>
        </form>
      </Box>
      <Box mb={8}>
        <Heading as="h2" size="lg" mb={4}>
          Export Data
        </Heading>
        <Text mb={4}>Export your account data.</Text>
        <Button onClick={handleExportData} isLoading={exportDataMutation.isLoading}>
          Export Data
        </Button>
      </Box>
      <Box>
        <Heading as="h2" size="lg" mb={4}>
          Delete Account
        </Heading>
        <Text mb={4}>Permanently delete your account and all associated data.</Text>
        <Button colorScheme="red" onClick={openDeleteDialog}>
          Delete Account
        </Button>
      </Box>

      <AlertDialog isOpen={isDeleteDialogOpen} onClose={closeDeleteDialog}>
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Delete Account
            </AlertDialogHeader>
            <AlertDialogBody>
              Are you sure you want to delete your account? This action cannot be undone.
            </AlertDialogBody>
            <AlertDialogFooter>
              <Button onClick={closeDeleteDialog}>Cancel</Button>
              <Button colorScheme="red" onClick={handleDeleteAccount} ml={3} isLoading={deleteAccountMutation.isLoading}>
                Delete
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  );
};

export default Settings;