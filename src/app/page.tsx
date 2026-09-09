import Image from "next/image";
import Link from "next/link";
import {
  applications,
  capabilityHighlights,
  certifications,
  getApplicationIcon,
  landingProducts,
  weProvide,
} from "@/lib/data";
import { LogoSlider } from "@/components/LogoSlider";
import { ProductCard } from "@/components/ProductCard";
import { TrustStrip } from "@/components/TrustStrip";
import { ApplicationsShowcase } from "@/components/ApplicationsShowcase";
import { CtaBanner } from "@/components/CtaBanner";
import { BrandStatement } from "@/components/BrandStatement";
import { HeritageSince } from "@/components/HeritageSince";
import { ServicesCta } from "@/components/ServicesCta";
import { ProductWheel } from "@/components/ProductWheel";
import { ClientFeedback } from "@/components/ClientFeedback";
import { ScrollProgressRail } from "@/components/ScrollProgressRail";
import { Eyebrow, SectionHeading } from "@/components/SectionHeading";
import {
  IconApplication,
  IconArrowRight,
  IconCert,
  IconCustom,
  IconFactory,
  IconPlane,
} from "@/components/Icon";

export default function HomePage() {
  return (
    <>
      <ScrollProgressRail />
      <section className="relative isolate flex items-center overflow-hidden">
        <div className="who-we-are-video-container">
          <video
            className="who-we-are-video"
            autoPlay
            muted
            loop
            playsInline
            aria-hidden="true"
          >
            <source src="/Landing_Video.mp4" type="video/mp4" />
          </video>
        </div>
        <div className="who-we-are-content">
          <Eyebrow tone="white">Who we are</Eyebrow>
          <SectionHeading tone="white">
            Engineered coating solutions for demanding industries.
          </SectionHeading>
          <p className="mt-6 max-w-lg text-base leading-8 text-slate-100">
            VR Coatings develops, manufactures, and supports industrial coating systems for OEM lines
            and maintenance programmes. We pair formulation science with application support so films
            perform in the field — not only in the lab.
          </p>
          <p className="mt-4 max-w-lg text-base leading-8 text-slate-100">
            From zinc-rich primers and high-build epoxies to architectural powders and electrocoat
            primers, our systems are specified by manufacturers who need predictable protection on
            critical surfaces.
          </p>
          <div className="mt-8 grid w-full max-w-sm gap-3 sm:grid-cols-2">
            {weProvide.slice(0, 4).map((item) => (
              <div
                key={item.title}
                className="w-full rounded-lg bg-white/90 px-4 py-3 text-sm font-medium text-brand-950"
              >
                {item.title}
              </div>
            ))}
          </div>
          <Link
            href="/about"
            className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-white hover:text-brand-100"
          >
            About VR Coatings
            <IconArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </section>

      <TrustStrip />

      <HeritageSince />

      <BrandStatement />

      <section id="products" className="scroll-mt-24 bg-[#F4F7FA]">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="lg:grid lg:grid-cols-[35%_1fr] lg:gap-12">
            <div className="lg:sticky lg:top-24 lg:self-start">
              <Eyebrow>Our Products</Eyebrow>
              <SectionHeading>Coating systems engineered for performance.</SectionHeading>
              <p className="mt-4 text-base leading-7 text-slate-600">
                Explore our range of engineered coating systems developed for performance, protection and
                long-term reliability across industrial applications.
              </p>
              <div className="mt-8">
                <Link
                  href="/products"
                  className="group inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-8 py-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
                >
                  View All Products
                  <IconArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
                </Link>
              </div>
            </div>

            <div className="mt-12 lg:mt-0">
              <div className="space-y-6 lg:hidden">
                {landingProducts.slice(0, 6).map((product) => (
                  <div
                    key={product.slug}
                    className="overflow-hidden rounded-2xl bg-[#082B4C] shadow-[0_8px_24px_rgba(8,43,76,0.06)]"
                  >
                    <div className="grid grid-cols-1 md:grid-cols-[45%_1fr]">
                      <div className="relative flex items-center justify-center bg-[#F4F7FA] p-6">
                        {product.image && (
                          <Image
                            src={product.image}
                            alt={product.name}
                            width={480}
                            height={360}
                            className="max-h-56 w-auto object-contain md:max-h-64"
                          />
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
                            className="h-4 w-4"
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
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="hidden lg:block">
                <ProductWheel products={landingProducts.slice(0, 6)} />
              </div>
            </div>
          </div>
        </div>
      </section>

      <ServicesCta />

      <section id="applications" className="bg-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-12 grid gap-8 lg:grid-cols-[1.1fr_1fr] lg:items-end">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-700">Applications</p>
              <h2 className="mt-3 text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
                Coatings engineered for demanding environments.
              </h2>
            </div>
            <p className="max-w-xl text-base leading-7 text-slate-600">
              Our coating systems are specified across OEM lines, infrastructure programmes and maintenance
              operations where consistent film performance is non-negotiable.
            </p>
          </div>
          <ApplicationsShowcase applications={applications} />
        </div>
      </section>

      <section
        className="relative overflow-hidden bg-white min-h-screen flex items-center"
        style={{
          backgroundImage: "url('/Quality_Background.avif')",
          backgroundSize: "cover",
          backgroundPosition: "center center",
          backgroundRepeat: "no-repeat",
        }}
      >
        <div className="relative z-10 mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:pb-12 w-full">
          <div className="grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-center">
            <div>
              <div className="rounded-xl bg-white/80 p-6">
                <Eyebrow>Quality & Performance</Eyebrow>
                <SectionHeading>Designed to perform where it matters.</SectionHeading>
                <p className="mt-6 text-base leading-8 text-slate-600">
                  Our quality programme is built around batch traceability, documented test methods, and
                  continuous production oversight. Standards are referenced across our coating portfolio so
                  customers can specify with confidence.
                </p>
              </div>
              <div className="mt-8 grid gap-4 sm:grid-cols-2">
                {certifications.map((cert) => (
                  <div
                    key={cert.name}
                    className="flex items-start gap-4 rounded-lg border border-slate-200 bg-surface px-5 py-4"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-white text-brand-800">
                      <IconCert className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-brand-950">{cert.name}</p>
                      <p className="mt-1 text-xs leading-5 text-slate-500">{cert.scope}</p>
                    </div>
                  </div>
                ))}
              </div>
              <Link
                href="/resources/certifications"
                className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-brand-700 hover:text-brand-800"
              >
                View certifications
                <IconArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
            <div className="grid gap-6 sm:grid-cols-2">
              <div className="rounded-xl border border-slate-200 bg-surface p-6">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-white text-brand-800">
                  <IconFactory className="h-6 w-6" />
                </div>
                <p className="text-sm font-semibold text-brand-950">Integrated Supply</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  Head office, manufacturing unit and North America operations work as one supply network —
                  from first trial through serial production.
                </p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-surface p-6">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-white text-brand-800">
                  <IconCustom className="h-6 w-6" />
                </div>
                <p className="text-sm font-semibold text-brand-950">Custom Formulation</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  Recipes developed around your substrate, climate and duty cycle — backed by lab trials
                  and application replicates.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <ClientFeedback />

      <section className="bg-surface lg:h-[calc(100vh-80px)] lg:flex lg:items-center">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-0 w-full">
          <div className="grid gap-8 lg:grid-cols-[1.1fr_1fr] lg:items-center min-h-0">
            <div className="relative overflow-hidden rounded-xl flex min-h-0 h-full">
              <video
                autoPlay
                muted
                loop
                playsInline
                preload="metadata"
                aria-hidden="true"
                className="absolute inset-0 h-full w-full object-cover"
              >
                <source src="/Scale_video.mp4" type="video/mp4" />
              </video>
            </div>
            <div>
              <Eyebrow>Our Capabilities</Eyebrow>
              <SectionHeading>Engineered for scale.</SectionHeading>
              <p className="mt-4 text-base leading-7 text-slate-600">
                Our manufacturing campus is organised for batch traceability, process repeatability and
                application support — so specification, sampling and fulfilment stay aligned.
              </p>
              <div className="mt-5 grid gap-2.5 sm:grid-cols-2">
                {capabilityHighlights.map((item) => (
                  <div
                    key={item.title}
                    className="rounded-lg border border-slate-200 bg-white px-3 py-2.5"
                  >
                    <p className="text-sm font-semibold text-brand-950">{item.title}</p>
                    <p className="mt-1 text-xs leading-5 text-slate-500">{item.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <LogoSlider />

      <CtaBanner
        eyebrow="Get in touch"
        title="Ready to discuss your coating requirements?"
        text="Talk to our team about the right coating system for your application, substrate and operating environment."
      />
    </>
  );
}
