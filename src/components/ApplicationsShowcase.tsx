"use client";

import { useState, useRef, useEffect, type ReactNode } from "react";
import Link from "next/link";
import type { Application } from "@/lib/data";

type ApplicationsShowcaseProps = {
  applications: Application[];
};

const MOBILE_BREAK = 768;

export function ApplicationsShowcase({ applications }: ApplicationsShowcaseProps) {
  const [activeSlug, setActiveSlug] = useState(applications[0]?.slug ?? null);
  const [visibleRows, setVisibleRows] = useState<boolean[]>([]);
  const [measuredHeights, setMeasuredHeights] = useState<Record<string, number>>({});
  const [animatingHeights, setAnimatingHeights] = useState<Record<string, number>>({});
  const [animatingOpacities, setAnimatingOpacities] = useState<Record<string, number>>({});
  const mediaRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const observerRef = useRef<IntersectionObserver | null>(null);
  const entranceDoneRef = useRef(false);

  useEffect(() => {
    if (entranceDoneRef.current) return;
    const entries = Array.from(
      document.querySelectorAll("[data-app-row]") ?? [],
    );
    const visible: boolean[] = new Array(entries.length).fill(false);
    setVisibleRows(visible);
    const obs = new IntersectionObserver(
      (items) => {
        items.forEach((entry) => {
          const idx = Number(
            (entry.target as HTMLElement).getAttribute("data-row-index"),
          );
          if (entry.isIntersecting && !visible[idx]) {
            visible[idx] = true;
            setVisibleRows([...visible]);
            if (idx === entries.length - 1) obs.disconnect();
          }
        });
      },
      { threshold: 0.1 },
    );
    entries.forEach((el) => obs.observe(el));
    observerRef.current = obs;
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setMeasuredHeights({});
      setAnimatingHeights({});
      setAnimatingOpacities({});
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const measureMedia = (slug: string) => {
    const el = mediaRefs.current[slug];
    if (!el) return;
    setMeasuredHeights((prev) => {
      const h = el.getBoundingClientRect().height;
      if (prev[slug] === h) return prev;
      const next = { ...prev, [slug]: h };
      if (activeSlug === slug) {
        setAnimatingHeights({ ...next });
      }
      return next;
    });
  };

  const handleRowMouseEnter = (slug: string) => {
    if (typeof window !== "undefined" && window.innerWidth >= MOBILE_BREAK) {
      activateApp(slug);
    }
  };

  const handleRowClick = (slug: string) => {
    activateApp(slug);
  };

  const activateApp = (slug: string) => {
    setActiveSlug(slug);
    requestAnimationFrame(() => measureMedia(slug));
  };

  const getMediaHeight = (slug: string) => {
    if (activeSlug !== slug) return 0;
    const h = measuredHeights[slug];
    if (typeof h === "number" && h > 0) return h;
    if (typeof h === "number" && animatingHeights[slug]) return animatingHeights[slug];
    return 280;
  };

  const getMediaOpacity = (slug: string) => {
    if (activeSlug !== slug) return 0;
    return animatingOpacities[slug] ?? 1;
  };

  return (
    <>
      {/* Rows list */}
      <div className="border-t border-slate-200">
        {applications.map((app, index) => {
          const isActive = activeSlug === app.slug;
          const isVisible = visibleRows[index];
          const delay = isVisible ? index * 60 : 0;
          return (
            <div
              key={app.slug}
              data-app-row
              data-row-index={index}
              style={
                {
                  opacity: isVisible ? 1 : 0,
                  transform: isVisible ? "translateY(0)" : "translateY(18px)",
                  transition:
                    "opacity 500ms cubic-bezier(0.16,1,0.3,1) " +
                    `${delay}ms, transform 500ms cubic-bezier(0.16,1,0.3,1) ${delay}ms`,
                } as React.CSSProperties
              }
            >
              <button
                type="button"
                onClick={() => handleRowClick(app.slug)}
                onMouseEnter={() => handleRowMouseEnter(app.slug)}
                className={[
                  "group flex w-full items-center justify-between gap-6 px-0 py-5 text-left transition-colors duration-300 sm:py-6 lg:py-[26px]",
                  isActive
                    ? "text-brand-950 border-b border-transparent"
                    : "text-slate-600 hover:text-brand-950 border-b border-slate-200",
                ].join(" ")}
                aria-expanded={isActive}
                aria-controls={`app-media-${app.slug}`}
              >
                {/* Left: title + description */}
                <div className="flex-1 min-w-0">
                  <Link
                    href={`/applications/${app.slug}`}
                    className={[
                      "block text-xl font-semibold transition-colors duration-300 sm:text-[26px] lg:text-[28px] leading-tight",
                      isActive
                        ? "text-[#1678C8]"
                        : "text-brand-950 group-hover:text-[#1678C8]",
                    ].join(" ")}
                    onClick={(e) => e.stopPropagation()}
                  >
                    {app.name}
                  </Link>
                  <p className="mt-1.5 text-xs leading-6 text-slate-600 sm:text-sm sm:leading-7 lg:max-w-2xl">
                    {app.text}
                  </p>
                </div>

                {/* Right: number */}
                <span
                  className={[
                    "shrink-0 text-sm font-semibold tabular-nums transition-colors duration-300",
                    isActive
                      ? "text-[#0B5C97]"
                      : "text-brand-700 group-hover:text-[#0B5C97]",
                  ].join(" ")}
                >
                  {String(index + 1).padStart(2, "0")}
                </span>
              </button>

              {/* Active row bottom accent */}
              {isActive && (
                <div className="h-[2px] w-full bg-[#1678C8]" />
              )}

              {/* Media panel */}
              <div
                id={`app-media-${app.slug}`}
                role="region"
                aria-label={`${app.name} preview`}
                className="overflow-hidden"
                style={
                  {
                    height: getMediaHeight(app.slug),
                    opacity: getMediaOpacity(app.slug),
                    transition:
                      "height 550ms cubic-bezier(0.16,1,0.3,1), opacity 450ms cubic-bezier(0.16,1,0.3,1)",
                  } as React.CSSProperties
                }
                onTransitionEnd={() => {
                  if (activeSlug === app.slug) {
                    setAnimatingOpacities((prev) => ({ ...prev, [app.slug]: 1 }));
                  }
                }}
              >
                <div
                  ref={(el) => {
                    mediaRefs.current[app.slug] = el;
                    if (
                      el &&
                      !measuredHeights[app.slug] &&
                      activeSlug === app.slug
                    ) {
                      requestAnimationFrame(() => measureMedia(app.slug));
                    }
                  }}
                  className="relative h-[240px] sm:h-[230px] lg:h-[260px]"
                >
                  {app.video ? (
                    <>
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
                      <div
                        className="absolute inset-0"
                        style={{
                          background:
                            "linear-gradient(135deg, rgba(11,92,151,0.10) 0%, rgba(11,92,151,0.04) 100%)",
                        }}
                      />
                    </>
                  ) : app.image ? (
                    <>
                      <img
                        src={app.image}
                        alt={`${app.name} industrial coating application`}
                        className="absolute inset-0 h-full w-full object-cover object-center"
                      />
                      <div
                        className="absolute inset-0"
                        style={{
                          background:
                            "linear-gradient(135deg, rgba(11,92,151,0.10) 0%, rgba(11,92,151,0.04) 100%)",
                        }}
                      />
                    </>
                  ) : (
                    <>
                      <div
                        className="absolute inset-0"
                        style={{
                          background:
                            "linear-gradient(135deg, #EDF5FA 0%, #E3EEF6 100%)",
                        }}
                      />
                      <div className="absolute inset-0 flex items-center justify-center">
                        <p className="text-sm font-medium text-slate-500 tracking-wide">
                          {app.name}
                        </p>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* View all CTA */}
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
            strokeWidth="2"
            className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
          >
            <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </Link>
      </div>
    </>
  );
}
