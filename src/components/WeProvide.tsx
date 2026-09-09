"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { weProvide } from "@/lib/data";

const STAGGER_MS = 110;

export function WeProvide() {
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
    <section
      ref={sectionRef}
      id="we-provide"
      className="bg-[#F4F7FA] pt-[96px] pb-20 sm:pb-24 lg:min-h-[calc(100vh-80px)] lg:flex lg:flex-col lg:justify-center lg:pt-[96px] lg:pb-0"
    >
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Top intro + headline area */}
        <div className="grid gap-10 lg:grid-cols-[0.75fr_1.75fr] lg:items-start lg:gap-16">
          <div
            className={`transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            }`}
          >
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#1678C8]">
              We provide
            </p>
            <p className="mt-4 text-sm leading-6 text-slate-600">
              VR Coatings supports customers from product selection and trials through application, quality
              control and supply.
            </p>
            <Link
              href="/products"
              className="mt-6 inline-flex items-center gap-2 rounded-md border-2 border-[#082B4C] bg-transparent px-5 py-2.5 text-sm font-semibold text-[#082B4C] transition-colors duration-200 hover:bg-[#082B4C] hover:text-white"
            >
              Explore our capabilities
              <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={2}>
                <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
          </div>

          <div
            className={`transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            }`}
            style={{ transitionDelay: "120ms" }}
          >
            <h2
              className="text-[34px] font-semibold leading-[1.08] text-[#082B4C] sm:text-[clamp(36px,3.4vw,46px)] lg:text-[clamp(42px,4vw,56px)]"
              style={{ maxWidth: "780px" }}
            >
              From application support to reliable supply, our capabilities help customers achieve
              consistent coating performance across demanding industrial environments.
            </h2>
          </div>
        </div>

        {/* Service columns */}
        <div className="mt-14 grid grid-cols-1 gap-px border border-slate-200 bg-slate-200 sm:grid-cols-2 lg:grid-cols-4">
          {weProvide.map((item, i) => (
            <ServiceColumn key={item.title} item={item} index={i} visible={visible} />
          ))}
        </div>
      </div>
    </section>
  );
}

function ServiceColumn({
  item,
  index,
  visible,
}: {
  item: (typeof weProvide)[number];
  index: number;
  visible: boolean;
}) {
  const number = String(index + 1).padStart(2, "0");

  return (
    <div
      className={`group bg-[#F4F7FA] transition-all duration-700 ease-out ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
      style={{ transitionDelay: `${240 + index * STAGGER_MS}ms` }}
    >
      <div className="px-6 py-7 sm:px-7">
        <div className="flex items-center gap-3">
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#1678C8] text-xs font-bold text-white">
            {number}
          </span>
          <h3 className="text-[19px] font-semibold text-[#082B4C] transition-colors duration-200 group-hover:text-[#1678C8]">
            {item.title}
          </h3>
        </div>
        <p className="mt-3 text-sm leading-6 text-slate-600">{item.text}</p>
      </div>
      <div className="px-6 pb-7 sm:px-7">
        <div className="h-[200px] w-full overflow-hidden rounded-md bg-[#E8EEF4] transition-all duration-300 ease-out group-hover:-translate-y-1 group-hover:shadow-sm" />
      </div>
    </div>
  );
}