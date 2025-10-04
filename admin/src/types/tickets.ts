import { User } from './users';

export interface TicketsState {
  tickets: Ticket[];
  isLoading: boolean;
}

export interface Ticket {
  id: number;
  resource: string;
  reason: string;
  period: string;
  is_approved: boolean;
  user: User;
}
