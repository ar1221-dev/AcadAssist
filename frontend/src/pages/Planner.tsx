import { useState } from 'react';
import { Check, Plus } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import MotivationalBanner from '../components/ui/MotivationalBanner';
import { useApp, UPCOMING_EXAMS, UPCOMING_DEADLINES } from '../context/AppContext';

const DAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
const TASK_ICON_BG: Record<string, string> = {
  study: '#eef8f2', practice: '#fff0ea', break: '#fef9ee', quiz: '#edf3fd',
};
const TASK_ICON: Record<string, string> = {
  study: '📗', practice: '📕', break: '☕', quiz: '📝',
};
const TAG_CLASSES: Record<string, string> = {
  QC: 'badge-qc', ROB: 'badge-rob', ASTRO: 'badge-astro',
  BIO: 'badge-bio', DCP: 'badge-dcp', LING: 'badge-ling',
  Mixed: 'badge-mixed', Break: 'badge-break',
};

function getCalendarDays(year: number, month: number): number[][] {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const weeks: number[][] = [];
  let week: number[] = new Array(firstDay).fill(0);
  for (let d = 1; d <= daysInMonth; d++) {
    week.push(d);
    if (week.length === 7) { weeks.push(week); week = []; }
  }
  if (week.length) { while (week.length < 7) week.push(0); weeks.push(week); }
  return weeks;
}

