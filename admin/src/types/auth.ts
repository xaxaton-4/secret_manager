import { User } from './users';

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isReady: boolean;
}

export interface AuthParams {
  email: string;
  password: string;
}
