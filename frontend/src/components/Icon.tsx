type IconProps = { className?: string };
export type { IconProps };

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

export function IconCar({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M8 30l3-10a4 4 0 0 1 4-3h18a4 4 0 0 1 4 3l3 10" strokeLinejoin="round" />
      <path d="M6 30h36v8H6z" strokeLinejoin="round" />
      <circle cx="14" cy="38" r="3" />
      <circle cx="34" cy="38" r="3" />
      <path d="M11 30v-3M37 30v-3" strokeLinecap="round" />
    </svg>
  );
}

export function IconShip({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 30h36l-4 10H10z" strokeLinejoin="round" />
      <path d="M24 4v26" strokeLinecap="round" />
      <path d="M24 8l14 6H24" strokeLinejoin="round" />
      <path d="M24 16l-10 4h10" strokeLinejoin="round" />
      <path d="M2 40c4 1 6 3 10 3s6-2 10-2 6 2 10 2 6-2 10-2 6 2 4-1" strokeLinecap="round" />
    </svg>
  );
}

export function IconShield({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 4l16 6v12c0 10-7 18-16 22-9-4-16-12-16-22V10z" strokeLinejoin="round" />
      <path d="M16 24h16M24 16v16" />
    </svg>
  );
}

export function IconPlane({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 28l36-14-6 22-10-2-4 8-3-1 1-9-10-2z" strokeLinejoin="round" />
      <path d="M28 20l4 6" strokeLinecap="round" />
    </svg>
  );
}

export function IconTrain({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="10" y="6" width="28" height="28" rx="6" />
      <path d="M10 22h28" />
      <circle cx="16" cy="40" r="3" />
      <circle cx="32" cy="40" r="3" />
      <path d="M6 44h36" strokeLinecap="round" />
      <circle cx="16" cy="14" r="1.5" />
      <circle cx="32" cy="14" r="1.5" />
    </svg>
  );
}

export function IconFuel({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="10" y="8" width="20" height="32" rx="3" />
      <path d="M10 18h20" />
      <path d="M30 16l4 3v18a3 3 0 0 1-3 3" strokeLinejoin="round" />
      <path d="M30 26h4" />
    </svg>
  );
}

export function IconConstruction({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 4l20 12v8L24 36 4 24v-8z" strokeLinejoin="round" />
      <path d="M4 24l20 12 20-12" />
      <path d="M4 32l20 12 20-12" />
      <path d="M24 16l8 4v6l-8 4-8-4v-6z" strokeLinejoin="round" />
    </svg>
  );
}

export function IconTree({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 4l10 14h-5l8 12h-6l8 12H9l8-12h-6l8-12h-5z" strokeLinejoin="round" />
      <path d="M24 42v-6" strokeLinecap="round" />
    </svg>
  );
}

export function IconPackage({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 4l18 9v22l-18 9L6 35V13z" strokeLinejoin="round" />
      <path d="M6 13l18 9 18-9" />
      <path d="M24 22v22" />
      <path d="M14 8l20 10" />
    </svg>
  );
}

export function IconPrinter({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="10" y="6" width="28" height="10" />
      <rect x="6" y="16" width="36" height="20" rx="2" />
      <rect x="14" y="32" width="20" height="10" />
      <circle cx="36" cy="24" r="1.5" />
      <path d="M10 16V10M38 16V10" />
    </svg>
  );
}

export function IconSprout({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M24 44V20" strokeLinecap="round" />
      <path d="M24 20c0-6 4-12 12-12-1 8-6 12-12 12z" strokeLinejoin="round" />
      <path d="M24 24c0-4-3-8-9-8 1 6 4 8 9 8z" strokeLinejoin="round" />
      <path d="M14 44h20" strokeLinecap="round" />
    </svg>
  );
}

export function IconPill({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="6" y="14" width="36" height="20" rx="10" transform="rotate(-30 24 24)" />
      <path d="M16 10l22 22" />
    </svg>
  );
}

export function IconCircuit({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="6" y="6" width="36" height="36" rx="3" />
      <rect x="14" y="14" width="20" height="20" rx="2" />
      <path d="M10 20h4M10 28h4M34 20h4M34 28h4M20 10v4M28 10v4M20 34v4M28 34v4" strokeLinecap="round" />
      <path d="M20 24h8M24 20v8" />
    </svg>
  );
}

export function IconWind({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 18h22a6 6 0 1 0-6-6" strokeLinecap="round" />
      <path d="M6 28h30a6 6 0 1 1-6 6" strokeLinecap="round" />
      <path d="M6 38h16" strokeLinecap="round" />
    </svg>
  );
}

export function IconBuilding({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M8 42V12l16-6 16 6v30" strokeLinejoin="round" />
      <path d="M4 42h40" strokeLinecap="round" />
      <rect x="14" y="18" width="6" height="6" />
      <rect x="28" y="18" width="6" height="6" />
      <rect x="14" y="28" width="6" height="6" />
      <rect x="28" y="28" width="6" height="6" />
    </svg>
  );
}

export function IconZap({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round">
      <path d="M26 4L10 26h12L20 44l16-22H24z" />
    </svg>
  );
}

export function IconSupport({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round">
      <circle cx="24" cy="24" r="16" />
      <path d="M24 8v8M24 32v8" strokeLinecap="round" />
      <path d="M8 24h8M32 24h8" strokeLinecap="round" />
      <path d="M14 14l6 6M28 28l6 6M14 34l6-6M28 14l6 6" strokeLinecap="round" />
    </svg>
  );
}

export function IconFlask({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round">
      <path d="M30 2V12c4-1 6-4 6-8H12c0 4 2 7 6 8V2h12z" strokeLinecap="round" />
      <path d="M32 4H16" />
      <path d="M30 24c3-2 5-5 5-9h-6" />
      <path d="M18 15a10 10 0 0 1 0 18c-4 2-6 6-6 10h-6v-2c0-4 2-8 6-10a10 10 0 0 1 6-18z" />
      <path d="M12 36c-2 0-4 2-4 4v4h20v-4c0-2-2-4-4-4h-2" />
    </svg>
  );
}

export function IconBadgeCheck({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round">
      <path d="M24 6L8 12v12c0 10 8 18 16 22s16-8 16-22V12z" />
      <circle cx="24" cy="24" r="9" />
      <path d="M20 28l3 3 5-5" strokeLinecap="round" />
    </svg>
  );
}

export function IconGlobe({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 40" className={className} fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round">
      <circle cx="24" cy="20" r="16" />
      <path d="M24 4c1.5 4-2 8-6 12s-12 10-16 14" />
      <path d="M24 4c1.5 4-2 8-6 12s-12 10-16 14" />
      <path d="M24 4c1.5 4-2 8-6 12s-12 10-16 14" />
      <path d="M24 42c5-2 9-7 11-14" />
      <path d="M24 42c5-2 9-7 11-14" />
      <path d="M8 20h32" strokeLinecap="round" />
      <path d="M24 4v36" strokeLinecap="round" />
    </svg>
  );
}
