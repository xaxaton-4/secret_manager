export interface SecretsState {
  secrets: Record<string, string>;
  currentSecret: Secret | null;
  isLoading: boolean;
}

export interface Secret {
  resource: string;
  value: string;
}
