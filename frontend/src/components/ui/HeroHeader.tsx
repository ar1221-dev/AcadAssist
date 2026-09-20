import type { ReactNode } from 'react';

interface HeroHeaderProps {
  tag: string;
  title: ReactNode;
  subtitle: string;
  image?: string;
  imageAlt?: string;
}

export default function HeroHeader({ tag, title, subtitle, image, imageAlt = '' }: HeroHeaderProps) {
  return (
    <div className="hero-header">
      <div className="hero-text">
        <div className="hero-tag">{tag}</div>
        <h1 className="hero-title">{title}</h1>
        <p className="hero-subtitle">{subtitle}</p>
      </div>
      <div className="hero-image">
        {image ? (
          <img src={image} alt={imageAlt} />
        ) : (
          <div style={{ background: 'linear-gradient(120deg, #e8e3d9 0%, #c9c2b4 100%)', width: '100%', height: '100%' }} />
        )}
      </div>
    </div>
  );
}
