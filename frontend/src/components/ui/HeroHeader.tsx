import type { ReactNode } from 'react';
import { Sparkles } from 'lucide-react';

interface HeroHeaderProps { tag:string; title:ReactNode; subtitle:string; image?:string; imageAlt?:string; }

export default function HeroHeader({tag,title,subtitle}:HeroHeaderProps){
  return <div className="hero-header">
    <div className="hero-text"><div className="hero-tag">{tag}</div><h1 className="hero-title">{title}</h1><p className="hero-subtitle">{subtitle}</p></div>
    <div className="hero-image"><div className="hero-orb"><Sparkles size={30}/></div><div className="hero-grid-lines"/></div>
  </div>;
}
