import { defineStore } from 'pinia';
import { createSecret } from '@/api/secrets';
import { toast } from '@/main';
import { Secret, SecretsState } from '@/types/secrets';

export const useSecretsStore = defineStore('secrets', {
  state: (): SecretsState => ({
    isLoading: false,
  }),
  actions: {
    async createSecret(params: Secret) {
      this.isLoading = true;
      try {
        await createSecret(params);
        toast.add({
          severity: 'success',
          summary: 'Секрет успешно создан',
          life: 3000,
        });
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось создать секрет',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
