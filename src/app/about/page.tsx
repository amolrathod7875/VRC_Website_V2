import type { Metadata } from "next";
import { weProvide } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "About Us" };

export default function AboutPage() {
  return (
    <>
      <PageHero
        kicker="About"
        title="About VR Coatings Pvt. Ltd."
        text="An industrial coatings manufacturer focused on protective performance, process reliability, and long-term partnership."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <Placeholder label="Infrastructure / factory photo" className="min-h-[320px] rounded-xl lg:min-h-[420px]" />
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-brand-700">Infrastructure</p>
            <h2 className="mt-2 text-3xl font-semibold text-brand-950">Built for scale and consistency</h2>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              Our manufacturing campus houses resin processing, mill rooms, powder extrusion, quality laboratories,
              and climate-controlled storage. Production cells are organised for batch traceability, while application
              labs replicate customer lines so recommendations are grounded in real process conditions.
            </p>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              Head office, factory, and North America operations work as one supply network—so specification,
              sampling, and fulfilment stay aligned from first trial to serial production.
            </p>
          </div>
        </div>
      </section>
      <section className="bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <h2 className="mb-8 text-3xl font-semibold text-brand-950">We provide</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {weProvide.map((item) => (
              <article key={item.title} className="rounded-xl border border-slate-200 bg-white p-6">
                <Placeholder label={`${item.title} icon`} className="mb-4 h-14 w-14 rounded-lg" />
                <h3 className="font-semibold text-brand-900">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
