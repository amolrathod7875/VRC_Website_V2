import type { ComponentType } from "react";
import { industries } from "@/lib/data";
import {
  IconBuilding,
  IconCar,
  IconCircuit,
  IconConstruction,
  IconFactory,
  IconFuel,
  IconPackage,
  IconPill,
  IconPlane,
  IconPrinter,
  IconShield,
  IconShip,
  IconSprout,
  IconTrain,
  IconTree,
  IconWind,
} from "./Icon";

type IconCmp = ComponentType<{ className?: string }>;

const ICON_BY_SLUG: Record<string, IconCmp> = {
  manufacturing: IconFactory,
  automotive: IconCar,
  "shipyard-marine": IconShip,
  defence: IconShield,
  aerospace: IconPlane,
  railways: IconTrain,
  "oil-gas": IconFuel,
  construction: IconConstruction,
  "wood-furniture": IconTree,
  packaging: IconPackage,
  printing: IconPrinter,
  agriculture: IconSprout,
  "pharma-food": IconPill,
  electronics: IconCircuit,
  "wind-energy": IconWind,
  infrastructure: IconBuilding,
};

export function IndustryGrid() {
  return (
    <section className="bg-surface">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-24">
        <div className="mb-12 max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-700">Industries We Serve</p>
          <h2 className="mt-3 text-3xl font-semibold leading-tight text-brand-950 sm:text-4xl">
            Coating programmes across industrial sectors.
          </h2>
          <p className="mt-4 text-base leading-7 text-slate-600">
            Specification, sampling and supply support for the sectors our coating systems serve.
          </p>
        </div>
        <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {industries.map((item) => {
            const Icon = ICON_BY_SLUG[item.slug] ?? IconFactory;
            return (
              <li key={item.slug}>
                <div className="group flex h-full flex-col items-center gap-4 rounded-lg border border-slate-200 bg-white p-6 text-center transition-all duration-200 ease-out hover:border-[#1678C8] hover:shadow-sm">
                  <span
                    aria-hidden
                    className="flex h-11 w-11 items-center justify-center text-[#1678C8] transition-transform duration-200 ease-out group-hover:scale-105"
                  >
                    <Icon className="h-11 w-11" />
                  </span>
                  <span className="text-sm font-semibold text-brand-950 transition-colors duration-200 ease-out group-hover:text-[#1678C8]">
                    {item.name}
                  </span>
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
