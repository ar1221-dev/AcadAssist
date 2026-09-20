import { useState } from 'react';
import HeroHeader from '../components/ui/HeroHeader';
import SectionHeader from '../components/ui/SectionHeader';
import ProgressBar from '../components/ui/ProgressBar';
import MotivationalBanner from '../components/ui/MotivationalBanner';

// Multiple arbitrary, made-up academic personas for demo & randomization
interface ArbitraryPersona {
  fullName: string;
  role: string;
  field: string;
  academicLevel: string;
  studentId: string;
  email: string;
  advisor: string;
  lab: string;
  location: string;
  memberSince: string;
  bio: string;
  tags: string[];
  quote: string;
  streakDays: number;
  streakStatus: string;
  cgpa: string;
  shortGoal: string;
  medGoal: string;
  longGoal: string;
  interests: { name: string; icon: string }[];
  badges: { name: string; icon: string; color: string; unlocked: boolean; desc: string }[];
  subjects: { name: string; progress: number; color: string }[];
  activities: { text: string; time: string; iconColor: string }[];
}

const ARBITRARY_PERSONAS: ArbitraryPersona[] = [
  {
    fullName: 'Rowan K. Vance',
    role: 'Junior Research Fellow & Scholar',
    field: 'Cognitive Computing & Cyber-Physical Systems',
    academicLevel: 'Honors Bachelor of Science (Class of 2027)',
    studentId: 'SOL-84920-NX',
    email: 'rowan.vance@solaris-institute.edu',
    advisor: 'Prof. Helena Vance-Mercer',
    lab: 'Swarm Cybernetics Lab #4',
    location: 'North Observatory Campus, Quadrant B',
    memberSince: '14 Oct 2024',
    bio: 'Investigating decentralized consensus protocols, neuromorphic sensory computing, and non-Euclidean manifold embeddings. Passionate about synthetic curiosity, generative modeling, and open science.',
    tags: ['Autonomous Systems', 'Neuromorphic Chips', 'Information Theory', 'Synthwave', 'Open Science'],
    quote: 'Curiosity is the architecture of discovery.',
    streakDays: 43,
    streakStatus: 'Ranked in top 1.5% most consistent researchers',
    cgpa: '3.92 / 4.00',
    shortGoal: 'Synthesize benchmark results for Sparse Graph Attention Networks',
    medGoal: 'Submit co-authored preprint on Neuromorphic Sensory Routing',
    longGoal: 'Found an open-source Autonomous Cybernetics Consortium',
    interests: [
      { name: 'Swarm Robotics', icon: '🤖' },
      { name: 'Neuromorphic Audio', icon: '🎵' },
      { name: 'Quantum Topology', icon: '🌐' },
      { name: 'Synthesizer Engineering', icon: '🎛️' },
      { name: 'Competitive Chess', icon: '♟️' },
      { name: 'Sci-Fi Philosophy', icon: '📖' },
    ],
    badges: [
      { name: 'Quantum Sprint', icon: '⚡', color: '#10b981', unlocked: true, desc: '40+ day continuous deep-work streak' },
      { name: 'Graph Pioneer', icon: '🕸️', color: '#3b82f6', unlocked: true, desc: 'Mastered 250 algorithmic graph models' },
      { name: 'Polymath Synthesizer', icon: '📜', color: '#8b5cf6', unlocked: true, desc: 'Synthesized 80 multi-agent research papers' },
      { name: 'Cosmic Navigator', icon: '🌌', color: '#f59e0b', unlocked: true, desc: 'Explored 6 advanced cognitive domains' },
      { name: 'Neural Architect', icon: '🛡️', color: '#ec4899', unlocked: true, desc: 'Trained 15 custom neuromorphic manifolds' },
    ],
    subjects: [
      { name: 'Autonomous Systems & Control', progress: 92, color: '#2d5f47' },
      { name: 'Distributed Consensus Protocols', progress: 84, color: '#e07a5f' },
      { name: 'Neuromorphic Sensory Computing', progress: 78, color: '#6366f1' },
      { name: 'Graph Neural Networks', progress: 95, color: '#d97706' },
      { name: 'Computational Complexity Theory', progress: 88, color: '#0ea5e9' },
    ],
    activities: [
      { text: 'Trained custom diffusion checkpoint on neural manifolds (Accuracy: 98.2%)', time: '18m ago', iconColor: '#2d5f47' },
      { text: 'Submitted diagnostic test on Non-Euclidean Graph Embeddings (Score: 96%)', time: '2h ago', iconColor: '#3b82f6' },
      { text: 'Compiled 38-page brief on Byzantine Fault Tolerant State Machines', time: 'Yesterday', iconColor: '#e07a5f' },
      { text: 'Completed 4-hour deep focus marathon on Sparse Tensor Factorization', time: '2 days ago', iconColor: '#f59e0b' },
      { text: 'Unlocked "Quantum Sprint" peer research milestone', time: '3 days ago', iconColor: '#8b5cf6' },
    ],
  },
  {
    fullName: 'Aria Sun-Covington',
    role: 'Theoretical Astrophysics Scholar',
    field: 'Computational Astrophysics & Stellar Hydrodynamics',
    academicLevel: 'Dual Major BSc / MSc Fellow',
    studentId: 'AST-39102-KZ',
    email: 'aria.covington@astralis-institute.org',
    advisor: 'Dr. Thaddeus Sterling',
    lab: 'Deep Field Interferometry Lab',
    location: 'Kepler Summit Observatory, Wing B',
    memberSince: '02 Feb 2025',
    bio: 'Simulating proto-planetary accretion disks, magnetohydrodynamic plasma turbulence, and gravitational lensing around Kerr black holes. Stargazer and amateur cellist.',
    tags: ['Plasma Physics', 'N-Body Simulation', 'GPU Shaders', 'Acoustic Waves', 'Spectroscopy'],
    quote: 'To look into deep space is to read our own origins.',
    streakDays: 61,
    streakStatus: 'Ranked #1 in Astronomical Modeling cohort',
    cgpa: '3.98 / 4.00',
    shortGoal: 'Run 100M particle Monte Carlo simulation of circumstellar discs',
    medGoal: 'Co-author observational spectral analysis for JWST Cycle 4 target',
    longGoal: 'Design orbital lunar-shielded radio telescope array',
    interests: [
      { name: 'Stellar Physics', icon: '✨' },
      { name: 'Radio Astronomy', icon: '📡' },
      { name: 'Cello & Acoustics', icon: '🎻' },
      { name: 'CUDA Kernel Tuning', icon: '⚡' },
      { name: 'Mountain Hiking', icon: '🏔️' },
      { name: 'Orbital Mechanics', icon: '🪐' },
    ],
    badges: [
      { name: 'Starlight Sentinel', icon: '⭐', color: '#f59e0b', unlocked: true, desc: '60-day unbroken research cycle' },
      { name: 'Plasma Master', icon: '🔥', color: '#ef4444', unlocked: true, desc: '1,000 GPU simulation runs validated' },
      { name: 'Deep Space Mapper', icon: '🔭', color: '#3b82f6', unlocked: true, desc: 'Processed 50 gigabytes of spectral data' },
      { name: 'Accretion Expert', icon: '🌀', color: '#8b5cf6', unlocked: true, desc: 'Validated non-linear disk equations' },
      { name: 'Horizon Scholar', icon: '🛡️', color: '#10b981', unlocked: true, desc: 'Published peer-reviewed workshop preprint' },
    ],
    subjects: [
      { name: 'Magnetohydrodynamics & Plasma', progress: 96, color: '#e07a5f' },
      { name: 'General Relativity & Curved Spacetime', progress: 89, color: '#6366f1' },
      { name: 'High Performance GPU Computing', progress: 91, color: '#2d5f47' },
      { name: 'Observational Spectroscopy', progress: 85, color: '#d97706' },
      { name: 'Stellar Evolution & Nucleosynthesis', progress: 93, color: '#0ea5e9' },
    ],
    activities: [
      { text: 'Rendered volumetric turbulence field of binary star accretion stream', time: '25m ago', iconColor: '#e07a5f' },
      { text: 'Ran CUDA kernel benchmarks for 200,000 particle N-body integrator', time: '3h ago', iconColor: '#2d5f47' },
      { text: 'Completed peer review on Gravitational Microlensing Light Curves', time: 'Yesterday', iconColor: '#6366f1' },
      { text: 'Achieved 100% on Advanced General Relativity mid-term diagnostic', time: '3 days ago', iconColor: '#f59e0b' },
      { text: 'Awarded "Starlight Sentinel" unbroken streak badge', time: '4 days ago', iconColor: '#10b981' },
    ],
  },
  {
    fullName: 'Kaelen Thorne',
    role: 'Bio-Computational Engineering Fellow',
    field: 'Synthetic Genomics & Protein Structural Informatics',
    academicLevel: 'Honors Bio-Informatics Senior (Year 4)',
    studentId: 'HLX-77341-BQ',
    email: 'kaelen.thorne@helix-foundry.ac.uk',
    advisor: 'Dr. Maeve Sinclair',
    lab: 'Generative Biomolecular Design Suite 9',
    location: 'Bio-Innovation Nexus, Suite 400',
    memberSince: '19 Nov 2023',
    bio: 'Designing de novo synthetic enzymes, exploring diffusion priors for RNA folding, and simulating microfluidic organoid arrays. Rock climber and sourdough fermentation enthusiast.',
    tags: ['Protein Folding', 'Diffusion Priors', 'CRISPR Design', 'Microfluidics', 'Bioethics'],
    quote: 'Evolution gave us the alphabet; generative computation writes the poems.',
    streakDays: 52,
    streakStatus: 'Top 1% in Molecular Simulation pipeline usage',
    cgpa: '3.95 / 4.00',
    shortGoal: 'Validate 24 synthetic allosteric enzyme binding pockets in vitro',
    medGoal: 'Publish generative macrocyclic peptide screening pipeline',
    longGoal: 'Build self-assembling biomaterials for atmospheric carbon capture',
    interests: [
      { name: 'Generative Biology', icon: '🧬' },
      { name: 'Protein Folding', icon: '🔬' },
      { name: 'Bouldering', icon: '🧗' },
      { name: 'Microfluidics', icon: '💧' },
      { name: 'Enzyme Kinetics', icon: '⚗️' },
      { name: 'Permaculture Design', icon: '🌿' },
    ],
    badges: [
      { name: 'Helix Weaver', icon: '🧬', color: '#10b981', unlocked: true, desc: 'Modeled 500+ de novo peptide structures' },
      { name: 'Diffusion Prodigy', icon: '🔮', color: '#8b5cf6', unlocked: true, desc: 'Optimized 3D backbone generative models' },
      { name: 'Bio-Foundry Pioneer', icon: '🧪', color: '#3b82f6', unlocked: true, desc: 'Synthesized 5 enzymatic proof-of-concepts' },
      { name: '50-Day Marathon', icon: '🏃', color: '#f59e0b', unlocked: true, desc: '50 continuous days of computational analysis' },
      { name: 'Enzyme Laureate', icon: '🛡️', color: '#ec4899', unlocked: true, desc: 'High-throughput affinity benchmark record' },
    ],
    subjects: [
      { name: 'Protein Folding & Structural Modeling', progress: 98, color: '#2d5f47' },
      { name: 'Synthetic Genomics & CRISPR Systems', progress: 91, color: '#0ea5e9' },
      { name: 'Statistical Thermodynamics of Macromolecules', progress: 82, color: '#e07a5f' },
      { name: 'Deep Learning on Molecular Graphs', progress: 94, color: '#6366f1' },
      { name: 'Microfluidics & High-Throughput Screening', progress: 87, color: '#d97706' },
    ],
    activities: [
      { text: 'Completed alpha-helical design loop on synthetic ligase scaffold', time: '12m ago', iconColor: '#10b981' },
      { text: 'Executed molecular dynamics simulation for 500 nanoseconds', time: '1h ago', iconColor: '#3b82f6' },
      { text: 'Presented seminar on Graph Transformers for Ligand Binding', time: 'Yesterday', iconColor: '#8b5cf6' },
      { text: 'Benchmarked diffusion model against PDB test benchmark suite', time: '2 days ago', iconColor: '#e07a5f' },
      { text: 'Received "Helix Weaver" distinction from research faculty', time: '4 days ago', iconColor: '#f59e0b' },
    ],
  },
];

