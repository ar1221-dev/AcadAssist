// AcadAssist Mock Data — Arbitrary & Simulated Academic Universe
// All data is completely arbitrary, fabricated, and simulated for demonstration.

export interface UserProfile {
  name: string;
  fullName: string;
  role: string;
  field: string;
  academicLevel: string;
  email: string;
  location: string;
  memberSince: string;
  bio: string;
  tags: string[];
  quote: string;
  streakDays: number;
  streakStatus: string;
  cgpa: string;
}

export interface StatsSummary {
  dayStreak: number;
  topicsCompleted: number;
  hoursStudied: number;
  averageScore: number;
  notesLearned: number;
  questionsPracticed: number;
  totalStudyTime: number;
  overallProgress: number;
  notesIncrease: string;
  questionsIncrease: string;
  studyTimeIncrease: string;
  progressIncrease: string;
}

export interface Subject {
  id: string;
  name: string;
  fullName: string;
  documentsCount: number;
  progress: number;
  topicsCompleted: number;
  totalTopics: number;
  color: string;
  tag: string;
}

export interface StudyPlanItem {
  id: string;
  time: string;
  title: string;
  description: string;
  subject: string;
  tag: string;
  duration: string;
  status: 'completed' | 'pending';
  actionLabel: string;
  color: string;
  icon: string;
}

export interface PlannerTask {
  id: string;
  time: string;
  title: string;
  description: string;
  subjectTag: string;
  duration: string;
  completed: boolean;
  type: 'study' | 'practice' | 'break' | 'quiz';
}

export interface Exam {
  id: string;
  subject: string;
  examName: string;
  daysLeft: number;
  dateStr: string;
  urgency: 'urgent' | 'high' | 'medium' | 'normal';
  icon: string;
}

export interface Deadline {
  title: string;
  daysLeft: string;
  dateStr: string;
  urgency: 'urgent' | 'high' | 'medium' | 'normal';
}

export interface KnowledgeMaterial {
  name: string;
  subject: string;
  type: 'PDF' | 'PPT' | 'DOCX' | 'TXT';
  size: string;
  addedOn: string;
  status: string;
  starred: boolean;
}

export interface Activity {
  iconColor: string;
  text: string;
  time: string;
  action: string;
}

export interface AssessmentPerformance {
  averageScore: number;
  delta: string;
  questionsAttempted: number;
  correctAnswers: number;
  topicsCovered: number;
}

export interface RecentAttempt {
  topic: string;
  difficulty: string;
  scoreFraction: string;
  percentage: string;
  date: string;
  status: 'excellent' | 'passed' | 'average' | 'failed';
}

export interface PracticeSet {
  title: string;
  subtitle: string;
  questionsCount: number;
  type: string;
  icon: string;
  color: string;
}

export interface Milestone {
  title: string;
  date: string;
  completed: boolean;
}

export interface Badge {
  name: string;
  icon: string;
  color: string;
  unlocked: boolean;
}

export interface HelpCategory {
  title: string;
  description: string;
  icon: string;
  color: string;
}

export interface SystemStatus {
  name: string;
  status: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  time: string;
  text: string;
}

// ─── DATA (100% ARBITRARY & SIMULATED) ──────────────────────────────────────────

export const USER_PROFILE: UserProfile = {
  name: 'Rowan',
  fullName: 'Rowan K. Vance',
  role: 'Junior Research Fellow & Scholar',
  field: 'Cognitive Computing & Cyber-Physical Systems',
  academicLevel: 'Honors Bachelor of Science (Class of 2027)',
  email: 'rowan.vance@solaris-institute.edu',
  location: 'Sector 4, Cambridge Quadrangle',
  memberSince: '14 Oct 2024',
  bio: 'Investigating decentralized consensus protocols, neuromorphic sensory computing, and non-Euclidean manifold embeddings. Passionate about synthetic curiosity, generative modeling, and open science.',
  tags: ['Autonomous Systems', 'Neuromorphic Chips', 'Information Theory', 'Synthwave', 'Open Science'],
  quote: 'Curiosity is the architecture of discovery.',
  streakDays: 43,
  streakStatus: 'Ranked in top 1.5% most consistent researchers',
  cgpa: '3.92 / 4.00',
};

export const STATS_SUMMARY: StatsSummary = {
  dayStreak: 43,
  topicsCompleted: 14,
  hoursStudied: 38.5,
  averageScore: 92,
  notesLearned: 164,
  questionsPracticed: 285,
  totalStudyTime: 56.5,
  overallProgress: 86,
  notesIncrease: '↑ 18% this cycle',
  questionsIncrease: '↑ 34% this cycle',
  studyTimeIncrease: '↑ 22% this cycle',
  progressIncrease: '↑ 14% this cycle',
};

