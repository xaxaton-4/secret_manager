export enum Role {
  User = 'user',
  Admin = 'admin',
}

export interface User {
  id: number;
  email: string;
  role: Role;
}
