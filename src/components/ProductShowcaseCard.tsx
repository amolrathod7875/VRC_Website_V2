import Link from "next/link";
import Image from "next/image";
import type { LandingProduct } from "@/lib/data";

type ProductShowcaseCardProps = {
  product: LandingProduct;
};

export function ProductShowcaseCard({ product }: ProductShowcaseCardProps) {
  return (
    <div className="overflow-hidden rounded-2xl bg-[#082B4C] shadow-[0_8px_24px_rgba(8,43,76,0.06)]">
      <div className="grid grid-cols-1 md:grid-cols-[45%_1fr]">
        <div className="relative flex items-center justify-center bg-[#F4F7FA] p-6">
          {product.image ? (
            <Image
              src={product.image}
              alt={product.name}
              width={480}
              height={360}
              className="max-h-56 w-auto object-contain md:max-h-64"
            />
          ) : (
            <div className="flex h-40 w-full items-center justify-center text-sm text-slate-400">
              {product.name}
            </div>
          )}
        </div>

        <div className="flex flex-col justify-center p-6 text-white md:p-8">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#1678C8]">
            {product.category}
          </p>
          <h3 className="mt-2 text-xl font-semibold text-white md:text-2xl">
            {product.name}
          </h3>
          <p className="mt-3 text-sm leading-6 text-white/75 line-clamp-3">
            {product.description}
          </p>
          <Link
            href={`/products/${product.slug}`}
            className="mt-5 inline-flex items-center gap-2 rounded-lg border border-white/15 px-4 py-2.5 text-sm font-semibold text-white transition-all duration-200 hover:border-[#1678C8] hover:bg-[#1678C8] w-fit"
          >
            View Full Details
            <svg
              viewBox="0 0 20 20"
              className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </Link>
        </div>
      </div>
    </div>
  );
}
