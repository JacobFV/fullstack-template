export const isValidEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const isValidPassword = (password: string) => {
  return password.length >= 8;
};

export const isValidName = (name: string) => {
  return name.trim().length > 0;
};

export const isValidDocumentNumber = (documentNumber: string) => {
  return documentNumber.trim().length > 0;
};

export const isValidExpirationDate = (expirationDate: string) => {
  const currentDate = new Date();
  const selectedDate = new Date(expirationDate);
  return selectedDate > currentDate;
};