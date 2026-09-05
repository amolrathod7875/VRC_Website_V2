import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";

export const metadata: Metadata = { title: "News" };

const items = [
  { date: "02 Sep 2026", title: "North America technical desk expansion", body: "Additional application engineers now support OEM trials from the Troy office." },
  { date: "15 Jun 2026", title: "High-temperature range in scale-up", body: "ThermoGuard 900 enters pre-commercial sampling for exhaust and furnace equipment." },
  { date: "21 Mar 2026", title: "Chakan line capacity upgrade", body: "Powder extrusion capacity increased to support architectural programme volumes." },
];

export default function NewsPage() {
  return (
    <>
      <PageHero kicker="Resources" title="News" text="Company announcements and product milestones." />
      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <ul className="space-y-6">
          {items.map((item) => (
            <li key={item.title} className="rounded-xl border border-slate-200 bg-white p-6">
              <p className="text-xs uppercase tracking-wider text-brand-600">{item.date}</p>
              <h2 className="mt-2 text-lg font-semibold text-brand-900">{item.title}</h2>
              <p className="mt-2 text-sm text-slate-600">{item.body}</p>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
