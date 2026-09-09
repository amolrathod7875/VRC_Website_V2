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
    <section className="relative bg-[#062746] text-white">
      <video
        autoPlay
        muted
        loop
        playsInline
        preload="metadata"
        className="absolute inset-0 z-0 h-full w-full object-cover"
      >
        <source src="/get_in_touch.mp4" type="video/mp4" />
      </video>
      <div
        className="absolute inset-0 z-10"
        style={{ backgroundColor: "rgba(6, 31, 54, 0.65)" }}
      />
      <div className="relative z-20 mx-auto flex max-w-7xl items-center px-4 py-20 sm:px-6 lg:px-8 lg:py-32">
        <div className="max-w-[720px]">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">{eyebrow}</p>
          <h2 className="mt-4 text-4xl font-semibold leading-[1.1] text-white sm:text-5xl">{title}</h2>
          <p className="mt-5 max-w-2xl text-base leading-8 text-slate-200">{text}</p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              href={primaryHref}
              className="inline-flex rounded-md bg-[#1678C8] px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-[#1269A8]"
            >
              {primaryLabel}
            </Link>
            <Link
              href={secondaryHref}
              className="inline-flex rounded-md border border-white/30 px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-white/10"
            >
              {secondaryLabel}
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
