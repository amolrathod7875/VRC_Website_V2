import type { Metadata } from "next";
import { faqs } from "@/lib/data";
import { PageHero } from "@/components/PageHero";

export const metadata: Metadata = { title: "FAQs" };

export default function FaqsPage() {
  return (
    <>
      <PageHero kicker="Resources" title="FAQs" text="Common questions about products, customization, and commercial engagement." />
      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <div className="space-y-4">
          {faqs.map((item) => (
            <details key={item.q} className="rounded-xl border border-slate-200 bg-white p-5">
              <summary className="cursor-pointer font-semibold text-brand-900">{item.q}</summary>
              <p className="mt-3 text-sm leading-6 text-slate-600">{item.a}</p>
            </details>
          ))}
        </div>
      </section>
    </>
  );
}