export const SUBJECTS: Subject[] = [
  {
    id: 'qc',
    name: 'Quantum Cognition',
    fullName: 'Quantum Cognition & Dynamic Manifolds',
    documentsCount: 14,
    progress: 88,
    topicsCompleted: 11,
    totalTopics: 14,
    color: '#2d5f47',
    tag: 'QC',
  },
  {
    id: 'rob',
    name: 'Autonomous Robotics',
    fullName: 'Autonomous Systems & Swarm Kinematics',
    documentsCount: 11,
    progress: 74,
    topicsCompleted: 8,
    totalTopics: 12,
    color: '#e07a5f',
    tag: 'ROB',
  },
  {
    id: 'astro',
    name: 'Astrophysics',
    fullName: 'Computational Astrophysics & Stellar Hydrodynamics',
    documentsCount: 9,
    progress: 68,
    topicsCompleted: 6,
    totalTopics: 10,
    color: '#6366f1',
    tag: 'ASTRO',
  },
  {
    id: 'bio',
    name: 'Synthetic Genomics',
    fullName: 'Synthetic Genomics & Protein Informatics',
    documentsCount: 12,
    progress: 91,
    topicsCompleted: 10,
    totalTopics: 11,
    color: '#0ea5e9',
    tag: 'BIO',
  },
  {
    id: 'dcp',
    name: 'Decentralized Systems',
    fullName: 'Decentralized Protocols & Byzantine Consensus',
    documentsCount: 8,
    progress: 62,
    topicsCompleted: 5,
    totalTopics: 9,
    color: '#d97706',
    tag: 'DCP',
  },
  {
    id: 'ling',
    name: 'Computational Linguistics',
    fullName: 'Computational Linguistics & Semantic Representation',
    documentsCount: 7,
    progress: 80,
    topicsCompleted: 8,
    totalTopics: 10,
    color: '#8b5cf6',
    tag: 'LING',
  },
];

export const TODAY_STUDY_PLAN: StudyPlanItem[] = [
  {
    id: 'plan-1',
    time: '09:00 AM',
    title: 'Stochastic Manifold Modeling',
    description: 'Simulate non-linear phase transitions & tensor contractions',
    subject: 'Quantum Cognition',
    tag: 'QC',
    duration: '45 min',
    status: 'completed',
    actionLabel: 'Review',
    color: '#2d5f47',
    icon: 'file-text',
  },
  {
    id: 'plan-2',
    time: '11:30 AM',
    title: 'Swarm Consensus Latency',
    description: 'Simulate Byzantine consensus across 500 edge nodes',
    subject: 'Decentralized Systems',
    tag: 'DCP',
    duration: '40 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#d97706',
    icon: 'code',
  },
  {
    id: 'plan-3',
    time: '02:30 PM',
    title: 'Kerr Metric Spacetime Analysis',
    description: 'Derive relativistic frame dragging geodesics',
    subject: 'Astrophysics',
    tag: 'ASTRO',
    duration: '50 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#6366f1',
    icon: 'database',
  },
  {
    id: 'plan-4',
    time: '07:00 PM',
    title: 'Synthetic Genomics Diagnostic',
    description: '15 arbitrary multidisciplinary scenarios',
    subject: 'Synthetic Genomics',
    tag: 'BIO',
    duration: '25 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#0ea5e9',
    icon: 'check-square',
  },
];

export const PLANNER_TIMELINE_TASKS: PlannerTask[] = [
  { id: 'pt-1', time: '08:00 AM', title: 'Morning Literature Brief', description: 'Review arXiv preprint on Non-Euclidean Graph Laplacians', subjectTag: 'QC', duration: '30 min', completed: true, type: 'study' },
  { id: 'pt-2', time: '09:00 AM', title: 'Quantum Manifolds Session', description: 'Derive state evolution equations in tensor spaces', subjectTag: 'QC', duration: '45 min', completed: true, type: 'study' },
  { id: 'pt-3', time: '11:00 AM', title: 'Swarm Navigation Simulation', description: 'Test collision avoidance under stochastic noise', subjectTag: 'ROB', duration: '45 min', completed: false, type: 'practice' },
  { id: 'pt-4', time: '01:00 PM', title: 'Refuel & Sensory Rest', description: 'Campus conservatory walk & hydration', subjectTag: 'Break', duration: '1 hr', completed: true, type: 'break' },
  { id: 'pt-5', time: '02:30 PM', title: 'Accretion Flow Derivation', description: 'Solve relativistic magnetohydrodynamics equations', subjectTag: 'ASTRO', duration: '50 min', completed: false, type: 'study' },
  { id: 'pt-6', time: '04:30 PM', title: 'Bio-Foundry Mock Diagnostic', description: '15 practice scenarios on synthetic ligase docking', subjectTag: 'BIO', duration: '30 min', completed: false, type: 'quiz' },
  { id: 'pt-7', time: '07:00 PM', title: 'Consensus Protocols Review', description: 'Synthesize notes on Raft election timeouts', subjectTag: 'DCP', duration: '35 min', completed: false, type: 'study' },
];

