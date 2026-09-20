import { NavLink } from 'react-router-dom';
import {
  Home, BookOpen, FileText, CalendarDays, Sparkles,
  BarChart3, Settings, HelpCircle,
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

const NAV_PRIMARY = [
  { to: '/dashboard', label: 'Dashboard', icon: Home },
  { to: '/knowledge', label: 'My Knowledge', icon: BookOpen },
  { to: '/assessment', label: 'Assessment', icon: FileText },
  { to: '/planner', label: 'Study Planner', icon: CalendarDays },
  { to: '/assistant', label: 'AI Study Assistant', icon: Sparkles },
  { to: '/progress', label: 'Progress', icon: BarChart3 },
];

const NAV_SECONDARY = [
  { to: '/settings', label: 'Settings', icon: Settings },
  { to: '/help', label: 'Help & Support', icon: HelpCircle },
];

export default function Sidebar() {
  const { sidebarOpen, setSidebarOpen } = useApp();

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        {/* Brand */}
        <div className="sidebar-brand">
          <img src="/assets/logo.png" alt="AcadAssist" />
          <div>
            <div className="sidebar-brand-title">AcadAssist</div>
            <div className="sidebar-brand-sub">Learn · Plan · Practice · Grow</div>
          </div>
        </div>

        {/* Primary Nav */}
        <nav className="sidebar-nav">
          {NAV_PRIMARY.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `sidebar-nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}

          <div className="sidebar-divider" />

          {NAV_SECONDARY.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `sidebar-nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="sidebar-footer">
          <img
            src="/assets/sidebar_footer.png"
            alt=""
            className="sidebar-footer-graphic"
            onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
          />
          <div className="sidebar-footer-quote">
            <p>"Discipline turns goals<br />into results."</p>
            <div className="quote-bar" />
          </div>
          <div className="sidebar-version">AcadAssist v0.1.0</div>
        </div>
      </aside>
    </>
  );
}
