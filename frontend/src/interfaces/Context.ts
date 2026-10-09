import type { User } from "./User";

export interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (token: string, userData: User) => void;
  logout: () => void;
}

export interface LayoutContextType {
  setPageTitle: (title: string) => void;
}
