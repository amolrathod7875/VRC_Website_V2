import Link from "next/link";
import { partners } from "@/lib/partnersData";
import { PartnerSection } from "@/components/PartnerSection";
import { GetInTouchSection } from "@/components/GetInTouchSection";

export function PartnersPage() {
  return (
    <>
      <section className="bg-brand-900 text-white">
        <div className="mx-auto grid max-w-7xl items-center gap-12 px-4 py-20 sm:px-6 lg:grid-cols-[1fr_1fr] lg:gap-16 lg:px-8">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">
              Global Technology Partners
            </p>
            <h1 className="mt-4 text-4xl font-semibold leading-[1.05] sm:text-5xl">
              Global engineering.
              <br />
              Local support.
            </h1>
            <p className="mt-5 max-w-lg text-base leading-7 text-slate-200">
              VR Coatings collaborates with leading manufacturers from Japan and Germany
              to bring advanced coating, dosing and fluid-handling technologies to India.
            </p>
          </div>
          <div className="flex items-center justify-center">
            <div className="relative flex items-center justify-center gap-4 text-center">
              <div className="flex flex-col items-center">
                <span className="text-xs font-semibold uppercase tracking-[0.15em] text-slate-300">
                  JAPAN
                </span>
                <span className="mt-1 text-xs text-slate-400">(Nagoya)</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-xl font-light text-slate-300">+</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-xs font-semibold uppercase tracking-[0.15em] text-slate-300">
                  GERMANY
                </span>
                <span className="mt-1 text-xs text-slate-400">(Munich / Hesse)</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-xl font-light text-slate-400" aria-hidden="true">
                  →
                </span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-xs font-semibold uppercase tracking-[0.15em] text-[#1678C8]">
                  VR COATINGS
                </span>
                <span className="mt-1 text-xs text-slate-300">INDIA</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-[#F4F7FA] py-20">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <p className="text-center text-xs font-semibold uppercase tracking-[0.24em] text-brand-600">
            Our Partners
          </p>
          <h2 className="mt-3 text-center text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
            Technology leaders behind every solution.
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-center text-base leading-7 text-slate-600">
            VR Coatings works with established technology manufacturers to provide advanced
            coating equipment, precision dosing systems and industrial pump technology with
            local sales, support and service.
          </p>
        </div>
      </section>

      {partners.map((partner) => (
        <PartnerSection key={partner.id} partner={partner} />
      ))}

      <section className="bg-brand-950 text-white py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <p className="text-center text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">
            Global technology. Local expertise.
          </p>
          <h2 className="mt-3 text-center text-3xl font-semibold leading-tight sm:text-4xl">
            World-class technology,
            <br />
            supported from India.
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-center text-base leading-7 text-slate-200">
            VR Coatings connects international engineering expertise with local application
            support, service and spare-parts availability.
          </p>

          <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center sm:gap-6 lg:gap-8">
            <div className="flex flex-col items-center">
              <span className="text-xl font-semibold text-[#1678C8]">JAPAN</span>
              <span className="mt-1 text-sm text-slate-300">Coating & Atomization Technology</span>
            </div>
            <div className="hidden h-px w-32 bg-slate-600 sm:w-40 sm:my-2 lg:mx-8" />
            <div className="flex flex-col items-center">
              <span className="text-xl font-semibold text-[#1678C8]">GERMANY</span>
              <span className="mt-1 text-sm text-slate-300">Dosing & Fluid Handling Technology</span>
            </div>
            <div className="hidden h-px w-32 bg-slate-600 sm:w-40 sm:my-2 lg:mx-8" />
            <div className="flex flex-col items-center">
              <span className="text-xl font-semibold text-[#1678C8]">INDIA</span>
              <span className="mt-1 text-sm text-slate-300">Sales, Application Support & Service</span>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-white py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <p className="text-center text-xs font-semibold uppercase tracking-[0.24em] text-brand-600">
            Why our partnerships matter
          </p>
          <h2 className="mt-3 text-center text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
            Why Our Partnerships Matter
          </h2>
          <div className="mx-auto mt-12 grid max-w-4xl gap-6 sm:grid-cols-2">
            <div className="border-l-2 border-brand-200 pl-6">
              <h3 className="text-xl font-semibold text-brand-900">Global Technology</h3>
              <p className="mt-2 text-sm text-slate-600">
                Access to established international engineering expertise.
              </p>
            </div>
            <div className="border-l-2 border-brand-200 pl-6">
              <h3 className="text-xl font-semibold text-brand-900">Local Support</h3>
              <p className="mt-2 text-sm text-slate-600">
                VR Coatings provides India-facing sales and application assistance.
              </p>
            </div>
            <div className="border-l-2 border-brand-200 pl-6">
              <h3 className="text-xl font-semibold text-brand-900">Spares & Service</h3>
              <p className="mt-2 text-sm text-slate-600">
                Support for genuine replacement parts and service requirements.
              </p>
            </div>
            <div className="border-l-2 border-brand-200 pl-6">
              <h3 className="text-xl font-semibold text-brand-900">Industrial Expertise</h3>
              <p className="mt-2 text-sm text-slate-600">
                Technologies suited for demanding manufacturing environments.
              </p>
            </div>
          </div>
        </div>
      </section>

      <GetInTouchSection />
    </>
  );
}
