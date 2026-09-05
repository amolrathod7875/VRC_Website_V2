import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { findIndustry, industries } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { IconArrowRight } from "@/components/Icon";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return industries.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const found = findIndustry(slug);
  return { title: found?.name ? `${found.name} — Services` : "Service" };
}

export default async function ServiceDetailPage({ params }: Props) {
  const { slug } = await params;
  const found = findIndustry(slug);
  if (!found) notFound();

  return (
    <>
      <PageHero kicker="Services" title={found.name} />
      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
        <div className="rounded-xl border border-slate-200 bg-white p-8">
          <p className="text-base leading-7 text-slate-600">Service details coming soon.</p>
        </div>
        <div className="mt-8">
          <Link
            href="/services"
            className="inline-flex items-center gap-2 rounded-md border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-brand-700 transition-colors duration-200 hover:border-[#1678C8] hover:text-[#0B5C97]"
          >
            <IconArrowRight className="h-3.5 w-3.5 rotate-180" />
            Back to Services
          </Link>
        </div>
      </section>
    </>
  );
}
