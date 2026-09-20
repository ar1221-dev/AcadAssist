import { useState } from 'react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import MotivationalBanner from '../components/ui/MotivationalBanner';
import { useApp } from '../context/AppContext';

const TABS = ['General', 'Study Preferences', 'Notifications', 'Appearance', 'Account', 'Data & Privacy', 'Integrations'];

export default function Settings() {
  const { settings, updateSetting, user } = useApp();
  const [activeTab, setActiveTab] = useState('General');
  const [name, setName] = useState(user.name);
  const [email, setEmail] = useState(user.email);
  const [studyDuration, setStudyDuration] = useState('50 minutes');
  const [diffLevel, setDiffLevel] = useState('Medium');

  return (
    <div>
      <HeroHeader
        tag="SETTINGS"
        title={<>Customize Your <span className="accent">Experience.</span></>}
        subtitle="Tailor AcadAssist to match your goals, preferences, and workflow."
        image="/assets/header_settings.png"
      />

      <div className="tab-nav overflow-x-auto">
        {TABS.map(t => (
          <button key={t} className={`tab-item ${activeTab === t ? 'active' : ''}`} onClick={() => setActiveTab(t)}>{t}</button>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Left */}
        <div>
          {/* General Settings */}
          <div className="card mb-6">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 rounded-full bg-[#eef8f2] flex items-center justify-center">👤</div>
              <div>
                <h3 className="font-bold text-sm">General Settings</h3>
                <p className="text-xs text-[var(--color-text-muted)]">Set up your basic preferences.</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Name</label>
                <input value={name} onChange={e => setName(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none focus:border-[var(--color-green-accent)]" />
              </div>
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Academic Level</label>
                <select className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none">
                  <option>{user.academicLevel}</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Email</label>
                <input value={email} onChange={e => setEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none focus:border-[var(--color-green-accent)]" />
              </div>
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Field of Study</label>
                <select className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none">
                  <option>{user.field}</option>
                </select>
              </div>
            </div>
          </div>

          {/* Study Preferences */}
          <div className="card mb-6">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 rounded-full bg-[#edf3fd] flex items-center justify-center">📚</div>
              <div>
                <h3 className="font-bold text-sm">Study Preferences</h3>
                <p className="text-xs text-[var(--color-text-muted)]">Customize how AcadAssist helps you learn.</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Default Study Duration</label>
                <select value={studyDuration} onChange={e => setStudyDuration(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none">
                  <option>25 minutes</option><option>50 minutes</option><option>90 minutes</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Subjects</label>
                <div className="flex flex-wrap gap-2">
                  {['Quantum Cognition', 'Autonomous Robotics', 'Astrophysics', 'Synthetic Genomics', 'Decentralized Systems', 'Computational Linguistics'].map(s => (
                    <span key={s} className="px-3 py-1 bg-[#f5f4ef] border border-[var(--color-card-border)] rounded-full text-xs font-medium">{s}</span>
                  ))}
                  <button className="px-3 py-1 border border-dashed border-[var(--color-green-accent)] rounded-full text-xs text-[var(--color-green-accent)] font-medium">+ Add Subject</button>
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold mb-1.5 block">Preferred Difficulty Level</label>
                <select value={diffLevel} onChange={e => setDiffLevel(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white outline-none">
                  <option>Easy</option><option>Medium</option><option>Hard</option>
                </select>
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="card mb-6">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 rounded-full bg-[#fef9ee] flex items-center justify-center">🔔</div>
              <div>
                <h3 className="font-bold text-sm">Notifications</h3>
                <p className="text-xs text-[var(--color-text-muted)]">Choose what updates you want to receive.</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {[
                { key: 'dailyReminder', icon: '📅', label: 'Daily Study Reminder', desc: 'Get reminded to stay on track.' },
                { key: 'assessmentFeedback', icon: '⭐', label: 'Assessment Feedback', desc: 'Get notified after quizzes and tests.' },
                { key: 'examAlerts', icon: '📋', label: 'Upcoming Exam Alerts', desc: 'Be notified about upcoming exams.' },
                { key: 'progressReport', icon: '📊', label: 'Weekly Progress Report', desc: 'Receive a summary of your progress.' },
                { key: 'streakUpdates', icon: '🔥', label: 'Study Streak Updates', desc: 'Motivational nudges to keep going.' },
                { key: 'newFeatures', icon: '✨', label: 'New Features & Tips', desc: 'Stay updated with improvements.' },
              ].map(n => (
                <div key={n.key} className="flex items-center gap-3">
                  <span className="text-sm">{n.icon}</span>
                  <div className="flex-1">
                    <div className="text-xs font-semibold">{n.label}</div>
                    <div className="text-[0.6rem] text-[var(--color-text-muted)]">{n.desc}</div>
                  </div>
                  <div
                    className={`toggle-switch ${settings[n.key as keyof typeof settings] ? 'active' : ''}`}
                    onClick={() => updateSetting(n.key, !settings[n.key as keyof typeof settings])}
                    role="switch"
                    aria-checked={!!settings[n.key as keyof typeof settings]}
                  />
                </div>
              ))}
            </div>
          </div>

          <MotivationalBanner
            tag="YOUR LEARNING. YOUR WAY."
            title='"Small settings. A big difference."'
            subtitle="Personalize, focus, and make the most of your journey."
            actionLabel="Save Changes"
          />
        </div>

        {/* Right Column */}
        <div>
          {/* Appearance */}
          <SectionHeader icon="🎨" title="Appearance" />
          <div className="card mb-6">
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Make it look and feel right for you.</p>
            <label className="text-xs font-semibold mb-2 block">Theme</label>
            <div className="flex gap-2 mb-4">
              {(['light', 'dark', 'system'] as const).map(t => (
                <button key={t} onClick={() => updateSetting('theme', t)}
                  className={`flex-1 py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1.5 ${
                    settings.theme === t ? 'bg-[var(--color-green-accent)] text-white' : 'bg-[#f5f4ef] border border-[var(--color-card-border)]'
                  }`}>
                  {t === 'light' ? '☀️' : t === 'dark' ? '🌙' : '🖥️'} {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
            <label className="text-xs font-semibold mb-2 block">Accent Color</label>
            <div className="flex gap-3 mb-4">
              {['#2d5f47', '#6366f1', '#3b82f6', '#f59e0b', '#ef4444', '#ec4899'].map(c => (
                <button key={c} onClick={() => updateSetting('accentColor', c)}
                  className={`w-7 h-7 rounded-full transition-transform ${settings.accentColor === c ? 'ring-2 ring-offset-2 ring-[var(--color-green-accent)] scale-110' : ''}`}
                  style={{ background: c }} />
              ))}
            </div>
            <label className="text-xs font-semibold mb-2 block">Font Size</label>
            <div className="flex gap-2">
              {(['small', 'medium', 'large'] as const).map(s => (
                <button key={s} onClick={() => updateSetting('fontSize', s)}
                  className={`flex-1 py-2 rounded-lg text-xs font-medium ${
                    settings.fontSize === s ? 'bg-[var(--color-green-accent)] text-white' : 'bg-[#f5f4ef] border border-[var(--color-card-border)]'
                  }`}>
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Account */}
          <SectionHeader icon="👤" title="Account" />
          <div className="card mb-6">
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Manage your account and security.</p>
            {['Change Password', 'Two-Factor Authentication', 'Manage Sessions', 'Delete Account'].map((item, i) => (
              <div key={i} className="flex items-center justify-between py-2.5 cursor-pointer" style={{ borderBottom: i < 3 ? '1px solid #f1efe9' : 'none' }}>
                <span className={`text-xs font-medium ${item === 'Delete Account' ? 'text-red-500' : ''}`}>{item}</span>
                <span className="text-[var(--color-text-muted)] text-xs">›</span>
              </div>
            ))}
          </div>

          {/* Data & Privacy */}
          <SectionHeader icon="🛡️" title="Data & Privacy" />
          <div className="card">
            <p className="text-xs text-[var(--color-text-muted)] mb-3">Control your data and privacy settings.</p>
            {['Manage Your Data', 'Export My Notes', 'Clear Chat History'].map((item, i) => (
              <div key={i} className="flex items-center justify-between py-2.5 cursor-pointer" style={{ borderBottom: i < 2 ? '1px solid #f1efe9' : 'none' }}>
                <span className="text-xs font-medium">{item}</span>
                <span className="text-[var(--color-text-muted)] text-xs">›</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
