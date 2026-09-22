import { createContext, useContext, useCallback, useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  USER_PROFILE, TODAY_STUDY_PLAN, PLANNER_TIMELINE_TASKS, KNOWLEDGE_MATERIALS, STUDY_GOALS,
  CHAT_HISTORY_INITIAL, STATS_SUMMARY, SUBJECTS, UPCOMING_EXAMS, UPCOMING_DEADLINES,
  RECENT_ACTIVITIES, ASSESSMENT_PERFORMANCE, RECENT_ATTEMPTS, POPULAR_PRACTICE_SETS,
  MILESTONES, BADGES, HELP_CATEGORIES, SYSTEM_STATUS_ITEMS, WEEKLY_STUDY_HOURS,
  ACTIVITY_DISTRIBUTION, PROGRESS_OVER_TIME, SUBJECT_PROGRESS, INTERESTS,
  type UserProfile, type StudyPlanItem, type PlannerTask, type KnowledgeMaterial, type ChatMessage,
  type Subject,
} from '../data/mockData';
import {
  fetchWeakTopics, fetchStudyRecommendation, type WeakTopic, type StudyRecommendation,
} from '../services/api';

export interface Course {
  id: string; name: string; code: string; category: string; description: string;
  topics: string[]; progress: number; enrolled: boolean; level: 'Beginner'|'Intermediate'|'Advanced';
  color: string; estimatedHours: number;
}
export interface Note { id: string; title: string; subject: string; source: string; content: string; type: 'AI Notes'|'Summary'|'Exam Notes'|'Easy Explanation'; createdAt: string; }
export interface QuizQuestion { id: string; text: string; options: string[]; answer: number; explanation: string; }
export interface Quiz { id: string; title: string; source: string; subject: string; difficulty: 'Easy'|'Medium'|'Hard'|'Mixed'|'Adaptive'; questions: QuizQuestion[]; score?: number; completedAt?: string; }
export interface CalendarEvent { id: string; date: string; title: string; type: 'Task'|'Exam'|'Class'|'Assignment'|'Study Session'|'Personal Event'; time?: string; subject?: string; completed?: boolean; notes?: string; }
export interface Notification { id: string; title: string; message: string; type: 'success'|'warning'|'info'; read: boolean; createdAt: string; link?: string; }
export interface Toast { id: string; message: string; type: 'success'|'error'|'info'; }

const COURSES: Course[] = [
  {id:'os',name:'Operating Systems',code:'CSE-302',category:'Computer Science',description:'Processes, CPU scheduling, deadlocks, memory management and file systems.',topics:['Processes & Threads','CPU Scheduling','Memory Management','Deadlocks','File Systems','Virtual Memory'],progress:61,enrolled:true,level:'Intermediate',color:'#315c8b',estimatedHours:36},
  {id:'cn',name:'Computer Networks',code:'CSE-304',category:'Computer Science',description:'Networking fundamentals from physical transmission to application protocols.',topics:['Data Link','Network Layer & IP','Transport Layer (TCP/UDP)','Application Layer','Network Security'],progress:43,enrolled:true,level:'Intermediate',color:'#8b5a31',estimatedHours:34},
  {id:'dbms',name:'Database Management Systems',code:'CSE-305',category:'Computer Science',description:'Relational models, SQL, normalization, transactions and B+ tree indexing.',topics:['ER Models','SQL Queries','Normalization (1NF-BCNF)','Transactions & ACID','Indexing & B+ Trees'],progress:28,enrolled:true,level:'Intermediate',color:'#6a4c93',estimatedHours:30},
  {id:'dsa',name:'Data Structures & Algorithms',code:'CSE-201',category:'Computer Science',description:'Core data structures, algorithms, asymptotic complexity and problem solving.',topics:['Arrays & Strings','Linked Lists','Stacks & Queues','Trees & AVL','Graphs (BFS/DFS)','Sorting & Searching'],progress:52,enrolled:true,level:'Intermediate',color:'#2d5f47',estimatedHours:42},
  {id:'ml',name:'Machine Learning',code:'CSE-401',category:'AI & ML',description:'Supervised and unsupervised learning with practical model intuition.',topics:['Linear Regression','Logistic Regression','Decision Trees','SVM','Clustering','Neural Networks'],progress:18,enrolled:false,level:'Advanced',color:'#a14b5d',estimatedHours:48},
  {id:'python',name:'Python Programming',code:'CS-101',category:'Programming',description:'Python fundamentals, data structures, functions, OOP and exception handling.',topics:['Syntax & Types','Functions & Scope','Collections','OOP Principles','File I/O','Modules'],progress:75,enrolled:false,level:'Beginner',color:'#b17b24',estimatedHours:24},
];

