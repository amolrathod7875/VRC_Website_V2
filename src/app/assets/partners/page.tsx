import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Partners" };

const partners = ["Resin Alliance", "Pigment Source Co.", "Global Logistics Hub", "Surface Prep Systems", "Lab Instruments Inc.", "Export Freight Group"];

export default function PartnersPage() {
  return (
    <>
      <PageHero kicker="Our Assets" title="Partners" text="Technology, raw-material, and logistics partners who support VR programmes worldwide." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {partners.map((name) => (
            <article key={name} className="rounded-xl border border-slate-200 bg-white p-5">
              <Placeholder label={`${name} logo`} className="h-28 rounded-md" />
              <h2 className="mt-4 font-semibold text-brand-900">{name}</h2>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
