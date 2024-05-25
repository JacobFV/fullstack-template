export const isValidEmail = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const isValidPassword = (password: string) => password.length >= 8;

export const isValidName = (name: string) => name.trim().length > 0;

export const isValidDocumentNumber = (documentNumber: string) =>
  documentNumber.trim().length > 0;

export const isValidDate = (date: string) => {
  const currentDate = new Date();
  const selectedDate = new Date(date);
  return selectedDate > currentDate;
};

export const isValidMessage = (message: string) => message.trim().length > 0;
