// Azure-ready API boundary. The UI never talks to Azure directly.
const API_BASE = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || '';

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

function localAssistantResponse(message: string): string {
  const q = message.toLowerCase();
  if (q.includes('tcp') && q.includes('udp')) return 'TCP is connection-oriented and provides reliable, ordered delivery using acknowledgements, sequencing and retransmission. UDP is connectionless and lightweight; it does not guarantee delivery or ordering. Use TCP when reliability matters and UDP when low overhead or real-time delivery matters.';
  if (q.includes('deadlock')) return 'Deadlock occurs when processes wait indefinitely for resources held by one another. The four necessary conditions are mutual exclusion, hold and wait, no preemption and circular wait. Breaking any one condition can prevent deadlock.';
  if (q.includes('cpu scheduling')) return 'CPU scheduling decides which ready process gets the CPU. FCFS is simple but can cause convoy effects; SJF minimizes average waiting time when burst lengths are known; Round Robin gives each process a time quantum and is common in interactive systems.';
  if (q.includes('quiz')) return 'I can create a quiz from a topic, document or note. Use Assessment for controls such as question count, difficulty and exam mode.';
  if (q.includes('summary') || q.includes('summarize')) return 'A useful study summary should preserve definitions, core mechanisms, formulas, examples, common mistakes and exam-focused comparisons while removing repetition.';
  return `Here is a study-focused explanation of “${message}”: start with the definition, identify the core mechanism, work through one concrete example, then test yourself with a few questions. If you share a document or topic, I can make the explanation more specific.`;
}

export { API_BASE };