export const UPCOMING_EXAMS: Exam[] = [
  { id: 'exam-1', subject: 'Quantum Cognition', examName: 'Quantum Information & Topology (Symposium)', daysLeft: 5, dateStr: '25 Sep 2026', urgency: 'urgent', icon: 'book-open' },
  { id: 'exam-2', subject: 'Decentralized Systems', examName: 'Decentralized Consensus Comprehensive', daysLeft: 12, dateStr: '02 Oct 2026', urgency: 'high', icon: 'database' },
  { id: 'exam-3', subject: 'Astrophysics', examName: 'Astrophysical Fluid Dynamics Defense', daysLeft: 19, dateStr: '09 Oct 2026', urgency: 'medium', icon: 'share-2' },
  { id: 'exam-4', subject: 'Synthetic Genomics', examName: 'Synthetic Genomics Benchmark Presentation', daysLeft: 26, dateStr: '16 Oct 2026', urgency: 'normal', icon: 'shield' },
];

export const UPCOMING_DEADLINES: Deadline[] = [
  { title: 'Quantum Topology Problem Set 4', daysLeft: '2 days left', dateStr: '22 Sep 2026', urgency: 'urgent' },
  { title: 'Quantum Information & Topology Exam', daysLeft: '5 days left', dateStr: '25 Sep 2026', urgency: 'urgent' },
  { title: 'Swarm Kinematics Lab Milestone', daysLeft: '9 days left', dateStr: '29 Sep 2026', urgency: 'high' },
  { title: 'Decentralized Consensus Comprehensive', daysLeft: '12 days left', dateStr: '02 Oct 2026', urgency: 'medium' },
  { title: 'Astrophysical Fluid Dynamics Defense', daysLeft: '19 days left', dateStr: '09 Oct 2026', urgency: 'normal' },
];

export const KNOWLEDGE_MATERIALS: KnowledgeMaterial[] = [
  { name: 'Quantum_Manifold_Topologies_v3.pdf', subject: 'Quantum Cognition', type: 'PDF', size: '3.8 MB', addedOn: '18 Sep 2026', status: 'Ready', starred: true },
  { name: 'Byzantine_Fault_Tolerance_Proof.docx', subject: 'Decentralized Systems', type: 'DOCX', size: '1.4 MB', addedOn: '16 Sep 2026', status: 'Ready', starred: true },
  { name: 'Accretion_Disk_Simulations.pptx', subject: 'Astrophysics', type: 'PPT', size: '6.2 MB', addedOn: '14 Sep 2026', status: 'Ready', starred: false },
  { name: 'CRISPR_Enzyme_Docking_Priors.pdf', subject: 'Synthetic Genomics', type: 'PDF', size: '4.5 MB', addedOn: '11 Sep 2026', status: 'Ready', starred: false },
  { name: 'Swarm_Kinematics_LabManual.docx', subject: 'Autonomous Robotics', type: 'DOCX', size: '980 KB', addedOn: '09 Sep 2026', status: 'Ready', starred: false },
  { name: 'Semantic_Graph_Embeddings.pdf', subject: 'Computational Linguistics', type: 'PDF', size: '2.7 MB', addedOn: '06 Sep 2026', status: 'Ready', starred: false },
];

export const RECENT_ACTIVITIES: Activity[] = [
  { iconColor: '#2d5f47', text: 'Completed quiz on Quantum Manifolds (Score: 95%)', time: '1 hour ago', action: 'quiz' },
  { iconColor: '#0ea5e9', text: 'Uploaded CRISPR_Enzyme_Docking_Priors.pdf', time: '4 hours ago', action: 'upload' },
  { iconColor: '#d97706', text: 'Studied Byzantine Fault Tolerance – 45 minutes', time: '1 day ago', action: 'study' },
  { iconColor: '#6366f1', text: 'Queried AI Assistant on relativistic frame dragging', time: '1 day ago', action: 'chat' },
  { iconColor: '#e07a5f', text: 'Completed simulation on Swarm Kinematics', time: '2 days ago', action: 'read' },
];

