import { ProductNav } from "@/components/ProductNav";
import { ProductCatalogueHero } from "@/components/ProductCatalogueHero";
import { CatalogueDownloadCTA } from "@/components/CatalogueDownloadCTA";
import { CatalogueVariantRow } from "@/components/CatalogueVariantRow";
import { CatalogueSingleProduct } from "@/components/CatalogueSingleProduct";
import type { CatalogueVariant } from "@/components/CatalogueVariantRow";

type CatalogueProductPageProps = {
  title: string;
  category: string;
  catalogue: string;
  description?: string;
  breadcrumb?: string;
  children?: React.ReactNode;
};

export function CatalogueProductPage({
  title,
  category,
  catalogue,
  description,
  breadcrumb,
  children,
}: CatalogueProductPageProps) {
  const hasCatalogue = Boolean(catalogue);

  return (
    <>
      <ProductCatalogueHero
        title={title}
        category={category}
        catalogue={catalogue}
        description={description}
      />
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
          <nav aria-label="Product Categories" className="pt-8">
            <ProductNav />
          </nav>
          <div className="py-8">
            {breadcrumb ? (
              <p className="mb-6 text-sm text-slate-500">{breadcrumb}</p>
            ) : null}
            {children}
          </div>
        </div>
      </section>
      {hasCatalogue && <CatalogueDownloadCTA catalogue={catalogue} />}
    </>
  );
}

type CatalogueVariantListProps = {
  title: string;
  category: string;
  catalogue: string;
  description?: string;
  breadcrumb?: string;
  variants: CatalogueVariant[];
};

export function CatalogueVariantList({
  title,
  category,
  catalogue,
  description,
  breadcrumb,
  variants,
}: CatalogueVariantListProps) {
  return (
    <CatalogueProductPage
      title={title}
      category={category}
      catalogue={catalogue}
      description={description}
      breadcrumb={breadcrumb}
    >
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
    </CatalogueProductPage>
  );
}

type CatalogueSingleProductPageProps = {
  title: string;
  category: string;
  catalogue: string;
  image: string | null | undefined;
  alt: string;
  description?: string;
  specifications?: { label: string; value: string }[];
  breadcrumb?: string;
};

export function CatalogueSingleProductPage({
  title,
  category,
  catalogue,
  image,
  alt,
  description,
  specifications,
  breadcrumb,
}: CatalogueSingleProductPageProps) {
  return (
    <CatalogueProductPage
      title={title}
      category={category}
      catalogue={catalogue}
      description={description}
      breadcrumb={breadcrumb}
    >
      <CatalogueSingleProduct
        title={title}
        image={image}
        alt={alt}
        description={description}
        specifications={specifications}
      />
    </CatalogueProductPage>
  );
}
