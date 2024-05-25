export const APP_NAME = 'GOTCHA';
export const APP_DESCRIPTION = 'Graphical Online Turing test to Confirm Human Activity';
export const APP_VERSION = '1.0.0';

export const VERIFICATION_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
};

export const API_KEY_PERMISSIONS = {
  READ: 'read',
  WRITE: 'write',
  ADMIN: 'admin',
};

export const USER_ROLES = {
  USER: 'user',
  ADMIN: 'admin',
};

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const PASSWORD_MIN_LENGTH = 8;
export const NAME_MAX_LENGTH = 50;
export const DOCUMENT_NUMBER_MAX_LENGTH = 20;