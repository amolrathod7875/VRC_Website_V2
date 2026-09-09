"use client";

import { useEffect, useRef, useState } from "react";

const SECTION_CODES = [
  "A-01",
  "A-02",
  "A-03",
  "A-04",
  "A-05",
  "A-06",
  "A-07",
  "A-08",
  "A-09",
  "A-10",
  "A-11",
  "A-12",
];

export function ScrollProgressRail() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [scrollProgress, setScrollProgress] = useState(0);
  const rafRef = useRef(0);

  useEffect(() => {
    const main = document.querySelector("main") as HTMLElement | null;
    if (!main) return;

    const sections = Array.from(main.querySelectorAll("section"));
    if (sections.length === 0) return;

    let currentIdx = 0;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]) {
          const idx = sections.indexOf(visible[0].target as HTMLElement);
          if (idx !== -1 && idx !== currentIdx) {
            currentIdx = idx;
            setActiveIndex(idx);
          }
        }
      },
      {
        rootMargin: "-40% 0px -50% 0px",
        threshold: [0, 0.2, 0.4, 0.6, 0.8],
      }
    );

    sections.forEach((section) => observer.observe(section));

    const handleScroll = () => {
      if (rafRef.current) return;
      rafRef.current = requestAnimationFrame(() => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? Math.min(scrollTop / docHeight, 1) : 0;
        setScrollProgress(progress);
        rafRef.current = 0;
      });
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", handleScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <nav
      aria-hidden
      className="fixed left-6 top-[120px] z-40 hidden lg:flex flex-col items-center pointer-events-none select-none"
    >
      <span
        key={activeIndex}
        className="text-[13px] font-medium tracking-[0.1em] text-slate-500"
        style={{
          animation: "labelIn 250ms ease-out",
        }}
      >
        {SECTION_CODES[activeIndex] ?? "A-01"}
      </span>
      <div className="relative mt-3 h-[65vh] w-px bg-[rgba(8,43,76,0.18)]">
        <div
          className="absolute inset-x-0 top-0 h-full w-px bg-[#1678C8] origin-top transition-transform duration-150 ease-out"
          style={{ transform: `scaleY(${scrollProgress})` }}
        />
      </div>
    </nav>
  );
}