export const ASSESSMENT_PERFORMANCE: AssessmentPerformance = {
  averageScore: 91,
  delta: '↑ 14% this cycle',
  questionsAttempted: 285,
  correctAnswers: 260,
  topicsCovered: 32,
};

export const RECENT_ATTEMPTS: RecentAttempt[] = [
  { topic: 'Tensor Contractions', difficulty: 'Hard', scoreFraction: '10 / 10', percentage: '100%', date: '18 Sep 2026', status: 'excellent' },
  { topic: 'Swarm Consensus Latency', difficulty: 'Medium', scoreFraction: '9 / 10', percentage: '90%', date: '16 Sep 2026', status: 'passed' },
  { topic: 'Relativistic Geodesics', difficulty: 'Hard', scoreFraction: '8 / 10', percentage: '80%', date: '14 Sep 2026', status: 'passed' },
  { topic: 'Enzyme Active Site Docking', difficulty: 'Medium', scoreFraction: '9 / 10', percentage: '90%', date: '12 Sep 2026', status: 'excellent' },
];

export const POPULAR_PRACTICE_SETS: PracticeSet[] = [
  { title: 'Quantum Dynamics Essentials', subtitle: 'Hilbert Spaces, Manifold Projections, Tensor Networks', questionsCount: 50, type: 'Mixed', icon: 'share-2', color: '#2d5f47' },
  { title: 'Decentralized Consensus Mastery', subtitle: 'Raft, Paxos, Byzantine Quorums, State Replicas', questionsCount: 45, type: 'Mixed', icon: 'database', color: '#d97706' },
  { title: 'Astrophysical Plasma Mechanics', subtitle: 'Magnetohydrodynamics, Shocks, Accretion Flows', questionsCount: 40, type: 'Mixed', icon: 'wifi', color: '#6366f1' },
  { title: 'Generative Protein Design', subtitle: 'Diffusion Priors, Macrocyclic Peptides, Docking', questionsCount: 35, type: 'Mixed', icon: 'zap', color: '#0ea5e9' },
];

export const MILESTONES: Milestone[] = [
  { title: 'Completed 250 simulated benchmark questions', date: '08 Sep 2026', completed: true },
  { title: '40-day continuous research streak', date: '14 Sep 2026', completed: true },
  { title: 'Validated Swarm Kinematics simulation', date: '17 Sep 2026', completed: true },
  { title: 'Publish Quantum Manifold preprint', date: 'Target: 30 Sep 2026', completed: false },
];

export const BADGES: Badge[] = [
  { name: 'Quantum Sprint', icon: 'calendar', color: '#2d5f47', unlocked: true },
  { name: 'Graph Pioneer', icon: 'award', color: '#3b82f6', unlocked: true },
  { name: 'Polymath', icon: 'book-open', color: '#8b5cf6', unlocked: true },
  { name: 'Cosmic Navigator', icon: 'grid', color: '#f59e0b', unlocked: true },
  { name: 'Neural Architect', icon: 'shield', color: '#ec4899', unlocked: true },
];

export const STUDY_GOALS = [
  { id: 'g1', text: 'Synthesize benchmark results for Sparse Graph Attention', completed: true },
  { id: 'g2', text: 'Run 100M particle Monte Carlo simulation for disc turbulence', completed: true },
  { id: 'g3', text: 'Validate 24 synthetic allosteric enzyme binding pockets', completed: false },
  { id: 'g4', text: 'Submit preprint on Neuromorphic Sensory Routing', completed: false },
];

export const HELP_CATEGORIES: HelpCategory[] = [
  { title: 'Knowledge Base', description: 'Upload notes, organize subject files, and manage your library.', icon: 'book-open', color: '#2d5f47' },
  { title: 'Simulated Assessments', description: 'Create adaptive quizzes, diagnostic runs, and track score analytics.', icon: 'file-text', color: '#3b82f6' },
  { title: 'Research Planner', description: 'Schedule milestones, set focus intervals, and sync project deadlines.', icon: 'calendar', color: '#8b5cf6' },
  { title: 'AI Assistant', description: 'Interactive synthetic assistant for complex derivation and paper synthesis.', icon: 'sparkles', color: '#f59e0b' },
  { title: 'Account & Dossier', description: 'Manage arbitrary personas, notification preferences, and themes.', icon: 'settings', color: '#6366f1' },
  { title: 'Security & Privacy', description: 'Local simulation confidentiality, storage policies, and exports.', icon: 'shield', color: '#10b981' },
];

