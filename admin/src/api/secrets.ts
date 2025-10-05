import { api } from '@/core/api';
import { Secret } from '@/types/secrets';

export const createSecret = async (params: Secret) => {
  return await api.post('/api/secrets/create/', params);
};
