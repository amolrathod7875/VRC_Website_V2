import Link from "next/link";
import Image from "next/image";
import type { Partner } from "@/lib/partnersData";

/**
 * Single shared partner-detail layout used for every partner on /partners.
 *
 * Every partner renders through this component so the catalogue stays visually
 * consistent. Layout rules (grid, spacing, card sizing, button placement) are
 * defined once here and reused for Asahi Sunac, Walther Systemtechnik and Timmer.
 */
export function PartnerSection({ partner }: { partner: Partner }) {
  const isDarkLogo = partner.logoBackground === "dark";
  const logoFit = partner.logoFit ?? "cover";

  return (
    <section className="border-b border-slate-200 py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[1fr_360px] lg:items-start">
          <div>
            <div className="mb-6 flex items-center gap-4 text-sm text-slate-500">
              <span className="text-2xl font-extralight text-brand-800">
                {partner.order}
              </span>
              <span className="h-4 w-px bg-slate-300" />
              <span className="uppercase tracking-[0.18em] text-brand-700">
                {partner.partnerType}
              </span>
            </div>

            <h2 className="text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
              {partner.name}
            </h2>
            <p className="mt-1 text-sm text-slate-500">{partner.location}</p>
            {partner.tagline && (
              <p className="mt-2 text-sm italic text-slate-500">{partner.tagline}</p>
            )}

            <p className="mt-5 text-sm font-semibold text-brand-700">
              {partner.description}
            </p>

            <div className="mt-6 text-slate-600 leading-relaxed">
              {partner.about}
            </div>

            <div className="mt-8">
              <p className="mb-4 text-xs font-semibold uppercase tracking-[0.15em] text-brand-800">
                Product range
              </p>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {partner.products.map((product) => (
                  <div
                    key={product.title}
                    className="group border border-slate-200 bg-white p-5 transition-all duration-250 hover:border-brand-200"
                  >
                    <h4 className="text-sm font-semibold text-brand-900">
                      {product.title}
                    </h4>
                    <p className="mt-1 text-sm text-slate-600">
                      {product.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {partner.highlights && partner.highlights.length > 0 && (
              <div className="mt-8">
                <p className="mb-4 text-xs font-semibold uppercase tracking-[0.15em] text-brand-800">
                  Key highlights
                </p>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  {partner.highlights.map((highlight) => (
                    <div key={highlight} className="flex items-start gap-3">
                      <span className="mt-0.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-brand-600" />
                      <span className="text-sm text-slate-700">{highlight}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-8 flex flex-wrap items-center gap-4">
              <Link
                href={partner.website}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 rounded-md bg-brand-800 px-6 py-3 text-sm font-semibold text-white transition-all duration-250 hover:bg-brand-700"
              >
                Visit Partner Website
                <svg
                  viewBox="0 0 20 20"
                  className="h-4 w-4 transition-transform duration-250 group-hover:translate-x-1"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    d="M5 10h10M11 5l5 5-5 5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </Link>
              <Link
                href="/contact"
                className="inline-flex items-center justify-center gap-2 rounded-md border border-brand-700 px-6 py-3 text-sm font-semibold text-brand-900 transition-all duration-250 hover:bg-brand-800 hover:text-white"
              >
                Enquire Through VR Coatings
              </Link>
            </div>
          </div>

          <div
            className={`flex items-center justify-center rounded-xl border border-slate-200 p-8 ${isDarkLogo ? "bg-[#0B1F2A]" : "bg-white"}`}
          >
            <div className="flex flex-col items-center justify-center">
              <Image
                src={partner.logo}
                alt={`${partner.name} logo`}
                width={isDarkLogo ? 320 : 200}
                height={isDarkLogo ? 88 : 200}
                className={`object-${logoFit} ${isDarkLogo ? "max-w-[82%]" : ""}`}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}