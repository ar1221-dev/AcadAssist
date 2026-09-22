// AcadAssist Project Data — Curriculum Baseline & Sample Dataset
// All scores, progress percentages, and activity histories below are explicitly marked as Sample / Demo Data.

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
  isDemo?: boolean;
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
  isDemo?: boolean;
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
  code?: string;
  semester?: string;
  examDate?: string;
  importance?: 'Low' | 'Medium' | 'High';
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
  id?: string;
  name: string;
  subject: string;
  type: 'PDF' | 'PPT' | 'DOCX' | 'TXT';
  size: string;
  addedOn: string;
  status: string;
  starred: boolean;
  isDemo?: boolean;
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
  isDemo?: boolean;
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

// ─── SAMPLE USER PROFILE (DEMO STUDENT) ───────────────────────────────────────

export const USER_PROFILE: UserProfile = {
  name: 'Demo Student',
  fullName: 'Demo Student',
  role: 'Undergraduate Student',
  field: 'Computer Science & Engineering',
  academicLevel: 'Undergraduate Degree Program',
  email: 'student.demo@acadassist.local',
  location: 'University Campus',
  memberSince: 'Aug 2026',
  bio: 'Sample workspace showcasing AcadAssist. Managing course documents, solving daily quizzes, and tracking revision progress for upcoming exams.',
  tags: ['Operating Systems', 'Computer Networks', 'Database Systems', 'Algorithms', 'Machine Learning'],
  quote: 'Consistent daily focus beats last-minute exam cramming.',
  streakDays: 12,
  streakStatus: 'Active study streak · Sample Workspace',
  cgpa: '8.8 / 10.0 (Sample)',
  isDemo: true,
};

export const STATS_SUMMARY: StatsSummary = {
  dayStreak: 12,
  topicsCompleted: 24,
  hoursStudied: 28.5,
  averageScore: 78,
  notesLearned: 42,
  questionsPracticed: 160,
  totalStudyTime: 38.0,
  overallProgress: 64,
  notesIncrease: '↑ 12% this week',
  questionsIncrease: '↑ 25% this week',
  studyTimeIncrease: '↑ 15% this week',
  progressIncrease: '↑ 8% this week',
  isDemo: true,
};

// ─── CORE CURRICULUM SUBJECTS ────────────────────────────────────────────────

export const SUBJECTS: Subject[] = [
  {
    id: 'os',
    name: 'Operating Systems',
    fullName: 'Operating Systems (CSE-302)',
    documentsCount: 6,
    progress: 61,
    topicsCompleted: 4,
    totalTopics: 6,
    color: '#315c8b',
    tag: 'OS',
    code: 'CSE-302',
    semester: 'Semester 5',
    examDate: '2026-09-27',
    importance: 'High',
  },
  {
    id: 'cn',
    name: 'Computer Networks',
    fullName: 'Computer Networks (CSE-304)',
    documentsCount: 5,
    progress: 43,
    topicsCompleted: 2,
    totalTopics: 5,
    color: '#8b5a31',
    tag: 'CN',
    code: 'CSE-304',
    semester: 'Semester 5',
    examDate: '2026-10-04',
    importance: 'High',
  },
  {
    id: 'dbms',
    name: 'Database Management Systems',
    fullName: 'Database Management Systems (CSE-305)',
    documentsCount: 4,
    progress: 28,
    topicsCompleted: 2,
    totalTopics: 5,
    color: '#6a4c93',
    tag: 'DBMS',
    code: 'CSE-305',
    semester: 'Semester 5',
    examDate: '2026-10-11',
    importance: 'Medium',
  },
  {
    id: 'dsa',
    name: 'Data Structures & Algorithms',
    fullName: 'Data Structures & Algorithms (CSE-201)',
    documentsCount: 7,
    progress: 52,
    topicsCompleted: 3,
    totalTopics: 6,
    color: '#2d5f47',
    tag: 'DSA',
    code: 'CSE-201',
    semester: 'Semester 3',
    examDate: '2026-10-18',
    importance: 'High',
  },
  {
    id: 'ml',
    name: 'Machine Learning',
    fullName: 'Machine Learning (CSE-401)',
    documentsCount: 3,
    progress: 18,
    topicsCompleted: 1,
    totalTopics: 6,
    color: '#a14b5d',
    tag: 'ML',
    code: 'CSE-401',
    semester: 'Semester 7',
    examDate: '2026-10-25',
    importance: 'Medium',
  },
  {
    id: 'python',
    name: 'Python Programming',
    fullName: 'Python Programming (CS-101)',
    documentsCount: 4,
    progress: 75,
    topicsCompleted: 4,
    totalTopics: 6,
    color: '#b17b24',
    tag: 'PY',
    code: 'CS-101',
    semester: 'Semester 1',
    examDate: '2026-11-02',
    importance: 'Low',
  },
];

