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
  if (!API_BASE) throw new Error('API is not connected');
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
  });
  if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function sendChatMessage(message: string): Promise<{ text: string }> {
  if (API_BASE) return request<{ text: string }>('/assistant/chat', { method: 'POST', body: JSON.stringify({ message }) });
  return { text: localAssistantResponse(message) };
}

export async function fetchDashboard() { return API_BASE ? request('/dashboard') : null; }
export async function fetchKnowledge() { return API_BASE ? request('/knowledge') : null; }
export async function submitAssessmentAnswer(questionId: string, answer: string) {
  return API_BASE ? request(`/assessment/questions/${questionId}/answer`, { method: 'POST', body: JSON.stringify({ answer }) }) : { questionId, answer, correct: false };
}

// Service layer boundary for Weak Topics and AI Recommendations
export async function fetchWeakTopics(): Promise<WeakTopic[]> {
  if (API_BASE) {
    return request<WeakTopic[]>('/analytics/weak-topics');
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
  if (API_BASE) {
    return request<StudyRecommendation>('/analytics/recommendation');
  }
  return {
    subjectName: 'Operating Systems',
    topicName: 'Deadlocks & Coffman Conditions',
    reason: 'Exam in 5 days with current diagnostic score of 58%.',
    suggestedDuration: '45 min',
    actionType: 'study',
    isDemo: true,
  };
}

export async function fetchStudyRecommendations(): Promise<StudyRecommendation[]> {
  if (API_BASE) {
    return request<StudyRecommendation[]>('/analytics/recommendations');
  }
  const primary = await fetchStudyRecommendation();
  return [
    primary,
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
  if (API_BASE) {
    return request<GeneratedQuizResponse>('/assessment/generate-quiz', {
      method: 'POST',
      body: JSON.stringify(req),
    });
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
  if (API_BASE) {
    const formData = new FormData();
    if (file instanceof File) {
      formData.append('file', file);
    } else {
      formData.append('metadata', JSON.stringify(file));
    }
    const response = await fetch(`${API_BASE}/knowledge/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error(`Upload failed (${response.status})`);
    return response.json();
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

export async function chatWithAssistant(
  message: string,
  context?: { materialId?: string; subject?: string }
): Promise<{ text: string }> {
  if (API_BASE) {
    return request<{ text: string }>('/assistant/chat', {
      method: 'POST',
      body: JSON.stringify({ message, context }),
    });
  }
  return sendChatMessage(message);
}

function localAssistantResponse(message: string): string {
  const q = message.toLowerCase();
  if (q.includes('tcp') && q.includes('udp')) {
    return `### TCP vs UDP Protocol Comparison\n\n• **TCP (Transmission Control Protocol)** is connection-oriented and ensures guaranteed, ordered, error-checked delivery via sequence numbers and acknowledgements. Best for web browsing (HTTP/HTTPS), file transfer (FTP), and email.\n• **UDP (User Datagram Protocol)** is connectionless and lightweight without retransmissions or ordering overhead. Best for real-time video streaming, VoIP, DNS lookups, and gaming.\n\n*Key takeaway*: Choose TCP when accuracy is critical; choose UDP when low latency is required.`;
  }
  if (q.includes('deadlock')) {
    return `### Operating System Deadlocks\n\nA deadlock occurs when two or more processes cannot proceed because each is waiting for a resource held by the other.\n\n**Four Coffman Conditions (Must all hold simultaneously):**\n1. **Mutual Exclusion**: At least one resource is held in a non-shareable mode.\n2. **Hold and Wait**: A process holds resources while requesting additional ones.\n3. **No Preemption**: Resources cannot be forcibly revoked.\n4. **Circular Wait**: A closed chain of processes exists where each waits for a resource held by the next.\n\n*Prevention Strategy*: Invalidate any single condition (e.g., impose strict global resource acquisition ordering to prevent circular wait).`;
  }
  if (q.includes('cpu scheduling')) {
    return `### CPU Scheduling Summary\n\n1. **FCFS (First-Come, First-Served)**: Non-preemptive, simple, but suffers from the *convoy effect*.\n2. **SJF (Shortest Job First)**: Minimizes average waiting time for known CPU bursts; can cause starvation for longer jobs.\n3. **Round Robin (RR)**: Preemptive scheduling using a fixed time quantum. Prevents starvation and balances interactive responsiveness.`;
  }
  if (q.includes('banker')) {
    return `### Banker's Algorithm (Deadlock Avoidance)\n\nDeveloped by Edsger Dijkstra, the Banker's algorithm evaluates whether granting a resource request leaves the system in a **Safe State**.\n\n- **Safe State**: There exists at least one sequence $\\langle P_1, P_2, \\dots, P_n \\rangle$ such that every process can finish using available resources plus resources currently held by preceding processes.\n- **Data Structures**: Vectors \`Available\`, matrices \`Max\`, \`Allocation\`, and \`Need = Max - Allocation\`.\n- If simulated allocation keeps the state safe, the request is granted; otherwise the process must wait.`;
  }
  if (q.includes('quiz')) {
    return 'You can generate practice quizzes directly from Assessment. Choose your source (Topic, Subject, Knowledge Document, or Weak Topics) to test your recall.';
  }
  if (q.includes('summary') || q.includes('summarize')) {
    return 'A concise study summary isolates: (1) core definitions, (2) essential mechanisms, (3) comparative trade-offs, and (4) high-frequency exam pitfalls.';
  }
  return `Here is a structured study breakdown for "${message}":\n\n1. **Core Concept**: Clarify what this term means in your curriculum.\n2. **Mechanism & Examples**: How it operates step-by-step.\n3. **Common Pitfalls**: Where students typically lose marks in exams.\n4. **Next Practice**: Test yourself with a 5-question quiz in Assessment.`;
}

export { API_BASE };