const initialNotes: Note[] = [
  {id:'n1',title:'Deadlocks & Coffman Conditions — Exam Notes',subject:'Operating Systems',source:'OS_Unit3_Deadlocks_and_Prevention.pdf',type:'Exam Notes',content:'Deadlock is a state where processes wait indefinitely for resources held by one another. Four necessary Coffman conditions: (1) Mutual exclusion, (2) Hold and wait, (3) No preemption, (4) Circular wait. Breaking any one condition prevents deadlock.',createdAt:'Today'},
  {id:'n2',title:'Transport Layer: TCP vs UDP Quick Summary',subject:'Computer Networks',source:'CN_Transport_Layer_TCP_UDP.docx',type:'Summary',content:'The transport layer provides logical end-to-end communication. TCP is connection-oriented and provides reliable ordered delivery with congestion and flow control. UDP is connectionless, lightweight, and low-latency.',createdAt:'Yesterday'},
  {id:'n3',title:'Relational Normalization & BCNF Guidelines',subject:'Database Management Systems',source:'DBMS_Relational_Algebra_and_SQL.pptx',type:'Exam Notes',content:'Normalization minimizes redundancy and eliminates update anomalies. 1NF: Atomic values. 2NF: No partial dependency on candidate keys. 3NF: No transitive dependency. BCNF: For every functional dependency X -> Y, X must be a super key.',createdAt:'2 days ago'},
];

const initialEvents: CalendarEvent[] = [
  {id:'e1',date:'2026-09-24',title:'Complete OS Deadlock Notes',type:'Task',subject:'Operating Systems',completed:false},
  {id:'e2',date:'2026-09-26',title:'Computer Networks Practice Quiz',type:'Assignment',subject:'Computer Networks',time:'6:00 PM',completed:false},
  {id:'e3',date:'2026-09-27',title:'Operating Systems Midterm Exam',type:'Exam',subject:'Operating Systems',time:'10:00 AM'},
  {id:'e4',date:'2026-10-04',title:'Computer Networks Mid-Term Assessment',type:'Exam',subject:'Computer Networks',time:'02:00 PM'},
  {id:'e5',date:'2026-10-02',title:'DBMS Revision Session (Indexing)',type:'Study Session',subject:'Database Management Systems',time:'5:00 PM'},
];

function readStorage<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return fallback;
    const parsed = JSON.parse(raw);
    // Sanitize any previous session data containing legacy fictional academic items
    if (key === 'acadassist.user' && (parsed?.name === 'Rowan' || parsed?.email?.includes('solaris'))) {
      return fallback;
    }
    if (key === 'acadassist.subjects' && Array.isArray(parsed) && parsed.some((s: { name?: string }) => s?.name?.includes('Quantum'))) {
      return fallback;
    }
    if (key === 'acadassist.materials' && Array.isArray(parsed) && parsed.some((m: { name?: string }) => m?.name?.includes('Quantum_Manifold'))) {
      return fallback;
    }
    return parsed;
  } catch {
    return fallback;
  }
}

function writeStorage(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage is optional */
  }
}

