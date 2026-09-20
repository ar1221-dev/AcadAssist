import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: ReactNode;
  className?: string;
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseClasses = 'btn inline-flex items-center justify-center font-semibold transition-all rounded-lg disabled:opacity-50 cursor-pointer';
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  }[size];
  const variantClasses = {
    primary: 'btn-primary bg-[#1d3528] text-white hover:bg-[#2d5f47]',
    secondary: 'btn-secondary bg-[#f5f4ef] text-[#111e17] hover:bg-[#eae8e2] border border-[#e5e3dc]',
    outline: 'border border-[var(--color-card-border)] bg-white text-[var(--color-text-dark)] hover:border-[var(--color-green-accent)] hover:text-[var(--color-green-accent)]',
    ghost: 'bg-transparent text-[var(--color-text-muted)] hover:text-[var(--color-text-dark)] hover:bg-black/5',
  }[variant];

  return (
    <button className={`${baseClasses} ${sizeClasses} ${variantClasses} ${className}`} {...props}>
      {children}
    </button>
  );
}
