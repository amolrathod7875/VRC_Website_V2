"use client";

import { useEffect, useRef, useState } from "react";
import {
  IconWind,
  IconConstruction,
  IconShield,
  IconCircuit,
  IconPackage,
  IconFlask,
  IconBadgeCheck,
  IconSupport,
} from "@/components/Icon";

const STAGGER_MS = 70;

const differentiators = [
  {
    title: "World's Best Air Motor",
    text: "Pneumatically sensed, maintenance-free air motors. Ice-free operation. Lowest exhaust noise. Hard-coated piston rods for extended service life.",
    Icon: IconWind,
  },
  {
    title: "Forged Pressure Components",
    text: "Unique in the world — our pressure components are forged (not cast), providing unmatched strength under extreme operating pressures.",
    Icon: IconConstruction,
  },
  {
    title: "100% Stainless Steel Bodies",
    text: "No carbon steel in our pump bodies whatsoever. Complete stainless steel hydraulic bodies for maximum corrosion resistance and longevity.",
    Icon: IconShield,
  },
  {
    title: "Composite Material Seals",
    text: "Specially developed composite material seals providing superior compatibility with aggressive coatings, solvents, and chemicals.",
    Icon: IconCircuit,
  },
  {
    title: "Modular Design",
    text: "Every system is designed modularly, making it easy to change configurations, mixing ratios, and accessories without replacing the entire system.",
    Icon: IconPackage,
  },
  {
    title: "Application Know-How",
    text: "Thorough technical and application know-how from four decades of serving automotive, marine, aerospace, railways, and many more industries.",
    Icon: IconFlask,
  },
  {
    title: "Competitive Pricing",
    text: "Products of superior design, ruggedness, and reliability — at competitive prices. Maximum performance per rupee invested.",
    Icon: IconBadgeCheck,
  },
  {
    title: "Easy Maintenance",
    text: "All products designed for easy field maintenance. Wear parts are accessible, standardised, and widely available from our Pune facility.",
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
      className="scroll-mt-24 bg-white py-16 sm:py-20 lg:min-h-[calc(100vh-80px)] lg:flex lg:flex-col lg:justify-center lg:py-0"
    >
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="mb-10 text-3xl font-semibold text-brand-950 lg:mt-[72px]">
          Why choose VR Coatings
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 lg:gap-x-6 lg:gap-y-6">
          {differentiators.map((item, i) => {
            const Icon = item.Icon;
            return (
              <article
                key={item.title}
                className={`group rounded-xl border border-slate-200 bg-white p-6 border-l-[3px] border-l-[#1678C8] transition-all duration-200 hover:-translate-y-1 hover:border-[#1678C8]/30 hover:shadow-sm ${
                  visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
                }`}
                style={
                  visible
                    ? {
                        transitionDelay: `${i * STAGGER_MS}ms`,
                        animation: `quality-fade-up 0.55s ease-out ${i * STAGGER_MS}ms both`,
                      }
                    : undefined
                }
              >
                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-md bg-brand-50 text-brand-800">
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-semibold text-brand-900">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
