import Link from "next/link";
import { IconArrowRight } from "@/components/Icon";
import { SpecificationTable } from "@/components/SpecificationTable";

type Spec = {
  label: string;
  value: string;
};

type SingleProductCatalogueProps = {
  title: string;
  category: string;
  catalogue: string;
  image: string | null | undefined;
  alt: string;
  description?: string;
  overview?: string;
  features?: string[];
  specifications?: Spec[];
  applications?: string[];
};

export function SingleProductCatalogue({
  title,
  category,
  catalogue,
  image,
  alt,
  description,
  overview,
  features,
  specifications,
  applications,
}: SingleProductCatalogueProps) {
  const hasDetail = Boolean(overview || features?.length || specifications?.length || applications?.length);

  return (
    <div className="grid gap-8 lg:grid-cols-2 lg:items-start">
      <div className="space-y-6">
        <p className="text-sm text-slate-500">{category}</p>
        {description && <p className="text-sm leading-7 text-slate-600">{description}</p>}
        {overview && <p className="text-sm leading-7 text-slate-600">{overview}</p>}
        {features && features.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-brand-700">Key Features</h3>
            <ul className="mt-2 list-disc list-inside space-y-1">
              {features.map((f) => (
                <li key={f} className="text-sm text-slate-600">{f}</li>
              ))}
            </ul>
          </div>
        )}
        {specifications && specifications.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-brand-700">Technical Specifications</h3>
            <SpecificationTable specifications={specifications} />
          </div>
        )}
        {applications && applications.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-brand-700">Applications</h3>
            <ul className="mt-2 list-disc list-inside space-y-1">
              {applications.map((a) => (
                <li key={a} className="text-sm text-slate-600">{a}</li>
              ))}
            </ul>
          </div>
        )}
        {!hasDetail && (
          <p className="text-sm leading-7 text-slate-600">
            Detailed technical specifications are available in the product catalogue.
          </p>
        )}
        <Link
          href="/contact"
          className="mt-2 inline-flex items-center gap-1.5 font-semibold text-brand-700"
        >
          Request a datasheet
          <IconArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>
      <div>
        {image ? (
          <img
            src={image}
            alt={alt}
            className="aspect-[4/3] w-full rounded-xl object-contain object-center"
          />
        ) : (
          <div className="aspect-[4/3] w-full rounded-xl bg-[#E8EEF4]" />
        )}
      </div>
    </div>
  );
}