interface AppState {
  user: UserProfile;
  todayPlan: StudyPlanItem[];
  plannerTasks: PlannerTask[];
  knowledgeMaterials: KnowledgeMaterial[];
  chatHistory: ChatMessage[];
  settings: { dailyReminder:boolean; examAlerts:boolean; streakUpdates:boolean; assessmentFeedback:boolean; progressReport:boolean; newFeatures:boolean; theme:'light'|'dark'|'system'; accentColor:string; fontSize:'small'|'medium'|'large'; defaultStudyDuration:number; preferredDifficulty:'Easy'|'Medium'|'Hard'|'Mixed' };
  sidebarOpen:boolean;
  studyGoals: typeof STUDY_GOALS;
  courses:Course[];
  notes:Note[];
  quizzes:Quiz[];
  events:CalendarEvent[];
  notifications:Notification[];
  toasts:Toast[];
  subjects:Subject[];
  weakTopics:WeakTopic[];
  studyRecommendation:StudyRecommendation|null;
}

interface AppContextType extends AppState {
  updateUser:(patch:Partial<UserProfile>)=>void;
  togglePlanItem:(id:string)=>void;
  togglePlannerTask:(id:string)=>void;
  toggleGoal:(id:string)=>void;
  addChatMessage:(role:'user'|'assistant',text:string)=>void;
  clearChatHistory:()=>void;
  addKnowledgeMaterial:(material:KnowledgeMaterial)=>void;
  updateKnowledgeMaterial:(idOrName:string,patch:Partial<KnowledgeMaterial>)=>void;
  deleteKnowledgeMaterial:(idOrName:string)=>void;
  updateSetting:(key:string,value:unknown)=>void;
  setSidebarOpen:(open:boolean)=>void;
  addCourse:(id:string)=>void;
  removeCourse:(id:string)=>void;
  addNote:(note:Note)=>void;
  updateNote:(id:string,patch:Partial<Note>)=>void;
  deleteNote:(id:string)=>void;
  addQuiz:(quiz:Quiz)=>void;
  updateQuiz:(id:string,patch:Partial<Quiz>)=>void;
  addEvent:(event:CalendarEvent)=>void;
  updateEvent:(id:string,patch:Partial<CalendarEvent>)=>void;
  deleteEvent:(id:string)=>void;
  addSubject:(subject:Subject)=>void;
  updateSubject:(id:string,patch:Partial<Subject>)=>void;
  deleteSubject:(id:string)=>void;
  markNotificationsRead:()=>void;
  markNotificationRead:(id:string)=>void;
  pushToast:(message:string,type?:Toast['type'])=>void;
  dismissToast:(id:string)=>void;
  reloadWeakTopics:()=>Promise<void>;
}

const AppContext=createContext<AppContextType|null>(null);

function normalizeMaterials(items: KnowledgeMaterial[]): KnowledgeMaterial[] {
  return items.map((item, index) => ({ ...item, id: (item as KnowledgeMaterial & {id?:string}).id || `${item.name}-${item.addedOn}-${index}` } as KnowledgeMaterial));
}

const defaultSettings: AppState['settings'] = {
  dailyReminder:true, examAlerts:true, streakUpdates:true, assessmentFeedback:true,
  progressReport:true, newFeatures:false, theme:'light', accentColor:'#2d5f47', fontSize:'medium',
  defaultStudyDuration:50, preferredDifficulty:'Mixed'
};

