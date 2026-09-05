import type { Metadata } from "next";
import Link from "next/link";
import { applications } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Applications" };

export default function ApplicationsPage() {
  return (
    <>
      <PageHero
        kicker="Markets"
        title="Applications"
        text="Industry uses for VR coating systems—from OEM lines to infrastructure maintenance."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {applications.map((item) => (
            <article key={item.slug} className="overflow-hidden rounded-xl border border-slate-200 bg-white">
              <Placeholder label={`${item.name} application thumbnail`} ratio="16 / 10" />
              <div className="p-5">
                <h2 className="text-lg font-semibold text-brand-900">{item.name}</h2>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
                <Link href="/contact" className="mt-4 inline-block text-sm font-semibold text-brand-700">
                  Discuss this application
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
