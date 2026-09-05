type IconProps = { className?: string };

const base = "h-full w-full";

export function IconEngineered({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M8 30h6l3-6h14l3 6h6v6H8z" strokeLinejoin="round" />
      <circle cx="16" cy="38" r="3" />
      <circle cx="32" cy="38" r="3" />
      <path d="M22 18l4-6 4 6" strokeLinejoin="round" />
    </svg>
  );
}

export function IconQuality({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 6l14 5v11c0 9-6 16-14 20-8-4-14-11-14-20V11z" strokeLinejoin="round" />
      <path d="M17 24l5 5 9-11" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  );
}

export function IconApplication({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M14 6h12v22a6 6 0 1 1-12 0z" strokeLinejoin="round" />
      <path d="M26 14h6a4 4 0 0 1 4 4v6" />
      <path d="M32 30l8 8" strokeLinecap="round" />
    </svg>
  );
}

export function IconProtection({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 6c8 4 14 6 14 14 0 9-6 18-14 22-8-4-14-13-14-22 0-8 6-10 14-14z" strokeLinejoin="round" />
      <path d="M16 24h16M24 16v16" />
    </svg>
  );
}

export function IconCustom({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 8a16 16 0 1 0 16 16" strokeLinecap="round" />
      <path d="M30 4v8h-8" strokeLinejoin="round" />
      <circle cx="24" cy="24" r="6" />
    </svg>
  );
}

export function IconCorrosion({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 36c6-2 8-6 10-12 2 6 6 10 12 12-4 2-6 6-10 6-6 0-8-4-12-6z" strokeLinejoin="round" />
      <path d="M28 14l4-8 4 8" strokeLinejoin="round" />
    </svg>
  );
}

export function IconDurability({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 6l4 12 12 2-9 9 2 13-9-5-9 5 2-13-9-9 12-2z" strokeLinejoin="round" />
    </svg>
  );
}

export function IconChemical({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M18 6h12v10l8 22a4 4 0 0 1-4 5H14a4 4 0 0 1-4-5l8-22z" strokeLinejoin="round" />
      <path d="M14 24h20" />
    </svg>
  );
}

export function IconTemperature({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M22 6a4 4 0 1 1 8 0v22a8 8 0 1 1-8 0z" strokeLinejoin="round" />
      <circle cx="26" cy="36" r="3" />
      <path d="M26 12v18" />
    </svg>
  );
}

export function IconPrecision({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <circle cx="24" cy="24" r="16" />
      <circle cx="24" cy="24" r="10" />
      <circle cx="24" cy="24" r="3" />
    </svg>
  );
}

export function IconCert({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M10 6h28v26l-14 8L10 32z" strokeLinejoin="round" />
      <path d="M18 18h12M18 24h8" strokeLinecap="round" />
    </svg>
  );
}

export function IconFactory({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 40V20l10 6V20l10 6V14h16v26z" strokeLinejoin="round" />
      <path d="M14 40v-6M22 40v-6M30 40v-6M38 40v-6" />
    </svg>
  );
}

export function IconArrowRight({ className = "h-4 w-4" }: IconProps) {
  return (
    <svg viewBox="0 0 20 20" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