export const TODAY_STUDY_PLAN: StudyPlanItem[] = [
  {
    id: 'plan-1',
    time: '09:00 AM',
    title: 'OS Deadlock Coffman Conditions',
    description: 'Review mutual exclusion, hold and wait, no preemption, circular wait',
    subject: 'Operating Systems',
    tag: 'OS',
    duration: '45 min',
    status: 'completed',
    actionLabel: 'Review',
    color: '#315c8b',
    icon: 'file-text',
  },
  {
    id: 'plan-2',
    time: '11:30 AM',
    title: 'TCP vs UDP Sliding Window & Flow Control',
    description: 'Solve 10 diagnostic questions on three-way handshakes and segment headers',
    subject: 'Computer Networks',
    tag: 'CN',
    duration: '40 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#8b5a31',
    icon: 'code',
  },
  {
    id: 'plan-3',
    time: '02:30 PM',
    title: 'B+ Tree Indexing & Node Splitting',
    description: 'Derive search depth and block pointers for clustered index queries',
    subject: 'Database Management Systems',
    tag: 'DBMS',
    duration: '50 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#6a4c93',
    icon: 'database',
  },
  {
    id: 'plan-4',
    time: '05:00 PM',
    title: 'Binary Search Tree Balancing Practice',
    description: 'AVL tree rotations and inorder traversal complexity',
    subject: 'Data Structures & Algorithms',
    tag: 'DSA',
    duration: '30 min',
    status: 'pending',
    actionLabel: 'Start',
    color: '#2d5f47',
    icon: 'check-square',
  },
];

export const PLANNER_TIMELINE_TASKS: PlannerTask[] = [
  { id: 'pt-1', time: '08:30 AM', title: 'OS Deadlocks Review', description: 'Study resource-allocation graphs and deadlock prevention rules', subjectTag: 'OS', duration: '40 min', completed: true, type: 'study' },
  { id: 'pt-2', time: '10:00 AM', title: 'Transport Layer Diagnostics', description: 'Complete 10 MCQs on TCP connection teardown and windowing', subjectTag: 'CN', duration: '35 min', completed: true, type: 'quiz' },
  { id: 'pt-3', time: '11:45 AM', title: 'DBMS Normalization Problem Set', description: 'Decompose relations into 3NF and BCNF without losing dependencies', subjectTag: 'DBMS', duration: '45 min', completed: false, type: 'practice' },
  { id: 'pt-4', time: '01:00 PM', title: 'Lunch & Break', description: 'Step away from screen, hydration and brief walk', subjectTag: 'Break', duration: '45 min', completed: true, type: 'break' },
  { id: 'pt-5', time: '02:30 PM', title: 'Graph BFS/DFS Practice', description: 'Implement cycle detection in directed graphs using recursion stack', subjectTag: 'DSA', duration: '50 min', completed: false, type: 'study' },
  { id: 'pt-6', time: '04:30 PM', title: 'Regression Cost Functions', description: 'Understand Mean Squared Error (MSE) and gradient descent updates', subjectTag: 'ML', duration: '35 min', completed: false, type: 'study' },
];