export default function Planner() {
  const { plannerTasks, togglePlannerTask } = useApp();
  const [viewMode, setViewMode] = useState<'Day' | 'Week' | 'Month'>('Day');
  const completedCount = plannerTasks.filter(t => t.completed).length;

  const calWeeks = getCalendarDays(2026, 8); // September 2026

  return (
    <div>
      <HeroHeader
        tag="Study Planner"
        title={<>Plan Today. Progress <span className="accent">Tomorrow.</span></>}
        subtitle="Stay organized, study smarter, and reach your goals."
        image="/assets/header_planner.png"
      />

      {/* View controls */}
      <div className="flex items-center gap-4 mb-6">
        <button className="text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)]">‹</button>
        <button className="text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)]">›</button>
        <h2 className="text-lg font-bold">September 2026</h2>
        <div className="ml-auto flex bg-[var(--color-card-bg)] border border-[var(--color-card-border)] rounded-lg overflow-hidden">
          {(['Day', 'Week', 'Month'] as const).map(m => (
            <button key={m} onClick={() => setViewMode(m)}
              className={`px-4 py-1.5 text-xs font-medium transition-colors ${viewMode === m ? 'bg-[var(--color-green-accent)] text-white' : 'text-[var(--color-text-dark)]'}`}>
              {m}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[240px_1fr_300px] gap-6">
        {/* Left — Calendar & Exams */}
        <div>
          {/* Mini Calendar */}
          <div className="card mb-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-[var(--color-text-muted)]">‹</span>
              <span className="text-sm font-bold">September 2026</span>
              <span className="text-xs text-[var(--color-text-muted)]">›</span>
            </div>
            <table className="mini-calendar">
              <thead><tr>{DAYS.map((d, i) => <th key={i}>{d}</th>)}</tr></thead>
              <tbody>
                {calWeeks.map((week, wi) => (
                  <tr key={wi}>
                    {week.map((day, di) => (
                      <td key={di} className={day === 0 ? 'empty' : day === 16 ? 'today' : ''}>{day || '·'}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* My Exams */}
          <SectionHeader title="My Exams" action="View All" />
          <div className="space-y-3">
            {UPCOMING_EXAMS.map(e => (
              <div key={e.id} className="card flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center text-sm"
                  style={{ background: e.urgency === 'high' ? '#fee2e2' : e.urgency === 'medium' ? '#dbeafe' : '#dcfce7' }}>📘</div>
                <div className="flex-1">
                  <div className="text-xs font-semibold">{e.subject}</div>
                </div>
                <div className="text-right">
                  <div className={`text-xs font-bold ${e.daysLeft <= 8 ? 'text-red-500' : e.daysLeft <= 14 ? 'text-orange-500' : 'text-green-600'}`}>
                    {e.daysLeft} days left
                  </div>
                  <div className="text-[0.6rem] text-[var(--color-text-muted)]">{e.dateStr}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Center — Timeline */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold">Today, 16 September</h3>
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-text-muted)]">{completedCount} / {plannerTasks.length} tasks completed</span>
              <div className="w-20 h-1.5 bg-[#eae8e2] rounded-full overflow-hidden">
                <div className="h-full bg-[var(--color-green-accent)] rounded-full transition-all" style={{ width: `${(completedCount / plannerTasks.length) * 100}%` }} />
              </div>
            </div>
          </div>

          <div className="space-y-0">
            {plannerTasks.map((task, i) => (
              <div key={task.id} className="flex gap-4">
                {/* Timeline line */}
                <div className="flex flex-col items-center w-6">
                  <div className={`w-3 h-3 rounded-full border-2 flex-shrink-0 ${task.completed ? 'bg-[var(--color-green-accent)] border-[var(--color-green-accent)]' : 'bg-white border-[#cbd5e1]'}`} />
                  {i < plannerTasks.length - 1 && <div className="w-0.5 flex-1 bg-[#e5e3dc]" />}
                </div>

                {/* Time */}
                <div className="text-xs text-[var(--color-text-muted)] w-16 pt-0.5 flex-shrink-0">{task.time}</div>

                {/* Task Card */}
                <div className="card flex-1 mb-3 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: TASK_ICON_BG[task.type] }}>
                    {TASK_ICON[task.type]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className={`text-sm font-semibold ${task.completed ? 'line-through opacity-50' : ''}`}>{task.title}</div>
                    <div className="text-xs text-[var(--color-text-muted)]">{task.description}</div>
                  </div>
                  <span className={`subject-badge ${TAG_CLASSES[task.subjectTag] || 'badge-mixed'}`}>{task.subjectTag}</span>
                  <span className="text-xs text-[var(--color-text-muted)]">{task.duration}</span>
                  <button onClick={() => togglePlannerTask(task.id)}
                    className={`w-5 h-5 rounded flex items-center justify-center border transition-colors ${
                      task.completed ? 'bg-[var(--color-green-accent)] border-[var(--color-green-accent)] text-white' : 'border-[#cbd5e1] bg-white'
                    }`}>
                    {task.completed && <Check size={12} strokeWidth={3} />}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Add Task */}
          <button className="flex items-center gap-2 text-sm text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)] mt-2 mx-auto">
            <Plus size={14} /> Add a new task
          </button>

          <MotivationalBanner
            tag="A SMALL REMINDER"
            title="Progress is a series of small, consistent steps."
          subtitle=""
          />
        </div>

        {/* Right — Focus Mode, Deadlines, Suggestions */}
        <div>
          {/* Focus Mode */}
          <div className="card mb-4 flex items-start justify-between">
            <div>
              <h4 className="text-sm font-bold flex items-center gap-1.5">🎯 Focus Mode</h4>
              <p className="text-xs text-[var(--color-text-muted)]">Block distractions. Get things done.</p>
            </div>
            <button className="px-4 py-1.5 bg-[var(--color-green-accent)] text-white rounded-lg text-xs font-semibold">Start →</button>
          </div>
          <div className="flex gap-2 mb-6">
            {['25 min', '50 min', 'Custom'].map((t, i) => (
              <button key={t} className={`flex-1 py-2 rounded-lg text-xs font-medium ${i === 0 ? 'bg-[var(--color-green-accent)] text-white' : 'bg-[#f5f4ef] border border-[var(--color-card-border)]'}`}>{t}</button>
            ))}
          </div>

          {/* Deadlines */}
          <SectionHeader icon="⏰" title="Upcoming Deadlines" action="View All" />
          <div className="card mb-6">
            {UPCOMING_DEADLINES.map((d, i) => (
              <div key={i} className="flex items-center gap-3 py-2" style={{ borderBottom: i < UPCOMING_DEADLINES.length - 1 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-7 h-7 rounded-lg flex items-center justify-center text-xs"
                  style={{ background: d.urgency === 'urgent' ? '#fee2e2' : d.urgency === 'high' ? '#fff0ea' : d.urgency === 'medium' ? '#dbeafe' : '#dcfce7' }}>📋</div>
                <div className="flex-1 text-xs font-medium">{d.title}</div>
                <div className="text-right">
                  <div className={`text-xs font-bold ${d.urgency === 'urgent' ? 'text-red-500' : d.urgency === 'high' ? 'text-orange-500' : d.urgency === 'medium' ? 'text-orange-400' : 'text-green-600'}`}>
                    {d.daysLeft}
                  </div>
                  <div className="text-[0.55rem] text-[var(--color-text-muted)]">{d.dateStr}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Suggested */}
          <SectionHeader icon="💡" title="Suggested for You" />
          <div className="space-y-3">
            <div className="card cursor-pointer hover:shadow-md transition-shadow">
              <div className="text-xs font-bold mb-0.5">Derive Tensor Retraction Mappings</div>
              <div className="text-[0.65rem] text-[var(--color-text-muted)]">You've mastered Poincaré projections. Strengthen Riemannian gradient flows.</div>
            </div>
            <div className="card cursor-pointer hover:shadow-md transition-shadow">
              <div className="text-xs font-bold mb-0.5">Review Byzantine Quorum Proofs</div>
              <div className="text-[0.65rem] text-[var(--color-text-muted)]">Your Decentralized Consensus exam is in 12 days.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
