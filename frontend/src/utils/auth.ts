import jwtDecode from 'jwt-decode';

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

export const setAccessToken = (token: string) => {
  localStorage.setItem('access_token', token);
};

export const removeAccessToken = () => {
  localStorage.removeItem('access_token');
};

export const isAuthenticated = () => {
  const token = getAccessToken();
  if (!token) {
    return false;
  }
  try {
    const decodedToken: any = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decodedToken.exp > currentTime;
  } catch (error) {
    return false;
  }
};

export const getUserRole = () => {
  const token = getAccessToken();
  if (!token) {
    return null;
  }
  try {
    const decodedToken: any = jwtDecode(token);
    return decodedToken.role;
  } catch (error) {
    return null;
  }
};