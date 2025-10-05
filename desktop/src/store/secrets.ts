import { defineStore } from 'pinia';
import { getSecret, getSecrets } from '@/api/secrets';
import { toast } from '@/main';
import { SecretsState } from '@/types/secrets';

export const useSecretsStore = defineStore('secrets', {
  state: (): SecretsState => ({
    secrets: {},
    secretsList: [],
    secretsVisible: {},
    secretsLoading: {},
    isLoading: false,
  }),
  persist: {
    pick: ['secrets', 'secretsList'],
  },
  actions: {
    async getSecrets() {
      this.isLoading = true;
      try {
        this.secretsList = await getSecrets();
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось найти секреты',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
    async getSecret(resource: string) {
      this.secretsLoading[resource] = true;
      try {
        const localSecret = this.secrets[resource];
        if (localSecret) {
          toast.add({
            severity: 'success',
            summary: 'Найден локальный секрет',
            life: 3000,
          });
          getSecret(resource).then((secret) => {
            this.secrets[resource] = secret.value;
          });
        } else {
          const secret = await getSecret(resource);
          this.secrets[resource] = secret.value;
          toast.add({
            severity: 'success',
            summary: 'Найден секрет на сервере',
            life: 3000,
          });
        }
        this.secretsVisible[resource] = true;
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось найти секрет',
          life: 3000,
        });
      } finally {
        this.secretsLoading[resource] = true;
      }
    },
  },
});
