import { api } from '@/core/api';
import { Ticket } from '@/types/tickets';

export const getTickets = async () => {
  const { data } = await api.get<Ticket[]>('/tickets');
  return data;
};
