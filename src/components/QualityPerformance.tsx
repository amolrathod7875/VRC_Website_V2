"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { capabilityHighlights, certifications } from "@/lib/data";
import { Eyebrow, SectionHeading } from "@/components/SectionHeading";
import { IconArrowRight, IconCert, IconCustom, IconFactory } from "@/components/Icon";

const STAGGER_BASE = 80;
const PARALLAX_MAX = 16;

export function QualityPerformance() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);
  const [bgOffset, setBgOffset] = useState(0);

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

    const handleScroll = () => {
      if (!section) return;
      const rect = section.getBoundingClientRect();
      const viewportH = window.innerHeight;
      if (rect.top < viewportH && rect.bottom > 0) {
        const progress = Math.max(0, Math.min(1, (viewportH - rect.top) / (viewportH + rect.height)));
        setBgOffset(Math.round(progress * PARALLAX_MAX));
      }
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative overflow-hidden bg-white min-h-screen flex items-center"
      style={{
        backgroundImage: "url('/Vids_imgs/Quality_Background.avif')",
        backgroundSize: "cover",
        backgroundPosition: `center ${bgOffset}px`,
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="relative z-10 mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:pb-12 w-full">
        <div className="grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-center relative">
          {/* Connection lines SVG - desktop only */}
          <svg
            aria-hidden
            className="hidden lg:block absolute pointer-events-none"
            style={{
              top: "38%",
              left: "calc(100% - 2px)",
              width: "48px",
              height: "24%",
              overflow: "visible",
            }}
          >
            <line
              x1="0"
              y1="0"
              x2="48"
              y2="0"
              className="quality-connection-line"
              style={{ stroke: "rgba(22,120,200,0.25)", strokeWidth: 1 }}
            />
            <circle cx="48" cy="0" r="3" fill="#1678C8" opacity="0.6" />
          </svg>
          <svg
            aria-hidden
            className="hidden lg:block absolute pointer-events-none"
            style={{
              top: "62%",
              left: "calc(100% - 2px)",
              width: "48px",
              height: "24%",
              overflow: "visible",
            }}
          >
            <line
              x1="0"
              y1="0"
              x2="48"
              y2="0"
              className="quality-connection-line"
              style={{ stroke: "rgba(22,120,200,0.25)", strokeWidth: 1 }}
            />
            <circle cx="48" cy="0" r="3" fill="#1678C8" opacity="0.6" />
          </svg>

          <div>
            <div
              className={`rounded-xl bg-white/80 p-6 ${visible ? "quality-animate-in" : "opacity-0"}`}
              style={visible ? { animationDelay: `${STAGGER_BASE}ms` } : undefined}
            >
              <Eyebrow>Quality & Performance</Eyebrow>
              <SectionHeading>Designed to perform where it matters.</SectionHeading>
              <p
                className={`mt-6 text-base leading-8 text-slate-600 ${visible ? "quality-animate-in" : "opacity-0"}`}
                style={visible ? { animationDelay: `${STAGGER_BASE * 2}ms` } : undefined}
              >
                Our quality programme is built around batch traceability, documented test methods, and
                continuous production oversight. Standards are referenced across our coating portfolio so
                customers can specify with confidence.
              </p>
            </div>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {certifications.map((cert, i) => (
                <div
                  key={cert.name}
                  className={`quality-card flex items-start gap-4 rounded-lg border border-slate-200 bg-surface px-5 py-4 ${visible ? "quality-animate-in" : "opacity-0"}`}
                  style={visible ? { animationDelay: `${STAGGER_BASE * (3 + i)}ms` } : undefined}
                >
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-white text-brand-800">
                    <IconCert className="h-6 w-6" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-brand-950">{cert.name}</p>
                    <p className="mt-1 text-xs leading-5 text-slate-500">{cert.scope}</p>
                  </div>
                </div>
              ))}
            </div>
            <Link
              href="/resources/certifications"
              className={`quality-cta mt-8 inline-flex items-center gap-2 text-sm font-semibold text-brand-700 hover:text-brand-800 ${visible ? "quality-animate-in" : "opacity-0"}`}
              style={visible ? { animationDelay: `${STAGGER_BASE * 7}ms` } : undefined}
            >
              View certifications
              <IconArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid gap-6 sm:grid-cols-2">
            <div
              className={`quality-card rounded-xl border border-slate-200 bg-surface p-6 ${visible ? "quality-float-a" : ""}`}
              style={visible ? { animationDelay: "0s" } : undefined}
            >
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-white text-brand-800 transition-transform duration-200 hover:-translate-y-0.5">
                <IconFactory className="h-6 w-6" />
              </div>
              <p className="text-sm font-semibold text-brand-950">Integrated Supply</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Head office, manufacturing unit and North America operations work as one supply network —
                from first trial through serial production.
              </p>
            </div>
            <div
              className={`quality-card rounded-xl border border-slate-200 bg-surface p-6 ${visible ? "quality-float-b" : ""}`}
              style={visible ? { animationDelay: "0s" } : undefined}
            >
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-white text-brand-800 transition-transform duration-200 hover:-translate-y-0.5">
                <IconCustom className="h-6 w-6" />
              </div>
              <p className="text-sm font-semibold text-brand-950">Custom Formulation</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Recipes developed around your substrate, climate and duty cycle — backed by lab trials
                and application replicates.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
