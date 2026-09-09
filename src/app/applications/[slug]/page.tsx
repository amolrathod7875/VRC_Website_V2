import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  applications,
  findApplication,
  weProvide,
} from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { GetInTouchSection } from "@/components/GetInTouchSection";
import { Eyebrow, SectionHeading } from "@/components/SectionHeading";
import { IconArrowRight } from "@/components/Icon";
import type { IconProps } from "@/components/Icon";
import {
  IconApplication,
  IconBadgeCheck,
  IconFlask,
  IconGlobe,
  IconSupport,
} from "@/components/Icon";

const WE_PROVIDE_ICONS: Record<string, React.FC<IconProps>> = {
  support: IconSupport,
  flask: IconFlask,
  badgeCheck: IconBadgeCheck,
  globe: IconGlobe,
};

function getWeProvideIcon(name: string) {
  return WE_PROVIDE_ICONS[name] ?? IconApplication;
}

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return applications.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const found = findApplication(slug);
  return { title: found ? `${found.name} Applications | VR Coatings` : "Application" };
}

const requirementCards: Record<string, { title: string; text: string }[]> = {
  automotive: [
    {
      title: "Application Environment",
      text: "Body and underbody assembly lines where coating integrity through e-coat, primer, and topcoat stages is critical.",
    },
    {
      title: "Protection Requirements",
      text: "Corrosion resistance for underbody sections and durable finishes for exterior body panels.",
    },
    {
      title: "Process Integration",
      text: "Systems designed to integrate with standard OEM coating line sequences and curing profiles.",
    },
  ],
  "defence-aerospace": [
    {
      title: "Application Environment",
      text: "Airframes, ground systems, and components exposed to demanding operational and environmental conditions.",
    },
    {
      title: "Specification Compliance",
      text: "Coatings specified against defined performance requirements with documented traceability and batch control.",
    },
    {
      title: "Durability & Protection",
      text: "Long-term barrier and surface protection for mission-critical platforms and components.",
    },
  ],
  electronics: [
    {
      title: "Application Environment",
      text: "Boards, housings, and connectors requiring reliable dielectric and environmental isolation.",
    },
    {
      title: "Protection Requirements",
      text: "Defence against moisture, contamination, and electrical shorting in assembled electronic systems.",
    },
    {
      title: "Precision Application",
      text: "Coating processes that preserve fine tolerances and do not compromise connector or component performance.",
    },
  ],
  infrastructure: [
    {
      title: "Application Environment",
      text: "Bridges, tanks, and industrial structures subject to long-term weather and service exposure.",
    },
    {
      title: "Barrier Protection",
      text: "Long-term barrier protection against corrosion and structural degradation in demanding environments.",
    },
    {
      title: "Maintenance Cycles",
      text: "Coatings selected to extend service life and reduce maintenance intervention over extended periods.",
    },
  ],
  marine: [
    {
      title: "Operating Environment",
      text: "S saline environments including hulls, decks, and offshore steel structures.",
    },
    {
      title: "Corrosion Protection",
      text: "Sustained corrosion protection against saltwater immersion, splash zones, and atmospheric salinity.",
    },
    {
      title: "Durability Requirements",
      text: "Coatings that maintain film integrity through constant wet/dry cycling and mechanical impact.",
    },
  ],
  "energy-process": [
    {
      title: "Operating Environment",
      text: "Pipelines, refineries, and power generation assets with demanding operational and climatic conditions.",
    },
    {
      title: "Protection Requirements",
      text: "Barrier and corrosion protection for critical energy infrastructure and processing equipment.",
    },
    {
      title: "Asset Integrity",
      text: "Coatings engineered to support long asset lifecycles and reliable facility operation.",
    },
  ],
};

