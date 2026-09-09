"use client";

import { useEffect, useRef, useState } from "react";
import { GlobalFootprintMap } from "@/components/GlobalFootprintMap";
import { offices } from "@/lib/data";

const STAGGER_MS = 120;

const eyebrowMap: Record<string, string> = {
  "Head Office": "HEAD OFFICE",
  Factory: "MANUFACTURING",
  "North America": "NORTH AMERICA",
};

const regionMap: Record<string, string> = {
  "Head Office": "Pune, India",
  Factory: "Chakan, India",
  "North America": "Troy, MI, USA",
};

const rotations = ["-rotate-2", "rotate-2", "-rotate-2"];

export function GlobalPresence() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(section);

    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} id="global-presence" className="scroll-mt-24 bg-surface py-16 sm:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className={`mb-10 ${visible ? "quality-animate-in" : "opacity-0"}`}>
          <h2 className="text-3xl font-semibold text-brand-950 sm:text-4xl lg:text-5xl">
            Global presence
          </h2>
        </div>

        <div
          className={`relative overflow-hidden rounded-3xl bg-gradient-to-br from-surface-muted to-surface p-6 sm:p-8 lg:p-10 ${
            visible ? "quality-animate-in" : "opacity-0"
          }`}
          style={visible ? { animationDelay: "80ms" } : undefined}
        >
          <div className="relative z-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-2xl">
              <span className="text-xs font-semibold uppercase tracking-[0.18em] text-brand-700">
                GLOBAL FOOTPRINT
              </span>
              <h3 className="mt-2 text-2xl font-semibold text-brand-950 sm:text-3xl lg:text-4xl">
                Connected from India to North America
              </h3>
              <p className="mt-3 max-w-xl text-sm leading-7 text-slate-600 sm:text-base">
                VR Coatings supports industrial customers through its head office, manufacturing base, and North America presence.
              </p>
            </div>
          </div>

          <div className="relative mt-8 h-[260px] sm:h-[300px] lg:h-[360px] w-full">
            <GlobalFootprintMap visible={visible} />
          </div>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {offices.map((office, i) => {
            const eyebrow = eyebrowMap[office.title] || office.title.toUpperCase();
            const region = regionMap[office.title] || "";
            const rotation = rotations[i % rotations.length];

            return (
              <article
                key={office.title}
                className={`group relative min-h-[360px] md:min-h-[460px] overflow-hidden rounded-2xl bg-[#082B4C] px-6 py-7 text-white border border-white/10 transition-all duration-300 ease-out hover:-translate-y-1 hover:border-white/20 hover:shadow-xl ${
                  visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-5"
                }`}
                style={
                  visible
                    ? {
                        transitionDelay: `${i * STAGGER_MS}ms`,
                        animation: `quality-fade-up 0.65s ease-out ${i * STAGGER_MS}ms both`,
                      }
                    : undefined
                }
              >
                <div className="absolute inset-x-0 top-0 h-[3px] bg-[#1678C8] transition-all duration-300 group-hover:h-1" />

                <span className="text-xs font-semibold uppercase tracking-[0.18em] text-[#1678C8]">
                  {eyebrow}
                </span>

                <h3 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">{region}</h3>

                <div className="mt-6 flex-1" />

                <div className="relative flex items-end justify-between gap-4">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white/90">{office.lines[0]}</p>
                    {office.lines.slice(1).map((line) => (
                      <p key={line} className="mt-1 text-sm text-white/65">
                        {line}
                      </p>
                    ))}
                    <a
                      href={office.phoneHref}
                      className="mt-4 inline-block text-sm font-semibold text-[#1678C8] transition-colors duration-200 hover:text-white"
                    >
                      {office.phone}
                    </a>
                  </div>

                  <div
                    className={`hidden sm:block h-[130px] w-[170px] shrink-0 rounded-lg bg-white/10 transition-transform duration-300 ease-out group-hover:-translate-y-1 ${rotation}`}
                  >
                    <div className="flex h-full w-full items-center justify-center">
                      <span className="text-xs font-medium uppercase tracking-widest text-white/40">
                        Photo
                      </span>
                    </div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
