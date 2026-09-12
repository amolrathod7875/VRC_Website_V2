import Link from "next/link";
import { IconArrowRight } from "./Icon";

type CareerCtaProps = {
  eyebrow: string;
  title: string;
  text: string;
  primaryLabel: string;
  primaryHref: string;
};

export function CareerCta({ eyebrow, title, text, primaryLabel, primaryHref }: CareerCtaProps) {
  return (
    <section className="bg-[#082B4C]">
      <div className="mx-auto max-w-[1320px] px-4 py-14 sm:px-6 lg:px-8 lg:py-16">
        <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#7FB1DC]">
              {eyebrow}
            </p>
            <h2 className="mt-3 text-2xl font-semibold leading-tight text-white sm:text-3xl">
              {title}
            </h2>
            <p className="mt-4 text-base leading-7 text-slate-200">{text}</p>
          </div>
          <div className="shrink-0">
            <Link
              href={primaryHref}
              className="group inline-flex items-center gap-2 rounded-md bg-[#1678C8] px-6 py-3.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#7FB1DC]"
            >
              {primaryLabel}
              <IconArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}