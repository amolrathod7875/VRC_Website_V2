import Link from "next/link";

type CtaBannerProps = {
  eyebrow: string;
  title: string;
  text: string;
  primaryHref?: string;
  primaryLabel?: string;
  secondaryHref?: string;
  secondaryLabel?: string;
};

export function CtaBanner({
  eyebrow,
  title,
  text,
  primaryHref = "/contact",
  primaryLabel = "Discuss Your Requirement",
  secondaryHref = "/catalog",
  secondaryLabel = "Request Catalog",
}: CtaBannerProps) {
  return (
    <section className="bg-[#062746] text-white">
      <div className="mx-auto grid max-w-7xl items-center gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[1.2fr_1fr] lg:px-8 lg:py-20">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">{eyebrow}</p>
          <h2 className="mt-3 text-3xl font-semibold leading-tight text-white sm:text-4xl">{title}</h2>
          <p className="mt-4 max-w-xl text-base leading-7 text-slate-200">{text}</p>
        </div>
        <div className="flex flex-wrap items-center gap-3 lg:justify-end">
          <Link
            href={primaryHref}
            className="inline-flex rounded-md bg-[#1678C8] px-6 py-3 text-sm font-semibold text-white transition hover:bg-[#1269A8]"
          >
            {primaryLabel}
          </Link>
          <Link
            href={secondaryHref}
            className="inline-flex rounded-md border border-white/30 px-6 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
          >
            {secondaryLabel}
          </Link>
        </div>
      </div>
    </section>
  );
}
