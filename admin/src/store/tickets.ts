import { defineStore } from 'pinia';
import { approveTicket, getTickets } from '@/api/tickets';
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
    async approveTicket(id: number) {
      this.isLoading = true;
      try {
        await approveTicket(id);
        this.tickets = this.tickets.filter((ticket) => ticket.id !== id);
        toast.add({
          severity: 'success',
          summary: 'Заявка успешно принята',
          life: 3000,
        });
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось принять заявку',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
