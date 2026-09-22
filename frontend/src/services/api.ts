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

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = API_BASE ? `${API_BASE}${path}` : path;
  const response = await fetch(url, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
  });
  if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function sendChatMessage(message: string, materialId?: string): Promise<{ text: string }> {
  return { text: localAssistantResponse(message, materialId) };
}

// Person 2: Document Management Endpoints (/api/documents)
export async function fetchDocuments(userId = 'default_student_user'): Promise<DocumentUploadResponse[] | null> {
  try {
    const res = await request<{
      documents: Array<{
        document_id: string;
        filename: string;
        title: string;
        file_type: string;
        status: string;
        uploaded_at: string;
      }>;
      total: number;
    }>(`/api/documents?user_id=${encodeURIComponent(userId)}`);
    return res.documents.map(d => ({
      id: d.document_id,
      name: d.filename || d.title,
      size: 0,
      type: d.file_type || 'application/pdf',
      uploadedAt: d.uploaded_at,
      isDemo: false,
    }));
  } catch {
    return null;
  }
}

// Person 3 / Person 4: Weak Topics (/api/performance/weak-topics or fallback)
export async function fetchWeakTopics(userId = 'default_student_user'): Promise<WeakTopic[]> {
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
    }>(
      '/api/performance/weak-topics',
      { headers: { 'X-User-ID': userId } }
    );
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
    // Graceful fallback to local demo data
  }
  // Local deterministic fallback (Sample / Demo Data)
  return [
    {
      id: 'wt-1',
      topic: 'Deadlocks & Coffman Conditions',
      subject: 'Operating Systems',
      accuracyScore: 58,
      recommendedAction: 'Review circular wait prevention and solve 5 deadlock practice problems.',
      examUrgency: 'urgent',
      examName: 'Operating Systems Midterm',
      daysToExam: 5,
      isDemo: true,
    },
    {
      id: 'wt-2',
      topic: 'Transport Layer & Flow Control',
      subject: 'Computer Networks',
      accuracyScore: 50,
      recommendedAction: 'Review TCP sliding window mechanics and take a 10-question practice quiz.',
      examUrgency: 'high',
      examName: 'Computer Networks Exam',
      daysToExam: 12,
      isDemo: true,
    },
    {
      id: 'wt-3',
      topic: 'B+ Tree Indexing & Hash Indices',
      subject: 'Database Management Systems',
      accuracyScore: 65,
      recommendedAction: 'Study multi-level indexing node splits and query retrieval bounds.',
      examUrgency: 'medium',
      examName: 'Database Systems Comprehensive',
      daysToExam: 19,
      isDemo: true,
    },
  ];
}

export async function fetchStudyRecommendation(): Promise<StudyRecommendation> {
  const recs = await fetchStudyRecommendations();
  return recs[0];
}

