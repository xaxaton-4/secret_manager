import { api } from '@/core/api';

export const getSecrets = async () => {
  const { data } = await api.get<string[]>('/api/secrets/list/');
  return data;
};

export const getSecret = async (resource: string) => {
  const { data } = await api.get<{ value: string }>('/api/secrets/detail/', {
    params: { resource },
  });
  return data;
};
