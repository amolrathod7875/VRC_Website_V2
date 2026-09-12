"use client";

import { useState } from "react";
import { CareerHero } from "@/components/CareerHero";
import { CultureStrip } from "@/components/CultureStrip";
import { FilterBar } from "@/components/FilterBar";
import { JobCard } from "@/components/JobCard";
import { CareerCta } from "@/components/CareerCta";
import { GetInTouchSection } from "@/components/GetInTouchSection";
import { listDepartments, roles } from "@/lib/careerData";

const cultureItems = [
  {
    title: "Engineering Focus",
    description: "Formulation science and application engineering drive every decision.",
    icon: (
      <path d="M14.3 6.3a2.1 2.1 0 0 1 3 3L8.6 18a2.1 2.1 0 0 1-3-3l.9-1L5 17l1.9-.9-.4-.4.4.4L9 15.4l7.3-7.3Z M12 14 5 21" />
    ),
  },
  {
    title: "Hands-on Work",
    description: "Field support, lab testing and production-floor collaboration.",
    icon: (
      <>
        <path d="M11 4v12M7 8H4a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h1v5a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-5h1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-3V5a1 1 0 0 0-1-1h-3a1 1 0 0 0-1 1Z M11 8h4" />
      </>
    ),
  },
  {
    title: "Industrial Impact",
    description: "Systems that protect critical surfaces in demanding environments.",
    icon: (
      <>
        <path d="M2 21V8l6-4 6 4v6l6-4v13H2Z M13 21v-6M9 21v-4M5 21v-3" />
      </>
    ),
  },
  {
    title: "Continuous Learning",
    description: "Ongoing training backed by documented QC and certification practice.",
    icon: (
      <>
        <path d="M4 19V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14M4 19a2 2 0 0 1 2-2h14M12 12v7" />
      </>
    ),
  },
];

export function CareerPage() {
  const [department, setDepartment] = useState("All");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const departments = listDepartments();
  const filtered =
    department === "All" ? roles : roles.filter((r) => r.department === department);

  const handleToggle = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <>
      <CareerHero
        headline="Build the systems that move industry forward."
        copy="Join a team working across engineering, manufacturing, application support, sales and technology to solve real industrial challenges."
        ctaLabel="View Open Positions"
        openingsCount={roles.length}
        imageAlt="VR Coatings manufacturing facility — image placeholder to be added"
      />

      <CultureStrip items={cultureItems} />

      <section className="bg-[#F4F7FA]">
        <div className="mx-auto max-w-[1320px] px-4 py-14 sm:px-6 lg:px-8 lg:py-16">
          <div className="max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">
              Open Positions
            </p>
            <h2 className="mt-3 text-3xl font-semibold leading-tight text-[#082B4C] sm:text-4xl">
              Find your next opportunity.
            </h2>
            <p className="mt-4 text-base leading-7 text-slate-600">
              Explore current openings across our teams and find a role that matches your experience.
            </p>
          </div>
        </div>
      </section>

      <FilterBar
        departments={[...departments]}
        active={department}
        onChange={setDepartment}
        total={roles.length}
        filtered={filtered.length}
      />

      <section className="bg-[#F4F7FA] pb-16">
        <div className="mx-auto max-w-[1320px] px-4 sm:px-6 lg:px-8">
          {filtered.length === 0 ? (
            <div className="rounded-xl border border-dashed border-slate-300 bg-white py-16 text-center">
              <p className="text-sm font-medium text-slate-500">
                No open positions in this department at the moment.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {filtered.map((role) => (
                <div key={role.id} className="flex">
                  <JobCard
                    role={role}
                    expanded={expandedId === role.id}
                    onToggle={handleToggle}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <CareerCta
        eyebrow="Don't see your role?"
        title="Stay connected with VR Coatings."
        text="We're always interested in hearing from talented professionals. Share your resume and we can keep it on file for suitable future opportunities."
        primaryLabel="Send Your Resume"
        primaryHref="/contact"
      />

      <GetInTouchSection />
    </>
  );
}