import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  findProduct,
  productCategories,
  type ProductCategory,
  type LandingProduct,
  landingProducts,
  findCatalogue,
  flattenProducts,
} from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ProductNav } from "@/components/ProductNav";
import { Placeholder } from "@/components/Placeholder";
import { IconArrowRight } from "@/components/Icon";
import { CatalogueLink } from "@/components/CatalogueLink";
import { ProductCatalogueHero } from "@/components/ProductCatalogueHero";
import { CatalogueVariantCard } from "@/components/CatalogueVariantCard";
import { CatalogueVariantRow, type CatalogueVariant as CatalogueVariantRowType } from "@/components/CatalogueVariantRow";
import { CatalogueDownloadCTA } from "@/components/CatalogueDownloadCTA";
import { SingleProductCatalogue } from "@/components/SingleProductCatalogue";
import { conventionalGunVariants, conventionalGunCatalogue } from "@/lib/conventionalGunsData";
import type { CatalogueVariant } from "@/components/CatalogueVariantCard";

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

function findLandingProduct(slug: string): LandingProduct | undefined {
  return landingProducts.find((p) => p.slug === slug);
}

function isLeafCategory(node: ProductCategory): boolean {
  return !node.children || node.children.length === 0;
}

function allChildrenAreLeaves(node: ProductCategory): boolean {
  if (!node.children || node.children.length === 0) return false;
  return node.children.every((child) => !child.children || child.children.length === 0);
}

function buildVariantFromCategoryNode(node: ProductCategory): CatalogueVariant {
  const landing = findLandingProduct(node.slug);
  const specs = landing?.specs?.map((spec) => ({ label: spec.label, value: spec.value })) || [];

  return {
    id: node.slug,
    name: node.name.toUpperCase(),
    image: node.image || "/Product_png_s/Flamingo 11817.png",
    alt: `${node.name} product image`,
    catalogueNote: landing?.overview || "Detailed technical specifications are available in the product catalogue.",
    specifications: specs,
  };
}

function getCategoryBreadcrumb(trail: ProductCategory[]): string {
  return trail.map((item) => item.name).join(" / ");
}

export function generateStaticParams() {
  const catSlugs = flattenCategories(productCategories).map(({ node }) => node.slug);
  const prodSlugs = flattenProducts().map(({ node }) => node.slug);
  const landingSlugs = landingProducts.map((p) => p.slug);
  const allSlugs = new Set([...catSlugs, ...prodSlugs, ...landingSlugs]);
  return Array.from(allSlugs).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const cat = findCategory(slug);
  const prod = findProduct(slug);
  const landing = findLandingProduct(slug);
  return { title: cat?.node.name ?? prod?.node.name ?? landing?.name ?? "Product" };
}

export default async function ProductDetailPage({ params }: Props) {
  const { slug } = await params;
  const cat = findCategory(slug);
  const prod = findProduct(slug);
  const landing = findLandingProduct(slug);

  if (!cat && !prod && !landing) notFound();

  if (cat) {
    const { node, trail } = cat;
    const breadcrumbs = getCategoryBreadcrumb(trail);
    const catalogue = findCatalogue(node.slug);

    if (node.slug === "conventional-guns") {
      const variants = conventionalGunVariants.map((v) => ({
        id: v.id,
        name: v.name,
        image: v.image,
        alt: v.alt,
        specifications: v.specifications,
        description: v.catalogueNote,
      }));

      return (
        <>
          <ProductCatalogueHero
            title={conventionalGunCatalogue.name}
            category={conventionalGunCatalogue.category}
            catalogue={conventionalGunCatalogue.catalogue}
            description={conventionalGunCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  {variants.map((variant, i) => (
                    <div key={variant.id} className="flex flex-col">
                      <CatalogueVariantRow variant={variant} index={i} />
                      {i < variants.length - 1 && (
                        <div className="my-8 h-px w-full bg-[rgba(22,120,200,0.20)]" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
          <CatalogueDownloadCTA catalogue={conventionalGunCatalogue.catalogue} />
        </>
      );
    }

    if (isLeafCategory(node) && catalogue) {
      const landingForNode = findLandingProduct(node.slug);
      return (
        <>
          <ProductCatalogueHero
            title={node.name.toUpperCase()}
            category={breadcrumbs}
            catalogue={catalogue}
             description={landingForNode?.description || ""}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <SingleProductCatalogue
                  title={node.name}
                  category={breadcrumbs}
                  catalogue={catalogue}
                  image={node.image}
                  alt={node.name}
                  description={landingForNode?.description}
                  overview={landingForNode?.overview}
                  features={landingForNode?.features}
                  specifications={landingForNode?.specs?.map((s) => ({ label: s.label, value: s.value }))}
                  applications={landingForNode?.applications}
                />
              </div>
            </div>
          </section>
          <CatalogueDownloadCTA catalogue={catalogue} />
        </>
      );
    }

    if (allChildrenAreLeaves(node)) {
      const variants = node.children!.map((child) => buildVariantFromCategoryNode(child));
      return (
        <>
          <ProductCatalogueHero
            title={`${node.name.toUpperCase()} CATALOGUE`}
            category={breadcrumbs}
            catalogue={catalogue || ""}
             description={`Explore the ${node.name} product family.`}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="grid gap-6 sm:grid-cols-2">
                  {variants.map((variant, i) => (
                    <CatalogueVariantCard key={variant.id} variant={variant} index={i} />
                  ))}
                </div>
              </div>
            </div>
          </section>
          {catalogue && <CatalogueDownloadCTA catalogue={catalogue} />}
        </>
      );
    }

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

  if (landing) {
    const breadcrumbs = landing.category ? `Products / ${landing.category}` : "Products";
    const catalogue = findCatalogue(landing.slug);

    return (
      <>
        <ProductCatalogueHero
          title={landing.name.toUpperCase()}
          category={breadcrumbs}
          catalogue={catalogue || ""}
          description={landing.description}
        />
        <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
            <nav aria-label="Product Categories" className="pt-8">
              <ProductNav />
            </nav>
            <div className="py-8">
              <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
              <SingleProductCatalogue
                title={landing.name}
                category={breadcrumbs}
                catalogue={catalogue || ""}
                image={landing.image || null}
                alt={landing.name}
                description={landing.description}
                overview={landing.overview}
                features={landing.features}
                specifications={landing.specs?.map((s) => ({ label: s.label, value: s.value }))}
                applications={landing.applications}
              />
            </div>
          </div>
        </section>
        {catalogue && <CatalogueDownloadCTA catalogue={catalogue} />}
      </>
    );
  }

  if (!prod) notFound();

  const { node, trail } = prod;
  const breadcrumbs = trail.map((item: { name: string }) => item.name).join(" / ");
  const catalogue = findCatalogue(node.slug);

  return (
    <>
      <ProductCatalogueHero
        title={node.name.toUpperCase()}
        category={breadcrumbs}
        catalogue={catalogue || ""}
        description={node.summary || ""}
      />
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
          <nav aria-label="Product Categories" className="pt-8">
            <ProductNav />
          </nav>
          <div className="py-8">
            <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
            <SingleProductCatalogue
              title={node.name}
              category={breadcrumbs}
              catalogue={catalogue || ""}
              image={node.image || null}
              alt={node.name}
              description={node.summary}
            />
          </div>
        </div>
      </section>
      {catalogue && <CatalogueDownloadCTA catalogue={catalogue} />}
    </>
  );
}
