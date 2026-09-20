import { useState, useRef, useEffect } from 'react';
import { Send, Mic } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import { useApp } from '../context/AppContext';
import { sendChatMessage } from '../services/api';

const QUICK_TOOLS = [
  { icon: '📖', bg: '#edf3fd', title: 'Explain Concept', desc: 'Get clear, simple explanations' },
  { icon: '📝', bg: '#fff0ea', title: 'Summarize Notes', desc: 'Turn material into concise notes' },
  { icon: '✓', bg: '#eef8f2', title: 'Solve Problems', desc: 'Step-by-step solutions' },
  { icon: '🎯', bg: '#fef9ee', title: 'Generate Quiz', desc: 'Practice instantly' },
  { icon: '⚖️', bg: '#f0edf9', title: 'Compare Topics', desc: 'See side-by-side differences' },
  { icon: '🗂️', bg: '#f5f4ef', title: 'Create Flashcards', desc: 'Quick revision cards' },
];

const SUGGESTED_PROMPTS = [
  'Derive Poincaré ball metric geodesics',
  'Explain Byzantine fault tolerance in distributed state machines',
  'Simulate accretion disc frame-dragging around Kerr black holes',
  'How do diffusion priors fold synthetic macrocyclic peptides?',
  'Compare Raft vs Paxos leader election under network partitions',
  'Synthesize notes on Sparse Graph Attention Networks',
];

const RECENT_CHATS = [
  { title: 'Hyperbolic Manifold Embeddings', date: 'Today, 10:14 AM' },
  { title: 'Derivation of Kerr Geodesics', date: 'Yesterday, 8:21 PM' },
  { title: 'Byzantine Fault Tolerance Proofs', date: '14 Sep 2026' },
];

