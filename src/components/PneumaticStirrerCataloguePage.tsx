"use client";

import { useEffect, useRef, useState } from "react";
import { stirrerFeatures, stirrerVariants } from "@/lib/stirrerData";

export function PneumaticStirrerFeatures() {
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
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Why Pneumatic Stirrer</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Key Features</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {stirrerFeatures.map((feature, i) => (
            <div
              key={i}
              className={`rounded-xl border border-slate-200 bg-white p-5 transition-all duration-600 ease-out ${
                visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
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

export function PneumaticStirrerVariants() {
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
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Variants</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Available configurations</h2>
        <p className="mt-2 text-sm text-slate-500">
          All values are taken directly from the Pneumatic Stirrer catalogue PDF.
        </p>
        <div className={`mt-8 overflow-x-auto transition-all duration-700 ease-out ${visible ? "opacity-100" : "opacity-0"}`}>
          <table className="min-w-[720px] border-collapse text-left text-sm">
            <thead>
              <tr className="bg-[#0B5C97] text-white">
                <th className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide">Type</th>
                <th className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">Motor Type</th>
                <th className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">Container Size</th>
                <th className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">Part Number</th>
                <th className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">Shaft Length (mm)</th>
                <th className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">Fan Dia. (mm)</th>
              </tr>
            </thead>
            <tbody>
              {stirrerVariants.map((variant, i) => (
                <tr key={variant.id} className={i % 2 === 0 ? "bg-white" : "bg-[#F4F7FA]"}>
                  <td className="whitespace-nowrap px-4 py-3 font-semibold text-[#082B4C]">
                    {variant.name}
                  </td>
                  <td className="px-4 py-3 text-slate-700 text-center">
                    {variant.motorType}
                  </td>
                  <td className="px-4 py-3 text-slate-700 text-center">
                    {variant.containerSize}
                  </td>
                  <td className="px-4 py-3 text-slate-700 text-center font-mono text-xs">
                    {variant.partNumber}
                  </td>
                  <td className="px-4 py-3 text-slate-700 text-center">
                    {variant.shaftLength}
                  </td>
                  <td className="px-4 py-3 text-slate-700 text-center">
                    {variant.fanDiameter}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-slate-500">
          * Customized specifications, Geared stirrers Pneumatic/Electrically driven available on request.
        </p>
      </div>
    </section>
  );
}