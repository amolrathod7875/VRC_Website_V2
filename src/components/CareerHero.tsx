import { IconArrowRight } from "./Icon";

type CareerHeroProps = {
  headline: string;
  copy: string;
  ctaLabel: string;
  openingsCount: number;
  imageAlt: string;
};

export function CareerHero({
  headline,
  copy,
  ctaLabel,
  openingsCount,
  imageAlt,
}: CareerHeroProps) {
  return (
    <section className="relative overflow-hidden bg-white">
      <div className="mx-auto max-w-[1320px] px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid items-center gap-10 lg:grid-cols-[1.15fr_0.85fr] lg:gap-14">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">
              Careers at VR Coatings
            </p>
            <h1 className="mt-4 text-[clamp(40px,5vw,68px)] font-semibold leading-[1.02] tracking-[-0.03em] text-[#082B4C]">
              {headline}
            </h1>
            <p className="mt-6 max-w-2xl text-base leading-7 text-slate-600 sm:text-[17px] sm:leading-8">
              {copy}
            </p>
            <div className="mt-9 flex flex-wrap items-center gap-5">
              <a
                href="#open-positions"
                className="group inline-flex items-center gap-2.5 rounded-md bg-[#082B4C] px-6 py-3.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#1678C8]"
              >
                {ctaLabel}
                <svg
                  viewBox="0 0 20 20"
                  className="h-4 w-4 transition-transform duration-200 group-hover:translate-y-0.5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path d="M10 4v12M4 10l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </a>
              <span className="text-sm font-medium text-slate-500">
                <span className="text-xl font-semibold text-[#082B4C]">{openingsCount}</span>{" "}
                open positions
              </span>
            </div>
          </div>

          <div className="relative">
            <div
              className="relative overflow-hidden rounded-2xl border border-slate-200 bg-[#F4F7FA] shadow-[0_18px_50px_rgba(8,43,76,0.08)]"
              style={{ aspectRatio: "4 / 3" }}
              role="img"
              aria-label={imageAlt}
            >
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="flex flex-col items-center gap-3 text-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-white text-[#1678C8] shadow-sm">
                    <svg
                      viewBox="0 0 24 24"
                      className="h-7 w-7"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={1.8}
                    >
                      <path d="M3 17l6-6 4 4 8-8" strokeLinecap="round" strokeLinejoin="round" />
                      <path d="M14 7h7v7" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                    Facility image
                  </p>
                  <p className="px-4 text-[11px] leading-5 text-slate-400">
                    Image placeholder — to be added later
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}