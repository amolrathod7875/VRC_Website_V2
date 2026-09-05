import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { findProduct, flattenProducts } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ProductNav } from "@/components/ProductNav";
import { Placeholder } from "@/components/Placeholder";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return flattenProducts().map(({ node }) => ({ slug: node.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const found = findProduct(slug);
  return { title: found?.node.name ?? "Product" };
}

export default async function ProductDetailPage({ params }: Props) {
  const { slug } = await params;
  const found = findProduct(slug);
  if (!found) notFound();
  const { node, trail } = found;

  return (
    <>
      <PageHero kicker="Products" title={node.name} text={node.summary} />
      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-[260px_1fr] lg:px-8">
        <ProductNav />
        <div>
          <p className="mb-4 text-sm text-slate-500">
            {trail.map((item, i) => (
              <span key={item.slug}>
                {i > 0 && " / "}
                <Link href={`/products/${item.slug}`} className="hover:text-brand-700">
                  {item.name}
                </Link>
              </span>
            ))}
          </p>
          <Placeholder label={`${node.name} product image`} className="mb-8 min-h-[280px] rounded-xl" />
          {node.children ? (
            <div className="grid gap-4 sm:grid-cols-2">
              {node.children.map((child) => (
                <Link
                  key={child.slug}
                  href={`/products/${child.slug}`}
                  className="rounded-lg border border-slate-200 bg-white p-5 hover:border-brand-200"
                >
                  <h2 className="font-semibold text-brand-900">{child.name}</h2>
                  <p className="mt-2 text-sm text-slate-600">{child.summary}</p>
                </Link>
              ))}
            </div>
          ) : (
            <div className="prose max-w-none text-sm leading-7 text-slate-600">
              <p>
                Technical data sheets, MSDS, and colour cards will be uploaded here. Until then, this page holds
                structured product copy and a placeholder for photography.
              </p>
              <Link href="/contact" className="mt-4 inline-flex font-semibold text-brand-700">
                Request a sample or datasheet
              </Link>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
