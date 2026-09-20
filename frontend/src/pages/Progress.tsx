import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import { Check } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import StatCard from '../components/ui/StatCard';
import SectionHeader from '../components/ui/SectionHeader';
import ProgressBar from '../components/ui/ProgressBar';
import {
  STATS_SUMMARY, SUBJECT_PROGRESS, WEEKLY_STUDY_HOURS, ACTIVITY_DISTRIBUTION,
  PROGRESS_OVER_TIME, MILESTONES,
} from '../context/AppContext';
import { useApp } from '../context/AppContext';

export default function Progress() {
  const { studyGoals, toggleGoal, user } = useApp();

  return (
    <div>
      <HeroHeader
        tag="YOUR PROGRESS"
        title={<>Small Steps. <span className="accent">Big Progress.</span></>}
        subtitle="Track your learning journey, stay consistent, and become the best version of yourself."
        image="/assets/header_progress.png"
      />

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-6">
        <StatCard icon="📒" iconBg="#fff0ea" value={String(STATS_SUMMARY.notesLearned)} label="Notes Learned" delta={STATS_SUMMARY.notesIncrease} />
        <StatCard icon="✅" iconBg="#eef8f2" value={String(STATS_SUMMARY.questionsPracticed)} label="Questions Practiced" delta={STATS_SUMMARY.questionsIncrease} />
        <StatCard icon="⏱️" iconBg="#fef9ee" value={`${STATS_SUMMARY.totalStudyTime} hrs`} label="Total Study Time" delta={STATS_SUMMARY.studyTimeIncrease} />
        <StatCard icon="🔥" iconBg="#fff0ea" value={String(STATS_SUMMARY.dayStreak)} label="Day Streak" delta="Keep it going!" />
        <StatCard icon="🎯" iconBg="#eef8f2" value={`${STATS_SUMMARY.overallProgress}%`} label="Overall Progress" delta={STATS_SUMMARY.progressIncrease} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_1fr_280px] gap-6">
        {/* Subject Progress */}
        <div>
          <SectionHeader icon="📊" title="Subject Progress" action="View Details" />
          <div className="card mb-6">
            <p className="text-xs text-[var(--color-text-muted)] mb-4">Your completion across all subjects</p>
            <div className="space-y-4">
              {SUBJECT_PROGRESS.map(s => (
                <div key={s.name} className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-lg flex items-center justify-center text-xs" style={{ background: `${s.color}15` }}>📘</div>
                  <div className="flex-1">
                    <div className="flex justify-between mb-1">
                      <span className="text-xs font-medium">{s.name}</span>
                      <span className="text-xs font-bold">{s.progress}%</span>
                    </div>
                    <ProgressBar value={s.progress} color={s.color} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Progress Over Time */}
          <SectionHeader icon="📈" title="Progress Over Time" />
          <div className="card">
            <p className="text-xs text-[var(--color-text-muted)] mb-4">Your learning journey so far</p>
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={PROGRESS_OVER_TIME}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eae8e2" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#6a7770' }} />
                <YAxis tick={{ fontSize: 11, fill: '#6a7770' }} domain={[0, 100]} unit="%" />
                <Tooltip contentStyle={{ borderRadius: 10, border: '1px solid #eae8e2', fontSize: 12 }} />
                <Area type="monotone" dataKey="progress" stroke="#2d5f47" fill="#2d5f4720" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Middle Column */}
        <div>
          {/* Study Time */}
          <SectionHeader icon="⏰" title="Study Time" />
          <div className="card mb-6">
            <p className="text-xs text-[var(--color-text-muted)] mb-4">Time spent studying each week</p>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={WEEKLY_STUDY_HOURS}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eae8e2" />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#6a7770' }} />
                <YAxis tick={{ fontSize: 11, fill: '#6a7770' }} unit="h" />
                <Tooltip contentStyle={{ borderRadius: 10, border: '1px solid #eae8e2', fontSize: 12 }} />
                <Bar dataKey="hours" fill="#2d5f47" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Activity Distribution */}
          <SectionHeader icon="🎯" title="Activity Distribution" />
          <div className="card">
            <p className="text-xs text-[var(--color-text-muted)] mb-4">How you spend your study time</p>
            <div className="flex items-center gap-4">
              <div className="w-40 h-40 relative">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={ACTIVITY_DISTRIBUTION} cx="50%" cy="50%" innerRadius={40} outerRadius={65} paddingAngle={2} dataKey="value">
                      {ACTIVITY_DISTRIBUTION.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-lg font-extrabold">{STATS_SUMMARY.totalStudyTime} hrs</span>
                  <span className="text-[0.55rem] text-[var(--color-text-muted)]">Total</span>
                </div>
              </div>
              <div className="flex-1 space-y-2">
                {ACTIVITY_DISTRIBUTION.map(a => (
                  <div key={a.name} className="flex items-center gap-2 text-xs">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ background: a.color }} />
                    <span className="flex-1">{a.name}</span>
                    <span className="font-semibold">{a.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div>
          {/* Goals */}
          <SectionHeader icon="🎯" title="Your Goals" action="View All" />
          <div className="card mb-6">
            {studyGoals.map(g => (
              <div key={g.id} className="flex items-center gap-3 py-2 cursor-pointer" onClick={() => toggleGoal(g.id)}>
                <div className={`w-5 h-5 rounded-full flex items-center justify-center border-2 transition-colors ${
                  g.completed ? 'bg-[var(--color-green-accent)] border-[var(--color-green-accent)]' : 'bg-white border-[#cbd5e1]'
                }`}>
                  {g.completed && <Check size={12} color="#fff" strokeWidth={3} />}
                </div>
                <span className={`text-xs font-medium ${g.completed ? 'line-through text-[var(--color-text-muted)]' : ''}`}>{g.text}</span>
              </div>
            ))}
          </div>

          {/* Milestones */}
          <SectionHeader icon="🏆" title="Milestones" action="View All" />
          <div className="card mb-6">
            {MILESTONES.map((m, i) => (
              <div key={i} className="flex items-start gap-3 py-2" style={{ borderBottom: i < MILESTONES.length - 1 ? '1px solid #f1efe9' : 'none' }}>
                <div className={`w-5 h-5 rounded-full flex items-center justify-center mt-0.5 ${
                  m.completed ? 'bg-[var(--color-green-accent)] text-white' : 'bg-gray-100 text-gray-400'
                }`}>
                  {m.completed ? <Check size={10} strokeWidth={3} /> : <span className="text-[0.5rem]">○</span>}
                </div>
                <div>
                  <div className="text-xs font-semibold">{m.title}</div>
                  <div className="text-[0.6rem] text-[var(--color-text-muted)]">{m.date}</div>
                </div>
              </div>
            ))}
          </div>

          {/* CTA */}
          <div className="rounded-2xl overflow-hidden relative p-5" style={{ background: 'linear-gradient(135deg, #1a3a2a, #0f1a14)' }}>
            <div className="relative z-10">
              <h4 className="text-white font-semibold text-sm mb-1">You're doing great, {user.name}.</h4>
              <p className="text-white/60 text-xs">Keep going. Your future self will thank you.</p>
            </div>
            <button className="relative z-10 mt-3 w-9 h-9 rounded-full bg-white/10 border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-colors ml-auto">→</button>
          </div>
        </div>
      </div>
    </div>
  );
}
