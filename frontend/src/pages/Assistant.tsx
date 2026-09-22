import { useEffect, useRef, useState } from 'react';
import { Send, Mic, Sparkles, Trash2, Copy, Check, Info, Bot } from 'lucide-react';
import { useSearchParams } from 'react-router-dom';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import Modal from '../components/ui/Modal';
import { useApp } from '../context/AppContext';
import { sendChatMessage } from '../services/api';

const QUICK = [
  ['💡 Explain Concept', 'Explain Deadlock Coffman conditions in simple language with an example'],
  ['📝 Summarize Material', 'Summarize key points and exam criteria for TCP vs UDP flow control'],
  ['📄 High-Yield Notes', 'Create exam-ready revision notes for B+ tree indexing'],
  ['⚖️ Compare Topics', 'Compare Deadlock Prevention vs Deadlock Avoidance'],
  ['🎯 Create Practice', 'Generate 5 conceptual questions on CPU scheduling algorithms'],
  ['📐 Step-by-Step Problem', 'Walk me through Banker’s algorithm safety check step by step'],
];

const PROMPTS = [
  'Explain the 4 Coffman conditions required for deadlock',
  'What is the difference between TCP and UDP sliding window?',
  'Explain BCNF decomposition and why it avoids update anomalies',
  'How does Round Robin scheduling choose the time quantum?',
  'Walk through Banker’s algorithm safety state evaluation',
];

