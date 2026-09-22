import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import * as auth from '../services/auth';
import type { LocalAccount } from '../services/auth';

interface AuthContextValue {
  account: LocalAccount | null;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => LocalAccount;
  signOut: () => void;
  signUp: (name: string, email: string, password: string) => LocalAccount;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [account, setAccount] = useState<LocalAccount | null>(() => auth.getSession());

  const signIn = useCallback((email: string, password: string) => {
    const next = auth.login(email, password);
    setAccount(next);
    return next;
  }, []);

  const signOut = useCallback(() => {
    auth.logout();
    setAccount(null);
  }, []);

  const signUp = useCallback((name: string, email: string, password: string) => auth.createAccount(name, email, password), []);

  const value = useMemo(() => ({
    account, isAuthenticated: !!account, signIn, signOut, signUp,
  }), [account, signIn, signOut, signUp]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used within AuthProvider');
  return value;
}
