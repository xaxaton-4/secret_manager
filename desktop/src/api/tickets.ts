import { api } from '@/core/api';
import { CreateTicketParams } from '@/types/tickets';

export const createTicket = async (params: CreateTicketParams) => {
  await api.post('/api/tickets/create/', params);
};
