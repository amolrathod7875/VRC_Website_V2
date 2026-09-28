"use client";

import { useEffect, useRef, useState } from "react";
import { lionFeatures, lionApplications, lionSpecRows } from "@/lib/lionData";
import { SpecificationTable } from "@/components/SpecificationTable";

export function LionFeatures() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="bg-white py-16 sm:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Why Lion</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Key Features</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {lionFeatures.map((feature, i) => (
            <div
              key={i}
              className={`rounded-xl border border-slate-200 bg-white p-5 transition-all duration-600 ease-out ${
                visible ? "opacity-100 translateY-0" : "opacity-0 translate-y-4"
              }`}
              style={{ transitionDelay: `${i * 80}ms` }}
            >
              <p className="text-sm font-medium leading-6 text-slate-700">{feature.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function LionApplications() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="bg-[#F4F7FA] py-16 sm:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Applications</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Where Lion performs</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {lionApplications.map((app, i) => (
            <div
              key={i}
              className={`rounded-xl border border-slate-200 bg-white p-6 transition-all duration-600 ease-out ${
                visible ? "opacity-100 translateY-0" : "opacity-0 translate-y-4"
              }`}
              style={{ transitionDelay: `${i * 80}ms` }}
            >
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#1678C8]">
                {String(i + 1).padStart(2, "0")}
              </p>
              <h3 className="mt-2 text-lg font-semibold text-[#082B4C]">{app.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{app.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function LionTechnicalSpecifications() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="bg-white py-16 sm:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Technical Specifications</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Lion specifications</h2>
        <p className="mt-2 text-sm text-slate-500">
          All values are taken directly from the Lion catalogue PDF.
        </p>
        <div className={`mt-8 overflow-x-auto transition-all duration-700 ease-out ${visible ? "opacity-100" : "opacity-0"}`}>
          <SpecificationTable specifications={lionSpecRows.map((row) => ({ label: row.label, value: row.value }))} />
        </div>
      </div>
    </section>
  );
}