export default async function ApplicationDetailPage({ params }: Props) {
  const { slug } = await params;
  const found = findApplication(slug);
  if (!found) notFound();

  const AppIcon = found.icon;
  const currentIndex = applications.findIndex((a) => a.slug === slug);
  const prevApp = currentIndex > 0 ? applications[currentIndex - 1] : null;
  const nextApp = currentIndex < applications.length - 1 ? applications[currentIndex + 1] : null;
  const reqs = requirementCards[slug] ?? [];

  return (
    <>
      <PageHero kicker="Applications" title={found.name} text={found.text} />

      {/* Breadcrumbs */}
      <nav className="mx-auto max-w-7xl px-4 pt-4 sm:px-6 lg:px-8">
        <ol className="flex items-center gap-2 text-xs text-slate-500">
          <li>
            <Link href="/" className="hover:text-brand-700">
              Home
            </Link>
          </li>
          <li>/</li>
          <li>
            <Link href="/applications" className="hover:text-brand-700">
              Applications
            </Link>
          </li>
          <li>/</li>
          <li className="text-slate-800">{found.name}</li>
        </ol>
      </nav>

      {/* Application Overview */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-2 lg:gap-16">
          <div>
            <Eyebrow>Application Overview</Eyebrow>
            <SectionHeading>{found.name}</SectionHeading>
            <p className="mt-4 text-base leading-7 text-slate-600">
              VR Coatings develops and supports coating systems tailored to the specific demands of each
              application. Our approach combines formulation science with field-proven application guidance
              to deliver consistent film performance across diverse substrates and operating conditions.
            </p>
          </div>
          <div className="mt-10 lg:mt-0">
            <div className="rounded-xl border border-slate-200 bg-white p-8">
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-md bg-brand-50 text-brand-800">
                  <AppIcon className="h-8 w-8" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-brand-950">{found.name}</h3>
                  <p className="mt-1 text-sm text-slate-500">{found.text}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Requirements */}
      {reqs.length > 0 && (
        <section className="bg-surface">
          <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <Eyebrow>Key Requirements</Eyebrow>
            <SectionHeading>What this application demands</SectionHeading>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              Every application environment imposes its own set of demands on a coating system.
              Understanding these requirements is the starting point for specifying the right solution.
            </p>
            <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {reqs.map((req) => (
                <div key={req.title} className="rounded-xl border border-slate-200 bg-white p-6">
                  <h3 className="text-base font-semibold text-brand-950">{req.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-600">{req.text}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* How VR Coatings Supports */}
      <section className="bg-white">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <Eyebrow>How VR Coatings Supports</Eyebrow>
          <SectionHeading>Support built around your process</SectionHeading>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
            We pair formulation science with application support so films perform in the field — not only in the lab.
          </p>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {weProvide.map((item) => {
              const WeProvideIcon = WE_PROVIDE_ICONS[item.icon] ?? IconApplication;
              return (
                <div key={item.title} className="rounded-xl border border-slate-200 bg-surface p-6">
                  <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-md bg-white text-brand-800">
                    <WeProvideIcon className="h-6 w-6" />
                  </div>
                  <h3 className="text-base font-semibold text-brand-950">{item.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Relevant Products */}
      <section className="bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="rounded-xl border border-slate-200 bg-white p-8 sm:p-12">
            <div className="lg:grid lg:grid-cols-2 lg:gap-12 lg:items-center">
              <div>
                <Eyebrow>Relevant Products</Eyebrow>
                <SectionHeading>Coating systems for this application</SectionHeading>
                <p className="mt-4 text-base leading-7 text-slate-600">
                  Explore our range of engineered coating systems developed for performance, protection and
                  long-term reliability across industrial applications.
                </p>
              </div>
              <div className="mt-8 lg:mt-0">
                <Link
                  href="/products"
                  className="inline-flex items-center justify-center gap-2 rounded-md bg-[#1678C8] px-8 py-4 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
                >
                  Explore Our Products
                  <IconArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <GetInTouchSection
        title="Discuss your application requirements"
        text="Talk to our team about the right coating system for your application, substrate and operating environment."
      />

      {/* Previous / Next Navigation */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {prevApp ? (
            <Link
              href={`/applications/${prevApp.slug}`}
              className="group inline-flex items-center gap-2 text-sm font-semibold text-brand-700 hover:text-brand-800"
            >
              <svg
                viewBox="0 0 20 20"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="h-4 w-4 rotate-180"
              >
                <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              {prevApp.name}
            </Link>
          ) : (
            <div />
          )}
          {nextApp ? (
            <Link
              href={`/applications/${nextApp.slug}`}
              className="group inline-flex items-center gap-2 text-sm font-semibold text-brand-700 hover:text-brand-800"
            >
              {nextApp.name}
              <IconArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
            </Link>
          ) : (
            <div />
          )}
        </div>
      </section>
    </>
  );
}
