"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { applications } from "@/lib/data";
import { IconArrowRight } from "@/components/Icon";

type ApplicationsShowcaseVideoProps = {
  items?: typeof applications;
};

const ACTIVE_COLOR = "#1678C8";
const INACTIVE_COLOR = "#082B4C";
const TRANSITION_MS = 320;

function numberFor(index: number): string {
  return String(index + 1).padStart(2, "0");
}

export function ApplicationsShowcaseVideo({
  items = applications,
}: ApplicationsShowcaseVideoProps) {
  const [activeSlug, setActiveSlug] = useState<string>(items[0]?.slug ?? "");
  const [measuredHeight, setMeasuredHeight] = useState<Record<string, number>>({});
  const [revealVisible, setRevealVisible] = useState(false);
  const mediaRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setRevealVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(section);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const handleResize = () => setMeasuredHeight({});
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const measureMedia = (slug: string) => {
    const el = mediaRefs.current[slug];
    if (!el) return;
    setMeasuredHeight((prev) => {
      const h = el.getBoundingClientRect().height;
      if (prev[slug] === h) return prev;
      return { ...prev, [slug]: h };
    });
  };

  const activate = (slug: string) => {
    setActiveSlug(slug);
    requestAnimationFrame(() => measureMedia(slug));
  };

  const getMediaHeight = (slug: string): number => {
    if (activeSlug !== slug) return 0;
    const h = measuredHeight[slug];
    if (typeof h === "number" && h > 0) return h;
    return 240;
  };

  return (
    <section
      ref={sectionRef}
      className="bg-white py-16 sm:py-20"
    >
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-700">
          Applications
        </p>
        <h2 className="mt-3 text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
          Coatings engineered for demanding environments.
        </h2>
        <p className="mt-4 max-w-xl text-base leading-7 text-slate-600">
          Our coating systems are specified across OEM lines, infrastructure programmes and maintenance
          operations where consistent film performance is non-negotiable.
        </p>

        <div className="mt-12 border-t border-slate-200">
          {items.map((app, index) => {
            const isActive = activeSlug === app.slug;
            const isVisible = revealVisible;
            const delay = isVisible ? index * 70 : 0;
            return (
              <div
                key={app.slug}
                className={`transition-all duration-700 ease-out ${
                  isVisible
                    ? "opacity-100 translate-y-0"
                    : "opacity-0 translate-y-4"
                }`}
                style={{ transitionDelay: `${delay}ms` }}
              >
                <button
                  type="button"
                  onClick={() => activate(app.slug)}
                  onMouseEnter={() => {
                    if (typeof window !== "undefined" && window.innerWidth >= 768) {
                      activate(app.slug);
                    }
                  }}
                  className="group flex w-full items-center justify-between gap-6 py-5 text-left transition-colors duration-300 sm:py-6 lg:py-[26px]"
                  aria-expanded={isActive}
                  aria-controls={`app-media-video-${app.slug}`}
                >
                  <div className="flex min-w-0 flex-1 items-center gap-4">
                    <span
                      className={`shrink-0 text-sm font-semibold tabular-nums transition-colors duration-300 ${
                        isActive ? "text-[#1678C8]" : "text-brand-700 group-hover:text-[#1678C8]"
                      }`}
                    >
                      {numberFor(index)}
                    </span>
                    <Link
                      href={`/media/images/applications/${app.slug}`}
                      className={`block text-xl font-semibold leading-tight transition-colors duration-300 sm:text-[26px] lg:text-[28px] ${
                        isActive ? "text-[#1678C8]" : "text-[#082B4C] group-hover:text-[#1678C8]"
                      }`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      {app.name}
                    </Link>
                  </div>
                  <span
                    className={`shrink-0 text-sm font-semibold transition-colors duration-300 ${
                      isActive ? "text-[#0B5C97]" : "text-brand-700 group-hover:text-[#0B5C97]"
                    }`}
                  >
                    Explore
                  </span>
                </button>

                {isActive && <div className="h-[2px] w-full bg-[#1678C8]" />}

                <div
                  id={`app-media-video-${app.slug}`}
                  role="region"
                  aria-label={`${app.name} preview`}
                  className="overflow-hidden"
                  style={{
                    height: getMediaHeight(app.slug),
                    opacity: isActive ? 1 : 0,
                    transition: `height ${TRANSITION_MS}ms cubic-bezier(0.16,1,0.3,1), opacity ${TRANSITION_MS}ms cubic-bezier(0.16,1,0.3,1)`,
                  }}
                  onTransitionEnd={() => {
                    if (activeSlug === app.slug) {
                      measureMedia(app.slug);
                    }
                  }}
                >
                  <div
                    ref={(el) => {
                      mediaRefs.current[app.slug] = el;
                      if (el && activeSlug === app.slug) {
                        requestAnimationFrame(() => measureMedia(app.slug));
                      }
                    }}
                    className="relative h-[240px] sm:h-[230px] lg:h-[260px]"
                  >
                    {app.video ? (
                      <video
                        src={app.video}
                        autoPlay
                        muted
                        loop
                        playsInline
                        preload="metadata"
                        aria-hidden="true"
                        className="absolute inset-0 h-full w-full object-cover object-top"
                      />
                    ) : app.image ? (
                      <img
                        src={app.image}
                        alt={`${app.name} industrial coating application`}
                        className="absolute inset-0 h-full w-full object-cover object-center"
                        loading="lazy"
                      />
                    ) : (
                      <div
                        className="absolute inset-0"
                        style={{
                          background: "linear-gradient(135deg, #EDF5FA 0%, #E3EEF6 100%)",
                        }}
                      />
                    )}
                    <div
                      className="absolute inset-0"
                      style={{
                        background:
                          "linear-gradient(135deg, rgba(11,92,151,0.10) 0%, rgba(11,92,151,0.04) 100%)",
                      }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-10 flex justify-center sm:mt-12">
          <Link
            href="/applications"
            className="group inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-8 py-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
          >
            View all applications
            <svg
              viewBox="0 0 20 20"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
            >
              <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}