export default function Assistant() {
  const { chatHistory, addChatMessage, user } = useApp();
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const msg = input.trim();
    setInput('');
    addChatMessage('user', msg);
    setIsTyping(true);
    try {
      const reply = await sendChatMessage(msg);
      addChatMessage('assistant', reply.text);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div>
      <HeroHeader
        tag="AI STUDY ASSISTANT"
        title={<>Your Personal Study <span className="accent">Companion.</span></>}
        subtitle="Ask doubts, get explanations, generate notes, solve problems — all in one place."
        image="/assets/header_assistant.png"
      />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Chat Column */}
        <div>
          <div className="card mb-3" style={{ padding: 0 }}>
            {/* Chat Header */}
            <div className="flex items-center justify-between px-5 py-3 border-b border-[var(--color-card-border)]">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-[var(--color-green-primary)] text-white flex items-center justify-center font-bold text-sm">A</div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold">AcadAssist AI</span>
                    <span className="flex items-center gap-1 text-[0.65rem] text-green-600 bg-green-50 px-2 py-0.5 rounded-full font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500" /> Online
                    </span>
                  </div>
                  <div className="text-[0.68rem] text-[var(--color-text-muted)]">Your study assistant, always here to help.</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs border border-[var(--color-card-border)] rounded-lg px-3 py-1 text-[var(--color-text-dark)]">Gemini 1.5 Flash ▾</span>
                <span className="text-[var(--color-text-muted)] cursor-pointer">•••</span>
              </div>
            </div>

            {/* Messages */}
            <div className="p-5 max-h-[500px] overflow-y-auto">
              {chatHistory.map((msg, i) => (
                msg.role === 'user' ? (
                  <div key={i} className="chat-bubble-user">
                    <div className="bubble">
                      {msg.text}
                      <div className="chat-time">{msg.time}</div>
                    </div>
                    <div className="w-8 h-8 rounded-full bg-[var(--color-green-accent)] text-white flex items-center justify-center text-xs font-bold flex-shrink-0">
                      {user.name[0]}
                    </div>
                  </div>
                ) : (
                  <div key={i} className="chat-bubble-ai">
                    <div className="w-8 h-8 rounded-full bg-[var(--color-green-primary)] text-white flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0">A</div>
                    <div className="bubble" dangerouslySetInnerHTML={{
                      __html: msg.text
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\n/g, '<br/>')
                        .replace(/\|(.*?)\|/g, (_, row) => `<span class="text-xs">${row}</span>`)
                    }} />
                  </div>
                )
              ))}
              {isTyping && (
                <div className="chat-bubble-ai">
                  <div className="w-8 h-8 rounded-full bg-[var(--color-green-primary)] text-white flex items-center justify-center text-xs font-bold flex-shrink-0">A</div>
                  <div className="bubble"><span className="animate-pulse">Thinking...</span></div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
          </div>

          {/* Input */}
          <div className="flex gap-2 mb-3">
            <div className="flex-1 flex items-center gap-2 px-4 py-2.5 bg-white border border-[var(--color-card-border)] rounded-xl">
              <input
                type="text"
                placeholder="Ask a question, upload a file, or give a topic..."
                className="flex-1 bg-transparent outline-none text-sm"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
              />
              <Mic size={16} className="text-[var(--color-text-muted)] cursor-pointer" />
            </div>
            <button
              onClick={handleSend}
              className="w-10 h-10 rounded-xl bg-[var(--color-green-accent)] text-white flex items-center justify-center hover:bg-[var(--color-green-primary)] transition-colors"
            >
              <Send size={16} />
            </button>
          </div>

          {/* Action Chips */}
          <div className="flex flex-wrap gap-2">
            {['💡 Explain', '📝 Summarize', '📄 Generate Notes', '📐 Solve Problem', '⚖️ Compare', '🎯 Create Quiz'].map(chip => (
              <button key={chip} className="px-3 py-1.5 bg-white border border-[var(--color-card-border)] rounded-full text-xs font-medium text-[var(--color-text-dark)] hover:border-[var(--color-green-accent)] transition-colors">
                {chip}
              </button>
            ))}
          </div>
        </div>

        {/* Right Column */}
        <div>
          <SectionHeader icon="⚡" title="Quick Tools" action="See all" />
          <div className="grid grid-cols-2 gap-3 mb-6">
            {QUICK_TOOLS.map((t, i) => (
              <div key={i} className="card cursor-pointer hover:shadow-md transition-shadow">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center text-sm mb-2" style={{ background: t.bg }}>{t.icon}</div>
                <div className="text-xs font-semibold">{t.title}</div>
                <div className="text-[0.6rem] text-[var(--color-text-muted)]">{t.desc}</div>
              </div>
            ))}
          </div>

          <SectionHeader icon="💬" title="Suggested Prompts" action="View all" />
          <div className="card mb-6">
            {SUGGESTED_PROMPTS.map((p, i) => (
              <div key={i} className="flex items-center justify-between py-2 cursor-pointer hover:bg-gray-50 px-1 rounded"
                style={{ borderBottom: i < SUGGESTED_PROMPTS.length - 1 ? '1px solid #f0ede6' : 'none' }}
                onClick={() => setInput(p)}>
                <div className="flex items-center gap-2 text-xs"><span className="text-[var(--color-text-light)]">●</span> {p}</div>
                <span className="text-[var(--color-green-accent)] font-bold text-sm">›</span>
              </div>
            ))}
          </div>

          <SectionHeader icon="⏱️" title="Your Recent Chats" action="View all" />
          <div className="card">
            {RECENT_CHATS.map((c, i) => (
              <div key={i} className="flex items-center justify-between py-2.5 cursor-pointer" style={{ borderBottom: i < RECENT_CHATS.length - 1 ? '1px solid #f0ede6' : 'none' }}>
                <div className="flex items-center gap-2">
                  <span className="text-[var(--color-text-light)] text-xs">●</span>
                  <span className="text-xs font-semibold">{c.title}</span>
                </div>
                <span className="text-[0.6rem] text-[var(--color-text-muted)]">{c.date}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
