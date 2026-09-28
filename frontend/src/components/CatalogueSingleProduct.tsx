"use client";

import { useEffect, useRef, useState } from "react";
import { SpecificationTable } from "@/components/SpecificationTable";
import { getMediaUrl } from "@/lib/media";

type CatalogueSingleProductProps = {
  title: string;
  image: string | null | undefined;
  alt: string;
  specifications?: { label: string; value: string }[];
  description?: string;
  features?: string[];
  applications?: string[];
  modelLabel?: string;
};

export function CatalogueSingleProduct({
  title,
  image,
  alt,
  specifications,
  description,
  features,
  applications,
  modelLabel = "Model 01",
}: CatalogueSingleProductProps) {
  const sectionRef = useRef<HTMLDivElement>(null);
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
    <div ref={sectionRef} className="relative min-h-[520px] lg:min-h-[600px]">
      <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:gap-12">
        <div
          className={`flex flex-1 items-center justify-center transition-all duration-700 ease-out ${
            visible ? "opacity-100" : "opacity-0"
          }`}
          style={{ transform: visible ? "translateX(0)" : "translateX(-20px)" }}
        >
          <div className="relative w-full">
            <div className="absolute inset-0 bg-[#E7F5FC] rounded-[32px_32px_8px_32px]" />
            <div className="relative flex items-center justify-center rounded-[32px_32px_8px_32px] bg-[#E7F5FC] px-6 py-10 sm:px-10 sm:py-14 lg:px-12 lg:py-16">
              {image ? (
                <img
                  src={getMediaUrl(image)}
                  alt={alt}
                  className="h-auto max-h-[400px] lg:max-h-[500px] w-auto object-contain transition-transform duration-300 ease-out hover:scale-[1.02]"
                  loading="lazy"
                />
              ) : (
                <div className="flex h-[260px] w-full items-center justify-center text-sm text-slate-400">
                  Product image
                </div>
              )}
            </div>
          </div>
        </div>

        <div
          className={`flex flex-1 flex-col justify-center transition-all duration-700 ease-out ${
            visible ? "opacity-100" : "opacity-0"
          }`}
          style={{ transform: visible ? "translateX(0)" : "translateX(20px)" }}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#1678C8]">
            {modelLabel}
          </p>
          <h2 className="mt-3 text-3xl font-semibold uppercase tracking-wide text-[#082B4C] sm:text-4xl lg:text-[40px]">
            {title}
          </h2>
          {description && (
            <p className="mt-4 text-sm leading-7 text-slate-600">{description}</p>
          )}
          {specifications && specifications.length > 0 ? (
            <div className="mt-6 w-full">
              <SpecificationTable specifications={specifications} />
            </div>
          ) : (
            <p className="mt-6 text-sm leading-7 text-slate-600">
              Detailed technical specifications are available in the product catalogue.
            </p>
          )}
          {features && features.length > 0 && (
            <div className="mt-6">
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#1678C8]">Key Features</h3>
              <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
                {features.map((f, idx) => (
                  <div
                    key={idx}
                    className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700"
                  >
                    {f}
                  </div>
                ))}
              </div>
            </div>
          )}
          {applications && applications.length > 0 && (
            <div className="mt-6">
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-[#1678C8]">Applications</h3>
              <ul className="mt-2 list-disc list-inside space-y-1 text-sm text-slate-600">
                {applications.map((a, idx) => (
                  <li key={idx}>{a}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
