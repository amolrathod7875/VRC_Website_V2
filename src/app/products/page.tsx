import type { Metadata } from "next";
import Link from "next/link";
import { productTree } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ProductNav } from "@/components/ProductNav";
import { Placeholder } from "@/components/Placeholder";

export const metadata: Metadata = { title: "Products" };

export default function ProductsPage() {
  return (
    <>
      <PageHero kicker="Portfolio" title="Products" text="Nested categories for protective, powder, and specialty coating systems." />
      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-[260px_1fr] lg:px-8">
        <ProductNav />
        <div className="grid gap-6 sm:grid-cols-2">
          {productTree.map((category) => (
            <Link
              key={category.slug}
              href={`/products/${category.slug}`}
              className="overflow-hidden rounded-xl border border-slate-200 bg-white hover:shadow-md"
            >
              <Placeholder label={`${category.name} image`} ratio="16 / 9" />
              <div className="p-5">
                <h2 className="text-lg font-semibold text-brand-900">{category.name}</h2>
                <p className="mt-2 text-sm text-slate-600">{category.summary}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
