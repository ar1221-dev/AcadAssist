import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import {
  USER_PROFILE, TODAY_STUDY_PLAN, PLANNER_TIMELINE_TASKS,
  KNOWLEDGE_MATERIALS, STUDY_GOALS, CHAT_HISTORY_INITIAL,
  type UserProfile, type StudyPlanItem, type PlannerTask, type KnowledgeMaterial, type ChatMessage,
} from '../data/mockData';

interface AppState {
  user: UserProfile;
  todayPlan: StudyPlanItem[];
  plannerTasks: PlannerTask[];
  knowledgeMaterials: KnowledgeMaterial[];
  chatHistory: ChatMessage[];
  settings: {
    dailyReminder: boolean;
    examAlerts: boolean;
    streakUpdates: boolean;
    assessmentFeedback: boolean;
    progressReport: boolean;
    newFeatures: boolean;
    theme: 'light' | 'dark' | 'system';
    accentColor: string;
    fontSize: 'small' | 'medium' | 'large';
  };
  sidebarOpen: boolean;
  studyGoals: typeof STUDY_GOALS;
}

interface AppContextType extends AppState {
  togglePlanItem: (id: string) => void;
  togglePlannerTask: (id: string) => void;
  toggleGoal: (id: string) => void;
  addChatMessage: (role: 'user' | 'assistant', text: string) => void;
  addKnowledgeMaterial: (material: KnowledgeMaterial) => void;
  updateSetting: (key: string, value: unknown) => void;
  setSidebarOpen: (open: boolean) => void;
}

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [todayPlan, setTodayPlan] = useState(structuredClone(TODAY_STUDY_PLAN));
  const [plannerTasks, setPlannerTasks] = useState(structuredClone(PLANNER_TIMELINE_TASKS));
  const [knowledgeMaterials, setKnowledgeMaterials] = useState(structuredClone(KNOWLEDGE_MATERIALS));
  const [chatHistory, setChatHistory] = useState(structuredClone(CHAT_HISTORY_INITIAL));
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [studyGoals, setStudyGoals] = useState(structuredClone(STUDY_GOALS));
  const [settings, setSettings] = useState<AppState['settings']>({
    dailyReminder: true,
    examAlerts: true,
    streakUpdates: true,
    assessmentFeedback: true,
    progressReport: true,
    newFeatures: false,
    theme: 'light',
    accentColor: '#2d5f47',
    fontSize: 'medium',
  });

  const togglePlanItem = useCallback((id: string) => {
    setTodayPlan(prev => prev.map(item =>
      item.id === id ? { ...item, status: item.status === 'completed' ? 'pending' as const : 'completed' as const } : item
    ));
  }, []);

  const togglePlannerTask = useCallback((id: string) => {
    setPlannerTasks(prev => prev.map(t =>
      t.id === id ? { ...t, completed: !t.completed } : t
    ));
  }, []);

  const toggleGoal = useCallback((id: string) => {
    setStudyGoals(prev => prev.map(g =>
      g.id === id ? { ...g, completed: !g.completed } : g
    ));
  }, []);

  const addChatMessage = useCallback((role: 'user' | 'assistant', text: string) => {
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
    setChatHistory(prev => [...prev, { role, text, time }]);
  }, []);

  const addKnowledgeMaterial = useCallback((material: KnowledgeMaterial) => {
    setKnowledgeMaterials(prev => [material, ...prev]);
  }, []);

  const updateSetting = useCallback((key: string, value: unknown) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  }, []);

  return (
    <AppContext.Provider value={{
      user: USER_PROFILE,
      todayPlan,
      plannerTasks,
      knowledgeMaterials,
      chatHistory,
      settings,
      sidebarOpen,
      studyGoals,
      togglePlanItem,
      togglePlannerTask,
      toggleGoal,
      addChatMessage,
      addKnowledgeMaterial,
      updateSetting,
      setSidebarOpen,
    }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}

// Re-export static data for pages that need it
export {
  STATS_SUMMARY, SUBJECTS, UPCOMING_EXAMS, UPCOMING_DEADLINES, RECENT_ACTIVITIES,
  ASSESSMENT_PERFORMANCE, RECENT_ATTEMPTS, POPULAR_PRACTICE_SETS, MILESTONES, BADGES,
  HELP_CATEGORIES, SYSTEM_STATUS_ITEMS, WEEKLY_STUDY_HOURS, ACTIVITY_DISTRIBUTION,
  PROGRESS_OVER_TIME, SUBJECT_PROGRESS, INTERESTS,
} from '../data/mockData';
