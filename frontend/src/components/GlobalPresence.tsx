"use client";

import { useEffect, useRef, useState } from "react";
import { offices } from "@/lib/contactData";

const STAGGER_MS = 120;

const eyebrowMap: Record<string, string> = {
  "HEAD OFFICE": "HEAD OFFICE",
  "FACTORY": "MANUFACTURING",
  "NORTH AMERICA": "NORTH AMERICA",
  "WAI MIDC": "WAI MIDC",
};

const regionMap: Record<string, string> = {
  "HEAD OFFICE": "Pune, India",
  "FACTORY": "Pune (Bhosari), India",
  "NORTH AMERICA": "Barrie, Ontario, Canada",
  "WAI MIDC": "Wai, Maharashtra, India",
};

const rotations = ["-rotate-2", "rotate-2", "-rotate-2", "rotate-2"];

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
      <div className="mx-auto max-w-[1400px] px-4 sm:px-6 lg:px-8">
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

          <div className="relative mt-8 flex justify-center">
            <div className="w-full max-w-[1150px] rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_18px_50px_-22px_rgba(8,43,76,0.35)] sm:p-5 lg:p-6">
              <img
                src="/media/images/about/Global_Presence.png"
                alt="VR Coatings global presence showing India, Canada and international partner locations"
                loading="lazy"
                decoding="async"
                className="h-auto w-full max-w-full"
                style={{ objectFit: "contain" }}
              />
            </div>
          </div>
        </div>

        <div className="mt-8 grid items-stretch gap-6 md:grid-cols-2 xl:grid-cols-4">
          {offices.map((office, i) => {
            const eyebrow = eyebrowMap[office.label] || office.label.toUpperCase();
            const region = regionMap[office.label] || "";
            const rotation = rotations[i % rotations.length];

            return (
              <article
                key={office.id}
                className={`group relative flex h-full flex-col overflow-hidden rounded-2xl bg-[#082B4C] px-5 py-6 text-white border border-white/10 transition-all duration-300 ease-out hover:-translate-y-1 hover:border-white/20 hover:shadow-xl sm:px-7 sm:py-8 ${
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

                <h3 className="mt-2 text-3xl font-semibold leading-[1.15] text-white sm:text-4xl">
                  {region}
                </h3>

                <p className="mt-6 text-sm font-semibold text-white/90">{office.name}</p>

                <div className="mt-1 space-y-0.5">
                  {office.addressLines.map((line) => (
                    <p key={line} className="text-[15px] leading-6 text-white/70">
                      {line}
                    </p>
                  ))}
                </div>

                {office.contacts.length > 0 && (
                  <a
                    href={office.contacts[0].href}
                    className="mt-4 inline-block whitespace-nowrap text-sm font-semibold text-[#1678C8] transition-colors duration-200 hover:text-white"
                  >
                    {office.contacts[0].value}
                  </a>
                )}

                <div className="mt-auto pt-6">
                  <div
                    className={`overflow-hidden rounded-xl transition-transform duration-300 ease-out group-hover:-translate-y-1 ${rotation}`}
                  >
                    <img
                      src={office.image}
                      alt={office.imageAlt}
                      loading="lazy"
                      decoding="async"
                      style={{ width: "100%", height: 190, objectFit: "cover", objectPosition: "center" }}
                    />
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
