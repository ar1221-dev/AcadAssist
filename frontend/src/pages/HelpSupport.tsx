import { useState } from 'react';
import { Search, Send } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import MotivationalBanner from '../components/ui/MotivationalBanner';
import { HELP_CATEGORIES, SYSTEM_STATUS_ITEMS } from '../context/AppContext';

const POPULAR_TAGS = ['Upload Notes', 'Create Quiz', 'Study Planner', 'Account & Login', 'AI Assistant', 'Data & Privacy'];

export default function HelpSupport() {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div>
      <HeroHeader
        tag="HELP & SUPPORT"
        title={<>We're Here to <span className="accent">Help.</span></>}
        subtitle="Find answers, get support, and make the most of AcadAssist."
        image="/assets/header_help_support.png"
      />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Left */}
        <div>
          {/* Search Help Center */}
          <div className="card mb-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-[#edf3fd] flex items-center justify-center text-lg">🔍</div>
              <div>
                <h3 className="font-bold text-sm">Search Help Center</h3>
                <p className="text-xs text-[var(--color-text-muted)]">Find answers to common questions, guides, and troubleshooting steps.</p>
              </div>
            </div>
            <div className="flex gap-2 mb-4">
              <div className="flex-1 flex items-center gap-2 px-3 py-2 border border-[var(--color-card-border)] rounded-lg">
                <Search size={14} className="text-[var(--color-text-muted)]" />
                <input
                  type="text"
                  placeholder='Search for help (e.g., "how to upload notes", "quiz not working")'
                  className="flex-1 bg-transparent outline-none text-sm"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                />
              </div>
              <button className="px-5 py-2 bg-[var(--color-green-primary)] text-white rounded-lg text-sm font-semibold hover:bg-[var(--color-green-accent)] transition-colors">
                Search
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="text-xs text-[var(--color-text-muted)] font-medium">Popular:</span>
              {POPULAR_TAGS.map(t => (
                <button key={t} className="px-3 py-1 bg-[#f5f4ef] border border-[var(--color-card-border)] rounded-full text-xs font-medium hover:border-[var(--color-green-accent)] transition-colors">
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* Browse Help Topics */}
          <SectionHeader icon="📖" title="Browse Help Topics" action="View All" />
          <p className="text-xs text-[var(--color-text-muted)] mb-4">Explore our guides and resources.</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            {HELP_CATEGORIES.map((cat, i) => (
              <div key={i} className="card hover:shadow-md transition-shadow cursor-pointer">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-lg mb-3" style={{ background: `${cat.color}15` }}>
                  {cat.icon === 'compass' ? '🧭' : cat.icon === 'folder' ? '📁' : cat.icon === 'check-circle' ? '✅' :
                   cat.icon === 'calendar' ? '📅' : cat.icon === 'cpu' ? '🤖' : cat.icon === 'bar-chart-2' ? '📊' :
                   cat.icon === 'settings' ? '⚙️' : '🛡️'}
                </div>
                <div className="font-semibold text-xs mb-1">{cat.title}</div>
                <div className="text-[0.65rem] text-[var(--color-text-muted)] mb-2">{cat.description}</div>
                <span className="text-[var(--color-text-muted)] text-xs">→</span>
              </div>
            ))}
          </div>

          <MotivationalBanner
            tag="STILL HAVE QUESTIONS?"
            title="Learning is a journey, and you're not alone."
            subtitle="We're here to support you at every step."
            actionLabel="Contact Support"
          />
        </div>

        {/* Right Column */}
        <div>
          {/* Get in Touch */}
          <SectionHeader icon="✉️" title="Get in Touch" />
          <div className="card mb-6">
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Still need help? Reach out to our support team.</p>
            {[
              { icon: '📧', label: 'Send a Support Request', desc: 'We usually respond within 24 hours.' },
              { icon: '💬', label: 'Live Chat (Beta)', desc: 'Chat with our support assistant.' },
              { icon: '✉️', label: 'Email Us', desc: 'support@acadassist.app' },
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-3 py-3 cursor-pointer" style={{ borderBottom: i < 2 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-8 h-8 rounded-lg bg-[#eef8f2] flex items-center justify-center">{item.icon}</div>
                <div className="flex-1">
                  <div className="text-xs font-semibold">{item.label}</div>
                  <div className="text-[0.6rem] text-[var(--color-text-muted)]">{item.desc}</div>
                </div>
                <span className="text-[var(--color-text-muted)]">›</span>
              </div>
            ))}
          </div>

          {/* System Status */}
          <SectionHeader icon="🟢" title="System Status" action="View Status" />
          <div className="card mb-6">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-green-500" />
              <span className="text-xs font-semibold">All Systems Operational</span>
            </div>
            {SYSTEM_STATUS_ITEMS.map((s, i) => (
              <div key={i} className="flex items-center justify-between py-1.5">
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                  <span className="text-xs">{s.name}</span>
                </div>
                <span className="text-xs text-green-600 font-medium">{s.status}</span>
              </div>
            ))}
          </div>

          {/* Give Feedback */}
          <SectionHeader icon="💡" title="Give Feedback" />
          <div className="card">
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Help us improve AcadAssist! Share your ideas, report issues, or suggest new features.</p>
            <button className="w-full px-4 py-2 border border-[var(--color-card-border)] rounded-lg text-xs font-semibold hover:border-[var(--color-green-accent)] transition-colors flex items-center justify-center gap-2">
              Share Feedback <Send size={12} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
