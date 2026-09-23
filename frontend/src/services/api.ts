// Azure-ready API boundary. The UI never talks to Azure directly.
const API_BASE = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || '';

export interface WeakTopic {
  id: string;
  topic: string;
  subject: string;
  accuracyScore: number;
  recommendedAction: string;
  examUrgency?: 'urgent' | 'high' | 'medium' | 'normal';
  examName?: string;
  daysToExam?: number;
  isDemo?: boolean;
}

export interface StudyRecommendation {
  subjectName: string;
  topicName: string;
  reason: string;
  suggestedDuration: string;
  actionType: 'quiz' | 'study' | 'notes';
  isDemo?: boolean;
}

function getAuthHeader(): Record<string, string> {
  try {
    const token = localStorage.getItem('acadassist.auth.token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  } catch {
    return {};
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = API_BASE ? `${API_BASE}${path}` : path;
  const response = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
      ...(init?.headers || {}),
    },
  });
  if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function sendChatMessage(message: string, materialId?: string): Promise<{ text: string }> {
  void materialId;
  const res = await request<{ message: string; sources?: any[]; actions?: any[]; execution_mode?: string }>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
  return { text: res.message };
}

// Person 2: Document Management Endpoints (/api/documents)
export interface DocumentUploadResponse {
  id: string;
  name: string;
  size: number;
  type: string;
  url?: string;
  uploadedAt: string;
  isDemo?: boolean;
}

export async function fetchDocuments(): Promise<DocumentUploadResponse[] | null> {
  try {
    const res = await request<{
      documents: Array<{
        document_id: string;
        filename: string;
        title: string;
        file_type: string;
        status: string;
        size_bytes?: number;
        uploaded_at: string;
      }>;
      total: number;
    }>('/api/documents');
    return res.documents.map(d => ({
      id: d.document_id,
      name: d.filename || d.title,
      size: d.size_bytes || 0,
      type: d.file_type || 'application/pdf',
      uploadedAt: d.uploaded_at,
      isDemo: false,
    }));
  } catch {
    return null;
  }
}

export async function uploadDocument(
  file: File | { name: string; size: number; type: string }
): Promise<DocumentUploadResponse> {
  if (!(file instanceof File)) {
    throw new Error('A real File object is required for document upload.');
  }

  const formData = new FormData();
  formData.append('file', file);
  formData.append('title', file.name);
  formData.append('visibility', 'private');

  const url = API_BASE ? `${API_BASE}/api/documents` : '/api/documents';
  const token = localStorage.getItem('acadassist.auth.token');
  const response = await fetch(url, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  });

  if (!response.ok) {
    throw new Error((await response.text()) || `Document upload failed (${response.status})`);
  }

  const data = await response.json();
  if (!data.document_id) {
    throw new Error('Document upload succeeded without a document ID.');
  }

  return {
    id: data.document_id,
    name: data.filename || file.name,
    size: file.size,
    type: file.type || 'application/pdf',
    uploadedAt: data.created_at || new Date().toISOString(),
    isDemo: false,
  };
}

export async function downloadDocument(documentId: string, filename: string): Promise<void> {
  const url = API_BASE ? `${API_BASE}/api/documents/${encodeURIComponent(documentId)}/download` : `/api/documents/${encodeURIComponent(documentId)}/download`;
  const token = localStorage.getItem('acadassist.auth.token');
  const res = await fetch(url, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`Download failed with status ${res.status}`);
  const blob = await res.blob();
  const blobUrl = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = blobUrl;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
}

