import Link from "next/link";
import { IconArrowRight } from "@/components/Icon";

type ProductCatalogueHeroProps = {
  title: string;
  category: string;
  catalogue: string;
  description?: string;
};

export function ProductCatalogueHero({ title, category, catalogue, description }: ProductCatalogueHeroProps) {
  const hasCatalogue = Boolean(catalogue);

  return (
    <div className="border-b border-slate-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#1678C8]">Product Catalogue</p>
            <h1 className="mt-3 text-3xl font-semibold uppercase text-[#082B4C] sm:text-4xl lg:text-5xl">{title}</h1>
            <p className="mt-3 text-sm text-slate-500">{category}</p>
            {description && <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-600">{description}</p>}
          </div>
          <div className="flex flex-wrap items-center gap-3">
            {hasCatalogue && (
              <Link
                href={catalogue}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-md bg-[#082B4C] px-5 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
              >
                Download Catalogue
                <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={2}>
                  <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </Link>
            )}
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 rounded-md border-2 border-[#082B4C] bg-transparent px-5 py-2.5 text-sm font-semibold text-[#082B4C] transition-colors duration-200 hover:bg-[#082B4C] hover:text-white"
            >
              Request Datasheet
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
