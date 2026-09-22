import { useEffect, useState, useCallback } from 'react';
import {
  CheckCircle2, FileQuestion, History, RotateCcw, Sparkles, Target, X, Clock3,
  AlertCircle, AlertTriangle, ArrowRight, ArrowLeft, Bookmark, Check,
  BookOpen, Timer, Lightbulb, Layers
} from 'lucide-react';
import { useSearchParams } from 'react-router-dom';
import { useApp, type Quiz, RECENT_ATTEMPTS } from '../context/AppContext';
import Modal from '../components/ui/Modal';

const TOPICS = [
  'Deadlocks',
  'CPU Scheduling',
  'Memory Management',
  'Transport Layer',
  'Application Layer',
  'Normalization',
  'B+ Trees & Indexing',
  'Graph Traversals (BFS/DFS)',
  'Linear Regression',
];

const BANK: Record<string, { q: string; options: string[]; answer: number; explanation: string }[]> = {
  Deadlocks: [
    {
      q: 'Which condition is required for deadlock?',
      options: ['Preemption of every resource', 'Circular wait', 'Unlimited resources', 'Only one process'],
      answer: 1,
      explanation: 'Circular wait is one of the four necessary Coffman conditions.',
    },
    {
      q: 'Which technique can prevent circular wait?',
      options: ['Impose a global resource ordering', 'Increase context switches', 'Disable interrupts', 'Use FCFS'],
      answer: 0,
      explanation: 'Ordering resource acquisition prevents cycles in the resource-allocation wait-for graph.',
    },
    {
      q: 'A process holds one resource while waiting for another. Which condition is this?',
      options: ['Mutual exclusion', 'Hold and wait', 'No preemption', 'Circular wait'],
      answer: 1,
      explanation: 'Hold and wait means a process holds resources while requesting additional resources.',
    },
    {
      q: 'What does Banker\'s algorithm primarily achieve?',
      options: ['Deadlock recovery', 'Deadlock avoidance via safe states', 'Deadlock detection only', 'Process preemption'],
      answer: 1,
      explanation: 'Banker\'s algorithm dynamically checks if granting a resource request maintains a safe state.',
    },
  ],
  'CPU Scheduling': [
    {
      q: 'Which scheduling algorithm uses a time quantum?',
      options: ['FCFS', 'SJF', 'Round Robin', 'Priority only'],
      answer: 2,
      explanation: 'Round Robin assigns each ready process a fixed time slice.',
    },
    {
      q: 'Which algorithm can minimize average waiting time when burst lengths are known?',
      options: ['SJF', 'FCFS', 'Round Robin', 'FIFO paging'],
      answer: 0,
      explanation: 'Shortest Job First is optimal for average waiting time under standard non-preemptive assumptions.',
    },
  ],
  'Memory Management': [
    {
      q: 'What is the main purpose of page tables in virtual memory?',
      options: ['Translate virtual page addresses to physical frame numbers', 'Encrypt memory contents', 'Speed up disk spindle speeds', 'Prevent cache hits'],
      answer: 0,
      explanation: 'Page tables map virtual memory page numbers to corresponding physical memory page frames.',
    },
    {
      q: 'What phenomenon causes severe performance degradation when paging continuously?',
      options: ['Pipelining', 'Thrashing', 'Segmentation', 'Compaction'],
      answer: 1,
      explanation: 'Thrashing occurs when the system spends more time servicing page faults than executing instructions.',
    },
  ],
  'Transport Layer': [
    {
      q: 'Which protocol provides reliable, ordered byte-stream delivery?',
      options: ['UDP', 'TCP', 'IP', 'ARP'],
      answer: 1,
      explanation: 'TCP provides connection-oriented reliable ordered delivery.',
    },
    {
      q: 'What is a key property of UDP?',
      options: ['Mandatory retransmission', 'Connectionless delivery', 'Guaranteed ordering', 'Three-way handshake'],
      answer: 1,
      explanation: 'UDP is connectionless and does not guarantee delivery or ordering.',
    },
    {
      q: 'Flow control primarily prevents what?',
      options: ['A sender from overwhelming a receiver', 'IP address exhaustion', 'DNS caching', 'MAC collisions'],
      answer: 0,
      explanation: 'Receiver-side flow control regulates how much unacknowledged data the sender may transmit.',
    },
  ],
  Normalization: [
    {
      q: 'What is the main purpose of relational normalization?',
      options: ['Increase redundancy', 'Reduce update anomalies and data redundancy', 'Remove all candidate keys', 'Avoid SQL'],
      answer: 1,
      explanation: 'Normalization structures relations to reduce duplication and eliminate insertion, update, and deletion anomalies.',
    },
    {
      q: 'A relation is in 2NF when it is in 1NF and has no:',
      options: ['Primary key', 'Partial functional dependency on a composite key', 'Foreign key', 'Tuples'],
      answer: 1,
      explanation: '2NF requires removing partial functional dependencies on a composite candidate key.',
    },
    {
      q: 'For a relation to be in BCNF, for every functional dependency X -> Y:',
      options: ['Y must be a prime attribute', 'X must be a super key', 'X and Y must be foreign keys', 'Y must be unique'],
      answer: 1,
      explanation: 'Boyce-Codd Normal Form (BCNF) strictly requires that the determinant X is a superkey.',
    },
  ],
  'B+ Trees & Indexing': [
    {
      q: 'Why are B+ Trees preferred over binary search trees for disk storage?',
      options: ['High fan-out reduces disk I/O seek operations', 'They take less memory', 'They do not support range queries', 'They are unordered'],
      answer: 0,
      explanation: 'High branching factor (fan-out) produces a shallow tree height, minimizing disk block access.',
    },
    {
      q: 'In a B+ Tree, where are actual record pointers or values stored?',
      options: ['Only in leaf nodes', 'Only in the root node', 'Evenly distributed across all levels', 'In internal nodes only'],
      answer: 0,
      explanation: 'B+ Trees keep all key-value pairs or record pointers in linked leaf nodes; internal nodes only store navigation keys.',
    },
  ],
  'Graph Traversals (BFS/DFS)': [
    {
      q: 'Which data structure is typically used to implement Breadth-First Search (BFS)?',
      options: ['Stack', 'Queue', 'Priority Queue', 'Disjoint Set'],
      answer: 1,
      explanation: 'BFS uses a FIFO Queue to traverse neighbors level-by-level.',
    },
    {
      q: 'What is the standard time complexity of DFS on a graph with V vertices and E edges using an adjacency list?',
      options: ['O(V * E)', 'O(V + E)', 'O(V^2)', 'O(log V)'],
      answer: 1,
      explanation: 'DFS visits each vertex once and inspects each edge once, yielding O(V + E) time complexity.',
    },
  ],
  'Linear Regression': [
    {
      q: 'What loss function is standard for ordinary least squares linear regression?',
      options: ['Cross-Entropy Loss', 'Mean Squared Error (MSE)', 'Hinge Loss', 'Kullback-Leibler Divergence'],
      answer: 1,
      explanation: 'Linear regression optimizes parameters by minimizing the sum of squared differences (MSE).',
    },
  ],
};

