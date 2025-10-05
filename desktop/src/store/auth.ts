import { defineStore } from 'pinia';
import { auth, login } from '@/api/auth';
import { toast } from '@/main';
import { AuthParams, AuthState } from '@/types/auth';

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isLoading: false,
    isReady: false,
  }),
  persist: {
    pick: ['token'],
  },
  getters: {
    isAuth: (state) => Boolean(state.user),
  },
  actions: {
    async login(params: AuthParams) {
      this.isLoading = true;
      try {
        const { token, user } = await login(params);

        this.token = token;
        this.user = user;

        toast.add({
          severity: 'success',
          summary: 'Вы успешно авторизовались',
          life: 3000,
        });
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось авторизоваться',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
    async auth() {
      try {
        if (this.token) {
          const user = await auth();
          this.user = user;
        }
      } finally {
        this.isReady = true;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      toast.add({
        severity: 'success',
        summary: 'Вы успешно вышли',
        life: 3000,
      });
    },
  },
});
