import Link from "next/link";
import { IconArrowRight } from "./Icon";

type CatalogueLinkProps = {
  catalogue?: string;
};

export function CatalogueLink({ catalogue }: CatalogueLinkProps) {
  if (!catalogue) return null;

  const href = catalogue.startsWith("/")
    ? catalogue
    : `/Catalogue/${encodeURIComponent(catalogue)}`;

  return (
    <Link
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="mt-4 inline-flex items-center gap-1.5 rounded-md bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 transition-colors duration-200 hover:bg-slate-200"
    >
      View catalogue
      <IconArrowRight className="h-3.5 w-3.5" />
    </Link>
  );
}
