import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Certifications" };

const certs = ["ISO 9001:2015", "ISO 14001:2015", "IATF 16949", "Qualicoat aligned processes"];

export default function CertificationsPage() {
  return (
    <>
      <PageHero kicker="Resources" title="Certifications" text="Quality and environmental certificates will replace these placeholders." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {certs.map((name) => (
            <article key={name} className="rounded-xl border border-slate-200 bg-white p-5 text-center">
              <Placeholder label={`${name} certificate`} className="mx-auto h-40 rounded-md" />
              <h2 className="mt-4 text-sm font-semibold text-brand-900">{name}</h2>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
