import { getMediaUrl } from "@/lib/media";
import Link from "next/link";

type CatalogueDownloadCTAProps = {
  catalogue: string;
  title?: string;
};

export function CatalogueDownloadCTA({ catalogue, title = "Need the complete technical catalogue?" }: CatalogueDownloadCTAProps) {
  if (!catalogue) return null;

  return (
    <div className="border-t border-slate-200 bg-[#F4F7FA]">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex flex-col items-start gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-lg font-semibold text-[#082B4C]">{title}</p>
            <p className="mt-1 text-sm text-slate-600">
              Download the full technical catalogue or contact our team for detailed specifications.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
             <a
               href={getMediaUrl(catalogue)}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md bg-[#082B4C] px-5 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
            >
              Download Catalogue
              <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={2}>
                <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </a>
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 rounded-md border-2 border-[#082B4C] bg-transparent px-5 py-2.5 text-sm font-semibold text-[#082B4C] transition-colors duration-200 hover:bg-[#082B4C] hover:text-white"
            >
              Contact Technical Team
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
