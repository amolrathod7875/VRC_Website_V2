import type { Metadata } from "next";
import Link from "next/link";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Catalog" };

export default function CatalogPage() {
  return (
    <>
      <PageHero kicker="Literature" title="Catalog" text="Download placeholders until the current product catalog PDF is uploaded." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <Placeholder label="Catalog cover" className="min-h-[360px] rounded-xl" />
          <div>
            <h2 className="text-2xl font-semibold text-brand-950">VR Coatings product catalog</h2>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              The catalog covers protective liquids, powders, primers, and specialty systems with typical uses and
              service environments. Replace this block with a PDF link when the file is ready.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <span className="rounded-md border border-dashed border-slate-300 px-5 py-2.5 text-sm text-slate-500">
                PDF download placeholder
              </span>
              <Link href="/contact" className="rounded-md bg-brand-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-600">
                Request a copy
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
