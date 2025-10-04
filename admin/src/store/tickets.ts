import { defineStore } from 'pinia';
import { getTickets } from '@/api/tickets';
import { toast } from '@/main';
import { TicketsState } from '@/types/tickets';

export const useTicketsStore = defineStore('tickets', {
  state: (): TicketsState => ({
    tickets: [],
    isLoading: false,
  }),
  actions: {
    async getTickets() {
      this.isLoading = true;
      try {
        this.tickets = await getTickets();
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось загрузить заявки',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
