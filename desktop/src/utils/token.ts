export const getToken = () => {
  const auth = localStorage.getItem('auth');
  if (!auth) return null;

  const { token } = JSON.parse(auth);

  return token as string;
};
