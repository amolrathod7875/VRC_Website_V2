import type { Metadata } from "next";
import { productCategories } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ProductNav } from "@/components/ProductNav";
import { Placeholder } from "@/components/Placeholder";
import Link from "next/link";

export const metadata: Metadata = { title: "Products" };

export default function ProductsPage() {
  return (
    <>
      <PageHero
        kicker="Portfolio"
        title="Products"
        text="Category-wise product listing for industrial coating, spray equipment, pumps, and accessories."
      />
      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-[250px_1fr] lg:gap-10 lg:px-8">
        <nav aria-label="Product Categories" className="pt-px">
          <ProductNav />
        </nav>
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          {productCategories.map((category) => (
              <Link
                key={category.slug}
                href={`/products/${category.slug}`}
                className="group flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white hover:shadow-md"
              >
                <div className="flex h-48 items-center justify-center overflow-hidden p-4 sm:h-56">
                  {category.image ? (
                    <img
                      src={category.image}
                      alt={category.name}
                      className="max-h-full max-w-full object-contain group-hover:opacity-90"
                    />
                  ) : (
                    <Placeholder
                      label={`${category.name} image`}
                      className="h-full w-full group-hover:opacity-90"
                    />
                  )}
                </div>
              <div className="flex flex-1 flex-col p-5">
                <h2 className="text-lg font-semibold text-brand-900">{category.name}</h2>
                {category.children && category.children.length > 0 && (
                  <p className="mt-2 text-sm text-slate-500">
                    {category.children.length} categor{category.children.length === 1 ? "y" : "ies"}
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
