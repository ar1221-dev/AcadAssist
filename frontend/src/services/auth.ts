export interface LocalAccount {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: string;
}

const KEY = 'acadassist.auth.accounts';
const SESSION_KEY = 'acadassist.auth.session';

function read<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) as T : fallback;
  } catch { return fallback; }
}

function write(key: string, value: unknown) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* local auth is optional */ }
}

export function getAccounts(): LocalAccount[] {
  return read<LocalAccount[]>(KEY, []);
}

export function getSession(): LocalAccount | null {
  const email = read<string | null>(SESSION_KEY, null);
  return email ? getAccounts().find(account => account.email === email) || null : null;
}

export function createAccount(name: string, email: string, password: string): LocalAccount {
  const normalized = email.trim().toLowerCase();
  const accounts = getAccounts();
  if (accounts.some(account => account.email === normalized)) {
    throw new Error('An account with this email already exists.');
  }
  const account: LocalAccount = {
    id: crypto.randomUUID(),
    name: name.trim(),
    email: normalized,
    password,
    createdAt: new Date().toISOString(),
  };
  write(KEY, [...accounts, account]);
  return account;
}

export function login(email: string, password: string): LocalAccount {
  const normalized = email.trim().toLowerCase();
  const account = getAccounts().find(item => item.email === normalized && item.password === password);
  if (!account) throw new Error('Incorrect email or password.');
  write(SESSION_KEY, account.email);
  return account;
}

export function logout() {
  try { localStorage.removeItem(SESSION_KEY); } catch { /* optional */ }
}

export function isAuthenticated() {
  return !!getSession();
}
