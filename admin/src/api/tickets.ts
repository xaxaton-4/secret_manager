import { api } from '@/core/api';
import { Ticket } from '@/types/tickets';

export const getTickets = async () => {
  const { data } = await api.get<Ticket[]>('/api/tickets/list/', { params: { limit: 1000 } });
  return data;
};

export const approveTicket = async (id: number) => {
  await api.post('/api/tickets/modify/', {
    ticket_id: id,
    is_approved: true,
  });
};

export const deleteTicket = async (id: number, reason?: string) => {
  await api.post('/api/tickets/delete/', {
    ticket_id: id,
    reason,
  });
};
