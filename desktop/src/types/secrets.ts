export interface SecretsState {
  secrets: Record<string, string>;
  secretsList: string[];
  secretsVisible: Record<string, boolean>;
  secretsLoading: Record<string, boolean>;
  isLoading: boolean;
}

export interface Secret {
  resource: string;
  value: string;
}
