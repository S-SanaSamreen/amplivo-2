import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  name: string;
  email: string;
  username?: string;
  role: 'admin' | 'client' | 'sales' | 'hr' | 'employee';
  company?: string;
  image?: string;
  is_active?: boolean;
  is_verified?: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string, refreshToken?: string) => void;
  logout: () => void;
  setToken: (token: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      login: (user, token, refreshToken = undefined) =>
        set({ user, token, refreshToken, isAuthenticated: true }),
      logout: () =>
        set({ user: null, token: null, refreshToken: null, isAuthenticated: false }),
      setToken: (token) => set({ token }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
