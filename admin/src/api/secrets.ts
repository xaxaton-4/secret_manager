import { api } from '@/core/api';
import { Secret } from '@/types/secrets';

export const createSecret = async (params: Secret) => {
  return await api.post('/secrets', params);
};
