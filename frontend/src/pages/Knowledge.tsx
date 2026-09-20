import { useState, useRef } from 'react';
import { Star, Upload, Search, MoreHorizontal, Plus } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import ProgressBar from '../components/ui/ProgressBar';
import { useApp, SUBJECTS, RECENT_ACTIVITIES } from '../context/AppContext';

const TABS = ['All Materials', 'Subjects', 'Recent', 'Starred', 'Trash'];
const TYPE_COLORS: Record<string, string> = { PDF: '#ef4444', PPT: '#f59e0b', DOCX: '#3b82f6', TXT: '#6b7280' };

export default function Knowledge() {
  const { knowledgeMaterials, addKnowledgeMaterial } = useApp();
  const [activeTab, setActiveTab] = useState('All Materials');
  const [searchQuery, setSearchQuery] = useState('');
  const [processingQueue, setProcessingQueue] = useState<{ name: string; progress: number }[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const filtered = knowledgeMaterials.filter(m => {
    if (activeTab === 'Starred') return m.starred;
    if (searchQuery) return m.name.toLowerCase().includes(searchQuery.toLowerCase());
    return true;
  });

  const handleUpload = (files: FileList | null) => {
    if (!files) return;
    Array.from(files).forEach(file => {
      const item = { name: file.name, progress: 0 };
      setProcessingQueue(prev => [...prev, item]);
      // Simulate processing
      const interval = setInterval(() => {
        setProcessingQueue(prev => prev.map(p =>
          p.name === file.name ? { ...p, progress: Math.min(p.progress + 15, 100) } : p
        ));
      }, 400);
      setTimeout(() => {
        clearInterval(interval);
        setProcessingQueue(prev => prev.filter(p => p.name !== file.name));
        addKnowledgeMaterial({
          name: file.name,
          subject: 'Data Structures',
          type: (file.name.split('.').pop()?.toUpperCase() || 'PDF') as 'PDF' | 'PPT' | 'DOCX' | 'TXT',
          size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
          addedOn: new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }),
          status: 'Ready',
          starred: false,
        });
      }, 3000);
    });
  };

  return (
    <div>
      <HeroHeader
        tag="My Knowledge"
        title={<>Your Knowledge, Your <span className="accent">Advantage.</span></>}
        subtitle="Upload, organize and turn your study material into personalized learning."
        image="/assets/header_knowledge.png"
      />

      {/* Tabs */}
      <div className="tab-nav">
        {TABS.map(t => (
          <button key={t} className={`tab-item ${activeTab === t ? 'active' : ''}`} onClick={() => setActiveTab(t)}>{t}</button>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-6">
        {/* Left */}
        <div>
          {/* Upload Zone */}
          <div
            className="card mb-6 flex flex-col sm:flex-row items-center gap-6 cursor-pointer border-dashed"
            onClick={() => fileInputRef.current?.click()}
            onDragOver={e => e.preventDefault()}
            onDrop={e => { e.preventDefault(); handleUpload(e.dataTransfer.files); }}
          >
            <div className="flex-1 text-center sm:text-left">
              <Upload size={32} className="mx-auto sm:mx-0 mb-2 text-[var(--color-text-muted)]" />
              <div className="font-semibold text-sm">Drop your files here</div>
              <div className="text-xs text-[var(--color-text-muted)]">PDF, PPT, DOCX, TXT (Max 50 MB each)</div>
              <button className="mt-3 px-6 py-2 bg-[var(--color-green-primary)] text-white rounded-lg text-sm font-semibold hover:bg-[var(--color-green-accent)] transition-colors">
                Upload Material
              </button>
            </div>
            <div className="flex flex-col gap-2 text-sm">
              {(['PDF', 'PPT', 'DOCX', 'TXT'] as const).map(t => (
                <div key={t} className="flex items-center gap-2">
                  <span>📄</span>
                  <div>
                    <div className="font-semibold text-xs">{t}</div>
                    <div className="text-[0.65rem] text-[var(--color-text-muted)]">
                      {t === 'PDF' ? 'Lecture notes, textbooks' : t === 'PPT' ? 'Class slides' : t === 'DOCX' ? 'Handwritten notes, assignments' : 'Quick notes'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <input ref={fileInputRef} type="file" className="hidden" multiple accept=".pdf,.ppt,.pptx,.doc,.docx,.txt"
              onChange={e => handleUpload(e.target.files)} />
          </div>

          {/* Your Subjects */}
          <SectionHeader icon="📚" title="Your Subjects" action="Manage Subjects" />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            {SUBJECTS.slice(0, 4).map(s => (
              <div key={s.id} className="card">
                <div className="text-sm font-semibold mb-0.5">{s.name}</div>
                <div className="text-xs text-[var(--color-text-muted)] mb-2">{s.documentsCount} documents</div>
                <ProgressBar value={s.progress} color={s.color} showLabel />
              </div>
            ))}
            <div className="card flex flex-col items-center justify-center text-[var(--color-text-muted)] cursor-pointer hover:bg-gray-50 transition-colors">
              <Plus size={20} className="mb-1" />
              <span className="text-xs font-medium">Add Subject</span>
            </div>
          </div>

          {/* All Materials Table */}
          <SectionHeader title={`All Materials (${filtered.length})`}>
            <div className="flex items-center gap-2 ml-auto mr-4">
              <div className="flex items-center gap-2 px-3 py-1.5 border border-[var(--color-card-border)] rounded-lg text-xs">
                <Search size={12} />
                <input
                  type="text"
                  placeholder="Search files..."
                  className="border-none outline-none bg-transparent text-xs w-24"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
          </SectionHeader>
          <div className="card overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-[var(--color-text-muted)] border-b border-[var(--color-card-border)]">
                  <th className="pb-2 font-medium">Name</th>
                  <th className="pb-2 font-medium">Subject</th>
                  <th className="pb-2 font-medium">Type</th>
                  <th className="pb-2 font-medium">Size</th>
                  <th className="pb-2 font-medium">Added On</th>
                  <th className="pb-2 font-medium">Status</th>
                  <th className="pb-2"></th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((m, i) => (
                  <tr key={i} className="border-b border-[var(--color-border-light)] last:border-b-0 hover:bg-gray-50/50">
                    <td className="py-2.5 flex items-center gap-2">
                      <span>📄</span>
                      <span className="font-medium">{m.name}</span>
                      {m.starred && <Star size={12} className="text-yellow-500 fill-yellow-500" />}
                    </td>
                    <td>
                      {(() => {
                        const s = SUBJECTS.find(x => x.name === m.subject || x.fullName === m.subject);
                        const bg = s ? `${s.color}18` : '#e8f5f0';
                        const col = s ? s.color : '#2d5f47';
                        return (
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold" style={{ background: bg, color: col }}>
                            {m.subject}
                          </span>
                        );
                      })()}
                    </td>
                    <td><span className="font-semibold text-xs" style={{ color: TYPE_COLORS[m.type] }}>{m.type}</span></td>
                    <td className="text-xs text-[var(--color-text-muted)]">{m.size}</td>
                    <td className="text-xs text-[var(--color-text-muted)]">{m.addedOn}</td>
                    <td><span className="flex items-center gap-1 text-xs"><span className="w-1.5 h-1.5 rounded-full bg-green-500" />{m.status}</span></td>
                    <td><button className="text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)]"><MoreHorizontal size={16} /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Column */}
        <div>
          {/* Processing Queue */}
          {processingQueue.length > 0 && (
            <>
              <SectionHeader icon="⏳" title={`Processing Queue ${processingQueue.length}`} action="View all" />
              <div className="card mb-4">
                {processingQueue.map((p, i) => (
                  <div key={i} className="mb-3 last:mb-0">
                    <div className="text-xs font-medium mb-1">{p.name}</div>
                    <ProgressBar value={p.progress} color="#2d5f47" />
                    <div className="text-[0.65rem] text-[var(--color-text-muted)] mt-1">Processing... {p.progress}%</div>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Storage Overview */}
          <SectionHeader icon="💾" title="Storage Overview" action="View details" />
          <div className="card mb-6">
            <ProgressBar value={24} color="#2d5f47" height={8} />
            <div className="flex justify-between mt-2 text-xs text-[var(--color-text-muted)]">
              <span>1.2 GB used of 5 GB</span>
              <span className="font-semibold">24%</span>
            </div>
          </div>

          {/* Recent Activity */}
          <SectionHeader icon="🕐" title="Recent Activity" action="View all" />
          <div className="card mb-6">
            {RECENT_ACTIVITIES.slice(0, 5).map((a, i) => (
              <div key={i} className="flex items-center gap-3 py-2" style={{ borderBottom: i < 4 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: a.iconColor }} />
                <span className="text-xs flex-1">{a.text}</span>
                <span className="text-[0.65rem] text-[var(--color-text-muted)] whitespace-nowrap">{a.time}</span>
              </div>
            ))}
          </div>

          {/* CTA Card */}
          <div className="rounded-2xl overflow-hidden relative p-6" style={{ background: 'linear-gradient(135deg, #1a3a2a, #0f1a14)' }}>
            <div className="relative z-10">
              <h4 className="text-white font-semibold text-sm mb-1">Turn your notes into understanding.</h4>
              <p className="text-white/60 text-xs">Upload. Learn. Practice. Grow.</p>
            </div>
            <button className="relative z-10 mt-3 w-9 h-9 rounded-full bg-white/10 border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-colors ml-auto">
              →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
