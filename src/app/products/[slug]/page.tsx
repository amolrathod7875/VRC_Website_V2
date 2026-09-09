import type { Metadata } from "next";
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
import { ProductCatalogueHero } from "@/components/ProductCatalogueHero";
import { CatalogueVariantRow } from "@/components/CatalogueVariantRow";
import { CatalogueDownloadCTA } from "@/components/CatalogueDownloadCTA";
import { CatalogueSingleProduct } from "@/components/CatalogueSingleProduct";
import { CatalogueVariantList, CatalogueSingleProductPage } from "@/components/CataloguePageShell";
import { conventionalGunVariants, conventionalGunCatalogue } from "@/lib/conventionalGunsData";
import { manualGunProducts, manualGunCatalogue } from "@/lib/manualGunsData";
import type { CatalogueVariant } from "@/components/CatalogueVariantRow";

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
    description: landing?.overview,
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
        <CatalogueVariantList
          title={conventionalGunCatalogue.name}
          category={conventionalGunCatalogue.category}
          catalogue={conventionalGunCatalogue.catalogue}
          description={conventionalGunCatalogue.description}
          breadcrumb={breadcrumbs}
          variants={variants}
        />
      );
    }

    if (node.slug === "manual-guns") {
      const variants = manualGunProducts.map((v) => ({
        id: v.id,
        name: v.name,
        image: v.image,
        alt: v.alt,
        specifications: v.specifications,
        description: v.description,
      }));

      return (
        <CatalogueVariantList
          title={manualGunCatalogue.name}
          category={manualGunCatalogue.category}
          catalogue={manualGunCatalogue.catalogue}
          description={manualGunCatalogue.description}
          breadcrumb={breadcrumbs}
          variants={variants}
        />
      );
    }

    if (isLeafCategory(node)) {
      const landingForNode = findLandingProduct(node.slug);
      const specs = landingForNode?.specs?.map((s) => ({ label: s.label, value: s.value }));

      return (
        <CatalogueSingleProductPage
          title={node.name.toUpperCase()}
          category={breadcrumbs}
          catalogue={catalogue || ""}
          image={node.image}
          alt={node.name}
          description={landingForNode?.description || landingForNode?.overview}
          specifications={specs}
          breadcrumb={breadcrumbs}
        />
      );
    }

    if (allChildrenAreLeaves(node)) {
      const variants = node.children!.map((child) => buildVariantFromCategoryNode(child));

      return (
        <CatalogueVariantList
          title={`${node.name.toUpperCase()} CATALOGUE`}
          category={breadcrumbs}
          catalogue={catalogue || ""}
          description={`Explore the ${node.name} product family.`}
          breadcrumb={breadcrumbs}
          variants={variants}
        />
      );
    }

    const landingForNode = findLandingProduct(node.slug);
    const specs = landingForNode?.specs?.map((s) => ({ label: s.label, value: s.value }));

    return (
      <CatalogueSingleProductPage
        title={node.name.toUpperCase()}
        category={breadcrumbs}
        catalogue={catalogue || ""}
        image={node.image}
        alt={node.name}
        description={landingForNode?.description || landingForNode?.overview}
        specifications={specs}
        breadcrumb={breadcrumbs}
      />
    );
  }

  if (landing) {
    const breadcrumbs = landing.category ? `Products / ${landing.category}` : "Products";
    const catalogue = findCatalogue(landing.slug);

    return (
      <CatalogueSingleProductPage
        title={landing.name.toUpperCase()}
        category={breadcrumbs}
        catalogue={catalogue || ""}
        image={landing.image || null}
        alt={landing.name}
        description={landing.description}
        specifications={landing.specs?.map((s) => ({ label: s.label, value: s.value }))}
        features={landing.features}
        applications={landing.applications}
        breadcrumb={breadcrumbs}
      />
    );
  }

  if (!prod) notFound();

  const { node, trail } = prod;
  const breadcrumbs = trail.map((item: { name: string }) => item.name).join(" / ");
  const catalogue = findCatalogue(node.slug);

  return (
    <CatalogueSingleProductPage
      title={node.name.toUpperCase()}
      category={breadcrumbs}
      catalogue={catalogue || ""}
      image={node.image || null}
      alt={node.name}
      description={node.summary}
      breadcrumb={breadcrumbs}
    />
  );
}