export async function fetchStudyRecommendations(userId = 'default_student_user'): Promise<StudyRecommendation[]> {
  try {
    const res = await request<{ recommendations?: Array<{ topic_name: string; reason: string; action: string; urgency: string }> }>(
      `/api/progress/recommendations?user_id=${encodeURIComponent(userId)}`
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
    // Graceful fallback to local demo data
  }
  return [
    {
      subjectName: 'Operating Systems',
      topicName: 'Deadlocks & Coffman Conditions',
      reason: 'Exam in 5 days with current diagnostic score of 58%.',
      suggestedDuration: '45 min',
      actionType: 'study',
      isDemo: true,
    },
    {
      subjectName: 'Computer Networks',
      topicName: 'Transport Layer & Flow Control',
      reason: 'Accuracy score at 50% across recent practice tests.',
      suggestedDuration: '30 min',
      actionType: 'quiz',
      isDemo: true,
    },
  ];
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
  try {
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
      headers: { 'X-User-ID': 'default_student_user' },
      body: JSON.stringify({
        subject_id: subjectId,
        topic_ids: [topicId],
        count: req.questionCount || 5,
        title: `${req.topic} — ${req.isExam ? 'Timed Assessment' : 'Practice Quiz'}`,
      }),
    });
    if (res?.quiz_id && res.questions && res.questions.length > 0) {
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
  } catch {
    // Fall back to deterministic local questions
  }
  return {
    id: crypto.randomUUID(),
    title: `${req.topic} — ${req.isExam ? 'Timed Assessment' : 'Practice Quiz'}`,
    source: req.topic,
    subject: req.subject || 'Computer Science',
    questions: [],
    isDemo: true,
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
  answers: Array<{ questionId: string; selectedAnswer: string; timeTaken?: number }>,
  userId = 'default_student_user'
): Promise<QuizSubmissionResult> {
  try {
    const res = await request<{
      attempt_id: string;
      quiz_id: string;
      score: number;
      total: number;
      percentage: number;
      weak_topics: Array<{ topic_id: string; topic: string; mastery: number }>;
    }>(`/api/quizzes/${encodeURIComponent(quizId)}/submit`, {
      method: 'POST',
      headers: { 'X-User-ID': userId },
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
  } catch {
    // Local deterministic fallback
    const total = answers.length || 5;
    const score = answers.length;
    return {
      attemptId: `attempt-${Date.now()}`,
      quizId,
      score,
      total,
      percentage: total > 0 ? Math.round((score / total) * 100) : 0,
      weakTopics: [],
      isDemo: true,
    };
  }
}

export interface DocumentUploadResponse {
  id: string;
  name: string;
  size: number;
  type: string;
  url?: string;
  uploadedAt: string;
  isDemo?: boolean;
}

export async function uploadDocument(
  file: File | { name: string; size: number; type: string }
): Promise<DocumentUploadResponse> {
  if (file instanceof File) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', 'default_student_user');
      formData.append('course_id', 'CS302');
      formData.append('subject_id', 'SUB_OS');
      formData.append('title', file.name);

      const url = API_BASE ? `${API_BASE}/api/documents` : '/api/documents';
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        return {
          id: data.document_id || `doc-${Date.now()}`,
          name: data.filename || file.name,
          size: file.size,
          type: file.type || 'application/pdf',
          uploadedAt: data.created_at || new Date().toISOString(),
          isDemo: false,
        };
      }
    } catch {
      // Fall through to local fallback
    }
  }
  return {
    id: `doc-${Date.now()}`,
    name: file.name,
    size: file.size,
    type: file.type || 'application/pdf',
    uploadedAt: new Date().toISOString(),
    isDemo: true,
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

export async function fetchTodayPlan(userId = 'default_student_user'): Promise<BackendTodayPlan | null> {
  try {
    const res = await request<BackendTodayPlan>(`/api/plans/today?user_id=${encodeURIComponent(userId)}`);
    return { ...res, isDemo: false };
  } catch {
    return null;
  }
}

export async function fetchStudyPlans(userId = 'default_student_user'): Promise<any[] | null> {
  try {
    return await request<any[]>(`/api/plans?user_id=${encodeURIComponent(userId)}`);
  } catch {
    return null;
  }
}

export async function createStudyPlan(payload: {
  userId?: string;
  startDate: string;
  endDate: string;
  availableMinutesPerDay?: number;
}): Promise<any | null> {
  try {
    return await request('/api/plans', {
      method: 'POST',
      body: JSON.stringify({
        user_id: payload.userId || 'default_student_user',
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
  status: 'pending' | 'in_progress' | 'completed' | 'skipped',
  userId = 'default_student_user'
): Promise<BackendStudyTask | null> {
  try {
    return await request<BackendStudyTask>(
      `/api/tasks/${encodeURIComponent(taskId)}?user_id=${encodeURIComponent(userId)}`,
      {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      }
    );
  } catch {
    return null;
  }
}

export async function chatWithAssistant(
  message: string,
  context?: { materialId?: string; subject?: string }
): Promise<{ text: string }> {
  if (API_BASE) {
    try {
      return await request<{ text: string }>('/assistant/chat', {
        method: 'POST',
        body: JSON.stringify({ message, context }),
      });
    } catch {
      // Fall through to local assistant
    }
  }
  return sendChatMessage(message, context?.materialId);
}

function localAssistantResponse(message: string, materialId?: string): string {
  const contextNote = materialId ? `*(Referencing Document ID: \`${materialId}\` — Local Demo Mode)*\n\n` : '';
  const q = message.toLowerCase();
  if (q.includes('tcp') && q.includes('udp')) {
    return `${contextNote}### TCP vs UDP Protocol Comparison\n\n• **TCP (Transmission Control Protocol)** is connection-oriented and ensures guaranteed, ordered, error-checked delivery via sequence numbers and acknowledgements. Best for web browsing (HTTP/HTTPS), file transfer (FTP), and email.\n• **UDP (User Datagram Protocol)** is connectionless and lightweight without retransmissions or ordering overhead. Best for real-time video streaming, VoIP, DNS lookups, and gaming.\n\n*Key takeaway*: Choose TCP when accuracy is critical; choose UDP when low latency is required.`;
  }
  if (q.includes('deadlock')) {
    return `${contextNote}### Operating System Deadlocks\n\nA deadlock occurs when two or more processes cannot proceed because each is waiting for a resource held by the other.\n\n**Four Coffman Conditions (Must all hold simultaneously):**\n1. **Mutual Exclusion**: At least one resource is held in a non-shareable mode.\n2. **Hold and Wait**: A process holds resources while requesting additional ones.\n3. **No Preemption**: Resources cannot be forcibly revoked.\n4. **Circular Wait**: A closed chain of processes exists where each waits for a resource held by the next.\n\n*Prevention Strategy*: Invalidate any single condition (e.g., impose strict global resource acquisition ordering to prevent circular wait).`;
  }
  if (q.includes('cpu scheduling')) {
    return `${contextNote}### CPU Scheduling Summary\n\n1. **FCFS (First-Come, First-Served)**: Non-preemptive, simple, but suffers from the *convoy effect*.\n2. **SJF (Shortest Job First)**: Minimizes average waiting time for known CPU bursts; can cause starvation for longer jobs.\n3. **Round Robin (RR)**: Preemptive scheduling using a fixed time quantum. Prevents starvation and balances interactive responsiveness.`;
  }
  if (q.includes('banker')) {
    return `${contextNote}### Banker's Algorithm (Deadlock Avoidance)\n\nDeveloped by Edsger Dijkstra, the Banker's algorithm evaluates whether granting a resource request leaves the system in a **Safe State**.\n\n- **Safe State**: There exists at least one sequence $\\langle P_1, P_2, \\dots, P_n \\rangle$ such that every process can finish using available resources plus resources currently held by preceding processes.\n- **Data Structures**: Vectors \`Available\`, matrices \`Max\`, \`Allocation\`, and \`Need = Max - Allocation\`.\n- If simulated allocation keeps the state safe, the request is granted; otherwise the process must wait.`;
  }
  if (q.includes('quiz')) {
    return `${contextNote}You can generate practice quizzes directly from Assessment. Choose your source (Topic, Subject, Knowledge Document, or Weak Topics) to test your recall.`;
  }
  if (q.includes('summary') || q.includes('summarize')) {
    return `${contextNote}A concise study summary isolates: (1) core definitions, (2) essential mechanisms, (3) comparative trade-offs, and (4) high-frequency exam pitfalls.`;
  }
  return `${contextNote}Here is a structured study breakdown for "${message}":\n\n1. **Core Concept**: Clarify what this term means in your curriculum.\n2. **Mechanism & Examples**: How it operates step-by-step.\n3. **Common Pitfalls**: Where students typically lose marks in exams.\n4. **Next Practice**: Test yourself with a 5-question quiz in Assessment.`;
}

export { API_BASE };