export const UPCOMING_EXAMS: Exam[] = [
  { id: 'exam-1', subject: 'Operating Systems', examName: 'Operating Systems Midterm Exam', daysLeft: 5, dateStr: '27 Sep 2026', urgency: 'urgent', icon: 'book-open' },
  { id: 'exam-2', subject: 'Computer Networks', examName: 'Computer Networks Mid-Term Assessment', daysLeft: 12, dateStr: '04 Oct 2026', urgency: 'high', icon: 'share-2' },
  { id: 'exam-3', subject: 'Database Management Systems', examName: 'DBMS Semester Comprehensive', daysLeft: 19, dateStr: '11 Oct 2026', urgency: 'medium', icon: 'database' },
  { id: 'exam-4', subject: 'Data Structures & Algorithms', examName: 'DSA Practical Lab Defense', daysLeft: 26, dateStr: '18 Oct 2026', urgency: 'normal', icon: 'shield' },
];

export const UPCOMING_DEADLINES: Deadline[] = [
  { title: 'OS Deadlock Coffman Problem Sheet', daysLeft: '2 days left', dateStr: '24 Sep 2026', urgency: 'urgent' },
  { title: 'Operating Systems Midterm Exam', daysLeft: '5 days left', dateStr: '27 Sep 2026', urgency: 'urgent' },
  { title: 'Networks Socket Programming Milestone', daysLeft: '9 days left', dateStr: '01 Oct 2026', urgency: 'high' },
  { title: 'Computer Networks Mid-Term Assessment', daysLeft: '12 days left', dateStr: '04 Oct 2026', urgency: 'high' },
  { title: 'DBMS Relational Normalization Quiz', daysLeft: '19 days left', dateStr: '11 Oct 2026', urgency: 'medium' },
];

export const KNOWLEDGE_MATERIALS: KnowledgeMaterial[] = [
  { name: 'OS_Unit3_Deadlocks_and_Prevention.pdf', subject: 'Operating Systems', type: 'PDF', size: '2.4 MB', addedOn: '18 Sep 2026', status: 'Ready', starred: true, isDemo: true },
  { name: 'CN_Transport_Layer_TCP_UDP.docx', subject: 'Computer Networks', type: 'DOCX', size: '1.2 MB', addedOn: '16 Sep 2026', status: 'Ready', starred: true, isDemo: true },
  { name: 'DBMS_Relational_Algebra_and_SQL.pptx', subject: 'Database Management Systems', type: 'PPT', size: '4.8 MB', addedOn: '14 Sep 2026', status: 'Ready', starred: false, isDemo: true },
  { name: 'DSA_Graph_Traversals_BFS_DFS.pdf', subject: 'Data Structures & Algorithms', type: 'PDF', size: '3.1 MB', addedOn: '12 Sep 2026', status: 'Ready', starred: false, isDemo: true },
  { name: 'ML_Linear_and_Logistic_Regression.pdf', subject: 'Machine Learning', type: 'PDF', size: '2.8 MB', addedOn: '09 Sep 2026', status: 'Ready', starred: false, isDemo: true },
  { name: 'Python_OOP_and_Exception_Handling.txt', subject: 'Python Programming', type: 'TXT', size: '85 KB', addedOn: '06 Sep 2026', status: 'Ready', starred: false, isDemo: true },
];

export const RECENT_ACTIVITIES: Activity[] = [
  { iconColor: '#315c8b', text: 'Completed quiz on CPU Scheduling (Score: 90%)', time: '2 hours ago', action: 'quiz' },
  { iconColor: '#8b5a31', text: 'Uploaded CN_Transport_Layer_TCP_UDP.docx', time: '5 hours ago', action: 'upload' },
  { iconColor: '#6a4c93', text: 'Practiced SQL normalization & BCNF — 40 minutes', time: '1 day ago', action: 'study' },
  { iconColor: '#2d5f47', text: 'Generated AI Notes from OS Deadlocks material', time: '1 day ago', action: 'notes' },
  { iconColor: '#a14b5d', text: 'Consulted AI Assistant on Gradient Descent convergence', time: '2 days ago', action: 'chat' },
];

export const ASSESSMENT_PERFORMANCE: AssessmentPerformance = {
  averageScore: 78,
  delta: '↑ 8% from last week',
  questionsAttempted: 160,
  correctAnswers: 125,
  topicsCovered: 14,
  isDemo: true,
};

