"use client";

import { useEffect, useRef, useState } from "react";
import { companyStats } from "@/lib/data";

type Stat = (typeof companyStats)[number];

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

function parseTarget(value: string): { target: number; suffix: string } {
  const match = value.match(/^(\d+)(.*)$/);
  if (!match) return { target: 0, suffix: "" };
  return { target: Number(match[1]), suffix: match[2] };
}

export function StatCountUp() {
  // Detect reduced-motion preference lazily so we never call setState
  // synchronously inside an effect.
  const [reducedMotion] = useState(
    () =>
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );

  // When reduced motion is preferred, show final values immediately.
  const [started, setStarted] = useState(reducedMotion);
  const stripRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Reduced motion: values are already shown, nothing to observe.
    if (reducedMotion) return;

    const strip = stripRef.current;
    if (!strip) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (entry.isIntersecting) {
          setStarted(true);
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(strip);
    return () => observer.disconnect();
  }, [reducedMotion]);

  return (
    <div ref={stripRef} className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5 lg:gap-0 lg:border lg:border-slate-700/50">
        {companyStats.map((stat, index) => (
          <StatColumn
            key={stat.label}
            stat={stat}
            index={index}
            started={started}
            reducedMotion={reducedMotion}
          />
        ))}
      </div>
    </div>
  );
}

function StatColumn({
  stat,
  index,
  started,
  reducedMotion,
}: {
  stat: Stat;
  index: number;
  started: boolean;
  reducedMotion: boolean;
}) {
  // Initial display: final value when reduced motion is on, otherwise blank
  // so the count-up has somewhere to start from.
  const [display, setDisplay] = useState(
    reducedMotion ? stat.value : ""
  );
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (!started || reducedMotion) return;

    const { target, suffix } = parseTarget(stat.value);
    // The founded year animates from 1900 so the reveal is quick and
    // appropriate; all other values count up from 0.
    const from = stat.label === "FOUNDED" ? 1900 : 0;
    const delay = index * 100;
    const duration = 1500;
    const startTime = performance.now() + delay;

    const tick = (now: number) => {
      const elapsed = Math.max(0, now - startTime);
      const progress = Math.min(1, elapsed / duration);
      const current = Math.round(from + (target - from) * easeOutCubic(progress));
      setDisplay(`${current}${suffix}`);
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        setDisplay(`${target}${suffix}`);
      }
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [stat.label, stat.value, index, started, reducedMotion]);

  return (
    <div
      className={`flex flex-col items-center justify-center py-6 ${
        index < 4
          ? "border-b sm:border-b-0 sm:border-r sm:border-slate-700/50 lg:border-b-0"
          : ""
      }`}
    >
      <span
        className="text-3xl font-bold text-white sm:text-4xl"
        style={{
          fontVariantNumeric: "tabular-nums",
          fontFeatureSettings: '"tnum"',
          opacity: started ? 1 : 0,
          transform: started ? "none" : "translateY(8px)",
          transition: "opacity 400ms ease-out, transform 400ms ease-out",
        }}
      >
        {display}
      </span>
      <span className="mt-1 text-xs font-semibold uppercase tracking-[0.12em] text-slate-300">
        {stat.label}
      </span>
    </div>
  );
}