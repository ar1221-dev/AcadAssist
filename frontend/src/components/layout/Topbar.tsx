import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Bell, Menu, Sun, Moon } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export default function Topbar() {
  const navigate = useNavigate();
  const { user, setSidebarOpen, settings, updateSetting } = useApp();
  const [searchVal, setSearchVal] = useState('');
  const [notifOpen, setNotifOpen] = useState(false);

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning,' : hour < 18 ? 'Good afternoon,' : 'Good evening,';

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchVal.trim()) {
      navigate(`/knowledge?q=${encodeURIComponent(searchVal.trim())}`);
    }
  };

  const toggleTheme = () => {
    const nextTheme = settings.theme === 'light' ? 'dark' : 'light';
    updateSetting('theme', nextTheme);
  };

  return (
    <header className="topbar">
      {/* Mobile hamburger */}
      <button
        type="button"
        className="topbar-icon-btn lg:hidden cursor-pointer"
        onClick={() => setSidebarOpen(true)}
        aria-label="Open menu"
      >
        <Menu size={18} />
      </button>

      {/* Search */}
      <form onSubmit={handleSearch} className="topbar-search">
        <Search size={16} strokeWidth={2} className="text-[var(--color-text-muted)] flex-shrink-0" />
        <input
          type="text"
          value={searchVal}
          onChange={(e) => setSearchVal(e.target.value)}
          placeholder="Search your notes, topics, or ask anything..."
          className="bg-transparent border-none outline-none text-xs w-full text-[var(--color-text-dark)]"
        />
        <span className="topbar-shortcut hidden sm:inline-block">Ctrl K</span>
      </form>

      {/* Theme toggle */}
      <button
        type="button"
        onClick={toggleTheme}
        className="topbar-icon-btn cursor-pointer transition-all hover:bg-gray-100"
        title={`Current theme: ${settings.theme}. Click to toggle.`}
        style={{ width: 'auto', borderRadius: 20, padding: '6px 12px', gap: 6, display: 'flex', alignItems: 'center' }}
      >
        {settings.theme === 'dark' ? (
          <>
            <Moon size={14} className="text-indigo-400" />
            <span className="text-[0.65rem] font-bold text-indigo-400">Dark</span>
          </>
        ) : (
          <>
            <Sun size={14} className="text-amber-500" />
            <span className="text-[0.65rem] font-bold text-amber-600">Light</span>
          </>
        )}
      </button>

      {/* Notification */}
      <div className="relative">
        <button
          type="button"
          onClick={() => setNotifOpen(!notifOpen)}
          className="topbar-icon-btn cursor-pointer relative"
          aria-label="Notifications"
        >
          <Bell size={18} />
          <span className="topbar-notif-dot" />
        </button>

        {notifOpen && (
          <div className="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-lg border border-[var(--color-card-border)] p-3 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-[var(--color-border-light)]">
              <span className="text-xs font-bold">Recent Notifications</span>
              <span className="text-[0.65rem] text-[var(--color-green-accent)] font-semibold cursor-pointer">Mark read</span>
            </div>
            <div className="space-y-2 text-xs">
              <div className="p-2 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-100">
                <div className="font-bold text-[0.72rem]">Diagnostic Milestone Unlocked</div>
                <div className="text-[0.65rem] text-emerald-700">Quantum Information Mid-Term in 5 days.</div>
              </div>
              <div className="p-2 rounded-lg bg-amber-50 text-amber-900 border border-amber-100">
                <div className="font-bold text-[0.72rem]">Study Plan Pending</div>
                <div className="text-[0.65rem] text-amber-700">2 modules remaining on today's schedule.</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Avatar pill */}
      <Link to="/profile" className="topbar-avatar-pill hover:bg-gray-50 transition-colors">
        <img
          src="/assets/avatar_topbar.png"
          alt={user.name}
          className="topbar-avatar-img"
          onError={(e) => {
            const el = e.target as HTMLImageElement;
            el.style.display = 'none';
            el.parentElement!.insertAdjacentHTML(
              'afterbegin',
              `<div class="topbar-avatar-initials">${user.name[0]}</div>`
            );
          }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.2 }}>
          <span style={{ fontSize: '0.65rem', color: '#6a7770', fontWeight: 400 }}>{greeting}</span>
          <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#111e17' }}>{user.name}</span>
        </div>
        <span style={{ color: '#9ca3af', fontSize: '0.75rem', marginLeft: 2 }}>▾</span>
      </Link>
    </header>
  );
}
