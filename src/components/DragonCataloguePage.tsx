"use client";

import { useEffect, useRef, useState } from "react";
import { dragonVariants, dragonFeatures, dragonApplications } from "@/lib/dragonData";

export function DragonFeatures() {
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
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Why Dragon</p>
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Key Features</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {dragonFeatures.map((feature, i) => (
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

export function DragonApplications() {
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
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Where Dragon performs</h2>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {dragonApplications.map((app, i) => (
            <div
              key={i}
              className={`rounded-xl border border-slate-200 bg-white p-6 transition-all duration-600 ease-out ${
                visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
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

export function DragonTechnicalSpecifications() {
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
        <h2 className="mt-3 text-3xl font-semibold text-[#082B4C]">Dragon configuration matrix</h2>
        <p className="mt-2 text-sm text-slate-500">
          All values are taken directly from the Dragon catalogue PDF.
        </p>
        <div className={`mt-8 overflow-x-auto transition-all duration-700 ease-out ${visible ? "opacity-100" : "opacity-0"}`}>
          <table className="min-w-[640px] border-collapse text-left text-sm">
            <thead>
              <tr className="bg-[#0B5C97] text-white">
                <th className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide">Parameter</th>
                {dragonVariants.map((variant) => (
                  <th key={variant.id} className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">
                    {variant.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr className={ "bg-white"}>
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  PRESSURE RATIO
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.pressureRatio}
                  </td>
                ))}
              </tr>
              <tr className="bg-[#F4F7FA]">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  DISCHARGE/CYCLE
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.dischargePerCycle}
                  </td>
                ))}
              </tr>
              <tr className="bg-white">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  PUMP COMBINATION
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.pumpCombination}
                  </td>
                ))}
              </tr>
              <tr className="bg-[#F4F7FA]">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  MAX INLET AIR PRESSURE
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.maxInletAirPressure}
                  </td>
                ))}
              </tr>
              <tr className="bg-white">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  MAX OUTPUT PRESSURE
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.maxOutputPressure}
                  </td>
                ))}
              </tr>
              <tr className="bg-[#F4F7FA]">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  MIXING RATIO
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.mixingRatio}
                  </td>
                ))}
              </tr>
              <tr className="bg-white">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  SUPPLY
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.supply}
                  </td>
                ))}
              </tr>
              <tr className="bg-[#F4F7FA]">
                <td className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide text-[#082B4C]">
                  REFERENCE INTUMESCENT MATERIAL
                </td>
                {dragonVariants.map((variant) => (
                  <td key={variant.id} className="px-4 py-3 text-slate-700 text-center">
                    {variant.referenceMaterial}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