type AssessmentSource = 'Topic' | 'Subject' | 'Knowledge' | 'Notes' | 'Weak Topics';

export default function Assessment() {
  const { subjects, knowledgeMaterials, notes, quizzes, addQuiz, updateQuiz, pushToast, weakTopics } = useApp();
  const [params] = useSearchParams();

  const initialSourceParam = params.get('source');
  const initialSource: AssessmentSource =
    initialSourceParam === 'document'
      ? 'Knowledge'
      : initialSourceParam === 'notes'
      ? 'Notes'
      : initialSourceParam === 'subject'
      ? 'Subject'
      : initialSourceParam === 'weak'
      ? 'Weak Topics'
      : 'Topic';

  const [source, setSource] = useState<AssessmentSource>(initialSource);
  const [subject, setSubject] = useState(params.get('subject') || subjects[0]?.name || 'Operating Systems');
  const [topic, setTopic] = useState(params.get('material') || 'Deadlocks');
  const [difficulty, setDifficulty] = useState<Quiz['difficulty']>('Mixed');
  const [count, setCount] = useState(10);
  const [mode, setMode] = useState(false);
  const [active, setActive] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [result, setResult] = useState<number | null>(null);
  const [showReview, setShowReview] = useState(false);
  const [history, setHistory] = useState(false);
  const [timer, setTimer] = useState(0);
  const [confirm, setConfirm] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);
  const [flagged, setFlagged] = useState<Record<string, boolean>>({});
  const [navFilter, setNavFilter] = useState<'all' | 'unanswered' | 'flagged'>('all');
  const [solutionFilter, setSolutionFilter] = useState<'all' | 'incorrect' | 'flagged'>('all');

  useEffect(() => {
    if (!active) return;
    document.body.classList.add('quiz-active');
    return () => document.body.classList.remove('quiz-active');
  }, [active]);

  useEffect(() => {
    if (!mode || result !== null || timer <= 0) return;
    const id = window.setInterval(() => setTimer(t => Math.max(0, t - 1)), 1000);
    return () => window.clearInterval(id);
  }, [mode, result, timer]);

  const toggleFlag = useCallback((id: string) => {
    setFlagged(f => ({ ...f, [id]: !f[id] }));
  }, []);

  const clearCurrentAnswer = useCallback((id: string) => {
    setAnswers(prev => {
      const next = { ...prev };
      delete next[id];
      return next;
    });
  }, []);

  const sourceItems =
    source === 'Knowledge'
      ? knowledgeMaterials.map(x => x.name)
      : source === 'Notes'
      ? notes.map(x => x.title)
      : source === 'Subject'
      ? subjects.map(s => s.name)
      : source === 'Weak Topics'
      ? weakTopics.map(w => w.topic)
      : TOPICS;

  const closeQuiz = () => {
    setActive(null);
    setAnswers({});
    setResult(null);
    setCurrentQuestion(0);
    setTimer(0);
    setConfirm(false);
    setShowReview(false);
    setMobileNav(false);
    setFlagged({});
    setNavFilter('all');
    setSolutionFilter('all');
  };

  const startQuizFromTopic = (targetTopic: string, targetSubject = 'Operating Systems', isExam = false) => {
    let resolvedBank = BANK[targetTopic];
    if (!resolvedBank) {
      const match = Object.keys(BANK).find(k => targetTopic.toLowerCase().includes(k.toLowerCase()) || k.toLowerCase().includes(targetTopic.toLowerCase()));
      resolvedBank = match ? BANK[match] : BANK['Deadlocks'];
    }
    const questions = Array.from({ length: 10 }, (_, i) => {
      const b = resolvedBank[i % resolvedBank.length];
      return {
        id: crypto.randomUUID(),
        text: b.q,
        options: [...b.options],
        answer: b.answer,
        explanation: b.explanation,
      };
    });
    const q: Quiz = {
      id: crypto.randomUUID(),
      title: `${targetTopic} — ${isExam ? 'Timed Assessment' : 'Practice Quiz'}`,
      source: targetTopic,
      subject: targetSubject,
      difficulty: 'Mixed',
      questions,
    };
    addQuiz(q);
    setActive(q);
    setAnswers({});
    setResult(null);
    setCurrentQuestion(0);
    setShowReview(false);
    setTimer(isExam ? 600 : 0);
    setMode(isExam);
    setMobileNav(false);
    setFlagged({});
    setNavFilter('all');
    setSolutionFilter('all');
    pushToast(`Quiz generated for ${targetTopic}`);
  };

  const generate = () => {
    const selectedItem = source === 'Topic' || source === 'Weak Topics' ? topic : sourceItems[0] || 'Deadlocks';
    startQuizFromTopic(selectedItem, subject, mode);
  };

  const submit = useCallback(() => {
    if (!active) return;
    const correct = active.questions.filter(q => answers[q.id] === q.answer).length;
    const score = Math.round((correct / active.questions.length) * 100);
    updateQuiz(active.id, { score, completedAt: new Date().toISOString() });
    setResult(score);
    setConfirm(false);
    setShowReview(false);
    pushToast(`Quiz submitted — ${score}%`);
  }, [active, answers, updateQuiz, pushToast]);

  useEffect(() => {
    if (active && mode && result === null && timer === 0) submit();
  }, [timer, active, mode, result, submit]);

  const retry = () => {
    if (!active) return;
    setAnswers({});
    setResult(null);
    setCurrentQuestion(0);
    setShowReview(false);
    setTimer(mode ? active.questions.length * 60 : 0);
    setFlagged({});
    setNavFilter('all');
    setSolutionFilter('all');
  };

  const jumpTo = (index: number) => {
    setCurrentQuestion(index);
    setMobileNav(false);
  };

  // Keyboard navigation for power users
  useEffect(() => {
    if (!active || result !== null) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      const currQ = active.questions[currentQuestion];
      if (!currQ) return;

      if (e.key === 'ArrowRight') {
        setCurrentQuestion(i => Math.min(active.questions.length - 1, i + 1));
      } else if (e.key === 'ArrowLeft') {
        setCurrentQuestion(i => Math.max(0, i - 1));
      } else if (e.key.toLowerCase() === 'f') {
        toggleFlag(currQ.id);
      } else if (['1', '2', '3', '4'].includes(e.key)) {
        const idx = parseInt(e.key, 10) - 1;
        if (idx < currQ.options.length) {
          setAnswers(a => ({ ...a, [currQ.id]: idx }));
        }
      } else if (['a', 'b', 'c', 'd'].includes(e.key.toLowerCase())) {
        const idx = e.key.toLowerCase().charCodeAt(0) - 97;
        if (idx < currQ.options.length) {
          setAnswers(a => ({ ...a, [currQ.id]: idx }));
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [active, result, currentQuestion, toggleFlag]);

  const question = active?.questions[currentQuestion];
  const answeredCount = active ? Object.keys(answers).length : 0;
  const unanswered = active ? active.questions.length - answeredCount : 0;
  const flaggedCount = active ? active.questions.filter(q => flagged[q.id]).length : 0;
  const progressPercent = active && active.questions.length > 0 ? Math.round((answeredCount / active.questions.length) * 100) : 0;

  return (
    <div className="page-stack">
      {/* Hero Header */}
      <div className="page-hero">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="eyebrow">AI ASSESSMENT STUDIO</span>
            <span className="soft-badge" style={{ fontSize: '0.62rem', padding: '2px 8px' }}>
              Deterministic Engine · Azure Foundry Ready
            </span>
          </div>
          <h1>Practice what matters.</h1>
          <p>
            Generate targeted quizzes from subjects, uploaded course materials, notes, or your identified weak topics.
          </p>
        </div>
        <button className="btn secondary" onClick={() => setHistory(true)}>
          <History size={16} /> Quiz history ({quizzes.length})
        </button>
      </div>

      {/* Main Generator Layout */}
      <div className="assessment-layout">
        {/* Left: Generator Form */}
        <div className="card generator-card">
          <div className="section-kicker">CREATE AN ASSESSMENT</div>
          <h2>AI Quiz Generator</h2>
          <p className="muted text-xs">
            Select a curriculum source to generate multiple-choice questions with step-by-step explanations.
          </p>

          <div className="source-tabs mt-4">
            {(['Topic', 'Subject', 'Knowledge', 'Notes', 'Weak Topics'] as const).map(s => (
              <button
                key={s}
                className={source === s ? 'active' : ''}
                onClick={() => {
                  setSource(s);
                  const items =
                    s === 'Knowledge'
                      ? knowledgeMaterials.map(x => x.name)
                      : s === 'Notes'
                      ? notes.map(x => x.title)
                      : s === 'Subject'
                      ? subjects.map(x => x.name)
                      : s === 'Weak Topics'
                      ? weakTopics.map(w => w.topic)
                      : TOPICS;
                  setTopic(items[0] || 'Deadlocks');
                }}
              >
                <FileQuestion size={14} />
                <span>{s}</span>
              </button>
            ))}
          </div>

          <label>
            Subject
            <select className="select full" value={subject} onChange={e => setSubject(e.target.value)}>
              {subjects.map(s => (
                <option key={s.id}>{s.name}</option>
              ))}
            </select>
          </label>

          <label>
            Target {source}
            <select className="select full" value={topic} onChange={e => setTopic(e.target.value)}>
              {sourceItems.map(x => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </label>

          <div className="form-grid">
            <label>
              Questions
              <select className="select full" value={count} onChange={e => setCount(Number(e.target.value))}>
                {[5, 10, 15, 20].map(n => (
                  <option key={n}>{n} questions</option>
                ))}
              </select>
            </label>
            <label>
              Difficulty
              <select
                className="select full"
                value={difficulty}
                onChange={e => setDifficulty(e.target.value as Quiz['difficulty'])}
              >
                {['Easy', 'Medium', 'Hard', 'Mixed', 'Adaptive'].map(x => (
                  <option key={x}>{x}</option>
                ))}
              </select>
            </label>
          </div>

          <label className="toggle-row">
            <input type="checkbox" checked={mode} onChange={e => setMode(e.target.checked)} />
            <span>
              <b>Timed Exam Mode</b>
              <small>Simulates official test conditions with countdown timer and final score review.</small>
            </span>
          </label>

          <button className="btn primary large w-full mt-2" onClick={generate}>
            <Sparkles size={17} /> Generate assessment
          </button>
        </div>

        {/* Right: Intelligence Overview */}
        <div className="card how-card">
          <div className="ai-icon">
            <Sparkles size={18} />
          </div>
          <h3>Assessment Intelligence</h3>
          <p className="muted text-xs mb-3">
            Every completed quiz feeds your weak topic diagnostics and updates the Study Planner.
          </p>

          {[
            'Select any course topic or uploaded document',
            'Take in untimed practice or timed exam mode',
            'Full navigation to flag and skip questions',
            'Instant score review with detailed explanations',
            'Weak topics dynamically populate revision tasks',
          ].map(x => (
            <div className="feature-row" key={x}>
              <CheckCircle2 size={16} />
              <span>{x}</span>
            </div>
          ))}

          <div className="callout mt-4">
            <b>Backend Readiness:</b> Local mode uses deterministic question banks. Azure AI Foundry can be connected in <code>src/services/api.ts</code> to generate dynamic questions from large documents.
          </div>
        </div>
      </div>

      {/* Recommended Assessments Section (Based on Real AcadAssist Data) */}
      <div>
        <div className="section-title-row mb-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="section-kicker">RECOMMENDED FOR YOU</span>
              <span className="text-[.62rem] text-[var(--color-text-muted)]">Curriculum Diagnostics</span>
            </div>
            <h2 className="text-base font-bold">Recommended Practice Targets</h2>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {weakTopics.map(wt => (
            <div key={wt.id} className="card p-4 flex flex-col justify-between border-t-2 border-t-[var(--color-green-accent)]">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <span className="soft-badge text-[.65rem]">{wt.subject}</span>
                  <span className="text-xs font-bold text-red-600 bg-red-50 dark:bg-red-950/40 px-2 py-0.5 rounded">
                    {wt.accuracyScore}% score
                  </span>
                </div>
                <h3 className="text-sm font-bold">{wt.topic}</h3>
                <p className="text-xs text-[var(--color-text-muted)] mt-1.5 leading-relaxed">
                  {wt.recommendedAction}
                </p>
                {wt.examName && (
                  <div className="flex items-center gap-1.5 text-xs text-orange-600 font-semibold mt-2.5">
                    <AlertTriangle size={13} /> {wt.examName} in {wt.daysToExam} days
                  </div>
                )}
              </div>
              <div className="flex gap-2 mt-4">
                <button
                  className="btn primary flex-1 text-xs"
                  onClick={() => startQuizFromTopic(wt.topic.split(' ')[0], wt.subject, false)}
                >
                  <Target size={14} /> Practice
                </button>
                <button
                  className="btn secondary text-xs"
                  onClick={() => startQuizFromTopic(wt.topic.split(' ')[0], wt.subject, true)}
                >
                  <Clock3 size={13} /> Timed
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Attempts and Practice History */}
      <div>
        <div className="section-title-row mb-3">
          <div>
            <div className="section-kicker">PRACTICE ATTEMPTS</div>
            <h2 className="text-base font-bold">Recent Assessment Performance</h2>
          </div>
          <button className="link-btn" onClick={() => setHistory(true)}>
            View all history <ArrowRight size={14} />
          </button>
        </div>

        <div className="card p-2 divide-y divide-[var(--color-border-light)]">
          {RECENT_ATTEMPTS.map((att, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 gap-3">
              <div className="flex items-center gap-3">
                <div
                  className={`w-9 h-9 rounded-lg flex items-center justify-center font-bold text-xs ${
                    att.status === 'excellent'
                      ? 'bg-green-100 text-green-700 dark:bg-green-950/50 dark:text-green-400'
                      : att.status === 'passed'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-950/50 dark:text-blue-400'
                      : 'bg-amber-100 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400'
                  }`}
                >
                  {att.percentage}
                </div>
                <div>
                  <b className="text-xs text-[var(--color-text-dark)] block">{att.topic}</b>
                  <small className="text-[.65rem] text-[var(--color-text-muted)]">
                    Difficulty: {att.difficulty} · Score: {att.scoreFraction} · Date: {att.date} (Sample Data)
                  </small>
                </div>
              </div>
              <button
                className="btn subtle text-xs"
                onClick={() => startQuizFromTopic(att.topic.split(' ')[0], 'Operating Systems', false)}
              >
                <RotateCcw size={13} /> Retry topic
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Active Full-Screen Quiz Experience */}
      {active && (
        <div className="quiz-shell" role="dialog" aria-modal="true" aria-label={active.title}>
          {/* Top Animated Progress Bar */}
          <div className="quiz-top-progress">
            <div
              className="quiz-top-progress-fill"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          <header className="quiz-shell-head">
            <div className="quiz-title-wrap">
              <button className="quiz-exit-btn" onClick={closeQuiz} aria-label="Exit quiz" title="Exit Quiz">
                <X size={18} />
              </button>
              <div>
                <div className="flex items-center gap-2 mb-0.5">
                  <span className={`quiz-mode-pill ${mode ? 'timed' : 'practice'}`}>
                    {mode ? <Timer size={11} /> : <BookOpen size={11} />}
                    {mode ? 'Timed Exam Mode' : 'Practice Mode'}
                  </span>
                  <span className="text-[0.68rem] font-semibold text-[var(--color-text-muted)]">
                    {active.subject}
                  </span>
                </div>
                <h2 className="text-base md:text-lg font-bold text-[var(--color-text-dark)] truncate max-w-[260px] sm:max-w-md">
                  {active.title}
                </h2>
              </div>
            </div>

            <div className="quiz-header-meta">
              <div className="quiz-stat-chip hidden sm:inline-flex">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span>
                  <b>{answeredCount}</b> of {active.questions.length} answered
                </span>
                <span className="text-xs text-[var(--color-green-accent)] font-extrabold ml-1">
                  ({progressPercent}%)
                </span>
              </div>

              {mode && result === null && (
                <div className={`timer-chip ${timer <= 60 ? 'warning' : ''}`}>
                  <Clock3 size={14} />
                  <span>
                    {Math.floor(timer / 60)}:{String(timer % 60).padStart(2, '0')}
                  </span>
                </div>
              )}

              {result === null && (
                <button
                  className="btn subtle text-xs hidden md:inline-flex"
                  onClick={() => setConfirm(true)}
                >
                  <CheckCircle2 size={14} className="text-emerald-600" />
                  Submit
                </button>
              )}
            </div>
          </header>

          {result === null ? (
            <div className="quiz-body">
              <main className="quiz-content">
                <div className="quiz-center-column">
                  <div className="quiz-card">
                    <div className="quiz-card-head">
                      <div className="flex items-center gap-2">
                        <span className="question-badge">
                          Question {currentQuestion + 1} of {active.questions.length}
                        </span>
                        {answers[question?.id || ''] !== undefined && (
                          <span className="inline-flex items-center gap-1 text-[0.68rem] font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-950/40 dark:text-emerald-400 px-2 py-0.5 rounded-md">
                            <Check size={11} /> Saved
                          </span>
                        )}
                      </div>

                      <div className="question-actions-group">
                        {question && answers[question.id] !== undefined && (
                          <button
                            className="clear-btn"
                            onClick={() => clearCurrentAnswer(question.id)}
                            title="Clear selection for this question"
                          >
                            Clear answer
                          </button>
                        )}
                        {question && (
                          <button
                            className={`flag-btn ${flagged[question.id] ? 'flagged' : ''}`}
                            onClick={() => toggleFlag(question.id)}
                            title="Flag for later review"
                          >
                            <Bookmark size={13} fill={flagged[question.id] ? 'currentColor' : 'none'} />
                            <span>{flagged[question.id] ? 'Flagged' : 'Flag'}</span>
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="question-text">
                      {question?.text}
                    </div>

                    <div className="option-stack" role="radiogroup" aria-label="Answer options">
                      {question?.options.map((optionText, j) => {
                        const isSelected = answers[question.id] === j;
                        const letter = String.fromCharCode(65 + j);
                        return (
                          <button
                            key={`${question.id}-${j}`}
                            className={`option-item ${isSelected ? 'selected' : ''}`}
                            onClick={() => setAnswers(a => ({ ...a, [question.id]: j }))}
                            role="radio"
                            aria-checked={isSelected}
                          >
                            <div className="option-letter">{letter}</div>
                            <div className="option-label">{optionText}</div>
                            <div className="option-check">
                              {isSelected && <Check size={13} strokeWidth={3} />}
                            </div>
                            <span className="option-key-badge hidden sm:inline-block">
                              {j + 1}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Navigation controls */}
                  <div className="quiz-controls-row">
                    <button
                      className="btn secondary"
                      onClick={() => setCurrentQuestion(i => Math.max(0, i - 1))}
                      disabled={currentQuestion === 0}
                    >
                      <ArrowLeft size={14} /> Previous
                    </button>

                    <div className="quiz-kbd-hints hidden md:flex">
                      <span><kbd>1</kbd>-<kbd>4</kbd> or <kbd>A</kbd>-<kbd>D</kbd> select</span>
                      <span>•</span>
                      <span><kbd>←</kbd> <kbd>→</kbd> navigate</span>
                      <span>•</span>
                      <span><kbd>F</kbd> flag</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        className="btn secondary mobile-question-btn"
                        onClick={() => setMobileNav(true)}
                      >
                        <Layers size={14} /> Questions ({answeredCount}/{active.questions.length})
                      </button>

                      {currentQuestion < active.questions.length - 1 ? (
                        <button
                          className="btn primary"
                          onClick={() => setCurrentQuestion(i => Math.min(active.questions.length - 1, i + 1))}
                        >
                          Next <ArrowRight size={14} />
                        </button>
                      ) : (
                        <button className="btn primary" onClick={() => setConfirm(true)}>
                          <CheckCircle2 size={15} /> Review & Submit
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </main>

              {/* Modern Question Navigator Sidebar */}
              <aside className={`quiz-nav-sidebar ${mobileNav ? 'open' : ''}`} aria-label="Question navigation">
                <div className="quiz-nav-header">
                  <div className="quiz-nav-title-row">
                    <div>
                      <b className="text-sm font-bold text-[var(--color-text-dark)]">Question Navigator</b>
                      <small className="block text-[0.66rem] text-[var(--color-text-muted)]">
                        Click any number to jump
                      </small>
                    </div>
                    <button
                      className="icon-button question-nav-close"
                      onClick={() => setMobileNav(false)}
                      aria-label="Close question navigation"
                    >
                      <X size={16} />
                    </button>
                  </div>

                  <div className="quiz-nav-stats-pills">
                    <div className="quiz-stat-box">
                      <b className="text-emerald-700 dark:text-emerald-400">{answeredCount}</b>
                      <small>Answered</small>
                    </div>
                    <div className="quiz-stat-box">
                      <b className="text-amber-600 dark:text-amber-400">{flaggedCount}</b>
                      <small>Flagged</small>
                    </div>
                    <div className="quiz-stat-box">
                      <b className="text-[var(--color-text-muted)]">{unanswered}</b>
                      <small>Left</small>
                    </div>
                  </div>

                  {/* Filter tabs */}
                  <div className="quiz-filter-chips">
                    <button
                      className={`quiz-filter-chip ${navFilter === 'all' ? 'active' : ''}`}
                      onClick={() => setNavFilter('all')}
                    >
                      All ({active.questions.length})
                    </button>
                    <button
                      className={`quiz-filter-chip ${navFilter === 'unanswered' ? 'active' : ''}`}
                      onClick={() => setNavFilter('unanswered')}
                    >
                      Left ({unanswered})
                    </button>
                    <button
                      className={`quiz-filter-chip ${navFilter === 'flagged' ? 'active' : ''}`}
                      onClick={() => setNavFilter('flagged')}
                    >
                      Flagged ({flaggedCount})
                    </button>
                  </div>
                </div>

                {/* 5-Column Question Grid */}
                <div className="quiz-nav-grid-modern">
                  {active.questions.map((q, i) => {
                    const isAnswered = answers[q.id] !== undefined;
                    const isCurrent = i === currentQuestion;
                    const isFlagged = Boolean(flagged[q.id]);

                    let dimmed = false;
                    if (navFilter === 'unanswered' && isAnswered) dimmed = true;
                    if (navFilter === 'flagged' && !isFlagged) dimmed = true;

                    return (
                      <button
                        key={q.id}
                        className={`nav-grid-btn ${isCurrent ? 'current' : ''} ${
                          isAnswered ? 'answered' : ''
                        } ${isFlagged ? 'flagged-mark' : ''}`}
                        style={{ opacity: dimmed ? 0.35 : 1 }}
                        onClick={() => jumpTo(i)}
                        aria-label={`Question ${i + 1}${isCurrent ? ' current' : ''}${isAnswered ? ' answered' : ''}${isFlagged ? ' flagged' : ''}`}
                      >
                        {i + 1}
                        {isFlagged && <span className="flag-dot" />}
                      </button>
                    );
                  })}
                </div>

                <div className="quiz-nav-legend">
                  <div>
                    <span className="w-2.5 h-2.5 rounded-sm bg-[var(--color-green-accent)] inline-block" />
                    <span>Current Question</span>
                  </div>
                  <div>
                    <span className="w-2.5 h-2.5 rounded-sm bg-[#eef8f2] border border-[#b3dfc6] inline-block" />
                    <span>Answered ({answeredCount})</span>
                  </div>
                  <div>
                    <span className="w-2.5 h-2.5 rounded-sm bg-amber-400 inline-block" />
                    <span>Flagged for review ({flaggedCount})</span>
                  </div>
                  <div>
                    <span className="w-2.5 h-2.5 rounded-sm border border-[var(--color-card-border)] bg-[var(--color-card-bg)] inline-block" />
                    <span>Unanswered ({unanswered})</span>
                  </div>
                </div>

                <div className="sidebar-submit-card">
                  <div className="flex items-center justify-between text-xs font-bold text-[var(--color-text-dark)]">
                    <span>Ready to submit?</span>
                    <span className="text-[var(--color-green-accent)]">{progressPercent}% done</span>
                  </div>
                  <p>
                    {unanswered > 0
                      ? `${unanswered} question${unanswered > 1 ? 's' : ''} still unanswered.`
                      : 'All questions completed!'}
                  </p>
                  <button className="btn primary w-full text-xs" onClick={() => setConfirm(true)}>
                    <CheckCircle2 size={14} /> Submit Quiz
                  </button>
                </div>
              </aside>

              {mobileNav && (
                <button
                  className="question-nav-overlay"
                  aria-label="Close navigation"
                  onClick={() => setMobileNav(false)}
                />
              )}
            </div>
          ) : (
            /* Result Screen */
            <div className="quiz-result-wrapper">
              <div className="quiz-result-container">
                <div className="result-hero-card">
                  <div
                    className={`result-score-circle ${
                      result >= 80 ? 'excellent' : result >= 60 ? 'good' : 'needs-work'
                    }`}
                  >
                    <span className="text-3xl font-black">{result}%</span>
                    <span className="text-[0.65rem] font-bold uppercase tracking-wider mt-0.5">Score</span>
                  </div>

                  <div className="eyebrow">ASSESSMENT COMPLETED</div>
                  <h2 className="text-xl md:text-2xl font-bold font-serif mt-1">
                    {result >= 80
                      ? 'Exceptional Mastery! 🌟'
                      : result >= 60
                      ? 'Solid Understanding 👍'
                      : 'Targeted Review Recommended 🎯'}
                  </h2>
                  <p className="text-xs text-[var(--color-text-muted)] max-w-lg mx-auto mt-2 leading-relaxed">
                    You answered <b>{active.questions.filter(q => answers[q.id] === q.answer).length}</b> of{' '}
                    <b>{active.questions.length}</b> questions correctly.
                    {result < 70 && ' We have marked key concepts in your study planner to reinforce your understanding.'}
                  </p>

                  <div className="result-metric-grid mt-6">
                    <div className="result-metric-card">
                      <b className="text-emerald-600 dark:text-emerald-400">
                        {active.questions.filter(q => answers[q.id] === q.answer).length}
                      </b>
                      <span>Correct</span>
                    </div>
                    <div className="result-metric-card">
                      <b className="text-rose-600 dark:text-rose-400">
                        {active.questions.filter(q => answers[q.id] !== undefined && answers[q.id] !== q.answer).length}
                      </b>
                      <span>Incorrect</span>
                    </div>
                    <div className="result-metric-card">
                      <b className="text-amber-600 dark:text-amber-400">
                        {unanswered}
                      </b>
                      <span>Skipped</span>
                    </div>
                    <div className="result-metric-card">
                      <b className="text-[var(--color-text-dark)]">
                        {active.questions.length}
                      </b>
                      <span>Total Questions</span>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center justify-center gap-3 mt-6">
                    <button className="btn secondary text-xs" onClick={retry}>
                      <RotateCcw size={14} /> Retake Quiz
                    </button>
                    <button
                      className="btn secondary text-xs"
                      onClick={() => setShowReview(v => !v)}
                    >
                      <Target size={14} /> {showReview ? 'Hide Solutions' : 'Review Solutions'}
                    </button>
                    <button
                      className="btn primary text-xs"
                      onClick={() => {
                        closeQuiz();
                        generate();
                      }}
                    >
                      <Sparkles size={14} /> Next Practice Set
                    </button>
                    <button className="btn subtle text-xs" onClick={closeQuiz}>
                      <X size={14} /> Exit Assessment
                    </button>
                  </div>
                </div>

                {showReview && (
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <h3 className="text-base font-bold text-[var(--color-text-dark)]">
                        Question & Solution Breakdown
                      </h3>
                      <div className="quiz-filter-chips">
                        <button
                          className={`quiz-filter-chip ${solutionFilter === 'all' ? 'active' : ''}`}
                          onClick={() => setSolutionFilter('all')}
                        >
                          All ({active.questions.length})
                        </button>
                        <button
                          className={`quiz-filter-chip ${solutionFilter === 'incorrect' ? 'active' : ''}`}
                          onClick={() => setSolutionFilter('incorrect')}
                        >
                          Incorrect Only (
                          {active.questions.filter(q => answers[q.id] !== q.answer).length}
                          )
                        </button>
                        <button
                          className={`quiz-filter-chip ${solutionFilter === 'flagged' ? 'active' : ''}`}
                          onClick={() => setSolutionFilter('flagged')}
                        >
                          Flagged ({flaggedCount})
                        </button>
                      </div>
                    </div>

                    <div className="grid gap-3">
                      {active.questions
                        .filter(q => {
                          if (solutionFilter === 'incorrect') return answers[q.id] !== q.answer;
                          if (solutionFilter === 'flagged') return Boolean(flagged[q.id]);
                          return true;
                        })
                        .map((q, i) => {
                          const isCorrect = answers[q.id] === q.answer;
                          const isUnanswered = answers[q.id] === undefined;

                          return (
                            <div className="solution-card" key={q.id}>
                              <div className="solution-header">
                                <span className="font-bold text-xs text-[var(--color-text-dark)]">
                                  Q{i + 1}. {q.text}
                                </span>
                                <span
                                  className={`solution-status-badge ${
                                    isCorrect
                                      ? 'correct'
                                      : isUnanswered
                                      ? 'unanswered'
                                      : 'incorrect'
                                  }`}
                                >
                                  {isCorrect ? '✓ Correct' : isUnanswered ? 'Skipped' : '✗ Incorrect'}
                                </span>
                              </div>

                              <div className="solution-answers-box">
                                <div className="flex items-start gap-2">
                                  <span className="text-[var(--color-text-muted)] font-semibold w-24 flex-none">
                                    Your Choice:
                                  </span>
                                  <span
                                    className={`font-semibold ${
                                      isCorrect
                                        ? 'text-emerald-600 dark:text-emerald-400'
                                        : isUnanswered
                                        ? 'text-gray-500'
                                        : 'text-rose-600 dark:text-rose-400'
                                    }`}
                                  >
                                    {isUnanswered
                                      ? 'Not answered'
                                      : `${String.fromCharCode(65 + answers[q.id])}. ${q.options[answers[q.id]]}`}
                                  </span>
                                </div>
                                {!isCorrect && (
                                  <div className="flex items-start gap-2">
                                    <span className="text-[var(--color-text-muted)] font-semibold w-24 flex-none">
                                      Correct Answer:
                                    </span>
                                    <span className="font-bold text-emerald-700 dark:text-emerald-400">
                                      {String.fromCharCode(65 + q.answer)}. {q.options[q.answer]}
                                    </span>
                                  </div>
                                )}
                              </div>

                              {q.explanation && (
                                <div className="solution-explanation">
                                  <Lightbulb size={16} className="text-emerald-600 flex-none mt-0.5" />
                                  <div>
                                    <b className="block text-xs font-bold text-[var(--color-text-dark)] mb-0.5">
                                      Explanation & Concept
                                    </b>
                                    <p className="m-0 text-[0.74rem] text-[var(--color-text-body)]">
                                      {q.explanation}
                                    </p>
                                  </div>
                                </div>
                              )}
                            </div>
                          );
                        })}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Submit Confirmation Dialog inside Quiz Shell */}
          {confirm && (
            <div
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/55 backdrop-blur-sm"
              role="dialog"
              aria-modal="true"
              aria-label="Confirm quiz submission"
              onClick={() => setConfirm(false)}
            >
              <div
                className="bg-[var(--color-card-bg)] border border-[var(--color-card-border)] rounded-2xl max-w-md w-full p-6 shadow-2xl flex flex-col gap-4 text-left"
                onClick={e => e.stopPropagation()}
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-amber-500/15 text-amber-600 flex items-center justify-center flex-none mt-0.5">
                    <AlertCircle size={22} />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-[var(--color-text-dark)] m-0">
                      Submit Assessment?
                    </h3>
                    <p className="text-xs text-[var(--color-text-muted)] mt-1 mb-0 leading-relaxed">
                      You have answered <b>{answeredCount}</b> of <b>{active.questions.length}</b> questions. Once submitted, your score will be calculated and saved.
                    </p>
                  </div>
                </div>

                {unanswered > 0 && (
                  <div className="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 rounded-xl text-xs text-amber-800 dark:text-amber-300">
                    ⚠️ <b>{unanswered}</b> question{unanswered > 1 ? 's are' : ' is'} unanswered and will count as incorrect.
                  </div>
                )}

                {flaggedCount > 0 && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800/40 rounded-xl text-xs text-blue-800 dark:text-blue-300">
                    📌 <b>{flaggedCount}</b> question{flaggedCount > 1 ? 's are' : ' is'} flagged for review.
                  </div>
                )}

                <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-[var(--color-border-light)]">
                  <button
                    className="btn secondary text-xs"
                    onClick={() => setConfirm(false)}
                  >
                    Keep Working
                  </button>
                  <button
                    className="btn primary text-xs"
                    onClick={() => {
                      setConfirm(false);
                      submit();
                    }}
                  >
                    <CheckCircle2 size={14} /> Submit Assessment
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Quiz History Modal */}
      <Modal open={history} onClose={() => setHistory(false)} title="Quiz History" wide>
        <div>
          {quizzes.length ? (
            quizzes.map(q => (
              <div className="history-row" key={q.id}>
                <div>
                  <b>{q.title}</b>
                  <small>
                    {q.subject} · {q.difficulty} · {q.questions.length} questions ·{' '}
                    {q.completedAt ? new Date(q.completedAt).toLocaleDateString() : 'Draft'}
                  </small>
                </div>
                <span className="font-extrabold text-sm">{q.score === undefined ? 'Not attempted' : `${q.score}%`}</span>
                <button
                  className="btn subtle text-xs"
                  onClick={() => {
                    setActive(q);
                    setAnswers({});
                    setResult(null);
                    setCurrentQuestion(0);
                    setShowReview(false);
                    setTimer(0);
                    setHistory(false);
                  }}
                >
                  Retake
                </button>
              </div>
            ))
          ) : (
            <div className="empty-inline">
              No assessments generated yet. Select a topic above to create your first quiz.
            </div>
          )}
        </div>
      </Modal>

      {/* Submit Confirmation Modal */}
      <Modal open={confirm} onClose={() => setConfirm(false)} title="Submit assessment" subtitle="You cannot change answers after submitting.">
        <div className="flex items-start gap-3">
          <AlertCircle size={20} className="text-amber-600" />
          <p className="text-sm">
            You have answered <b>{answeredCount}</b> of {active?.questions.length || 0} questions.{' '}
            {unanswered > 0 ? (
              <>
                <b>{unanswered}</b> question{unanswered > 1 ? 's are' : ' is'} unanswered and will count as incorrect.
              </>
            ) : (
              <>All questions are answered.</>
            )}{' '}
            Submit now?
          </p>
        </div>
        <div className="modal-actions">
          <button className="btn secondary" onClick={() => setConfirm(false)}>
            Keep working
          </button>
          <button className="btn primary" onClick={submit}>
            Submit now
          </button>
        </div>
      </Modal>
    </div>
  );
}
