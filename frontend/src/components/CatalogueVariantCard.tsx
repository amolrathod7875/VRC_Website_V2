"use client";

import { useEffect, useRef, useState } from "react";
import { SpecificationTable } from "@/components/SpecificationTable";

type VariantSpec = {
  label: string;
  value: string;
};

export type CatalogueVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  catalogueNote?: string;
  specifications: VariantSpec[];
};

type CatalogueVariantCardProps = {
  variant: CatalogueVariant;
  index: number;
};

export function CatalogueVariantCard({ variant, index }: CatalogueVariantCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = cardRef.current;
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
    <div
      ref={cardRef}
      className={`transition-all duration-500 ease-out ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      <div className="flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white">
        <div className="relative flex flex-1 items-center justify-center bg-[#EAF5FB] p-6 sm:p-8">
          <img
            src={variant.image}
            alt={variant.alt}
            className="h-auto max-h-[220px] w-auto object-contain transition-transform duration-300 ease-out hover:scale-105"
            loading="lazy"
          />
        </div>
        <div className="border-t border-slate-200 px-6 py-5 sm:px-7">
          <h3 className="text-lg font-semibold uppercase tracking-wide text-[#082B4C]">{variant.name}</h3>
          {variant.catalogueNote && (
            <p className="mt-2 text-sm leading-6 text-slate-600">{variant.catalogueNote}</p>
          )}
          {variant.specifications.some((spec) => spec.value !== "See catalogue") ? (
            <SpecificationTable specifications={variant.specifications} />
          ) : (
            <p className="mt-4 text-sm leading-6 text-slate-600">
              Detailed technical specifications are available in the product catalogue.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
