import { defineStore } from 'pinia';
import { getSecret } from '@/api/secrets';
import { toast } from '@/main';
import { SecretsState } from '@/types/secrets';

export const useSecretsStore = defineStore('secrets', {
  state: (): SecretsState => ({
    secrets: {},
    currentSecret: null,
    isLoading: false,
  }),
  persist: {
    pick: ['secrets'],
  },
  actions: {
    async getSecret(resource: string) {
      this.isLoading = true;
      this.currentSecret = null;
      try {
        const localSecret = this.secrets[resource];
        if (localSecret) {
          this.currentSecret = {
            resource,
            value: localSecret,
          };
          toast.add({
            severity: 'success',
            summary: 'Найден локальный секрет',
            life: 3000,
          });
          getSecret(resource).then((secret) => {
            this.currentSecret = secret;
          });
        } else {
          this.currentSecret = await getSecret(resource);
          toast.add({
            severity: 'success',
            summary: 'Найден секрет на сервере',
            life: 3000,
          });
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось найти секрет',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