// Person 3 / Person 4: Weak Topics (/api/performance/weak-topics)
export async function fetchWeakTopics(): Promise<WeakTopic[]> {
  try {
    const res = await request<{
      topics?: Array<{
        topic_id: string;
        topic?: string;
        topic_name?: string;
        mastery?: number;
        accuracy_rate?: number;
        recommended_action?: string;
        recommended_difficulty?: string;
      }>;
    }>('/api/performance/weak-topics');
    if (res?.topics && res.topics.length > 0) {
      return res.topics.map(t => {
        const accuracy = t.mastery !== undefined ? t.mastery : (t.accuracy_rate !== undefined ? t.accuracy_rate : 0.5);
        const name = t.topic || t.topic_name || t.topic_id;
        return {
          id: t.topic_id,
          topic: name,
          subject: 'Academic Curriculum',
          accuracyScore: Math.round(accuracy * 100),
          recommendedAction: t.recommended_action || `Review ${name} core principles and solve practice problems.`,
          examUrgency: accuracy < 0.6 ? 'urgent' : 'high',
          isDemo: false,
        };
      });
    }
  } catch {
    // empty state
  }
  return [];
}

export async function fetchStudyRecommendation(): Promise<StudyRecommendation | null> {
  const recs = await fetchStudyRecommendations();
  return recs.length > 0 ? recs[0] : null;
}

export async function fetchStudyRecommendations(): Promise<StudyRecommendation[]> {
  try {
    const res = await request<{ recommendations?: Array<{ topic_name: string; reason: string; action: string; urgency: string }> }>(
      '/api/progress/recommendations'
    );
    if (res?.recommendations && res.recommendations.length > 0) {
      return res.recommendations.map(r => ({
        subjectName: 'Computer Science',
        topicName: r.topic_name,
        reason: r.reason,
        suggestedDuration: '45 min',
        actionType: (r.action?.toLowerCase().includes('quiz') ? 'quiz' : 'study') as 'quiz' | 'study',
        isDemo: false,
      }));
    }
  } catch {
    // empty state
  }
  return [];
}

export interface PerformanceMetrics {
  userId: string;
  overallAccuracy: number;
  recentAccuracy: number;
  attemptCount: number;
  totalQuestionsAttempted: number;
  totalCorrect: number;
  totalIncorrect: number;
  topicMastery: Record<string, number>;
  weakTopics: Array<{ topicId: string; topic: string; mastery: number }>;
  strongTopics: Array<{ topicId: string; topic: string; mastery: number }>;
}

export async function fetchPerformanceMetrics(): Promise<PerformanceMetrics | null> {
  try {
    const res = await request<{
      user_id: string;
      overall_accuracy: number;
      recent_accuracy: number;
      attempt_count: number;
      total_questions_attempted: number;
      total_correct: number;
      total_incorrect: number;
      topic_mastery: Record<string, number>;
      weak_topics: Array<{ topic_id: string; topic: string; mastery: number }>;
      strong_topics: Array<{ topic_id: string; topic: string; mastery: number }>;
    }>('/api/performance');
    if (res) {
      return {
        userId: res.user_id,
        overallAccuracy: res.overall_accuracy,
        recentAccuracy: res.recent_accuracy,
        attemptCount: res.attempt_count,
        totalQuestionsAttempted: res.total_questions_attempted,
        totalCorrect: res.total_correct,
        totalIncorrect: res.total_incorrect,
        topicMastery: res.topic_mastery || {},
        weakTopics: (res.weak_topics || []).map(w => ({ topicId: w.topic_id, topic: w.topic, mastery: w.mastery })),
        strongTopics: (res.strong_topics || []).map(s => ({ topicId: s.topic_id, topic: s.topic, mastery: s.mastery })),
      };
    }
  } catch {
    // empty state
  }
  return null;
}

export interface BackendUpcomingExam {
  examId: string;
  userId: string;
  subjectId: string;
  title: string;
  examDate: string;
  daysUntilExam?: number;
  assessmentFocus?: string;
}

export async function fetchUpcomingExams(): Promise<BackendUpcomingExam[]> {
  try {
    const res = await request<Array<{
      exam_id: string;
      user_id: string;
      subject_id: string;
      title: string;
      exam_date: string;
      days_until_exam?: number;
      assessment_focus?: string;
    }>>('/api/exams/upcoming');
    if (Array.isArray(res)) {
      return res.map(e => ({
        examId: e.exam_id,
        userId: e.user_id,
        subjectId: e.subject_id,
        title: e.title,
        examDate: e.exam_date,
        daysUntilExam: e.days_until_exam,
        assessmentFocus: e.assessment_focus,
      }));
    }
  } catch {
    // empty state
  }
  return [];
}

