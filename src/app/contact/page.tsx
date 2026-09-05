import type { Metadata } from "next";
import { companyEmail, offices } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { InquiryForm } from "@/components/InquiryForm";

export const metadata: Metadata = { title: "Contact Us" };

export default function ContactPage() {
  return (
    <>
      <PageHero kicker="Get in touch" title="Contact Us" text="Send an inquiry or reach a regional office directly." />
      <section className="mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:px-8">
        <div className="rounded-xl border border-slate-200 bg-white p-6">
          <h2 className="mb-6 text-xl font-semibold text-brand-900">Inquiry form</h2>
          <InquiryForm />
        </div>
        <div className="rounded-xl bg-surface p-6">
          <h2 className="mb-6 text-xl font-semibold text-brand-900">Addresses</h2>
          <div className="space-y-6">
            {offices.map((office) => (
              <div key={office.title}>
                <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-brand-700">{office.title}</h3>
                {office.lines.map((line) => (
                  <p key={line} className="text-sm leading-6 text-slate-600">
                    {line}
                  </p>
                ))}
                <a href={office.phoneHref} className="mt-1 inline-block text-sm font-semibold text-brand-800">
                  {office.phone}
                </a>
              </div>
            ))}
            <a href={`mailto:${companyEmail}`} className="inline-block text-sm font-semibold text-brand-800">
              {companyEmail}
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
