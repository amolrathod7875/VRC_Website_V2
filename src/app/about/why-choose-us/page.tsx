import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Why Choose Us" };

const reasons = [
  {
    title: "Application-first engineering",
    text: "Formulations are validated against blasting profiles, bake schedules, and field climates—not generic data sheets alone.",
  },
  {
    title: "Documented quality",
    text: "Incoming raw materials, in-process checks, and finished-film tests are logged against each batch.",
  },
  {
    title: "Responsive technical service",
    text: "Coating advisors support line trials, defect analysis, and specification writing.",
  },
  {
    title: "Regional presence, export discipline",
    text: "India manufacturing plus North America coverage for OEM programmes that span continents.",
  },
];

export default function WhyChooseUsPage() {
  return (
    <>
      <PageHero kicker="About" title="Why choose VR Coatings" text="Performance, process fit, and partnership across the coating lifecycle." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 md:grid-cols-2">
          {reasons.map((item) => (
            <article key={item.title} className="rounded-xl border border-slate-200 bg-white p-6">
              <Placeholder label="Reason icon" className="mb-4 h-12 w-12 rounded-md" />
              <h2 className="text-lg font-semibold text-brand-900">{item.title}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
