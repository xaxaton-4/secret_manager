import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (req) => {
    const auth = localStorage.getItem('auth');
    if (!auth) return req;

    const { token } = JSON.parse(auth);
    if (!token) return req;

    req.headers.Authorization = `Bearer ${token}`;
    return req;
  },
  (err) => Promise.reject(err),
);