export default function Assistant() {
  const { chatHistory, addChatMessage, clearChatHistory, pushToast } = useApp();
  const [params] = useSearchParams();

  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [tool, setTool] = useState<string | null>(null);
  const [modelModal, setModelModal] = useState(false);
  const [recentModal, setRecentModal] = useState(false);
  const [confirmClear, setConfirmClear] = useState(false);
  const [modelName, setModelName] = useState('Local Demo Mode (Azure AI Ready)');
  const [copied, setCopied] = useState<number | null>(null);
  const end = useRef<HTMLDivElement>(null);

  // Preload prompt from URL if navigated from Knowledge / Assessment
  useEffect(() => {
    const urlPrompt = params.get('prompt');
    const urlMaterial = params.get('material');
    if (urlPrompt) {
      setInput(urlMaterial ? `${urlPrompt} (${urlMaterial})` : urlPrompt);
    }
  }, [params]);

  useEffect(() => {
    end.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, typing]);

  const send = async (text = input) => {
    const value = text.trim();
    if (!value || typing) return;
    setInput('');
    addChatMessage('user', value);
    setTyping(true);
    try {
      const r = await sendChatMessage(value);
      addChatMessage('assistant', r.text);
    } catch (e) {
      addChatMessage(
        'assistant',
        `Could not reach the AI service. ${e instanceof Error ? e.message : 'Please try again.'}`
      );
    } finally {
      setTyping(false);
    }
  };

  const selectTool = (label: string, prompt: string) => {
    setTool(label);
    setInput(prompt);
  };

  const voice = () => {
    const SpeechRecognition = (
      window as Window & {
        webkitSpeechRecognition?: new () => {
          lang: string;
          start: () => void;
          onresult: (e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void;
          onerror: () => void;
        };
      }
    ).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      pushToast('Voice input is not supported in this browser', 'error');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = e => setInput(e.results[0][0].transcript);
    recognition.onerror = () => pushToast('Voice input failed', 'error');
    recognition.start();
    pushToast('Listening for voice prompt…', 'info');
  };

  const copy = (text: string, index: number) => {
    navigator.clipboard?.writeText(text).then(() => {
      setCopied(index);
      window.setTimeout(() => setCopied(null), 1200);
      pushToast('Response copied to clipboard');
    }).catch(() => pushToast('Clipboard copy unavailable', 'error'));
  };

  return (
    <div className="page-stack">
      <HeroHeader
        tag="AI STUDY ASSISTANT"
        title={
          <>
            Your Coursework <span className="accent">Study Companion.</span>
          </>
        }
        subtitle="Clarify doubts, explain course concepts, generate summaries, and prepare for upcoming exams."
      />

      {/* Integration Readiness Banner */}
      <div className="card p-3 flex items-center justify-between text-xs bg-[var(--color-green-light)] text-[var(--color-green-accent)] border-[var(--color-green-border)]">
        <div className="flex items-center gap-2">
          <Bot size={16} />
          <span>
            <b>Integration Ready:</b> Front-end is configured for Azure OpenAI and Azure AI Foundry. Currently operating in deterministic local demo mode.
          </span>
        </div>
        <span className="font-semibold text-[.65rem] px-2 py-0.5 rounded bg-white/60 dark:bg-black/20">
          Azure Foundry Ready
        </span>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Left Chat Window */}
        <div>
          <div className="card mb-3 p-0">
            {/* Chat Header */}
            <div className="flex items-center justify-between px-5 py-3 border-b border-[var(--color-card-border)]">
              <div>
                <b className="text-sm">AcadAssist AI</b>
                <span className="ml-2 text-[.65rem] text-green-600 font-semibold">
                  ● {modelName}
                </span>
              </div>
              <div className="flex gap-2">
                <button className="btn subtle" onClick={() => setConfirmClear(true)}>
                  <Trash2 size={14} /> Clear chat
                </button>
                <button className="btn subtle" onClick={() => setModelModal(true)}>
                  Model mode ▾
                </button>
              </div>
            </div>

            {/* Chat Message Scroll Area */}
            <div className="p-5 max-h-[540px] overflow-y-auto">
              {chatHistory.length ? (
                chatHistory.map((m, i) => (
                  <div key={i} className={m.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}>
                    <div className="bubble">
                      <div className="whitespace-pre-wrap">{m.text}</div>
                      <div className="chat-time flex items-center justify-between mt-2 pt-1 border-t border-black/5 dark:border-white/10">
                        <span>{m.time}</span>
                        {m.role === 'assistant' && (
                          <button
                            onClick={() => copy(m.text, i)}
                            aria-label="Copy response"
                            className="text-inherit opacity-70 hover:opacity-100"
                          >
                            {copied === i ? <Check size={12} /> : <Copy size={12} />}
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">
                  <Sparkles size={28} />
                  <h3>Start a coursework conversation</h3>
                  <p>Ask a question about your curriculum or select a quick study tool below.</p>
                </div>
              )}
              {typing && (
                <div className="chat-bubble-ai">
                  <div className="bubble">Formulating study explanation…</div>
                </div>
              )}
              <div ref={end} />
            </div>
          </div>

          {/* Chat Input Bar */}
          <div className="flex gap-2 mb-3">
            <div className="flex-1 flex items-center gap-2 px-4 py-2.5 bg-[var(--color-card-bg)] border border-[var(--color-card-border)] rounded-xl">
              <input
                className="flex-1 bg-transparent outline-none text-sm text-[var(--color-text-dark)]"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && send()}
                placeholder="Ask about Deadlocks, TCP/UDP, Normalization, or problem derivations…"
              />
              <button
                onClick={voice}
                aria-label="Voice input"
                className="text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)]"
              >
                <Mic size={16} />
              </button>
            </div>
            <button
              onClick={() => send()}
              disabled={typing || !input.trim()}
              className="w-10 h-10 rounded-xl bg-[var(--color-green-accent)] text-white flex items-center justify-center disabled:opacity-50 cursor-pointer flex-shrink-0"
              aria-label="Send message"
            >
              <Send size={16} />
            </button>
          </div>

          {/* Quick Tool Filter Chips */}
          <div className="flex flex-wrap gap-2">
            {QUICK.map(([label, prompt]) => (
              <button key={label} className="filter-chip" onClick={() => selectTool(label, prompt)}>
                {label}
              </button>
            ))}
          </div>
        </div>

        {/* Right Sidebar: Tools & Prompts */}
        <div>
          <SectionHeader icon="⚡" title="Quick Study Tools" action="See all" onAction={() => setRecentModal(true)} />
          <div className="grid grid-cols-2 gap-3 mb-6">
            {QUICK.slice(0, 4).map(([label, prompt]) => (
              <button key={label} className="card text-left p-3 hover:border-[var(--color-green-accent)]" onClick={() => selectTool(label, prompt)}>
                <div className="text-lg mb-1.5">{label.split(' ')[0]}</div>
                <b className="text-xs block text-[var(--color-text-dark)]">{label.slice(2)}</b>
                <p className="text-[.62rem] text-[var(--color-text-muted)] mt-1 line-clamp-2">{prompt}</p>
              </button>
            ))}
          </div>

          <SectionHeader icon="💬" title="High-Yield Prompts" action="View all" onAction={() => setRecentModal(true)} />
          <div className="card mb-6 p-2 divide-y divide-[var(--color-border-light)]">
            {PROMPTS.map(p => (
              <button
                key={p}
                className="w-full text-left py-2.5 px-2 text-xs text-[var(--color-text-dark)] flex items-center justify-between hover:bg-[var(--color-green-light)]/40 rounded-lg transition-colors"
                onClick={() => {
                  setInput(p);
                  setRecentModal(false);
                }}
              >
                <span className="truncate pr-2">{p}</span>
                <span className="text-[var(--color-text-muted)] flex-shrink-0">→</span>
              </button>
            ))}
          </div>

          <div className="card p-3 text-xs text-[var(--color-text-muted)]">
            <div className="flex items-center gap-1.5 font-bold text-[var(--color-text-dark)] mb-1">
              <Info size={14} /> Azure AI Integration Point
            </div>
            When Person 1 connects Azure OpenAI / Foundry in <code>src/services/api.ts</code>, responses will automatically stream from your deployed models.
          </div>
        </div>
      </div>

      {/* Tool Execution Modal */}
      <Modal open={!!tool} onClose={() => setTool(null)} title={tool || ''} subtitle="Customize prompt before asking AI">
        <textarea
          className="textarea"
          rows={5}
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <div className="modal-actions">
          <button className="btn secondary" onClick={() => setTool(null)}>
            Cancel
          </button>
          <button
            className="btn primary"
            onClick={() => {
              setTool(null);
              send();
            }}
          >
            <Sparkles size={15} /> Run prompt
          </button>
        </div>
      </Modal>

      {/* Model Selection Modal */}
      <Modal
        open={modelModal}
        onClose={() => setModelModal(false)}
        title="Choose AI Model Mode"
        subtitle="Frontend representation of deployment configurations for Azure integration"
      >
        <button
          className="card w-full text-left mb-2 p-3 hover:border-[var(--color-green-accent)]"
          onClick={() => {
            setModelName('Fast Study Mode (Azure OpenAI Ready)');
            setModelModal(false);
            pushToast('Fast Study Mode selected');
          }}
        >
          <div className="flex justify-between items-center">
            <b>Fast Study Mode</b>
            <span className="soft-badge text-[.6rem]">Demo Mode</span>
          </div>
          <p className="muted text-xs mt-1">
            Concise explanations, rapid definition lookups, and fast quiz hints. Prepared for <code>gpt-4o-mini</code>.
          </p>
        </button>

        <button
          className="card w-full text-left mb-2 p-3 hover:border-[var(--color-green-accent)]"
          onClick={() => {
            setModelName('Deep Reasoning Mode (Foundry Ready)');
            setModelModal(false);
            pushToast('Deep Reasoning Mode selected');
          }}
        >
          <div className="flex justify-between items-center">
            <b>Deep Reasoning Mode</b>
            <span className="soft-badge text-[.6rem]">Demo Mode</span>
          </div>
          <p className="muted text-xs mt-1">
            Formal proofs, step-by-step mathematical derivations, and code simulations. Prepared for Azure AI Foundry reasoning endpoints.
          </p>
        </button>

        <button
          className="card w-full text-left p-3 hover:border-[var(--color-green-accent)]"
          onClick={() => {
            setModelName('Deterministic Local Mode (Offline)');
            setModelModal(false);
            pushToast('Deterministic Local Mode selected');
          }}
        >
          <div className="flex justify-between items-center">
            <b>Deterministic Local Assistant</b>
            <span className="soft-badge text-[.6rem]">Active Fallback</span>
          </div>
          <p className="muted text-xs mt-1">
            Built-in deterministic coursework question answering. Operates offline without external network dependency.
          </p>
        </button>
      </Modal>

      {/* All Tools Modal */}
      <Modal open={recentModal} onClose={() => setRecentModal(false)} title="Study Tools & High-Yield Prompts">
        <div className="space-y-2">
          {QUICK.map(([label, prompt]) => (
            <button
              key={label}
              className="card w-full text-left p-3 flex justify-between items-center hover:border-[var(--color-green-accent)]"
              onClick={() => {
                setRecentModal(false);
                selectTool(label, prompt);
              }}
            >
              <div>
                <b className="text-xs block">{label}</b>
                <small className="text-[var(--color-text-muted)] text-[.65rem]">{prompt}</small>
              </div>
              <span className="text-[var(--color-text-muted)]">→</span>
            </button>
          ))}
        </div>
      </Modal>

      {/* Confirm Clear Chat Modal */}
      <Modal
        open={confirmClear}
        onClose={() => setConfirmClear(false)}
        title="Clear conversation history"
        subtitle="This only removes local chat messages in this browser."
      >
        <p className="text-sm">Delete current conversation messages? Course documents, notes, and assessments will stay intact.</p>
        <div className="modal-actions">
          <button className="btn secondary" onClick={() => setConfirmClear(false)}>
            Cancel
          </button>
          <button
            className="btn danger"
            onClick={() => {
              clearChatHistory();
              setConfirmClear(false);
              pushToast('Chat history cleared', 'info');
            }}
          >
            Clear history
          </button>
        </div>
      </Modal>
    </div>
  );
}
