import { api } from '@/core/api';
import { Secret } from '@/types/secrets';

export const getSecret = async (resource: string) => {
  const { data } = await api.get<Secret>(`/secrets/${resource}`);
  return data;
};