export const RECENT_ATTEMPTS: RecentAttempt[] = [
  { topic: 'CPU Scheduling Algorithms', difficulty: 'Medium', scoreFraction: '9 / 10', percentage: '90%', date: '21 Sep 2026', status: 'excellent' },
  { topic: 'Deadlocks & Coffman Conditions', difficulty: 'Medium', scoreFraction: '6 / 10', percentage: '60%', date: '19 Sep 2026', status: 'average' },
  { topic: 'Transport Layer Protocols', difficulty: 'Hard', scoreFraction: '5 / 10', percentage: '50%', date: '17 Sep 2026', status: 'failed' },
  { topic: 'SQL Normalization (1NF-3NF)', difficulty: 'Medium', scoreFraction: '8 / 10', percentage: '80%', date: '15 Sep 2026', status: 'passed' },
];

export const POPULAR_PRACTICE_SETS: PracticeSet[] = [
  { title: 'Operating Systems Core', subtitle: 'Processes, CPU Scheduling, Deadlocks, Memory Management', questionsCount: 40, type: 'Mixed', icon: 'cpu', color: '#315c8b' },
  { title: 'Computer Networks Protocols', subtitle: 'TCP, UDP, Subnetting, IP Addressing, Routing Algorithms', questionsCount: 35, type: 'Mixed', icon: 'share-2', color: '#8b5a31' },
  { title: 'Database Relational Design', subtitle: 'ER Models, Functional Dependencies, Normalization, Indexing', questionsCount: 30, type: 'Mixed', icon: 'database', color: '#6a4c93' },
  { title: 'Algorithms & Complexity', subtitle: 'Asymptotic Analysis, Trees, Graphs, Sorting & Searching', questionsCount: 45, type: 'Mixed', icon: 'code', color: '#2d5f47' },
];

export const MILESTONES: Milestone[] = [
  { title: 'Completed 150 practice questions', date: '14 Sep 2026', completed: true },
  { title: 'Maintained 10-day continuous study streak', date: '18 Sep 2026', completed: true },
  { title: 'Organized 5 course documents in Knowledge library', date: '20 Sep 2026', completed: true },
  { title: 'Target: Score >85% in Operating Systems Midterm', date: 'Target: 27 Sep 2026', completed: false },
];

export const BADGES: Badge[] = [
  { name: 'Consistent Focus', icon: 'calendar', color: '#2d5f47', unlocked: true },
  { name: 'Systems Scholar', icon: 'cpu', color: '#315c8b', unlocked: true },
  { name: 'Problem Solver', icon: 'award', color: '#8b5a31', unlocked: true },
  { name: 'Knowledge Curator', icon: 'book-open', color: '#6a4c93', unlocked: true },
  { name: 'Exam Ready', icon: 'shield', color: '#a14b5d', unlocked: false },
];

export const STUDY_GOALS = [
  { id: 'g1', text: 'Revise Operating Systems Unit 3 (Deadlocks & Memory)', completed: true },
  { id: 'g2', text: 'Solve 15 practice questions on TCP three-way handshake', completed: true },
  { id: 'g3', text: 'Master BCNF decomposition without information loss', completed: false },
  { id: 'g4', text: 'Complete mock assessment before Operating Systems exam', completed: false },
];

export const HELP_CATEGORIES: HelpCategory[] = [
  { title: 'Knowledge Base', description: 'Upload notes, organize subject files, and manage your library.', icon: 'book-open', color: '#2d5f47' },
  { title: 'Assessments & Quizzes', description: 'Create adaptive quizzes, diagnostic runs, and track score analytics.', icon: 'file-text', color: '#315c8b' },
  { title: 'Study Planner', description: 'Schedule exam blocks, set focus intervals, and sync project deadlines.', icon: 'calendar', color: '#8b5a31' },
  { title: 'AI Assistant', description: 'Concept clarifications, step-by-step problem breakdown and exam notes.', icon: 'sparkles', color: '#6a4c93' },
  { title: 'Account & Preferences', description: 'Manage appearance themes, notification preferences and profile info.', icon: 'settings', color: '#a14b5d' },
  { title: 'Data & Privacy', description: 'Local storage policies, export local workspace, and future cloud sync.', icon: 'shield', color: '#10b981' },
];

