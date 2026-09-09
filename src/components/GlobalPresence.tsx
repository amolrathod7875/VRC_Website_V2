"use client";

import { useEffect, useRef, useState } from "react";
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

          <div className="relative mt-8 h-[260px] sm:h-[300px] lg:h-[340px] w-full">
            <svg
              viewBox="0 0 1000 420"
              className="h-full w-full"
              preserveAspectRatio="xMidYMid meet"
              aria-hidden="true"
            >
              <defs>
                <radialGradient id="pulse" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#1678C8" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#1678C8" stopOpacity="0" />
                </radialGradient>
              </defs>

              <g opacity="0.12">
                <path d="M160 180 h70 a30 30 0 0 1 0 60 h-70 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M180 170 h110 a40 40 0 0 1 0 80 h-110 a40 40 0 0 1 0 -80" fill="#082B4C" />
                <path d="M260 190 h90 a25 25 0 0 1 0 50 h-90 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M220 210 h130 a35 35 0 0 1 0 70 h-130 a35 35 0 0 1 0 -70" fill="#082B4C" />
                <path d="M300 175 h80 a30 30 0 0 1 0 60 h-80 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M340 200 h100 a25 25 0 0 1 0 50 h-100 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M420 185 h70 a30 30 0 0 1 0 60 h-70 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M450 170 h90 a40 40 0 0 1 0 80 h-90 a40 40 0 0 1 0 -80" fill="#082B4C" />
                <path d="M520 190 h110 a30 30 0 0 1 0 60 h-110 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M580 210 h80 a25 25 0 0 1 0 50 h-80 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M620 185 h90 a35 35 0 0 1 0 70 h-90 a35 35 0 0 1 0 -70" fill="#082B4C" />
                <path d="M680 200 h70 a30 30 0 0 1 0 60 h-70 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M720 175 h100 a40 40 0 0 1 0 80 h-100 a40 40 0 0 1 0 -80" fill="#082B4C" />
                <path d="M780 195 h80 a30 30 0 0 1 0 60 h-80 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M160 260 h60 a20 20 0 0 1 0 40 h-60 a20 20 0 0 1 0 -40" fill="#082B4C" />
                <path d="M200 270 h90 a25 25 0 0 1 0 50 h-90 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M260 280 h70 a20 20 0 0 1 0 40 h-70 a20 20 0 0 1 0 -40" fill="#082B4C" />
                <path d="M300 260 h100 a30 30 0 0 1 0 60 h-100 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M360 275 h80 a25 25 0 0 1 0 50 h-80 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M420 260 h90 a30 30 0 0 1 0 60 h-90 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M480 280 h70 a20 20 0 0 1 0 40 h-70 a20 20 0 0 1 0 -40" fill="#082B4C" />
                <path d="M520 265 h100 a25 25 0 0 1 0 50 h-100 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M580 285 h80 a20 20 0 0 1 0 40 h-80 a20 20 0 0 1 0 -40" fill="#082B4C" />
                <path d="M640 270 h90 a30 30 0 0 1 0 60 h-90 a30 30 0 0 1 0 -60" fill="#082B4C" />
                <path d="M700 290 h70 a20 20 0 0 1 0 40 h-70 a20 20 0 0 1 0 -40" fill="#082B4C" />
                <path d="M740 275 h80 a25 25 0 0 1 0 50 h-80 a25 25 0 0 1 0 -50" fill="#082B4C" />
                <path d="M800 260 h60 a20 20 0 0 1 0 40 h-60 a20 20 0 0 1 0 -40" fill="#082B4C" />
              </g>

              <line x1="240" y1="210" x2="720" y2="210" stroke="#082B4C" strokeWidth="1" opacity="0.18" strokeDasharray="6 6" />
              <line x1="240" y1="210" x2="820" y2="210" stroke="#082B4C" strokeWidth="1" opacity="0.18" strokeDasharray="6 6" />
              <line x1="240" y1="210" x2="480" y2="340" stroke="#082B4C" strokeWidth="1" opacity="0.18" strokeDasharray="6 6" />

              <circle cx="240" cy="210" r="28" fill="url(#pulse)">
                <animate attributeName="r" values="24;32;24" dur="3s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0.2;0.6" dur="3s" repeatCount="indefinite" />
              </circle>
              <circle cx="240" cy="210" r="6" fill="#1678C8" />
              <text x="240" y="250" textAnchor="middle" fill="#082B4C" fontSize="12" fontWeight="600">
                Pune / Chakan
              </text>

              <circle cx="720" cy="210" r="28" fill="url(#pulse)">
                <animate attributeName="r" values="24;32;24" dur="3s" begin="0.6s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0.2;0.6" dur="3s" begin="0.6s" repeatCount="indefinite" />
              </circle>
              <circle cx="720" cy="210" r="6" fill="#1678C8" />
              <text x="720" y="250" textAnchor="middle" fill="#082B4C" fontSize="12" fontWeight="600">
                Troy, MI
              </text>

              <circle cx="820" cy="210" r="24" fill="url(#pulse)">
                <animate attributeName="r" values="20;28;20" dur="3.2s" begin="1.2s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0.2;0.6" dur="3.2s" begin="1.2s" repeatCount="indefinite" />
              </circle>
              <circle cx="820" cy="210" r="5" fill="#1678C8" />
              <text x="820" y="250" textAnchor="middle" fill="#082B4C" fontSize="12" fontWeight="600">
                Europe
              </text>

              <circle cx="480" cy="340" r="24" fill="url(#pulse)">
                <animate attributeName="r" values="20;28;20" dur="2.8s" begin="1.8s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0.2;0.6" dur="2.8s" begin="1.8s" repeatCount="indefinite" />
              </circle>
              <circle cx="480" cy="340" r="5" fill="#1678C8" />
              <text x="480" y="380" textAnchor="middle" fill="#082B4C" fontSize="12" fontWeight="600">
                Middle East
              </text>
            </svg>
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
