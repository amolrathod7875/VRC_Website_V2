"use client";

import { useEffect, useRef, useState } from "react";
import {
  IconConstruction,
  IconShield,
  IconCircuit,
  IconPackage,
  IconFlask,
  IconSupport,
} from "@/components/Icon";

const STAGGER_MS = 90;

const reasons = [
  {
    number: "01",
    title: "Forged Pressure Components",
    text: "Unique in the world — our pressure components are forged (not cast), providing unmatched strength under extreme operating pressures.",
    image: "/media/images/misc/why_choose_us/Forged Pressure Components.jpg",
    alt: "Forged industrial pressure component",
    Icon: IconConstruction,
  },
  {
    number: "02",
    title: "100% Stainless Steel Bodies",
    text: "No carbon steel in our pump bodies whatsoever. Complete stainless steel hydraulic bodies for maximum corrosion resistance and longevity.",
    image: "/media/images/misc/why_choose_us/100-percent-stainless-steel-bodies.jpg",
    alt: "Stainless steel industrial equipment",
    Icon: IconShield,
  },
  {
    number: "03",
    title: "Composite Material Seals",
    text: "Specially developed composite material seals providing superior compatibility with aggressive coatings, solvents, and chemicals.",
    image: "/media/images/misc/why_choose_us/Composite Material Seals.jpg",
    alt: "Precision engineered composite seal component",
    Icon: IconCircuit,
  },
  {
    number: "04",
    title: "Modular Design",
    text: "Every system is designed modularly, making it easy to change configurations, mixing ratios, and accessories without replacing the entire system.",
    image: "/media/images/misc/why_choose_us/Modular Design.jpg",
    alt: "Modular industrial equipment system",
    Icon: IconPackage,
  },
  {
    number: "05",
    title: "Application Know-How",
    text: "Thorough technical and application know-how from four decades of serving automotive, marine, aerospace, railways, and many more industries.",
    image: "/media/images/misc/why_choose_us/Application Know-How.jpg",
    alt: "Engineer performing industrial application work",
    Icon: IconFlask,
  },
  {
    number: "06",
    title: "Easy Maintenance",
    text: "All products designed for easy field maintenance. Wear parts are accessible, standardised, and widely available from our Pune facility.",
    image: "/media/images/misc/why_choose_us/Easy Maintenance.jpg",
    alt: "Technician maintaining industrial equipment",
    Icon: IconSupport,
  },
];

export function WhyChooseUs() {
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
      id="why-choose-us"
      className="scroll-mt-24 bg-white py-16 sm:py-20 lg:pt-[80px] lg:pb-0 lg:min-h-[calc(100vh-80px)] lg:flex lg:flex-col lg:justify-center"
    >
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">
          Our differentiators
        </p>
        <h2 className="mt-2 text-3xl font-semibold text-brand-950 lg:mt-[72px]">
          Why choose VR Coatings
        </h2>

        <div className="mt-12 grid grid-cols-1 gap-x-8 gap-y-14 md:grid-cols-2 lg:grid-cols-3 lg:gap-x-12 lg:gap-y-16">
          {reasons.map((item, i) => (
            <ReasonColumn key={item.title} item={item} index={i} visible={visible} />
          ))}
        </div>
      </div>
    </section>
  );
}

function ReasonColumn({
  item,
  index,
  visible,
}: {
  item: (typeof reasons)[number];
  index: number;
  visible: boolean;
}) {
  const Icon = item.Icon;

  return (
    <div
      className={`group transition-all duration-700 ease-out ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
      style={{ transitionDelay: `${index * STAGGER_MS}ms` }}
    >
      <div className="flex items-center gap-3">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[#1678C8] text-xs font-bold text-white">
          {item.number}
        </span>
        <span className="flex h-9 w-9 items-center justify-center rounded-md bg-[#E8F4FB] text-[#1678C8]">
          <Icon className="h-5 w-5" />
        </span>
      </div>
      <h3 className="mt-5 text-[22px] font-semibold leading-[1.15] text-[#082B4C] transition-colors duration-300 group-hover:text-[#1678C8]">
        {item.title}
      </h3>
      <p className="mt-3 min-h-[4.5em] text-[15px] leading-[1.6] text-slate-600">{item.text}</p>
      <div className="mt-5">
        <div className="relative w-full overflow-hidden rounded-[12px] bg-[#E9EEF3] aspect-[4/3] transition-transform duration-400 ease-out group-hover:scale-[1.015]">
          <img
            src={item.image}
            alt={item.alt}
            className="h-full w-full object-cover object-center"
            loading="lazy"
          />
        </div>
      </div>
    </div>
  );
}