export interface QuizAttemptRecord {
  attemptId: string;
  quizId: string;
  title: string;
  subject: string;
  score: number;
  total: number;
  percentage: number;
  completedAt: string | null;
}

export async function fetchQuizAttempts(): Promise<QuizAttemptRecord[]> {
  try {
    const res = await request<Array<{
      attempt_id: string;
      quiz_id: string;
      title: string;
      subject: string;
      score: number;
      total: number;
      percentage: number;
      completed_at: string | null;
    }>>('/api/quizzes/attempts');
    if (Array.isArray(res)) {
      return res.map(r => ({
        attemptId: r.attempt_id,
        quizId: r.quiz_id,
        title: r.title,
        subject: r.subject,
        score: r.score,
        total: r.total,
        percentage: r.percentage,
        completedAt: r.completed_at,
      }));
    }
  } catch {
    // empty state
  }
  return [];
}

export interface QuizGenerationRequest {
  topic: string;
  subject?: string;
  isExam?: boolean;
  questionCount?: number;
  sourceType?: 'Topic' | 'Subject' | 'Knowledge' | 'Notes' | 'Weak Topics';
}

export interface GeneratedQuestion {
  id: string;
  text: string;
  options: string[];
  answer: number;
  explanation: string;
}

export interface GeneratedQuizResponse {
  id: string;
  title: string;
  source: string;
  subject: string;
  questions: GeneratedQuestion[];
  isDemo?: boolean;
}

export async function generateQuiz(req: QuizGenerationRequest): Promise<GeneratedQuizResponse> {
  const subjectId = req.subject?.toLowerCase().replace(/\s+/g, '_') || 'operating_systems';
  const topicId = req.topic || 'General';
  const res = await request<{
    quiz_id?: string;
    title?: string;
    questions?: Array<{
      question_id: string;
      question_text: string;
      options: string[];
      explanation?: string;
    }>;
  }>('/api/quizzes', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: subjectId,
      topic_ids: [topicId],
      count: req.questionCount || 5,
      title: `${req.topic} — ${req.isExam ? 'Timed Assessment' : 'Practice Quiz'}`,
    }),
  });

  if (!res?.quiz_id || !res.questions || res.questions.length === 0) {
    throw new Error('Quiz generation returned no questions. Please try again.');
  }

  return {
    id: res.quiz_id,
    title: res.title || `${req.topic} — Practice Quiz`,
    source: req.topic,
    subject: req.subject || 'Computer Science',
    questions: res.questions.map(q => ({
      id: q.question_id,
      text: q.question_text,
      options: q.options || [],
      answer: 0,
      explanation: q.explanation || '',
    })),
    isDemo: false,
  };
}

export interface QuizSubmissionResult {
  attemptId: string;
  quizId: string;
  score: number;
  total: number;
  percentage: number;
  weakTopics: Array<{ topicId: string; topic: string; mastery: number }>;
  isDemo?: boolean;
}

export async function submitQuiz(
  quizId: string,
  answers: Array<{ questionId: string; selectedAnswer: string; timeTaken?: number }>
): Promise<QuizSubmissionResult> {
  const res = await request<{
    attempt_id: string;
    quiz_id: string;
    score: number;
    total: number;
    percentage: number;
    weak_topics: Array<{ topic_id: string; topic: string; mastery: number }>;
  }>(`/api/quizzes/${encodeURIComponent(quizId)}/submit`, {
    method: 'POST',
    body: JSON.stringify({
      answers: answers.map(a => ({
        question_id: a.questionId,
        selected_answer: a.selectedAnswer,
        time_taken: a.timeTaken || 0.0,
      })),
    }),
  });

  return {
    attemptId: res.attempt_id,
    quizId: res.quiz_id,
    score: res.score,
    total: res.total,
    percentage: res.percentage,
    weakTopics: (res.weak_topics || []).map(w => ({
      topicId: w.topic_id,
      topic: w.topic,
      mastery: w.mastery,
    })),
    isDemo: false,
  };
}

