import { useNavigate } from 'react-router-dom';
import { Check, Upload, Brain, CalendarDays, ArrowRight } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import StatCard from '../components/ui/StatCard';
import SectionHeader from '../components/ui/SectionHeader';
import ProgressBar from '../components/ui/ProgressBar';
import MotivationalBanner from '../components/ui/MotivationalBanner';
import Card from '../components/ui/Card';
import SubjectBadge from '../components/ui/SubjectBadge';
import Button from '../components/ui/Button';
import { useApp, STATS_SUMMARY, SUBJECTS, UPCOMING_EXAMS, RECENT_ACTIVITIES } from '../context/AppContext';

const PLAN_ICONS: Record<string, [string, string, string]> = {
  'Stochastic Manifold Modeling': ['📗', '#e8f8ee', '#2d5f47'],
  'Swarm Consensus Latency': ['📙', '#fef3c7', '#92400e'],
  'Kerr Metric Spacetime Analysis': ['📘', '#ede9fe', '#6d28d9'],
  'Synthetic Genomics Diagnostic': ['🔬', '#e0f2fe', '#075985'],
  'Linked Lists – Revision': ['📗', '#e8f8ee', '#2d5f47'],
  'Binary Trees – Practice': ['📕', '#fce8e6', '#c0392b'],
  'Normalization': ['📘', '#e8f0fe', '#1a73e8'],
  'Quick Quiz': ['📙', '#fef7e0', '#f9a825'],
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, todayPlan, togglePlanItem } = useApp();
  const now = new Date();
  const dateStr = now.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
  const greeting = now.getHours() < 12 ? 'morning' : now.getHours() < 18 ? 'afternoon' : 'evening';

  return (
    <div className="space-y-6">
      {/* Hero */}
      <HeroHeader
        tag={dateStr}
        title={<>Good {greeting}, <span className="accent">{user.name}.</span></>}
        subtitle="Consistent effort today, stronger results tomorrow."
        image="/assets/header_dashboard.png"
        imageAlt="Study desk illustration"
      />

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <StatCard icon="🔥" iconBg="#fff0ea" value={String(STATS_SUMMARY.dayStreak)} label="Day Streak" delta="Keep it going!" />
        <StatCard icon="🎯" iconBg="#e8f5f0" value={String(STATS_SUMMARY.topicsCompleted)} label="Topics Completed" delta="This cycle" />
        <StatCard icon="⏱️" iconBg="#edf3fd" value={String(STATS_SUMMARY.hoursStudied)} label="Hours Studied" delta="This cycle" />
        <StatCard icon="📊" iconBg="#f0edf9" value={`${STATS_SUMMARY.averageScore}%`} label="Average Score" delta="Across diagnostics" />
      </div>

      {/* Main 2-Column Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-[1.85fr_1.15fr] gap-6 items-start">
        {/* Left Column: Study Plan & Subject Progress & Banner */}
        <div className="space-y-6">
          {/* Today's Study Plan */}
          <div>
            <SectionHeader
              icon="📅"
              title="Today's Study Plan"
              action="View full plan"
              onAction={() => navigate('/planner')}
            />
            <Card>
              {todayPlan.map((item) => {
                const isDone = item.status === 'completed';
                const [, iconBg] = PLAN_ICONS[item.title] ?? ['📄', '#e8f8ee', '#2d5f47'];
                return (
                  <div
                    key={item.id}
                    className="flex items-center gap-3 sm:gap-4 py-3 border-b border-[var(--color-border-light)] last:border-b-0"
                  >
                    {/* Checkbox */}
                    <button
                      type="button"
                      onClick={() => togglePlanItem(item.id)}
                      className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 border-2 transition-all cursor-pointer"
                      style={{
                        background: isDone ? '#1b3d2f' : '#fff',
                        borderColor: isDone ? '#1b3d2f' : '#cbd5e1',
                      }}
                      aria-label={`Toggle ${item.title}`}
                    >
                      {isDone && <Check size={12} color="#fff" strokeWidth={3} />}
                    </button>

                    {/* Time */}
                    <div className="text-xs text-[var(--color-text-muted)] w-16 sm:w-[70px] flex-shrink-0 font-medium">
                      {item.time}
                    </div>

                    {/* Icon */}
                    <div
                      className="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0 hidden sm:flex"
                      style={{ background: iconBg }}
                    >
                      {PLAN_ICONS[item.title]?.[0] ?? '📄'}
                    </div>

                    {/* Title & Desc */}
                    <div className="flex-1 min-w-0">
                      <div className={`text-sm font-semibold truncate ${isDone ? 'line-through opacity-50' : ''}`}>
                        {item.title}
                      </div>
                      <div className="text-xs text-[var(--color-text-muted)] truncate">{item.description}</div>
                    </div>

                    {/* Subject Badge */}
                    <SubjectBadge tag={item.tag} className="hidden xs:inline-flex" />

                    {/* Duration */}
                    <span className="text-xs text-[var(--color-text-muted)] w-12 text-right flex-shrink-0 hidden md:inline">
                      {item.duration}
                    </span>

                    {/* Action Button */}
                    <Button
                      size="sm"
                      variant={isDone ? 'secondary' : 'primary'}
                      onClick={() => {
                        if (isDone) {
                          navigate('/planner');
                        } else {
                          togglePlanItem(item.id);
                        }
                      }}
                    >
                      {isDone ? 'Review' : 'Start'}
                    </Button>
                  </div>
                );
              })}
            </Card>
          </div>

          {/* Subject Progress */}
          <div>
            <SectionHeader
              icon="📊"
              title="Subject Progress"
              action="View detailed analytics"
              onAction={() => navigate('/progress')}
            />
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {SUBJECTS.slice(0, 3).map((s) => (
                <Card key={s.id} hoverable onClick={() => navigate('/progress')}>
                  <div className="font-semibold text-sm mb-1 truncate">{s.name}</div>
                  <div className="text-2xl font-extrabold mb-2">{s.progress}%</div>
                  <ProgressBar value={s.progress} color={s.color} height={6} />
                  <div className="text-xs text-[var(--color-text-muted)] mt-2">
                    {s.topicsCompleted} / {s.totalTopics} modules
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Motivational Banner */}
          <MotivationalBanner
            tag="NEXT MILESTONE"
            title={`Stay consistent, ${user.name}.`}
            subtitle="You're building a stronger, more capable academic self every single day."
            actionLabel="Jump to Study Planner"
            onAction={() => navigate('/planner')}
          />
        </div>

        {/* Right Column: Upcoming Exams & Quick Actions & Activity */}
        <div className="space-y-6">
          {/* Upcoming Exams */}
          <div>
            <SectionHeader
              icon="📋"
              title="Upcoming Exams"
              action="View all"
              onAction={() => navigate('/planner')}
            />
            <Card>
              {UPCOMING_EXAMS.map((exam) => (
                <div
                  key={exam.id}
                  className="flex items-center gap-3 py-2.5 border-b border-[var(--color-border-light)] last:border-b-0"
                >
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
                    style={{
                      background:
                        exam.urgency === 'urgent'
                          ? '#fee2e2'
                          : exam.urgency === 'high'
                          ? '#ffedd5'
                          : exam.urgency === 'medium'
                          ? '#dbeafe'
                          : '#dcfce7',
                    }}
                  >
                    📘
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold text-[var(--color-text-dark)] truncate">{exam.subject}</div>
                    <div className="text-[0.68rem] text-[var(--color-text-muted)] truncate">{exam.examName}</div>
                  </div>
                  <span
                    className={`text-[0.68rem] font-bold px-2 py-0.5 rounded-full flex-shrink-0 ${
                      exam.daysLeft <= 5
                        ? 'bg-red-100 text-red-700'
                        : exam.daysLeft <= 14
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-emerald-100 text-emerald-800'
                    }`}
                  >
                    {exam.daysLeft}d left
                  </span>
                  <span className="text-[0.68rem] text-[var(--color-text-muted)] flex-shrink-0 hidden sm:inline">
                    {exam.dateStr}
                  </span>
                </div>
              ))}
            </Card>
          </div>

          {/* Quick Actions */}
          <div>
            <SectionHeader icon="⚡" title="Quick Actions" />
            <div className="grid grid-cols-2 gap-3">
              {[
                { icon: <Upload size={16} />, bg: '#edf3fd', label: 'Upload Notes', sub: 'Add library items', path: '/knowledge' },
                { icon: <Check size={16} />, bg: '#fff0ea', label: 'Take a Quiz', sub: 'Diagnostic test', path: '/assessment' },
                { icon: <Brain size={16} />, bg: '#eef8f2', label: 'Ask AI Assistant', sub: 'Instant synthesis', path: '/assistant' },
                { icon: <CalendarDays size={16} />, bg: '#f5f4ef', label: 'Plan My Study', sub: 'Adaptive schedule', path: '/planner' },
              ].map((action) => (
                <Card
                  key={action.label}
                  hoverable
                  onClick={() => navigate(action.path)}
                  className="flex items-start gap-2.5 p-3.5"
                >
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    style={{ background: action.bg }}
                  >
                    {action.icon}
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs font-bold text-[var(--color-text-dark)] flex items-center gap-1">
                      <span>{action.label}</span>
                      <ArrowRight size={10} className="text-[var(--color-text-muted)] opacity-60" />
                    </div>
                    <div className="text-[0.65rem] text-[var(--color-text-muted)] truncate">{action.sub}</div>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div>
            <SectionHeader
              icon="🕐"
              title="Recent Activity"
              action="View all"
              onAction={() => navigate('/profile')}
            />
            <Card>
              {RECENT_ACTIVITIES.map((a, i) => (
                <div
                  key={i}
                  className="flex items-center gap-2.5 py-2.5 border-b border-[var(--color-border-light)] last:border-b-0"
                >
                  <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: a.iconColor }} />
                  <div className="flex-1 text-xs text-[var(--color-text-body)] leading-snug line-clamp-2">{a.text}</div>
                  <span className="text-[0.65rem] text-[var(--color-text-muted)] whitespace-nowrap flex-shrink-0">
                    {a.time}
                  </span>
                </div>
              ))}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
