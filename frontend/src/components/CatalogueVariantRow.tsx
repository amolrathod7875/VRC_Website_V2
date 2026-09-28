"use client";

import { useEffect, useRef, useState } from "react";
import { SpecificationTable } from "@/components/SpecificationTable";
import { getMediaUrl } from "@/lib/media";

export type CatalogueVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: { label: string; value: string }[];
  description?: string;
  variantTable?: {
    columns: string[];
    rows: { name: string; values: string[] }[];
  };
};

type CatalogueVariantRowProps = {
  variant: CatalogueVariant;
  index: number;
};

export function CatalogueVariantRow({ variant, index }: CatalogueVariantRowProps) {
  const rowRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const isEven = index % 2 === 1;

  useEffect(() => {
    const el = rowRef.current;
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

  const imageTranslate = isEven ? "translateX(20px)" : "translateX(-20px)";
  const detailsTranslate = isEven ? "translateX(-20px)" : "translateX(20px)";
  const imageVisibleTransform = visible ? "translateX(0)" : imageTranslate;
  const detailsVisibleTransform = visible ? "translateX(0)" : detailsTranslate;

  return (
    <div
      ref={rowRef}
      className="relative min-h-[520px] lg:min-h-[600px]"
    >
      <div className={`flex flex-col gap-8 lg:flex-row lg:items-center lg:gap-12 ${isEven ? "lg:flex-row-reverse" : ""}`}>
        <div
          className={`flex flex-1 items-center justify-center transition-all duration-700 ease-out ${
            visible ? "opacity-100" : "opacity-0"
          }`}
          style={{ transform: imageVisibleTransform }}
        >
          <div className="relative w-full">
            <div className="absolute inset-0 bg-[#E7F5FC] rounded-[32px_32px_8px_32px]" />
            <div className="relative flex items-center justify-center rounded-[32px_32px_8px_32px] bg-[#E7F5FC] px-6 py-10 sm:px-10 sm:py-14 lg:px-12 lg:py-16">
              <img
                src={getMediaUrl(variant.image)}
                alt={variant.alt}
                className="h-auto max-h-[400px] lg:max-h-[500px] w-auto object-contain transition-transform duration-300 ease-out hover:scale-[1.02]"
                loading="lazy"
              />
            </div>
          </div>
        </div>

        <div
          className={`flex flex-1 flex-col justify-center transition-all duration-700 ease-out ${
            visible ? "opacity-100" : "opacity-0"
          }`}
          style={{ transform: detailsVisibleTransform }}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#1678C8]">
            Model {String(index + 1).padStart(2, "0")}
          </p>
          <h2 className="mt-3 text-3xl font-semibold uppercase tracking-wide text-[#082B4C] sm:text-4xl lg:text-[40px]">
            {variant.name}
          </h2>
          {variant.description && (
            <p className="mt-4 text-sm leading-7 text-slate-600">{variant.description}</p>
          )}
          <div className="mt-6 w-full">
            <SpecificationTable specifications={variant.specifications} />
            {variant.variantTable && (
              <div className="mt-6 overflow-x-auto">
                <table className="min-w-[800px] border-collapse text-left text-sm">
                  <thead>
                    <tr className="bg-[#0B5C97] text-white">
                      <th className="whitespace-nowrap px-4 py-3 font-semibold uppercase tracking-wide">
                        {variant.variantTable.columns[0]}
                      </th>
                      {variant.variantTable.columns.slice(1).map((col, idx) => (
                        <th key={idx} className="whitespace-nowrap px-4 py-3 font-semibold text-center uppercase tracking-wide">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {variant.variantTable.rows.map((row, rowIdx) => (
                      <tr key={row.name} className={rowIdx % 2 === 0 ? "bg-white" : "bg-[#F4F7FA]"} >
                        <td className="whitespace-nowrap px-4 py-3 font-semibold text-[#082B4C]">
                          {row.name}
                        </td>
                        {row.values.map((value, valIdx) => (
                          <td key={valIdx} className="px-4 py-3 text-slate-700 text-center">
                            {value}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
