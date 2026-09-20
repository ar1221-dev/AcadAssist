// Clean API boundary for future Python backend integration
// All mock implementations live here — swap with real fetch calls later.

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchDashboard() {
  // Future: return fetch(`${API_BASE}/dashboard`).then(r => r.json());
  return Promise.resolve(null);
}

export async function fetchKnowledge() {
  return Promise.resolve(null);
}

export async function submitAssessmentAnswer(questionId: string, answer: string) {
  return Promise.resolve({ correct: Math.random() > 0.3, questionId, answer });
}

export async function sendChatMessage(message: string) {
  // Mock AI response with slight delay
  await new Promise(r => setTimeout(r, 600));
  return {
    text: `### Theoretical Synthesis: **${message}**\n\n1. **Core Mathematical Formulation**:\n   Under high-dimensional simulated conditions, this dynamic behaves according to non-linear operator bounds.\n2. **Manifold Mapping**:\n   State vectors converge exponentially along projected geodesics without loss of topological invariants.\n3. **Practical Verification**:\n   Evaluate on the 100-node synthetic benchmark to confirm convergence stability!`,
  };
}

export async function uploadFile(file: File) {
  // Simulate processing
  await new Promise(r => setTimeout(r, 1500));
  return {
    name: file.name,
    subject: 'Quantum Cognition',
    type: file.name.split('.').pop()?.toUpperCase() || 'PDF',
    size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
    addedOn: new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }),
    status: 'Ready',
    starred: false,
  };
}

export { API_BASE };
