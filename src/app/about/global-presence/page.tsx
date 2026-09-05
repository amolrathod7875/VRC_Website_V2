import type { Metadata } from "next";
import { offices } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Global Presence" };

export default function GlobalPresencePage() {
  return (
    <>
      <PageHero
        kicker="About"
        title="Global presence"
        text="Manufacturing in India with commercial and technical coverage in North America and export markets."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <Placeholder label="World map / global footprint" className="mb-10 min-h-[240px] rounded-xl" />
        <div className="grid gap-6 md:grid-cols-3">
          {offices.map((office) => (
            <article key={office.title} className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-brand-900">{office.title}</h2>
              {office.lines.map((line) => (
                <p key={line} className="mt-1 text-sm text-slate-600">
                  {line}
                </p>
              ))}
              <a href={office.phoneHref} className="mt-4 inline-block text-sm font-semibold text-brand-700">
                {office.phone}
              </a>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
