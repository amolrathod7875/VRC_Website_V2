import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Blog" };

const posts = [
  { title: "Surface preparation that actually lasts", date: "12 Aug 2026", excerpt: "Why blast profile and soluble salts decide coating life more than topcoat colour." },
  { title: "Choosing zinc primers for coastal steel", date: "28 Jul 2026", excerpt: "Inorganic vs organic zinc, overcoating windows, and common field failures." },
  { title: "Powder vs liquid for OEM housings", date: "04 Jul 2026", excerpt: "Throughput, film build, and repair strategy when both chemistries are viable." },
];

export default function BlogPage() {
  return (
    <>
      <PageHero kicker="Resources" title="Blog" text="Technical notes and process guidance. Imagery is placeholder until photography is added." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-3">
          {posts.map((post) => (
            <article key={post.title} className="overflow-hidden rounded-xl border border-slate-200 bg-white">
              <Placeholder label="Blog cover image" ratio="16 / 9" />
              <div className="p-5">
                <p className="text-xs uppercase tracking-wider text-brand-600">{post.date}</p>
                <h2 className="mt-2 text-lg font-semibold text-brand-900">{post.title}</h2>
                <p className="mt-2 text-sm text-slate-600">{post.excerpt}</p>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
