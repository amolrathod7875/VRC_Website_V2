import Link from "next/link";
import { IconArrowRight } from "./Icon";

export function ServicesCta() {
  return (
    <section className="bg-surface">
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
        <div className="rounded-xl border border-slate-200 bg-white p-8 sm:p-10 lg:p-12">
          <div className="grid items-center gap-8 lg:grid-cols-[1.4fr_1fr]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-700">Services</p>
              <h2 className="mt-3 text-2xl font-semibold leading-tight text-brand-950 sm:text-3xl">
                Coating programmes across industrial sectors.
              </h2>
              <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
                Browse the 16 industrial sectors our coating systems serve — from automotive and aerospace
                to packaging, printing, and infrastructure.
              </p>
            </div>
            <div className="flex flex-col gap-3 sm:flex-row lg:justify-end">
              <Link
                href="/services"
                className="inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors duration-200 hover:bg-[#0B5C97]"
              >
                Explore Services
                <IconArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
