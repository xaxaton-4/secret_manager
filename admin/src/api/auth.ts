import { api } from '@/core/api';
import { AuthParams } from '@/types/auth';
import { User } from '@/types/users';

export const login = async (params: AuthParams) => {
  const { data } = await api.post<{
    token: string;
    user: User;
  }>('/api/login/', params);
  return data;
};

export const auth = async () => {
  const { data } = await api.get<User>('/api/auth/');
  return data;
};
