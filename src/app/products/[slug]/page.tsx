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
import { ProductNav } from "@/components/ProductNav";
import { conventionalGunVariants, conventionalGunCatalogue } from "@/lib/conventionalGunsData";
import { manualGunProducts, manualGunCatalogue } from "@/lib/manualGunsData";
import { automaticGunProducts, automaticGunCatalogue } from "@/lib/automaticGunsData";
import { tigerCatalogue, tigerFeatures } from "@/lib/tigerData";
import { miniTigerCatalogue, miniTigerFeatures } from "@/lib/miniTigerData";
import { rhinoCatalogue, rhinoFeatures } from "@/lib/rhinoData";
import { hippoCatalogue, hippoFeatures } from "@/lib/hippoData";
import { dragonCatalogue, dragonFeatures } from "@/lib/dragonData";
import { stirrerCatalogue, stirrerFeatures } from "@/lib/stirrerData";
import { valveCatalogue } from "@/lib/valvesData";
import { filterCatalogue, filterFeatures } from "@/lib/filtersCatalogueData";
import { polyureaCatalogue, polyureaFeatures } from "@/lib/polyureaData";
import { cheetahCatalogue, cheetahFeatures } from "@/lib/cheetahData";
import { vrcMixHpCatalogue, vrcMixHpFeatures } from "@/lib/vrcMixHpData";
import { barrelPumpCatalogue, barrelPumpFeatures } from "@/lib/barrelPumpData";
import { portablePressureFeedPotCatalogue, portablePressureFeedPotFeatures } from "@/lib/portablePressureFeedPotData";
import { cubCatalogue, cubFeatures } from "@/lib/cubData";
import { elephantCatalogue, elephantFeatures } from "@/lib/elephantData";
import { turbineCatalogue, turbineFeatures } from "@/lib/turbineData";
import { TigerFeatures, TigerApplications, TigerTechnicalSpecifications } from "@/components/TigerCataloguePage";
import { MiniTigerApplications, MiniTigerTechnicalSpecifications } from "@/components/MiniTigerCataloguePage";
import { RhinoApplications, RhinoTechnicalSpecifications } from "@/components/RhinoCataloguePage";
import { HippoApplications, HippoTechnicalSpecifications } from "@/components/HippoCataloguePage";
import { DragonApplications, DragonTechnicalSpecifications } from "@/components/DragonCataloguePage";
import { PolyureaApplications, PolyureaTechnicalSpecifications } from "@/components/PolyureaCataloguePage";
import { CheetahFeatures, CheetahApplications, CheetahTechnicalSpecifications } from "@/components/CheetahCataloguePage";
import { VrcMixHpFeatures, VrcMixHpApplications, VrcMixHpTechnicalSpecifications, VrcMixHpFaultTable } from "@/components/VrcMixHpCataloguePage";
import { CubFeatures, CubApplications, CubTechnicalSpecifications } from "@/components/CubCataloguePage";
import { ElephantFeatures, ElephantApplications, ElephantTechnicalSpecifications } from "@/components/ElephantCataloguePage";
import { TurbineFeatures, TurbineApplications, TurbineTechnicalSpecifications } from "@/components/TurbineCataloguePage";
import { BarrelPumpFeatures, BarrelPumpApplications, BarrelPumpTechnicalSpecifications } from "@/components/BarrelPumpCataloguePage";
import { PortablePressureFeedPotFeatures, PortablePressureFeedPotApplications, PortablePressureFeedPotTechnicalSpecifications } from "@/components/PortablePressureFeedPotCataloguePage";
import { drumCatalogue, drumFeatures, drumApplications, drumSpecRows, drumSpecColumns } from "@/lib/drumData";
import { DrumApplications, DrumTechnicalSpecifications } from "@/components/DrumCataloguePage";
import { StirrerCataloguePage } from "@/components/StirrerCataloguePage";
import { PneumaticStirrerFeatures, PneumaticStirrerVariants } from "@/components/PneumaticStirrerCataloguePage";
import { FiltersFeatures, FiltersTechnicalSpecifications } from "@/components/FiltersCataloguePage";
import { ValvesCataloguePage } from "@/components/ValvesCataloguePage";
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

    if (node.slug === "automatic-guns") {
      const variants = automaticGunProducts.map((v) => ({
        id: v.id,
        name: v.name,
        image: v.image,
        alt: v.alt,
        specifications: v.specifications,
        description: v.description,
      }));

      return (
        <CatalogueVariantList
          title={automaticGunCatalogue.name}
          category={automaticGunCatalogue.category}
          catalogue={automaticGunCatalogue.catalogue}
          description={automaticGunCatalogue.description}
          breadcrumb={breadcrumbs}
          variants={variants}
        />
      );
    }

    if (node.slug === "tiger") {
      return (
        <>
          <ProductCatalogueHero
            title={tigerCatalogue.name}
            category={tigerCatalogue.category}
            catalogue={tigerCatalogue.catalogue}
            description={tigerCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={tigerCatalogue.description}
                    specifications={[]}
                    features={tigerFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <TigerApplications />
          <TigerTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={tigerCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "mini-tiger") {
      return (
        <>
          <ProductCatalogueHero
            title={miniTigerCatalogue.name}
            category={miniTigerCatalogue.category}
            catalogue={miniTigerCatalogue.catalogue}
            description={miniTigerCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={miniTigerCatalogue.description}
                    specifications={[]}
                    features={miniTigerFeatures.map((f) => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <MiniTigerApplications />
          <MiniTigerTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={miniTigerCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "rhino") {
      return (
        <>
          <ProductCatalogueHero
            title={rhinoCatalogue.name}
            category={rhinoCatalogue.category}
            catalogue={rhinoCatalogue.catalogue}
            description={rhinoCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={rhinoCatalogue.description}
                    specifications={[]}
                    features={rhinoFeatures.map((f) => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <RhinoApplications />
          <RhinoTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={rhinoCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "hippo" || node.slug === "hippo-pump") {
      const hippoImage = "/Product_png_s/Hippo.png";
      return (
        <>
          <ProductCatalogueHero
            title={hippoCatalogue.name}
            category={hippoCatalogue.category}
            catalogue={hippoCatalogue.catalogue}
            description={hippoCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={hippoImage}
                    alt={node.name}
                    description={hippoCatalogue.description}
                    specifications={[]}
                    features={hippoFeatures.map((f) => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <HippoApplications />
          <HippoTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={hippoCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "dragon") {
      return (
        <>
          <ProductCatalogueHero
            title={dragonCatalogue.name}
            category={dragonCatalogue.category}
            catalogue={dragonCatalogue.catalogue}
            description={dragonCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={dragonCatalogue.description}
                    specifications={[]}
                    features={dragonFeatures.map((f) => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <DragonApplications />
          <DragonTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={dragonCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "polyurea") {
      return (
        <>
          <ProductCatalogueHero
            title={polyureaCatalogue.name}
            category={polyureaCatalogue.category}
            catalogue={polyureaCatalogue.catalogue}
            description={polyureaCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={polyureaCatalogue.description}
                    specifications={[]}
                    features={polyureaFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <PolyureaApplications />
          <PolyureaTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={polyureaCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "cheetah") {
      return (
        <>
          <ProductCatalogueHero
            title={cheetahCatalogue.name}
            category={cheetahCatalogue.category}
            catalogue={cheetahCatalogue.catalogue}
            description={cheetahCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={cheetahCatalogue.description}
                    specifications={[]}
                    features={cheetahFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <CheetahApplications />
          <CheetahTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={cheetahCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "vrc-mix-hp") {
      return (
        <>
          <ProductCatalogueHero
            title={vrcMixHpCatalogue.name}
            category={vrcMixHpCatalogue.category}
            catalogue={vrcMixHpCatalogue.catalogue}
            description={vrcMixHpCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={vrcMixHpCatalogue.description}
                    specifications={[]}
                    features={vrcMixHpFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <VrcMixHpApplications />
          <VrcMixHpTechnicalSpecifications />
          <VrcMixHpFaultTable />
          <CatalogueDownloadCTA catalogue={vrcMixHpCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "barrel-pump") {
      return (
        <>
          <ProductCatalogueHero
            title={barrelPumpCatalogue.name}
            category={barrelPumpCatalogue.category}
            catalogue={barrelPumpCatalogue.catalogue}
            description={barrelPumpCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={barrelPumpCatalogue.description}
                    specifications={[]}
                    features={barrelPumpFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <BarrelPumpFeatures />
          <BarrelPumpApplications />
          <BarrelPumpTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={barrelPumpCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "portable-pressure-feed-pot") {
      return (
        <>
          <ProductCatalogueHero
            title={portablePressureFeedPotCatalogue.name}
            category={portablePressureFeedPotCatalogue.category}
            catalogue={portablePressureFeedPotCatalogue.catalogue}
            description={portablePressureFeedPotCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={portablePressureFeedPotCatalogue.description}
                    specifications={[]}
                    features={portablePressureFeedPotFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <PortablePressureFeedPotFeatures />
          <PortablePressureFeedPotApplications />
          <PortablePressureFeedPotTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={portablePressureFeedPotCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "cub") {
      return (
        <>
          <ProductCatalogueHero
            title={cubCatalogue.name}
            category={cubCatalogue.category}
            catalogue={cubCatalogue.catalogue}
            description={cubCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={cubCatalogue.description}
                    specifications={[]}
                    features={cubFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <CubApplications />
          <CubTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={cubCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "drum-press") {
      return (
        <>
          <ProductCatalogueHero
            title={drumCatalogue.name}
            category={drumCatalogue.category}
            catalogue={drumCatalogue.catalogue}
            description={drumCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={drumCatalogue.description}
                    specifications={[]}
                    features={drumFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <DrumApplications />
          <DrumTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={drumCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "elephant") {
      return (
        <>
          <ProductCatalogueHero
            title={elephantCatalogue.name}
            category={elephantCatalogue.category}
            catalogue={elephantCatalogue.catalogue}
            description={elephantCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={elephantCatalogue.description}
                    specifications={[]}
                    features={elephantFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <ElephantApplications />
          <ElephantTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={elephantCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "turbine-stirrer") {
      return (
        <>
          <ProductCatalogueHero
            title={turbineCatalogue.name}
            category={turbineCatalogue.category}
            catalogue={turbineCatalogue.catalogue}
            description={turbineCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={turbineCatalogue.description}
                    specifications={[]}
                    features={turbineFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <TurbineApplications />
          <TurbineTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={turbineCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "pneumatic-stirrer") {
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
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={stirrerCatalogue.description}
                    specifications={[]}
                    features={stirrerFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <PneumaticStirrerFeatures />
          <PneumaticStirrerVariants />
          <CatalogueDownloadCTA catalogue={stirrerCatalogue.catalogue} />
        </>
      );
    }

    if (node.slug === "valves") {
      return <ValvesCataloguePage />;
    }

    if (node.slug === "filters") {
      return (
        <>
          <ProductCatalogueHero
            title={filterCatalogue.name}
            category={filterCatalogue.category}
            catalogue={filterCatalogue.catalogue}
            description={filterCatalogue.description}
          />
          <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-8 lg:grid-cols-[240px_1fr] lg:gap-10">
              <nav aria-label="Product Categories" className="pt-8">
                <ProductNav />
              </nav>
              <div className="py-8">
                <p className="mb-6 text-sm text-slate-500">{breadcrumbs}</p>
                <div className="flex flex-col">
                  <CatalogueSingleProduct
                    title={node.name}
                    image={node.image}
                    alt={node.name}
                    description={filterCatalogue.description}
                    specifications={[]}
                    features={filterFeatures.map(f => f.text)}
                  />
                </div>
              </div>
            </div>
          </section>
          <FiltersFeatures />
          <FiltersTechnicalSpecifications />
          <CatalogueDownloadCTA catalogue={filterCatalogue.catalogue} />
        </>
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
          features={landingForNode?.features}
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
        features={landingForNode?.features}
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
