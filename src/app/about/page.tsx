import type { Metadata } from "next";
import { weProvide, companyStats } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { IconSupport, IconFlask, IconBadgeCheck, IconGlobe } from "@/components/Icon";

const iconMap = {
  support: IconSupport,
  flask: IconFlask,
  badgeCheck: IconBadgeCheck,
  globe: IconGlobe,
};

export const metadata: Metadata = { title: "About Us" };

export default function AboutPage() {
  return (
    <>
      <PageHero
        kicker="About"
        title="About VR Coatings Pvt. Ltd."
        text="An industrial coatings manufacturer focused on protective performance, process reliability, and long-term partnership."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <img
            src="/VR-Coatings-Pvt-Ltd-Factory.png"
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
          </div>
        </div>
      </section>
      <section className="bg-[#0a1f40] py-10">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5 lg:gap-0 lg:border lg:border-slate-700/50">
            {companyStats.map((stat, index) => (
              <div
                key={stat.label}
                className={`flex flex-col items-center justify-center py-6 ${index < 4 ? "border-b sm:border-b-0 sm:border-r sm:border-slate-700/50 lg:border-b-0" : ""}`}
              >
                <span className="text-3xl font-bold text-white sm:text-4xl">{stat.value}</span>
                <span className="mt-1 text-xs font-semibold uppercase tracking-[0.12em] text-slate-300">
                  {stat.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>
      <section className="bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <h2 className="mb-8 text-3xl font-semibold text-brand-950">We provide</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {weProvide.map((item) => {
              const IconComponent = iconMap[item.icon as keyof typeof iconMap];
              return (
                <article key={item.title} className="rounded-xl border border-slate-200 bg-white p-6 flex flex-col items-center text-center">
                  <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-lg bg-slate-50">
                    {IconComponent && <IconComponent className="h-8 w-8 text-brand-700" />}
                  </div>
                  <h3 className="font-semibold text-brand-900">{item.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>
    </>
  );
}
