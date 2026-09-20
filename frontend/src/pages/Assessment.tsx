import { useState } from 'react';
import { ArrowRight } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import MotivationalBanner from '../components/ui/MotivationalBanner';
import { ASSESSMENT_PERFORMANCE, RECENT_ATTEMPTS, POPULAR_PRACTICE_SETS, SUBJECTS } from '../context/AppContext';

const TABS = ['Start Practice', 'Previous Attempts', 'Weak Areas', 'Custom Tests'];
const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
const Q_COUNTS = [5, 10, 20, 50];

export default function Assessment() {
  const [activeTab, setActiveTab] = useState('Start Practice');
  const [subject, setSubject] = useState(SUBJECTS[0]?.name || 'Quantum Cognition');
  const [topic, setTopic] = useState('Quantum Tensor Networks');
  const [difficulty, setDifficulty] = useState('Medium');
  const [qCount, setQCount] = useState(10);

  const perf = ASSESSMENT_PERFORMANCE;

  return (
    <div>
      <HeroHeader
        tag="Assessment"
        title={<>Practice with <span className="accent">Purpose.</span></>}
        subtitle="Sharpen your concepts. Track your progress. Be exam-ready."
        image="/assets/header_assessment.png"
      />

      <div className="tab-nav">
        {TABS.map(t => (
          <button key={t} className={`tab-item ${activeTab === t ? 'active' : ''}`} onClick={() => setActiveTab(t)}>{t}</button>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Left */}
        <div>
          {/* Create Assessment */}
          <div className="card mb-6">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-10 h-10 rounded-full bg-[#eef8f2] flex items-center justify-center text-lg">📝</div>
              <div className="flex-1">
                <h3 className="font-bold text-sm">Create a New Assessment</h3>
                <p className="text-xs text-[var(--color-text-muted)]">Choose your preferences and start practicing.</p>
              </div>
              <div className="card bg-[#f8f6f0] flex items-center gap-3 cursor-pointer px-4 py-3">
                <div className="w-8 h-8 rounded-lg bg-[#eef8f2] flex items-center justify-center">📋</div>
                <div>
                  <div className="text-xs font-semibold">Not sure what to practice?</div>
                  <div className="text-[0.65rem] text-[var(--color-text-muted)]">Let AI suggest a test based on your weak areas.</div>
                </div>
                <ArrowRight size={14} />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="text-xs font-semibold text-[var(--color-text-dark)] mb-1.5 block">Subject</label>
                <select value={subject} onChange={e => setSubject(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white focus:border-[var(--color-green-accent)] outline-none">
                  {SUBJECTS.map(s => <option key={s.id}>{s.name}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-[var(--color-text-dark)] mb-1.5 block">Topic</label>
                <select value={topic} onChange={e => setTopic(e.target.value)}
                  className="w-full px-3 py-2 border border-[var(--color-card-border)] rounded-lg text-sm bg-white focus:border-[var(--color-green-accent)] outline-none">
                  <option>Quantum Tensor Networks</option>
                  <option>Swarm Kinematics & Avoidance</option>
                  <option>Relativistic Hydrodynamics</option>
                  <option>Protein Generative Priors</option>
                  <option>Byzantine Fault Quorums</option>
                  <option>Semantic Manifold Embeddings</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <label className="text-xs font-semibold text-[var(--color-text-dark)] mb-2 block">Difficulty</label>
                <div className="flex gap-2">
                  {DIFFICULTIES.map(d => (
                    <button key={d} onClick={() => setDifficulty(d)}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                        difficulty === d ? 'bg-[var(--color-green-accent)] text-white' : 'bg-[#f5f4ef] text-[var(--color-text-dark)] border border-[var(--color-card-border)]'
                      }`}>
                      {d}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold text-[var(--color-text-dark)] mb-2 block">Number of Questions</label>
                <div className="flex gap-2">
                  {Q_COUNTS.map(q => (
                    <button key={q} onClick={() => setQCount(q)}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                        qCount === q ? 'bg-[var(--color-green-accent)] text-white' : 'bg-[#f5f4ef] text-[var(--color-text-dark)] border border-[var(--color-card-border)]'
                      }`}>
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button className="px-6 py-2.5 bg-[var(--color-green-primary)] text-white rounded-lg text-sm font-semibold hover:bg-[var(--color-green-accent)] transition-colors flex items-center gap-2">
                Start Assessment <ArrowRight size={14} />
              </button>
            </div>
          </div>

          {/* Popular Practice Sets */}
          <SectionHeader icon="🔥" title="Popular Practice Sets" action="View All" />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            {POPULAR_PRACTICE_SETS.map((s, i) => (
              <div key={i} className="card hover:shadow-md transition-shadow cursor-pointer">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-lg mb-3" style={{ background: `${s.color}15` }}>
                  {s.icon === 'share-2' ? '🔗' : s.icon === 'database' ? '🗄️' : s.icon === 'wifi' ? '📡' : '⚡'}
                </div>
                <div className="font-semibold text-sm mb-0.5">{s.title}</div>
                <div className="text-[0.68rem] text-[var(--color-text-muted)] mb-3">{s.subtitle}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-[var(--color-text-muted)]">{s.questionsCount} Questions</span>
                  <span className="text-[var(--color-green-accent)] font-semibold">{s.type} →</span>
                </div>
              </div>
            ))}
          </div>

          <MotivationalBanner
            tag="KEEP GOING"
            title="Every attempt makes you better."
            subtitle="Practice today. Progress tomorrow."
            actionLabel="Keep Practicing"
          />
        </div>

        {/* Right Column */}
        <div>
          {/* Performance */}
          <SectionHeader icon="📊" title="Your Performance" action="View Detailed" />
          <div className="card mb-6">
            <div className="flex items-center gap-4 mb-4">
              <div className="relative w-20 h-20">
                <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none" stroke="#eae8e2" strokeWidth="3" />
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none" stroke="#2d5f47" strokeWidth="3" strokeDasharray={`${perf.averageScore}, 100`} strokeLinecap="round" />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-lg font-extrabold">{perf.averageScore}%</span>
                  <span className="text-[0.55rem] text-[var(--color-text-muted)]">Average Score</span>
                </div>
              </div>
              <div className="flex-1 space-y-2">
                <div className="flex items-center gap-2"><span className="text-xs text-[var(--color-text-muted)]">✅</span><span className="text-lg font-bold">{perf.questionsAttempted}</span><span className="text-xs text-[var(--color-text-muted)]">Questions Attempted</span></div>
                <div className="flex items-center gap-2"><span className="text-xs text-[var(--color-text-muted)]">☑️</span><span className="text-lg font-bold">{perf.correctAnswers}</span><span className="text-xs text-[var(--color-text-muted)]">Correct Answers</span></div>
                <div className="flex items-center gap-2"><span className="text-xs text-[var(--color-text-muted)]">📄</span><span className="text-lg font-bold">{perf.topicsCovered}</span><span className="text-xs text-[var(--color-text-muted)]">Topics Covered</span></div>
              </div>
            </div>
            <div className="text-xs text-[var(--color-green-accent)] font-semibold">{perf.delta}</div>
          </div>

          {/* Recent Attempts */}
          <SectionHeader icon="📋" title="Recent Attempts" action="View All" />
          <div className="card mb-6">
            {RECENT_ATTEMPTS.map((a, i) => (
              <div key={i} className="flex items-center gap-3 py-2.5" style={{ borderBottom: i < RECENT_ATTEMPTS.length - 1 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-7 h-7 rounded-lg bg-[#eef8f2] flex items-center justify-center text-xs">📋</div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-semibold truncate">{a.topic} ({a.difficulty})</div>
                  <div className="text-[0.6rem] text-[var(--color-text-muted)]">{a.scoreFraction}</div>
                </div>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  a.status === 'excellent' ? 'bg-green-50 text-green-700' :
                  a.status === 'passed' ? 'bg-blue-50 text-blue-700' :
                  'bg-orange-50 text-orange-700'
                }`}>{a.percentage}</span>
                <span className="text-[0.6rem] text-[var(--color-text-muted)]">{a.date}</span>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <SectionHeader icon="⚡" title="Quick Actions" />
          <div className="grid grid-cols-2 gap-3">
            {[
              { icon: '✨', bg: '#eef8f2', label: 'AI Generate Quiz', sub: 'Based on your notes' },
              { icon: '🎯', bg: '#fff0ea', label: 'Practice Weak Areas', sub: 'Target your gaps' },
              { icon: '📝', bg: '#edf3fd', label: 'Take a Mock Test', sub: 'Exam-like experience' },
              { icon: '📊', bg: '#f0edf9', label: 'View Analytics', sub: 'See your progress' },
            ].map((a, i) => (
              <div key={i} className="card flex items-start gap-3 cursor-pointer hover:shadow-md transition-shadow">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: a.bg }}>{a.icon}</div>
                <div>
                  <div className="text-xs font-semibold">{a.label}</div>
                  <div className="text-[0.65rem] text-[var(--color-text-muted)]">{a.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
