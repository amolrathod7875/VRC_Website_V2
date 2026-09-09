"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { IconArrowRight } from "@/components/Icon";

type IconComp = React.FC<{ className?: string }>;

function useReveal() {
  const ref = useRef<HTMLDivElement>(null);
  const [v, setV] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const o = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setV(true);
          o.disconnect();
        }
      },
      { threshold: 0.12 }
    );
    o.observe(el);
    return () => o.disconnect();
  }, []);
  return [ref, v] as const;
}

function Reveal({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  const [ref, v] = useReveal();
  return (
    <div ref={ref} className={`transition-all duration-700 ease-out ${v ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`} style={{ transitionDelay: `${delay}ms` }}>
      {children}
    </div>
  );
}

function Eyebrow({ children }: { children: React.ReactNode }) {
  return <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#1678C8]">{children}</p>;
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return <h2 className="text-[clamp(2rem,3vw,3rem)] font-semibold leading-[1.05] text-[#082B4C]">{children}</h2>;
}

export function ApplicationEditorialHero({
  title, subtitle, icon: Icon, industry, application, requirements, process,
}: {
  title: string;
  subtitle: string;
  icon: IconComp;
  industry: string;
  application: string;
  requirements: string;
  process: string;
}) {
  const [ref, v] = useReveal();
  return (
    <section ref={ref} className="bg-[#F4F7FA] py-20 sm:py-28">
      <div className="mx-auto w-full max-w-[1440px] px-6 sm:px-10 lg:px-16">
        <div className="grid items-start gap-10 lg:grid-cols-[1fr_380px] lg:gap-16">
          <div className={`transition-all duration-700 ease-out ${v ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`}>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Application</p>
            <h1 className="mt-4 text-[clamp(3rem,5vw,5.5rem)] font-semibold leading-[0.98] text-[#082B4C]">{title}</h1>
            <p className="mt-6 max-w-[620px] text-base leading-7 text-slate-600">{subtitle}</p>
          </div>
          <div className={`transition-all duration-700 ease-out ${v ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`} style={{ transitionDelay: "120ms" }}>
            <div className="rounded-xl border border-slate-200 bg-white p-7">
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-md bg-[#E8F4FB] text-[#1678C8]">
                  <Icon className="h-7 w-7" />
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#1678C8]">Application</p>
                  <p className="mt-1 text-lg font-semibold text-[#082B4C]">{title}</p>
                </div>
              </div>
              <div className="mt-5 space-y-0">
                {[
                  { k: "INDUSTRY", v: industry },
                  { k: "APPLICATION", v: application },
                  { k: "PRIMARY REQUIREMENTS", v: requirements },
                  { k: "PROCESS ENVIRONMENT", v: process },
                ].map((row, i) => (
                  <div key={row.k} className={i > 0 ? "border-t border-slate-100 pt-4" : ""}>
                    <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#1678C8]">{row.k}</p>
                    <p className="mt-1 text-sm font-medium text-[#082B4C]">{row.v}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export function ApplicationEditorialImage({ image }: { image?: string }) {
  return (
    <section className="bg-white">
      <div className="mx-auto w-full max-w-[1440px] px-6 sm:px-10 lg:px-16">
        <div className="relative overflow-hidden rounded-[12px] bg-[#E9EEF3] aspect-[16/7]">
          {image ? (
            <img src={image} alt="Application" className="h-full w-full object-cover object-center" loading="lazy" />
          ) : (
            <div className="flex h-full w-full items-center justify-center">
              <p className="text-sm font-medium tracking-wide text-slate-400">AUTOMOTIVE APPLICATION IMAGE</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export function ApplicationEditorialBody({
  overview, requirements, objectives, support,
}: {
  overview: string;
  requirements: { title: string; text: string }[];
  objectives: string[];
  support: { title: string; text: string }[];
}) {
  return (
    <section className="bg-white py-20 sm:py-28">
      <div className="mx-auto w-full max-w-[1440px] px-6 sm:px-10 lg:px-16">
        <div className="grid gap-12 lg:grid-cols-[220px_1fr] lg:gap-16">
          <div className="hidden lg:block">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#1678C8]">Application details</p>
          </div>
          <div className="max-w-[820px] space-y-20">
            <Reveal>
              <Eyebrow>Overview</Eyebrow>
              <SectionHeading>Overview</SectionHeading>
              <p className="mt-5 text-base leading-7 text-slate-600">{overview}</p>
            </Reveal>

            <Reveal delay={80}>
              <Eyebrow>Application requirements</Eyebrow>
              <SectionHeading>Application requirements</SectionHeading>
              <p className="mt-5 text-base leading-7 text-slate-600">
                Every application environment imposes its own demands on a coating system. Understanding these
                requirements is the starting point for specifying the right solution.
              </p>
              <div className="mt-8 space-y-5">
                {requirements.map((r, i) => (
                  <div key={i} className="border-t border-slate-100 pt-5">
                    <p className="text-sm font-semibold text-[#082B4C]">{r.title}</p>
                    <p className="mt-1.5 text-sm leading-6 text-slate-600">{r.text}</p>
                  </div>
                ))}
              </div>
            </Reveal>

            <Reveal delay={160}>
              <Eyebrow>Key coating objectives</Eyebrow>
              <SectionHeading>Key coating objectives</SectionHeading>
              <ul className="mt-6 space-y-3">
                {objectives.map((o, i) => (
                  <li key={i} className="flex items-start gap-3 text-base leading-7 text-slate-600">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1678C8]" />
                    <span>{o}</span>
                  </li>
                ))}
              </ul>
            </Reveal>

            <Reveal delay={240}>
              <Eyebrow>How VR Coatings supports</Eyebrow>
              <SectionHeading>How VR Coatings supports the process</SectionHeading>
              <p className="mt-5 text-base leading-7 text-slate-600">
                We pair formulation science with application support so films perform in the field — not only in the lab.
              </p>
              <div className="mt-8 space-y-5">
                {support.map((s, i) => (
                  <div key={i} className="border-t border-slate-100 pt-5">
                    <p className="text-sm font-semibold text-[#082B4C]">{s.title}</p>
                    <p className="mt-1.5 text-sm leading-6 text-slate-600">{s.text}</p>
                  </div>
                ))}
              </div>
            </Reveal>

            <Reveal delay={320}>
              <Eyebrow>Relevant products</Eyebrow>
              <SectionHeading>Coating systems for automotive applications</SectionHeading>
              <p className="mt-5 text-base leading-7 text-slate-600">
                Explore our range of engineered coating systems developed for performance, protection and long-term
                reliability across industrial applications.
              </p>
              <div className="mt-7">
                <Link href="/products" className="inline-flex items-center gap-2 text-sm font-semibold text-[#1678C8] hover:text-[#0B5C97]">
                  Explore Our Products
                  <IconArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}