export const SYSTEM_STATUS_ITEMS: SystemStatus[] = [
  { name: 'Synthetic Embedding Service', status: 'Operational' },
  { name: 'Tensor Compilation Engine', status: 'Operational' },
  { name: 'Simulation Pipeline (GPU)', status: 'Operational' },
  { name: 'Local Cache Store', status: 'Optimal' },
];

export const CHAT_HISTORY_INITIAL: ChatMessage[] = [
  {
    role: 'user',
    time: '10:14 AM',
    text: 'How do Non-Euclidean manifold projections preserve semantic hierarchy in multi-agent models?',
  },
  {
    role: 'assistant',
    time: '10:15 AM',
    text: `### Geometric Manifold Projections & Semantic Hierarchy

In high-dimensional representation learning, embedding complex hierarchical structures into standard Euclidean space suffers from exponential volume distortion. Mapping latent representations to Riemannian manifolds (such as the **Poincaré Ball** or **Lorentz Hyperboloid**) solves this directly.

**Key Mathematical Insights:**

1. **Exponential Volume Growth**
   - In hyperbolic space $\\mathbb{H}^n$, volume grows exponentially with radius $r$: $\\text{Vol}(r) \\propto \\sinh^{n-1}(r)$.
   - This naturally accommodates tree-like hierarchical branchings without crowding the boundary.

2. **Geodesic Distance Preservation**
   - The hyperbolic distance between two points $u, v$ in the Poincaré ball model is:
     $$d_{\\mathbb{D}}(u, v) = \\text{arcosh}\\left(1 + 2 \\frac{\\|u - v\\|^2}{(1 - \\|u\\|^2)(1 - \\|v\\|^2)}\\right)$$

3. **Tangent Space Retractions**
   - Optimization updates compute Riemannian gradients projected back onto the manifold via exponential and logarithmic maps:
     $$\\exp_x(v) = x \\oplus \\left(\\tanh\\left(\\frac{\\lambda_x \\|v\\|}{2}\\right) \\frac{v}{\\|v\\|}\\right)$$

Would you like to simulate a toy embedding or explore a benchmark comparison?`,
  },
];

// Study time chart data (weekly bar chart for Progress page)
export const WEEKLY_STUDY_HOURS = [
  { day: 'Mon', hours: 4.5 },
  { day: 'Tue', hours: 5.2 },
  { day: 'Wed', hours: 3.8 },
  { day: 'Thu', hours: 6.0 },
  { day: 'Fri', hours: 5.5 },
  { day: 'Sat', hours: 3.0 },
  { day: 'Sun', hours: 4.0 },
];

// Activity distribution (donut chart for Progress page)
export const ACTIVITY_DISTRIBUTION = [
  { name: 'Tensor Derivation', value: 38, color: '#2d5f47' },
  { name: 'Simulation Runs', value: 28, color: '#6366f1' },
  { name: 'Diagnostic Assessments', value: 18, color: '#e07a5f' },
  { name: 'AI Synthesis Query', value: 11, color: '#0ea5e9' },
  { name: 'Other', value: 5, color: '#8b5cf6' },
];

// Progress over time (line chart for Progress page)
export const PROGRESS_OVER_TIME = [
  { date: '17 Aug', progress: 32 },
  { date: '24 Aug', progress: 45 },
  { date: '31 Aug', progress: 58 },
  { date: '07 Sep', progress: 72 },
  { date: '14 Sep', progress: 86 },
];

// Subject progress (extended for progress page)
export const SUBJECT_PROGRESS = [
  { name: 'Quantum Cognition & Dynamic Manifolds', progress: 88, icon: 'cpu', color: '#2d5f47' },
  { name: 'Autonomous Systems & Swarm Kinematics', progress: 74, icon: 'share-2', color: '#e07a5f' },
  { name: 'Computational Astrophysics & Hydrodynamics', progress: 68, icon: 'wifi', color: '#6366f1' },
  { name: 'Synthetic Genomics & Protein Informatics', progress: 91, icon: 'zap', color: '#0ea5e9' },
  { name: 'Decentralized Protocols & Consensus', progress: 62, icon: 'database', color: '#d97706' },
  { name: 'Computational Linguistics & Semantics', progress: 80, icon: 'book-open', color: '#8b5cf6' },
];

// Interests for Profile page
export const INTERESTS = [
  { name: 'Swarm Robotics', icon: 'cpu' },
  { name: 'Quantum Topology', icon: 'globe' },
  { name: 'Stellar Hydrodynamics', icon: 'music' },
  { name: 'Synthetic Genomics', icon: 'briefcase' },
  { name: 'Synthesizer Engineering', icon: 'book-open' },
  { name: 'Competitive Chess', icon: 'github' },
];
