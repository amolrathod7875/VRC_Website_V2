import type { Metadata } from "next";
import Link from "next/link";
import { applications } from "@/lib/data";
import { PageHero } from "@/components/PageHero";

export const metadata: Metadata = { title: "Industries We Serve" };

function applicationAltText(name: string): string {
  switch (name) {
    case "Automotive":
      return "Automotive industrial coating application";
    case "Defence & Aerospace":
      return "Defence and aerospace coating application";
    case "Electronics":
      return "Electronics coating application";
    case "Infrastructure":
      return "Infrastructure coating application";
    case "Marine":
      return "Marine coating application";
    case "Energy & Process":
      return "Energy and process industry coating application";
    default:
      return name;
  }
}

export default function IndustriesPage() {
  return (
    <>
      <PageHero kicker="Our Assets" title="Industries we serve" text="Cross-sector coating programmes with shared quality systems and local support." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 md:grid-cols-2">
          {applications.map((item) => (
            <Link
              key={item.slug}
              href={`/applications/${item.slug}`}
              className="group grid gap-0 overflow-hidden rounded-xl border border-slate-200 bg-white transition-all duration-300 hover:border-brand-400 hover:shadow-lg hover:-translate-y-0.5 sm:grid-cols-[28%_1fr]"
            >
              <div className="relative overflow-hidden min-h-[160px] sm:min-h-0">
                <img
                  src={item.image}
                  alt={applicationAltText(item.name)}
                  className="h-full w-full object-cover object-center transition-transform duration-300 group-hover:scale-[1.02]"
                  loading="lazy"
                />
              </div>
              <div className="p-5">
                <h2 className="font-semibold text-brand-900">{item.name}</h2>
                <p className="mt-2 text-sm text-slate-600">{item.text}</p>
                <div className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-700 transition-transform duration-300 group-hover:translate-x-1">
                  <span>See applications</span>
                  <svg
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="h-4 w-4"
                  >
                    <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
