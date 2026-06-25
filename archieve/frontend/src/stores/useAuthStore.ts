import { create } from 'zustand';

interface AuthState {
  token: string | null;
  user: any | null;
  permissions: string[];
  setAuth: (token: string, user: any, permissions: string[]) => void;
  logout: () => void;
  hasPermission: (perm: string) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem('token'),
  user: null,
  permissions: [],
  setAuth: (token, user, permissions) => {
    localStorage.setItem('token', token);
    set({ token, user, permissions });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null, permissions: [] });
  },
  hasPermission: (perm) => {
    // In dev mode without a real token, mock true
    if (process.env.NODE_ENV === 'development' && !get().token) return true;
    return get().permissions.includes(perm);
  }
}));
