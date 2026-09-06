import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { findProduct, productCategories, type ProductCategory, findCatalogue } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ProductNav } from "@/components/ProductNav";
import { Placeholder } from "@/components/Placeholder";
import { IconArrowRight } from "@/components/Icon";
import { CatalogueLink } from "@/components/CatalogueLink";

type Props = { params: Promise<{ slug: string }> };

function flattenCategories(
  nodes: ProductCategory[],
  trail: ProductCategory[] = []
): { node: ProductCategory; trail: ProductCategory[] }[] {
  return nodes.flatMap((node) => {
    const next = [...trail, node];
    const self = [{ node, trail: next }];
    return node.children ? [...self, ...flattenCategories(node.children, next)] : self;
  });
}

function findCategory(slug: string) {
  return flattenCategories(productCategories).find((entry) => entry.node.slug === slug);
}

export function generateStaticParams() {
  return flattenCategories(productCategories).map(({ node }) => ({ slug: node.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const cat = findCategory(slug);
  const prod = findProduct(slug);
  return { title: cat?.node.name ?? prod?.node.name ?? "Product" };
}

export default async function ProductDetailPage({ params }: Props) {
  const { slug } = await params;
  const cat = findCategory(slug);
  const prod = findProduct(slug);

  if (!cat && !prod) notFound();

  if (cat) {
    const { node, trail } = cat;
    const breadcrumbs = trail.map((item) => item.name).join(" / ");
    return (
      <>
        <PageHero kicker="Products" title={node.name} text={breadcrumbs} />
        <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-[250px_1fr] lg:gap-10 lg:px-8">
          <nav aria-label="Product Categories" className="pt-px">
            <ProductNav />
          </nav>
          <div>
            <p className="mb-4 text-sm text-slate-500">{breadcrumbs}</p>
            {node.image ? (
                <img
                  src={node.image}
                  alt={node.name}
                  className="mb-8 aspect-[16/9] w-full rounded-xl object-contain object-center"
                />
              ) : (
                <Placeholder
                  label={`${node.name} image`}
                  ratio="16 / 9"
                  className="mb-8 rounded-xl"
                />
              )}
            {node.children && node.children.length > 0 ? (
              <div className="grid gap-4 sm:grid-cols-2">
                {node.children.map((child) => (
                  <Link
                    key={child.slug}
                    href={`/products/${child.slug}`}
                    className="group relative flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white p-5 transition hover:border-brand-200 hover:shadow-sm"
                  >
                    <h2 className="text-lg font-semibold text-brand-900 group-hover:text-brand-700">
                      {child.name}
                    </h2>
                    {child.children && child.children.length > 0 && (
                      <p className="mt-2 text-sm text-slate-500">
                        {child.children.length} categor{child.children.length === 1 ? "y" : "ies"}
                      </p>
                    )}
                    {child.catalogue && (
                      <span
                        aria-label={`Catalogue available for ${child.name}`}
                        className="absolute right-2 top-2 rounded-md bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold text-slate-600"
                      >
                        PDF
                      </span>
                    )}
                  </Link>
                ))}
              </div>
            ) : (
              <div className="prose max-w-none text-sm leading-7 text-slate-600">
                <p>
                  Technical data sheets, MSDS, and detailed specifications will be uploaded here. Until
                  then, this page holds structured product information for {node.name}.
                </p>
                <Link
                  href="/contact"
                  className="mt-4 inline-flex items-center gap-1.5 font-semibold text-brand-700"
                >
                  Request a datasheet
                  <IconArrowRight className="h-3.5 w-3.5" />
                </Link>
                {node.catalogue && <CatalogueLink catalogue={node.catalogue} />}
              </div>
            )}
          </div>
        </section>
      </>
    );
  }

  if (!prod) notFound();

  const { node, trail } = prod;
  return (
    <>
      <PageHero kicker="Products" title={node.name} text={node.summary} />
      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-[250px_1fr] lg:gap-10 lg:px-8">
        <nav aria-label="Product Categories" className="pt-px">
          <ProductNav />
        </nav>
        <div>
          <p className="mb-4 text-sm text-slate-500">
            {trail.map((item: { name: string }) => item.name).join(" / ")}
          </p>
          {node.image ? (
            <img
              src={node.image}
              alt={node.name}
              className="mb-8 aspect-[16/9] w-full rounded-xl object-contain object-center"
            />
          ) : (
            <Placeholder
              label={`${node.name} image`}
              ratio="16 / 9"
              className="mb-8 rounded-xl"
            />
          )}
          <div className="prose max-w-none text-sm leading-7 text-slate-600">
            <p>{node.summary || "Detailed technical specifications coming soon."}</p>
            <Link
              href="/contact"
              className="mt-4 inline-flex items-center gap-1.5 font-semibold text-brand-700"
            >
              Request a datasheet
              <IconArrowRight className="h-3.5 w-3.5" />
            </Link>
            {findCatalogue(node.slug) && <CatalogueLink catalogue={findCatalogue(node.slug)} />}
          </div>
        </div>
      </section>
    </>
  );
}