export function AppProvider({children}:{children:ReactNode}) {
  const [user,setUser]=useState<UserProfile>(()=>readStorage('acadassist.user',structuredClone(USER_PROFILE)));
  const [todayPlan,setTodayPlan]=useState<StudyPlanItem[]>(()=>readStorage('acadassist.todayPlan',structuredClone(TODAY_STUDY_PLAN)));
  const [plannerTasks,setPlannerTasks]=useState<PlannerTask[]>(()=>readStorage('acadassist.plannerTasks',structuredClone(PLANNER_TIMELINE_TASKS)));
  const [knowledgeMaterials,setKnowledgeMaterials]=useState<KnowledgeMaterial[]>(()=>normalizeMaterials(readStorage('acadassist.materials',structuredClone(KNOWLEDGE_MATERIALS))));
  const [chatHistory,setChatHistory]=useState<ChatMessage[]>(()=>readStorage('acadassist.chat',structuredClone(CHAT_HISTORY_INITIAL)));
  const [studyGoals,setStudyGoals]=useState(()=>readStorage('acadassist.goals',structuredClone(STUDY_GOALS)));
  const [courses,setCourses]=useState<Course[]>(()=>readStorage('acadassist.courses',COURSES));
  const [notes,setNotes]=useState<Note[]>(()=>readStorage('acadassist.notes',initialNotes));
  const [quizzes,setQuizzes]=useState<Quiz[]>(()=>readStorage('acadassist.quizzes',[]));
  const [events,setEvents]=useState<CalendarEvent[]>(()=>readStorage('acadassist.events',initialEvents));
  const [notifications,setNotifications]=useState<Notification[]>(()=>readStorage('acadassist.notifications',[
    {id:'nt1',title:'AI notes ready',message:'Operating Systems Deadlocks notes available in Knowledge.',type:'success',read:false,createdAt:'Today',link:'/knowledge'},
    {id:'nt2',title:'Upcoming Exam: OS Midterm',message:'Operating Systems Midterm is in 5 days. Practice your weak topic: Deadlocks.',type:'warning',read:false,createdAt:'Today',link:'/planner'},
    {id:'nt3',title:'Diagnostic suggestion',message:'Computer Networks Transport Layer quiz recommended based on recent score (50%).',type:'info',read:false,createdAt:'Yesterday',link:'/assessment'},
  ]));
  const [toasts,setToasts]=useState<Toast[]>([]);
  const [subjects,setSubjects]=useState<Subject[]>(()=>readStorage('acadassist.subjects',structuredClone(SUBJECTS)));
  const [sidebarOpen,setSidebarOpen]=useState(false);
  const [settings,setSettings]=useState<AppState['settings']>(()=>({...defaultSettings,...readStorage('acadassist.settings',defaultSettings)}));
  
  // Weak topics and study recommendations behind service layer interface
  const [weakTopics,setWeakTopics]=useState<WeakTopic[]>([]);
  const [studyRecommendation,setStudyRecommendation]=useState<StudyRecommendation|null>(null);

  const reloadWeakTopics=useCallback(async()=>{
    try {
      const [topics, rec] = await Promise.all([fetchWeakTopics(), fetchStudyRecommendation()]);
      setWeakTopics(topics);
      setStudyRecommendation(rec);
    } catch {
      // Fallback kept safe and clean
    }
  },[]);

  useEffect(()=>{
    reloadWeakTopics();
  },[reloadWeakTopics]);

  useEffect(()=>{ writeStorage('acadassist.user',user); },[user]);
  useEffect(()=>{ writeStorage('acadassist.todayPlan',todayPlan); },[todayPlan]);
  useEffect(()=>{ writeStorage('acadassist.plannerTasks',plannerTasks); },[plannerTasks]);
  useEffect(()=>{ writeStorage('acadassist.materials',knowledgeMaterials); },[knowledgeMaterials]);
  useEffect(()=>{ writeStorage('acadassist.chat',chatHistory); },[chatHistory]);
  useEffect(()=>{ writeStorage('acadassist.goals',studyGoals); },[studyGoals]);
  useEffect(()=>{ writeStorage('acadassist.courses',courses); },[courses]);
  useEffect(()=>{ writeStorage('acadassist.notes',notes); },[notes]);
  useEffect(()=>{ writeStorage('acadassist.quizzes',quizzes); },[quizzes]);
  useEffect(()=>{ writeStorage('acadassist.events',events); },[events]);
  useEffect(()=>{ writeStorage('acadassist.notifications',notifications); },[notifications]);
  useEffect(()=>{ writeStorage('acadassist.subjects',subjects); },[subjects]);
  useEffect(()=>{ writeStorage('acadassist.settings',settings); },[settings]);

  useEffect(()=>{
    const root=document.documentElement;
    const applyTheme=(dark:boolean)=>{
      const t = dark ? 'dark' : 'light';
      document.body.dataset.theme=t;
      root.dataset.theme=t;
    };

    if(settings.theme==='system'){
      const media=typeof window!=='undefined'&&window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
      applyTheme(media ? media.matches : false);
      const listener=(e:MediaQueryListEvent)=>applyTheme(e.matches);
      media?.addEventListener?.('change',listener);
      return ()=>{
        media?.removeEventListener?.('change',listener);
      };
    } else {
      applyTheme(settings.theme==='dark');
    }
  },[settings.theme]);

  useEffect(()=>{
    const root=document.documentElement;
    root.style.setProperty('--color-green-accent',settings.accentColor);
    root.style.setProperty('--color-accent',settings.accentColor);
    root.style.setProperty('--app-font-size',settings.fontSize==='small'?'14px':settings.fontSize==='large'?'17px':'15px');
  },[settings.accentColor,settings.fontSize]);

  const updateUser=useCallback((patch:Partial<UserProfile>)=>setUser(p=>({...p,...patch})),[]);
  const togglePlanItem=useCallback((id:string)=>setTodayPlan(p=>p.map(x=>x.id===id?{...x,status:x.status==='completed'?'pending':'completed'}:x)),[]);
  const togglePlannerTask=useCallback((id:string)=>setPlannerTasks(p=>p.map(x=>x.id===id?{...x,completed:!x.completed}:x)),[]);
  const toggleGoal=useCallback((id:string)=>setStudyGoals(p=>p.map(x=>x.id===id?{...x,completed:!x.completed}:x)),[]);
  const addChatMessage=useCallback((role:'user'|'assistant',text:string)=>setChatHistory(p=>[...p,{role,text,time:new Date().toLocaleTimeString([], {hour:'numeric',minute:'2-digit'})}]),[]);
  const clearChatHistory=useCallback(()=>setChatHistory([]),[]);
  const addKnowledgeMaterial=useCallback((m:KnowledgeMaterial)=>setKnowledgeMaterials(p=>[m,...p]),[]);
  const updateKnowledgeMaterial=useCallback((key:string,patch:Partial<KnowledgeMaterial>)=>setKnowledgeMaterials(p=>p.map(m=>((m as KnowledgeMaterial & {id?:string}).id===key||m.name===key)?{...m,...patch}:m)),[]);
  const deleteKnowledgeMaterial=useCallback((key:string)=>setKnowledgeMaterials(p=>p.filter(m=>!((m as KnowledgeMaterial & {id?:string}).id===key||m.name===key))),[]);
  const updateSetting=useCallback((key:string,value:unknown)=>setSettings(p=>({...p,[key]:value})),[]);
  const addCourse=useCallback((id:string)=>setCourses(p=>p.map(c=>c.id===id?{...c,enrolled:true}:c)),[]);
  const removeCourse=useCallback((id:string)=>setCourses(p=>p.map(c=>c.id===id?{...c,enrolled:false}:c)),[]);
  const addNote=useCallback((n:Note)=>setNotes(p=>[n,...p]),[]);
  const updateNote=useCallback((id:string,patch:Partial<Note>)=>setNotes(p=>p.map(n=>n.id===id?{...n,...patch}:n)),[]);
  const deleteNote=useCallback((id:string)=>setNotes(p=>p.filter(n=>n.id!==id)),[]);
  const addQuiz=useCallback((q:Quiz)=>setQuizzes(p=>[q,...p]),[]);
  const updateQuiz=useCallback((id:string,patch:Partial<Quiz>)=>setQuizzes(p=>p.map(q=>q.id===id?{...q,...patch}:q)),[]);
  const addEvent=useCallback((e:CalendarEvent)=>setEvents(p=>[...p,e]),[]);
  const updateEvent=useCallback((id:string,patch:Partial<CalendarEvent>)=>setEvents(p=>p.map(e=>e.id===id?{...e,...patch}:e)),[]);
  const deleteEvent=useCallback((id:string)=>setEvents(p=>p.filter(e=>e.id!==id)),[]);
  const addSubject=useCallback((s:Subject)=>setSubjects(p=>[...p,s]),[]);
  const updateSubject=useCallback((id:string,patch:Partial<Subject>)=>setSubjects(p=>p.map(s=>s.id===id?{...s,...patch}:s)),[]);
  const deleteSubject=useCallback((id:string)=>setSubjects(p=>p.filter(s=>s.id!==id)),[]);
  const markNotificationsRead=useCallback(()=>setNotifications(p=>p.map(n=>({...n,read:true}))),[]);
  const markNotificationRead=useCallback((id:string)=>setNotifications(p=>p.map(n=>n.id===id?{...n,read:true}:n)),[]);
  const dismissToast=useCallback((id:string)=>setToasts(p=>p.filter(t=>t.id!==id)),[]);
  const pushToast=useCallback((message:string,type:Toast['type']='success')=>{
    const id=crypto.randomUUID();
    setToasts(p=>[...p,{id,message,type}]);
    window.setTimeout(()=>setToasts(p=>p.filter(t=>t.id!==id)),3500);
  },[]);

  const value=useMemo(()=>({
    user,todayPlan,plannerTasks,knowledgeMaterials,chatHistory,settings,sidebarOpen,studyGoals,
    courses,notes,quizzes,events,notifications,toasts,subjects,weakTopics,studyRecommendation,
    updateUser,togglePlanItem,togglePlannerTask,toggleGoal,addChatMessage,clearChatHistory,
    addKnowledgeMaterial,updateKnowledgeMaterial,deleteKnowledgeMaterial,updateSetting,setSidebarOpen,
    addCourse,removeCourse,addNote,updateNote,deleteNote,addQuiz,updateQuiz,addEvent,updateEvent,
    deleteEvent,addSubject,updateSubject,deleteSubject,markNotificationsRead,markNotificationRead,
    pushToast,dismissToast,reloadWeakTopics
  }),[
    user,todayPlan,plannerTasks,knowledgeMaterials,chatHistory,settings,sidebarOpen,studyGoals,
    courses,notes,quizzes,events,notifications,toasts,subjects,weakTopics,studyRecommendation,
    updateUser,togglePlanItem,togglePlannerTask,toggleGoal,addChatMessage,clearChatHistory,
    addKnowledgeMaterial,updateKnowledgeMaterial,deleteKnowledgeMaterial,updateSetting,addCourse,
    removeCourse,addNote,updateNote,deleteNote,addQuiz,updateQuiz,addEvent,updateEvent,deleteEvent,
    addSubject,updateSubject,deleteSubject,markNotificationsRead,markNotificationRead,pushToast,
    dismissToast,reloadWeakTopics
  ]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp(){const ctx=useContext(AppContext); if(!ctx) throw new Error('useApp must be used within AppProvider'); return ctx;}
export { STATS_SUMMARY,SUBJECTS,UPCOMING_EXAMS,UPCOMING_DEADLINES,RECENT_ACTIVITIES,ASSESSMENT_PERFORMANCE,RECENT_ATTEMPTS,POPULAR_PRACTICE_SETS,MILESTONES,BADGES,HELP_CATEGORIES,SYSTEM_STATUS_ITEMS,WEEKLY_STUDY_HOURS,ACTIVITY_DISTRIBUTION,PROGRESS_OVER_TIME,SUBJECT_PROGRESS,INTERESTS };
export { COURSES };