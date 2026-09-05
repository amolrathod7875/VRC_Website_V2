import type { Metadata } from "next";
import Link from "next/link";
import { PageHero } from "@/components/PageHero";

export const metadata: Metadata = { title: "Career" };

const roles = [
  { title: "Coatings Chemist", location: "Pune, India", type: "Full-time" },
  { title: "Application Engineer", location: "Troy, MI", type: "Full-time" },
  { title: "Quality Analyst", location: "Chakan Factory", type: "Full-time" },
];

export default function CareerPage() {
  return (
    <>
      <PageHero kicker="Resources" title="Career" text="Join formulation, manufacturing, and technical service teams." />
      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <div className="space-y-4">
          {roles.map((role) => (
            <article key={role.title} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white p-5">
              <div>
                <h2 className="font-semibold text-brand-900">{role.title}</h2>
                <p className="text-sm text-slate-600">
                  {role.location} · {role.type}
                </p>
              </div>
              <Link href="/contact" className="rounded-md bg-brand-700 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-600">
                Apply
              </Link>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
