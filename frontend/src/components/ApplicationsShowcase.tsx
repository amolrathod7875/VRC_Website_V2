"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { applications } from "@/lib/data";
import { IconArrowRight } from "@/components/Icon";

type ApplicationsShowcaseProps = {
  applications?: typeof applications;
};

const STAGGER_MS = 90;

function numberFor(index: number): string {
  return String(index + 1).padStart(2, "0");
}

export function ApplicationsShowcase({
  applications: items = applications,
}: ApplicationsShowcaseProps) {
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
      className="bg-white py-16 sm:py-20"
    >
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">
          Applications
        </p>
        <h2 className="mt-2 text-3xl font-semibold text-brand-950">
          Coatings engineered for demanding environments
        </h2>
        <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
          Industry uses for VR coating systems—from OEM lines to infrastructure maintenance.
        </p>

        <div className="mt-12 grid grid-cols-1 gap-x-8 gap-y-14 md:grid-cols-2 lg:grid-cols-3 lg:gap-x-12 lg:gap-y-16">
          {items.map((item, i) => (
            <ApplicationColumn
              key={item.slug}
              item={item}
              index={i}
              number={numberFor(i)}
              visible={visible}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

function ApplicationColumn({
  item,
  index,
  number,
  visible,
}: {
  item: (typeof applications)[number];
  index: number;
  number: string;
  visible: boolean;
}) {
  // Each application now stores its own category-specific icon component
  // directly, so no string-keyed lookup or fallback is needed at render.
  const Icon = item.icon;

  return (
    <div
      className={`group transition-all duration-700 ease-out ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
      style={{ transitionDelay: `${index * STAGGER_MS}ms` }}
    >
      <div className="flex items-center gap-3">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[#1678C8] text-xs font-bold text-white">
          {number}
        </span>
        <span className="flex h-9 w-9 items-center justify-center rounded-[8px] bg-[#E8F4FB] text-[#1678C8] transition-colors duration-250 group-hover:text-[#0B5C97]">
          <Icon className="h-5 w-5" />
        </span>
      </div>
      <h3 className="mt-5 text-[22px] font-semibold leading-[1.15] text-[#082B4C] transition-colors duration-300 group-hover:text-[#1678C8]">
        {item.name}
      </h3>
      <p className="mt-3 min-h-[4.5em] text-[15px] leading-[1.6] text-slate-600">{item.text}</p>
      <Link
        href={`/media/images/applications/${item.slug}`}
        className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-[#1678C8] transition-colors duration-200 hover:text-[#0B5C97]"
      >
        Explore
        <IconArrowRight className="h-3.5 w-3.5 transition-transform duration-200 ease-out group-hover:translate-x-0.5" />
      </Link>
      <div className="mt-5">
        <div className="relative w-full overflow-hidden rounded-[12px] bg-[#E9EEF3] aspect-[4/3]">
          <img
            src={item.image}
            alt={applicationAltText(item.name)}
            className="h-full w-full object-cover object-center transition-transform duration-500 ease-out group-hover:scale-[1.025]"
            loading="lazy"
          />
        </div>
      </div>
    </div>
  );
}

function applicationAltText(name: string): string {
  switch (name) {
    case "Automotive":
      return "Automotive coating and manufacturing application";
    case "Defence & Aerospace":
      return "Aerospace and defence industrial coating application";
    case "Electronics":
      return "Electronics manufacturing and protective coating application";
    case "Infrastructure":
      return "Structural steel and infrastructure coating application";
    case "Marine":
      return "Marine and shipyard coating application";
    case "Energy & Process":
      return "Industrial process plant and energy coating application";
    default:
      return name;
  }
}