export default function Profile() {
  const [personaIndex, setPersonaIndex] = useState(0);
  const [isEditing, setIsEditing] = useState(false);

  // Active arbitrary persona
  const currentPersona = ARBITRARY_PERSONAS[personaIndex];

  // Editable state
  const [customData, setCustomData] = useState({
    fullName: currentPersona.fullName,
    role: currentPersona.role,
    field: currentPersona.field,
    bio: currentPersona.bio,
    quote: currentPersona.quote,
    email: currentPersona.email,
    location: currentPersona.location,
  });

  const handleRandomize = () => {
    const nextIndex = (personaIndex + 1) % ARBITRARY_PERSONAS.length;
    setPersonaIndex(nextIndex);
    const p = ARBITRARY_PERSONAS[nextIndex];
    setCustomData({
      fullName: p.fullName,
      role: p.role,
      field: p.field,
      bio: p.bio,
      quote: p.quote,
      email: p.email,
      location: p.location,
    });
  };

  const handleSaveEdit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditing(false);
  };

  return (
    <div>
      <HeroHeader
        tag="MY PROFILE · ARBITRARY MOCK PERSONA"
        title={<>Academic Dossier. <span className="accent">Fictional & Arbitrary.</span></>}
        subtitle="Explore rich, simulated student researcher profiles. All metrics, affiliations, and goals are completely fabricated for demonstration."
        image="/assets/header_profile.png"
      />

      {/* Control Bar: Switch Persona / Edit / Indicator */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6 p-4 rounded-xl bg-white border border-[var(--color-card-border)] shadow-sm">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-semibold text-[var(--color-text-dark)]">
            Arbitrary Mock Persona: <span className="text-[var(--color-green-accent)] font-bold">{customData.fullName}</span> ({currentPersona.field})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleRandomize}
            className="px-3.5 py-1.5 bg-[#f0f7f3] hover:bg-[#e2f0e7] text-[var(--color-green-accent)] border border-[var(--color-green-border)] rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5"
            title="Cycle through arbitrary personas"
          >
            <span>🎲</span>
            <span>Switch Arbitrary Persona ({personaIndex + 1}/{ARBITRARY_PERSONAS.length})</span>
          </button>
          <button
            onClick={() => setIsEditing(true)}
            className="px-3.5 py-1.5 bg-white hover:bg-gray-50 border border-[var(--color-card-border)] rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5"
          >
            <span>✏️</span>
            <span>Edit Details</span>
          </button>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {isEditing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 w-full max-w-lg shadow-xl border border-[var(--color-card-border)] max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold">Edit Arbitrary Persona Details</h3>
              <button
                onClick={() => setIsEditing(false)}
                className="text-gray-400 hover:text-gray-600 text-lg leading-none"
              >
                ✕
              </button>
            </div>
            <form onSubmit={handleSaveEdit} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold mb-1">Full Name (Made-up)</label>
                <input
                  type="text"
                  value={customData.fullName}
                  onChange={(e) => setCustomData({ ...customData, fullName: e.target.value })}
                  className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold mb-1">Academic Role</label>
                  <input
                    type="text"
                    value={customData.role}
                    onChange={(e) => setCustomData({ ...customData, role: e.target.value })}
                    className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                  />
                </div>
                <div>
                  <label className="block font-semibold mb-1">Field / Department</label>
                  <input
                    type="text"
                    value={customData.field}
                    onChange={(e) => setCustomData({ ...customData, field: e.target.value })}
                    className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold mb-1">Fictional Email</label>
                  <input
                    type="text"
                    value={customData.email}
                    onChange={(e) => setCustomData({ ...customData, email: e.target.value })}
                    className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                  />
                </div>
                <div>
                  <label className="block font-semibold mb-1">Campus / Location</label>
                  <input
                    type="text"
                    value={customData.location}
                    onChange={(e) => setCustomData({ ...customData, location: e.target.value })}
                    className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                  />
                </div>
              </div>
              <div>
                <label className="block font-semibold mb-1">Personal Research Bio</label>
                <textarea
                  rows={3}
                  value={customData.bio}
                  onChange={(e) => setCustomData({ ...customData, bio: e.target.value })}
                  className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                />
              </div>
              <div>
                <label className="block font-semibold mb-1">Favorite Scholar Quote</label>
                <input
                  type="text"
                  value={customData.quote}
                  onChange={(e) => setCustomData({ ...customData, quote: e.target.value })}
                  className="w-full p-2 border border-[var(--color-card-border)] rounded-lg focus:outline-none focus:border-[var(--color-green-accent)]"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg font-medium hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-[var(--color-green-accent)] text-white font-semibold rounded-lg hover:opacity-90"
                >
                  Save Profile Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Profile Header Card */}
      <div className="card mb-6 flex flex-col sm:flex-row gap-6">
        {/* Avatar */}
        <div className="relative flex-shrink-0">
          <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-full border-4 border-white shadow-md bg-gradient-to-tr from-[#1d3528] to-[#3d7a5c] flex items-center justify-center text-white text-3xl font-extrabold select-none">
            {customData.fullName.split(' ').map(n => n[0]).join('')}
          </div>
          <button
            onClick={handleRandomize}
            title="Randomize Persona"
            className="absolute bottom-1 right-1 w-7 h-7 rounded-full bg-white shadow flex items-center justify-center text-xs border border-[var(--color-card-border)] hover:bg-gray-100 transition-colors"
          >
            🎲
          </button>
        </div>

        {/* Info */}
        <div className="flex-1">
          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold">{customData.fullName}</h2>
                <span className="text-[0.65rem] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold">
                  SIMULATED
                </span>
              </div>
              <div className="text-sm text-[var(--color-text-muted)]">{customData.role}</div>
              <div className="text-xs text-[var(--color-text-muted)] mt-0.5 font-medium">{customData.field}</div>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-[#eef8f2] text-[var(--color-green-accent)] border border-[var(--color-green-border)] rounded-full text-xs font-bold">
                CGPA: {currentPersona.cgpa}
              </span>
              <button
                onClick={() => setIsEditing(true)}
                className="px-3.5 py-1.5 border border-[var(--color-card-border)] rounded-lg text-xs font-medium flex items-center gap-1.5 hover:border-[var(--color-green-accent)] transition-colors"
              >
                ✏️ Edit
              </button>
            </div>
          </div>
          <p className="text-sm text-[var(--color-text-body)] mt-3 mb-3 leading-relaxed">{customData.bio}</p>
          <div className="flex flex-wrap gap-2">
            {currentPersona.tags.map(t => (
              <span key={t} className="px-3 py-1 bg-[#f5f4ef] border border-[var(--color-card-border)] rounded-full text-xs font-medium text-[var(--color-text-body)]">
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_1fr_280px] gap-6">
        {/* Left Column: Personal Info & Badges */}
        <div>
          {/* Personal Info Card */}
          <div className="card mb-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <span className="text-base">👤</span>
                <div>
                  <h3 className="font-bold text-sm">Academic Dossier</h3>
                  <p className="text-xs text-[var(--color-text-muted)]">Simulated institutional profile records.</p>
                </div>
              </div>
              <button onClick={() => setIsEditing(true)} className="text-xs text-[var(--color-green-accent)] font-semibold hover:underline">
                Edit
              </button>
            </div>
            {[
              { icon: '🆔', label: 'Student ID', value: currentPersona.studentId },
              { icon: '📧', label: 'Official Email', value: customData.email },
              { icon: '🎓', label: 'Degree Level', value: currentPersona.academicLevel },
              { icon: '🏛️', label: 'Faculty / Field', value: customData.field },
              { icon: '🔬', label: 'Research Lab', value: currentPersona.lab },
              { icon: '👩‍🏫', label: 'Faculty Mentor', value: currentPersona.advisor },
              { icon: '📍', label: 'Campus Sector', value: customData.location },
              { icon: '📅', label: 'Matriculation', value: currentPersona.memberSince },
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-3 py-2" style={{ borderBottom: i < 7 ? '1px solid #f1efe9' : 'none' }}>
                <span className="text-sm flex-shrink-0">{item.icon}</span>
                <span className="text-xs text-[var(--color-text-muted)] w-28 flex-shrink-0">{item.label}</span>
                <span className="text-xs font-medium text-[var(--color-text-dark)] truncate">{item.value}</span>
              </div>
            ))}
          </div>

          {/* Achievements & Badges */}
          <SectionHeader icon="🏆" title="Honors & Achievements" action="View All (5)" />
          <p className="text-xs text-[var(--color-text-muted)] mb-3">Simulated research milestones and accolades.</p>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-6">
            {currentPersona.badges.map((b, i) => (
              <div
                key={i}
                className="flex flex-col items-center text-center gap-1.5 p-3 rounded-xl border bg-white border-[var(--color-card-border)] hover:border-gray-300 transition-all shadow-xs"
              >
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center text-lg shadow-inner"
                  style={{ background: `${b.color}15`, border: `1px solid ${b.color}30` }}
                >
                  {b.icon}
                </div>
                <span className="text-xs font-bold leading-tight">{b.name}</span>
                <span className="text-[0.65rem] text-[var(--color-text-muted)] line-clamp-2 leading-tight">{b.desc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Middle Column: Arbitrary Goals & Subject Overview */}
        <div>
          {/* Goals Card */}
          <div className="card mb-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <span className="text-base">🎯</span>
                <div>
                  <h3 className="font-bold text-sm">Academic Research Goals</h3>
                  <p className="text-xs text-[var(--color-text-muted)]">Fabricated trajectory milestones.</p>
                </div>
              </div>
              <span className="text-[0.65rem] text-[var(--color-green-accent)] font-semibold px-2 py-0.5 bg-green-50 rounded">
                Active
              </span>
            </div>
            {[
              { color: '#10b981', label: 'Short Term (Next 30 Days)', value: currentPersona.shortGoal },
              { color: '#f59e0b', label: 'Medium Term (This Semester)', value: currentPersona.medGoal },
              { color: '#8b5cf6', label: 'Long Term (Career Horizon)', value: currentPersona.longGoal },
            ].map((g, i) => (
              <div key={i} className="flex items-start gap-3 py-3" style={{ borderBottom: i < 2 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-2.5 h-2.5 rounded-full mt-1 flex-shrink-0" style={{ background: g.color }} />
                <div>
                  <div className="text-xs font-bold text-[var(--color-text-dark)]">{g.label}</div>
                  <div className="text-xs text-[var(--color-text-body)] mt-0.5 leading-relaxed">{g.value}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Subjects Overview */}
          <SectionHeader icon="📊" title="Course Mastery Overview" action="All Syllabi" />
          <p className="text-xs text-[var(--color-text-muted)] mb-3">Simulated course progress metrics.</p>
          <div className="card mb-6 space-y-3">
            {currentPersona.subjects.map((s, i) => (
              <div key={i} className="flex items-center gap-3">
                <div className="w-6 h-6 rounded flex items-center justify-center text-xs flex-shrink-0" style={{ background: `${s.color}15` }}>
                  📘
                </div>
                <span className="text-xs font-medium flex-1 truncate">{s.name}</span>
                <div className="w-24">
                  <ProgressBar value={s.progress} color={s.color} height={5} />
                </div>
                <span className="text-xs font-bold w-9 text-right">{s.progress}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Quote, Streak, Interests, Activities */}
        <div>
          {/* Quote Card */}
          <div className="card mb-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1.5">
                <span className="text-base text-[var(--color-green-accent)]">❝</span>
                <span className="text-xs font-bold">Guiding Motto</span>
              </div>
              <button onClick={() => setIsEditing(true)} className="text-[0.65rem] text-[var(--color-green-accent)] font-semibold hover:underline">
                Edit
              </button>
            </div>
            <p className="text-xs font-medium italic text-[var(--color-text-dark)] leading-relaxed">
              "{customData.quote}"
            </p>
          </div>

          {/* Study Streak Card */}
          <div className="card mb-6 flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-2xl flex-shrink-0">
              🔥
            </div>
            <div>
              <div className="text-xs font-semibold text-[var(--color-text-muted)]">Research Streak</div>
              <div className="text-xl font-extrabold text-[var(--color-text-dark)]">{currentPersona.streakDays} days</div>
              <div className="text-[0.65rem] text-emerald-600 font-medium">{currentPersona.streakStatus}</div>
            </div>
          </div>

          {/* Interests Card */}
          <SectionHeader title="Specialties & Hobbies" action="Manage" />
          <p className="text-xs text-[var(--color-text-muted)] mb-3">Interdisciplinary focus areas.</p>
          <div className="grid grid-cols-2 gap-2 mb-6">
            {currentPersona.interests.map((interest, i) => (
              <div key={i} className="card flex items-center gap-2 py-2 px-2.5 shadow-none border border-[var(--color-card-border)]">
                <span className="text-sm">{interest.icon}</span>
                <span className="text-xs font-medium truncate">{interest.name}</span>
              </div>
            ))}
          </div>

          {/* Recent Activity Card */}
          <SectionHeader icon="🕐" title="Simulated Log" action="Archive" />
          <div className="card">
            {currentPersona.activities.map((a, i) => (
              <div key={i} className="flex items-center gap-2.5 py-2" style={{ borderBottom: i < currentPersona.activities.length - 1 ? '1px solid #f1efe9' : 'none' }}>
                <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: a.iconColor }} />
                <span className="text-[0.72rem] text-[var(--color-text-body)] flex-1 leading-snug">{a.text}</span>
                <span className="text-[0.6rem] text-[var(--color-text-muted)] whitespace-nowrap">{a.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <MotivationalBanner
        tag="ACADASSIST · SIMULATED RESEARCH PORTAL"
        title="Curiosity fuels understanding. Rigor turns it into mastery."
        subtitle="Every metric and record here is designed to inspire your own personal study trajectory."
        actionLabel="Jump to Study Planner"
      />
    </div>
  );
}
