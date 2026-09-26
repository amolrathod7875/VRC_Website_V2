"use client";

import { CatalogueVariantRow } from "@/components/CatalogueVariantRow";
import { CatalogueDownloadCTA } from "@/components/CatalogueDownloadCTA";
import { ProductCatalogueHero } from "@/components/ProductCatalogueHero";
import { ProductNav } from "@/components/ProductNav";
import { stirrerVariants, stirrerCatalogue } from "@/lib/stirrerData";
import type { CatalogueVariant } from "@/components/CatalogueVariantRow";

export function StirrerCataloguePage() {
  const variants: CatalogueVariant[] = stirrerVariants.map((v) => ({
    id: v.id,
    name: v.name,
    image: "/Product_png_s/pneumatic_stirrer.png",
    alt: v.name,
    specifications: [
      { label: "MOTOR TYPE", value: v.motorType },
      { label: "CONTAINER SIZE", value: v.containerSize },
      { label: "PART NUMBER", value: v.partNumber },
      { label: "SHAFT LENGTH", value: `${v.shaftLength} MM` },
      { label: "FAN DIAMETER", value: `${v.fanDiameter} MM` },
    ],
  }));

  return (
    <>
      <ProductCatalogueHero
        title={stirrerCatalogue.name}
        category={stirrerCatalogue.category}
        catalogue={stirrerCatalogue.catalogue}
        description={stirrerCatalogue.description}
      />
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
          <nav aria-label="Product Categories" className="pt-8">
            <ProductNav />
          </nav>
          <div className="py-8">
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
      <CatalogueDownloadCTA catalogue={stirrerCatalogue.catalogue} />
    </>
  );
}
