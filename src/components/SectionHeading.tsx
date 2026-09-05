import type { ReactNode } from "react";

type EyebrowProps = {
  children: ReactNode;
  tone?: "navy" | "blue" | "white";
};

export function Eyebrow({ children, tone = "blue" }: EyebrowProps) {
  const colors =
    tone === "white"
      ? "text-brand-100"
      : tone === "navy"
        ? "text-brand-800"
        : "text-brand-700";
  return (
    <p className={`text-xs font-semibold uppercase tracking-[0.28em] ${colors}`}>{children}</p>
  );
}

type SectionHeadingProps = {
  children: ReactNode;
  tone?: "dark" | "white";
  className?: string;
};

export function SectionHeading({ children, tone = "dark", className = "" }: SectionHeadingProps) {
  const color = tone === "white" ? "text-white" : "text-brand-950";
  return (
    <h2 className={`mt-3 text-3xl font-semibold leading-tight sm:text-4xl ${color} ${className}`}>
      {children}
    </h2>
  );
}