// Person 4: Study Planner and Tasks Endpoints (/api/plans, /api/plans/today, /api/tasks/{task_id})
export interface BackendStudyTask {
  task_id: string;
  study_plan_id?: string;
  user_id: string;
  course_id?: string;
  subject_id?: string;
  topic_id?: string;
  title: string;
  description?: string;
  scheduled_date: string;
  start_time?: string;
  duration_minutes: number;
  priority: string;
  status: string;
}

export interface BackendTodayPlan {
  date: string;
  user_id: string;
  total_tasks: number;
  total_scheduled_minutes: number;
  completed_minutes: number;
  tasks: BackendStudyTask[];
  isDemo?: boolean;
}

export async function fetchTodayPlan(): Promise<BackendTodayPlan | null> {
  try {
    const res = await request<BackendTodayPlan>('/api/plans/today');
    return { ...res, isDemo: false };
  } catch {
    return null;
  }
}

export async function fetchStudyPlans(): Promise<any[] | null> {
  try {
    return await request<any[]>('/api/plans');
  } catch {
    return null;
  }
}

export async function createStudyPlan(payload: {
  startDate: string;
  endDate: string;
  availableMinutesPerDay?: number;
}): Promise<any | null> {
  try {
    return await request('/api/plans', {
      method: 'POST',
      body: JSON.stringify({
        start_date: payload.startDate,
        end_date: payload.endDate,
        available_minutes_per_day: payload.availableMinutesPerDay || 120,
      }),
    });
  } catch {
    return null;
  }
}

export async function updateTaskStatus(
  taskId: string,
  status: 'pending' | 'in_progress' | 'completed' | 'skipped'
): Promise<BackendStudyTask | null> {
  try {
    return await request<BackendStudyTask>(
      `/api/tasks/${encodeURIComponent(taskId)}`,
      {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      }
    );
  } catch {
    return null;
  }
}

// Notes API (/api/notes)
export interface BackendNote {
  id: string;
  user_id: string;
  document_id?: string;
  title: string;
  content: string;
  subject?: string;
  note_type: string;
  created_at: string;
  updated_at: string;
}

export async function fetchNotes(): Promise<BackendNote[]> {
  try {
    return await request<BackendNote[]>('/api/notes');
  } catch {
    return [];
  }
}

export async function createNote(payload: {
  title: string;
  content: string;
  subject?: string;
  note_type?: string;
  document_id?: string;
}): Promise<BackendNote | null> {
  try {
    return await request<BackendNote>('/api/notes', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  } catch {
    return null;
  }
}

export async function updateNote(
  noteId: string,
  payload: { title?: string; content?: string; subject?: string; note_type?: string }
): Promise<BackendNote | null> {
  try {
    return await request<BackendNote>(`/api/notes/${encodeURIComponent(noteId)}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
  } catch {
    return null;
  }
}

export async function deleteNote(noteId: string): Promise<boolean> {
  try {
    await request(`/api/notes/${encodeURIComponent(noteId)}`, { method: 'DELETE' });
    return true;
  } catch {
    return false;
  }
}

// Chat API (/api/chat)
export interface BackendChatMessage {
  id: string;
  role: string;
  text: string;
  time: string;
}

export async function fetchChatHistory(): Promise<BackendChatMessage[]> {
  try {
    return await request<BackendChatMessage[]>('/api/chat/history');
  } catch {
    return [];
  }
}

export async function appendChatMessage(role: string, text: string): Promise<BackendChatMessage | null> {
  try {
    return await request<BackendChatMessage>('/api/chat/message', {
      method: 'POST',
      body: JSON.stringify({ role, text }),
    });
  } catch {
    return null;
  }
}

export async function clearBackendChatHistory(): Promise<void> {
  try {
    await request('/api/chat/history', { method: 'DELETE' });
  } catch {
    /* ignore */
  }
}

export async function chatWithAssistant(
  message: string,
  context?: { materialId?: string; subject?: string }
): Promise<{ text: string }> {
  return sendChatMessage(message, context?.materialId);
}

export { API_BASE };
