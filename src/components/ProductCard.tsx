import Link from "next/link";
import { Placeholder } from "./Placeholder";
import type { LandingProduct } from "@/lib/data";

type ProductCardProps = {
  product: LandingProduct;
  href?: string;
};

export function ProductCard({ product, href = "/products" }: ProductCardProps) {
  return (
    <Link
      href={href}
      className="group flex h-full flex-col overflow-hidden rounded-lg border border-slate-200 bg-white transition hover:border-brand-200 hover:shadow-sm"
    >
      <div className="relative overflow-hidden">
        <div className="transition duration-300 group-hover:scale-[1.02]">
          <Placeholder
            label={`${product.name} image`}
            ratio="16 / 10"
            className="rounded-none"
          />
        </div>
      </div>
      <div className="flex flex-1 flex-col p-5">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-brand-700">
          {product.category}
        </p>
        <h3 className="mt-2 text-lg font-semibold text-brand-950">{product.name}</h3>
        <p className="mt-2 text-sm leading-6 text-slate-600">{product.description}</p>
        <span className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-700 transition group-hover:text-brand-600">
          View Product
          <svg viewBox="0 0 20 20" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </span>
      </div>
    </Link>
  );
}
