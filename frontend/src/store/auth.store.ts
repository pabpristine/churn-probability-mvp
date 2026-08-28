import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, AuthTokens, LoginCredentials } from '@/types';

// ============================================================
// Auth Store
// ============================================================

interface AuthStore {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  setTokens: (tokens: AuthTokens | null) => void;
  setIsLoading: (loading: boolean) => void;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) =>
        set({ user, isAuthenticated: !!user }),

      setTokens: (tokens) => {
        set({ tokens });
        if (tokens) {
          localStorage.setItem('access_token', tokens.accessToken);
          localStorage.setItem('refresh_token', tokens.refreshToken);
        } else {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      },

      setIsLoading: (isLoading) => set({ isLoading }),

      login: async (_credentials: LoginCredentials) => {
        set({ isLoading: true });
        // Implementation deferred — wired in auth module
        set({ isLoading: false });
      },

      logout: () => {
        set({ user: null, tokens: null, isAuthenticated: false });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      },

      refreshUser: async () => {
        // Implementation deferred — wired in auth module
      },
    }),
    {
      name: 'd2d-auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user, tokens: state.tokens, isAuthenticated: state.isAuthenticated }),
    }
  )
);
