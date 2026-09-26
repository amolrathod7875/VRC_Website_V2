"use client";

import { useState } from "react";
import { offices, defaultOfficeId, type Office } from "@/lib/contactData";
import { OfficeGrid } from "@/components/OfficeCard";
import { OfficeMap } from "@/components/OfficeMap";
import { OpenInGoogleMapsButton, QuickContactActions } from "@/components/QuickContactActions";

export function ContactFindUs() {
  const [selectedId, setSelectedId] = useState<string>(defaultOfficeId);
  const selectedOffice: Office = offices.find((o) => o.id === selectedId) ?? offices[0];

  return (
    <section className="bg-[#F4F7FA] py-16 sm:py-20">
      <div className="mx-auto max-w-[1280px] px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-[46%_54%] lg:gap-10">
          <div className="lg:sticky lg:top-24 lg:self-start">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Our offices</p>
            <h2 className="mt-2 text-3xl font-bold text-[#082B4C] sm:text-4xl">Find Us</h2>
            <p className="mt-2 text-sm text-slate-500">
              Click any office card to see it on the map.
            </p>

            <div className="mt-8">
              <OfficeGrid selectedId={selectedId} onSelect={setSelectedId} />
            </div>
          </div>

          <div className="mt-12 lg:mt-0">
            <OfficeMap office={selectedOffice} />

            <div className="mt-4">
              <OpenInGoogleMapsButton office={selectedOffice} />
            </div>

            <div className="mt-5">
              <p className="mb-2.5 text-[11px] font-bold uppercase tracking-[0.16em] text-slate-400">
                Quick contact
              </p>
              <QuickContactActions />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}