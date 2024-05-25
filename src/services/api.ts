import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
});

export const login = async (data: { email: string; password: string }) => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const register = async (data: { name: string; email: string; password: string }) => {
  const response = await api.post('/auth/register', data);
  return response.data;
};

export const forgotPassword = async (data: { email: string }) => {
  const response = await api.post('/auth/forgot-password', data);
  return response.data;
};

export const resetPassword = async (data: { token: string; password: string }) => {
  const response = await api.post('/auth/reset-password', data);
  return response.data;
};

export const getAccount = async () => {
  const response = await api.get('/account');
  return response.data;
};

export const getPlaygroundData = async () => {
  const response = await api.get('/playground');
  return response.data;
};

export const getVerificationHistory = async () => {
  const response = await api.get('/verification/history');
  return response.data;
};

export const getBillingData = async () => {
  const response = await api.get('/billing');
  return response.data;
};

export const getAPIKeys = async () => {
  const response = await api.get('/api-keys');
  return response.data;
};

export const createAPIKey = async () => {
  const response = await api.post('/api-keys');
  return response.data;
};

export const revokeAPIKey = async (keyId: string) => {
  const response = await api.delete(`/api-keys/${keyId}`);
  return response.data;
};

export const getUserSettings = async () => {
  const response = await api.get('/settings');
  return response.data;
};

export const updateUserSettings = async (data: { name: string; email: string }) => {
  const response = await api.put('/settings', data);
  return response.data;
};

export const changePassword = async (data: { currentPassword: string; newPassword: string }) => {
  const response = await api.post('/settings/change-password', data);
  return response.data;
};

export const exportData = async () => {
  const response = await api.post('/settings/export-data');
  return response.data;
};

export const deleteAccount = async () => {
  const response = await api.delete('/settings/delete-account');
  return response.data;
};

export const getVerificationRequest = async () => {
  const response = await api.get('/verification/request');
  return response.data;
};

export const initiateVerification = async (data: {
  fullName: string;
  documentType: string;
  documentNumber: string;
  expirationDate: string;
}) => {
  const response = await api.post('/verification/initiate', data);
  return response.data;
};

export const completeVerification = async () => {
  const response = await api.post('/verification/complete');
  return response.data;
};

export const streamVideo = async (verificationRequestId: number, videoChunk: Blob) => {
  const formData = new FormData();
  formData.append('video', videoChunk);
  const response = await api.post(`/face_image_match_detection/video/${verificationRequestId}`, formData);
  return response.data;
};