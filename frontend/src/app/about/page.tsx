import type { Metadata } from "next";
import Link from "next/link";
import { PageHero } from "@/components/PageHero";
import { StatCountUp } from "@/components/StatCountUp";
import { WeProvide } from "@/components/WeProvide";
import { WhyChooseUs } from "@/components/WhyChooseUs";
import { GlobalPresence } from "@/components/GlobalPresence";

export const metadata: Metadata = { title: "About Us" };

export default function AboutPage() {
  return (
    <>
      <PageHero
        kicker="About"
        title="About VR Coatings Pvt. Ltd."
        text="An industrial coatings manufacturer focused on protective performance, process reliability, and long-term partnership."
      />
      <section className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="absolute inset-0 -z-10 overflow-hidden rounded-xl">
          <img
            src="/Vids_imgs/metal-structure.jpg"
            alt=""
            aria-hidden="true"
            className="h-full w-full object-cover object-center"
          />
          <div className="absolute inset-0 bg-white/85" />
        </div>
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <img
            src="/Vids_imgs/VR-Coatings-Pvt-Ltd-Factory.png"
            alt="VR Coatings manufacturing facility"
            className="min-h-[320px] rounded-xl object-cover object-center lg:min-h-[420px]"
          />
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-brand-700">
              About VR Coatings
            </p>
            <h2 className="mt-2 text-3xl font-semibold text-brand-950">
              Built around performance, reliability and application expertise.
            </h2>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              VR Coatings develops, manufactures, and supports industrial coating systems for demanding
              applications. Our approach combines formulation science with practical application support
              to deliver coating solutions designed for real operating conditions.
            </p>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              Our systems are developed around the requirements of the substrate, process, environment
              and end-use application. From protective coatings and primers to specialised industrial
              systems, we focus on consistent performance and dependable protection.
            </p>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              We work closely with customers across OEM and industrial applications, supporting the
              process from product selection and trials through application and production.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-5 sm:gap-6">
              <Link
                href="/contact"
                className="inline-flex h-16 min-w-[192px] items-center justify-center rounded-[14px] bg-brand-700 px-8 py-3 text-sm font-semibold text-white transition-all duration-200 hover:-translate-y-0.5 hover:bg-brand-600 lg:px-9"
              >
                Contact Us
              </Link>
              <Link
                href="/products"
                className="inline-flex h-16 min-w-[192px] items-center justify-center rounded-[14px] border-2 border-brand-700 bg-transparent px-8 py-3 text-sm font-semibold text-brand-700 transition-all duration-200 hover:-translate-y-0.5 hover:bg-brand-700 hover:text-white lg:px-9"
              >
                Our Products
              </Link>
            </div>
          </div>
        </div>
      </section>
      <section className="bg-[#0a1f40] py-10">
        <StatCountUp />
      </section>
      <WeProvide />

      <WhyChooseUs />

      <GlobalPresence />
    </>
  );
}
