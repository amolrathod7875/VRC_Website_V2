import Image from "next/image";
import Link from "next/link";
import {
  applications,
  capabilityHighlights,
  certifications,
  featuredProducts,
  landingProducts,
  performanceAttributes,
  presenceLocations,
  weProvide,
} from "@/lib/data";
import { LogoSlider } from "@/components/LogoSlider";
import { Placeholder } from "@/components/Placeholder";
import { ProductCard } from "@/components/ProductCard";
import { TrustStrip } from "@/components/TrustStrip";
import { PerformanceCard } from "@/components/PerformanceCard";
import { ApplicationTile } from "@/components/ApplicationTile";
import { CtaBanner } from "@/components/CtaBanner";
import { BrandStatement } from "@/components/BrandStatement";
import { HeritageSince } from "@/components/HeritageSince";
import { ServicesCta } from "@/components/ServicesCta";
import { ProductWheel } from "@/components/ProductWheel";
import { Eyebrow, SectionHeading } from "@/components/SectionHeading";
import {
  IconApplication,
  IconArrowRight,
  IconBuilding,
  IconCar,
  IconCert,
  IconChemical,
  IconCircuit,
  IconCorrosion,
  IconCustom,
  IconDurability,
  IconFactory,
  IconPlane,
  IconPrecision,
  IconProtection,
  IconShield,
  IconShip,
  IconTemperature,
  IconZap,
  type IconProps,
} from "@/components/Icon";

const PERFORMANCE_ICONS = [
  IconProtection,
  IconCorrosion,
  IconDurability,
  IconChemical,
  IconTemperature,
  IconPrecision,
];

type IconCmp = (props: IconProps) => React.ReactElement;

const APPLICATION_ICONS: Record<string, IconCmp> = {
  automotive: IconCar,
  "defence-aerospace": IconShield,
  electronics: IconCircuit,
  infrastructure: IconBuilding,
  marine: IconShip,
  energy: IconZap,
};

export default function HomePage() {
  return (
    <>
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
            </div>

            <div className="mt-12 lg:mt-0">
              <div className="space-y-6 lg:hidden">
                {landingProducts.slice(0, 6).map((product) => (
                  <div
                    key={product.slug}
                    className="overflow-hidden rounded-2xl bg-[#082B4C] shadow-[0_16px_40px_rgba(8,43,76,0.10)]"
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
                <div className="mt-10 flex justify-center lg:justify-start">
                  <Link
                    href="/products"
                    className="group inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-8 py-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
                  >
                    View All Products
                    <IconArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <ServicesCta />

      <section id="applications" className="bg-[#062746] text-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-12 grid gap-8 lg:grid-cols-[1.1fr_1fr] lg:items-end">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">Applications</p>
              <h2 className="mt-3 text-3xl font-semibold leading-tight text-white sm:text-4xl">
                Coatings engineered for demanding environments.
              </h2>
            </div>
            <p className="max-w-xl text-base leading-7 text-slate-200">
              Our coating systems are specified across OEM lines, infrastructure programmes and maintenance
              operations where consistent film performance is non-negotiable.
            </p>
          </div>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {applications.map((app) => {
              const Icon = APPLICATION_ICONS[app.slug] ?? IconApplication;
              return (
                <ApplicationTile
                  key={app.slug}
                  icon={<Icon className="h-7 w-7" />}
                  name={app.name}
                  text={app.text}
                />
              );
            })}
          </div>
          <div className="mt-12 flex justify-center">
            <Link
              href="/applications"
              className="group inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-8 py-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
            >
              View all applications
              <IconArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
            </Link>
          </div>
        </div>
      </section>

      <section className="bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-12 max-w-2xl">
            <Eyebrow>Technical Authority</Eyebrow>
            <SectionHeading>Built around performance. Engineered for reliability.</SectionHeading>
            <p className="mt-4 text-base leading-7 text-slate-600">
              Every system is specified against the conditions it must survive — substrate chemistry,
              climate, operating temperature and the realities of the application line.
            </p>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {performanceAttributes.map((attr, i) => {
              const Icon = PERFORMANCE_ICONS[i] ?? IconPrecision;
              return (
                <PerformanceCard
                  key={attr.title}
                  icon={<Icon className="h-7 w-7" />}
                  title={attr.title}
                  text={attr.text}
                />
              );
            })}
          </div>
        </div>
      </section>

      <section className="bg-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-center">
            <div>
              <Eyebrow>Quality & Performance</Eyebrow>
              <SectionHeading>Designed to perform where it matters.</SectionHeading>
              <p className="mt-6 text-base leading-8 text-slate-600">
                Our quality programme is built around batch traceability, documented test methods, and
                continuous production oversight. Standards are referenced across our coating portfolio so
                customers can specify with confidence.
              </p>
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
              <div className="rounded-xl border border-slate-200 bg-surface p-6 sm:col-span-2">
                <p className="text-sm font-semibold text-brand-950">Regional presence</p>
                <ul className="mt-3 grid gap-2 sm:grid-cols-3">
                  {presenceLocations.map((loc) => (
                    <li key={loc.title} className="rounded-md bg-white px-4 py-3">
                      <p className="text-xs uppercase tracking-[0.16em] text-brand-700">{loc.title}</p>
                      <p className="mt-1 text-sm font-medium text-brand-950">{loc.region}</p>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="grid gap-12 lg:grid-cols-[1.1fr_1fr] lg:items-center">
            <div className="relative overflow-hidden rounded-xl">
              <video
                autoPlay
                muted
                loop
                playsInline
                preload="metadata"
                aria-hidden="true"
                className="h-full w-full object-cover"
              >
                <source src="/Scale_video.mp4" type="video/mp4" />
              </video>
            </div>
            <div>
              <Eyebrow>Our Capabilities</Eyebrow>
              <SectionHeading>Engineered for scale.</SectionHeading>
              <p className="mt-6 text-base leading-8 text-slate-600">
                Our manufacturing campus is organised for batch traceability, process repeatability and
                application support — so specification, sampling and fulfilment stay aligned.
              </p>
              <div className="mt-8 grid gap-3 sm:grid-cols-2">
                {capabilityHighlights.map((item) => (
                  <div
                    key={item.title}
                    className="rounded-lg border border-slate-200 bg-white px-4 py-3"
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

      <section className="bg-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
          <div className="mb-12 grid gap-6 lg:grid-cols-[1fr_1.2fr] lg:items-end">
            <div>
              <Eyebrow>Portfolio</Eyebrow>
              <SectionHeading>Featured products.</SectionHeading>
            </div>
            <p className="max-w-xl text-base leading-7 text-slate-600">
              A selection from our protective, powder, primer, marine and electronic coating lines —
              specified across OEM and maintenance programmes.
            </p>
          </div>
           <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {featuredProducts.map((product) => (
              <Link
                key={product.slug}
                href={`/products/${product.slug}`}
                className="group overflow-hidden rounded-xl border border-slate-200 bg-white transition hover:border-brand-200 hover:shadow-sm"
              >
                <Placeholder label={`${product.name} image`} ratio="4 / 3" />
                <div className="p-5">
                  <p className="text-xs uppercase tracking-wider text-brand-600">{product.category}</p>
                  <h3 className="mt-1 text-lg font-semibold text-brand-900">{product.name}</h3>
                </div>
              </Link>
            ))}
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