export const SYSTEM_STATUS_ITEMS: SystemStatus[] = [
  { name: 'Document Ingestion Service', status: 'Ready (Local Cache)' },
  { name: 'Deterministic Question Engine', status: 'Operational' },
  { name: 'Local Study Store', status: 'Optimal' },
  { name: 'Azure AI Foundry Boundary', status: 'Integration Ready' },
];

export const CHAT_HISTORY_INITIAL: ChatMessage[] = [
  {
    role: 'user',
    time: '10:14 AM',
    text: 'Can you explain the difference between Deadlock Prevention and Deadlock Avoidance in Operating Systems?',
  },
  {
    role: 'assistant',
    time: '10:15 AM',
    text: `### Deadlock Prevention vs. Deadlock Avoidance

Both techniques aim to prevent deadlocks, but they approach the problem differently:

1. **Deadlock Prevention (Static Approach)**
   - **Mechanism**: Eliminates at least one of the four Coffman conditions (*Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait*) before runtime.
   - **Example**: Impose a strict linear ordering on all resources. If every process must acquire resource $R_i$ before $R_j$ whenever $i < j$, circular wait is mathematically impossible.
   - **Trade-off**: Highly conservative; causes low device utilization and restricts process concurrency.

2. **Deadlock Avoidance (Dynamic Approach)**
   - **Mechanism**: The OS examines resource requests at runtime and only grants a request if the allocation leaves the system in a **Safe State**.
   - **Example**: Dijkstra's **Banker's Algorithm**, which checks if there is at least one sequence of processes that can run to completion with remaining resources.
   - **Trade-off**: Requires processes to declare their maximum resource requirements upfront.

*Exam Tip*: When asked for differences, contrast the **upfront constraints** of prevention against the **runtime evaluation** of avoidance.`,
  },
];

export const WEEKLY_STUDY_HOURS = [
  { day: 'Mon', hours: 3.5 },
  { day: 'Tue', hours: 4.2 },
  { day: 'Wed', hours: 2.8 },
  { day: 'Thu', hours: 5.0 },
  { day: 'Fri', hours: 4.5 },
  { day: 'Sat', hours: 3.0 },
  { day: 'Sun', hours: 3.5 },
];

export const ACTIVITY_DISTRIBUTION = [
  { name: 'Concept Study', value: 40, color: '#315c8b' },
  { name: 'Practice Quizzes', value: 25, color: '#2d5f47' },
  { name: 'Document Review', value: 20, color: '#8b5a31' },
  { name: 'AI Assistance', value: 15, color: '#6a4c93' },
];

export const PROGRESS_OVER_TIME = [
  { date: '25 Aug', progress: 30 },
  { date: '01 Sep', progress: 42 },
  { date: '08 Sep', progress: 54 },
  { date: '15 Sep', progress: 61 },
  { date: '22 Sep', progress: 64 },
];

export const SUBJECT_PROGRESS = [
  { name: 'Operating Systems', progress: 61, icon: 'cpu', color: '#315c8b' },
  { name: 'Data Structures & Algorithms', progress: 52, icon: 'code', color: '#2d5f47' },
  { name: 'Computer Networks', progress: 43, icon: 'share-2', color: '#8b5a31' },
  { name: 'Database Management Systems', progress: 28, icon: 'database', color: '#6a4c93' },
  { name: 'Machine Learning', progress: 18, icon: 'zap', color: '#a14b5d' },
  { name: 'Python Programming', progress: 75, icon: 'terminal', color: '#b17b24' },
];

export const INTERESTS = [
  { name: 'Systems Architecture', icon: 'cpu' },
  { name: 'Distributed Systems', icon: 'globe' },
  { name: 'Database Engines', icon: 'database' },
  { name: 'Algorithm Design', icon: 'code' },
  { name: 'Machine Learning', icon: 'zap' },
];
