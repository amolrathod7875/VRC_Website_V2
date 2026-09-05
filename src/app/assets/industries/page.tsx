import type { Metadata } from "next";
import Link from "next/link";
import { applications } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Industries We Serve" };

export default function IndustriesPage() {
  return (
    <>
      <PageHero kicker="Our Assets" title="Industries we serve" text="Cross-sector coating programmes with shared quality systems and local support." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 md:grid-cols-2">
          {applications.map((item) => (
            <article key={item.slug} className="grid gap-0 overflow-hidden rounded-xl border border-slate-200 bg-white sm:grid-cols-[180px_1fr]">
              <Placeholder label={`${item.name} industry`} className="min-h-[140px]" />
              <div className="p-5">
                <h2 className="font-semibold text-brand-900">{item.name}</h2>
                <p className="mt-2 text-sm text-slate-600">{item.text}</p>
                <Link href="/applications" className="mt-3 inline-block text-sm font-semibold text-brand-700">
                  See applications
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
