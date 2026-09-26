type PlaceholderProps = {
  label: string;
  className?: string;
  ratio?: string;
};

export function Placeholder({ label, className = "", ratio }: PlaceholderProps) {
  return (
    <div
      className={`placeholder-block flex items-center justify-center text-center ${className}`}
      style={ratio ? { aspectRatio: ratio } : undefined}
      role="img"
      aria-label={label}
    >
      <span className="relative z-10 px-3 text-xs font-medium uppercase tracking-wide text-slate-600 sm:text-sm">
        {label}
      </span>
    </div>
  );
}
