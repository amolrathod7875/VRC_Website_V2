import { trustPillars } from "@/lib/data";
import { IconCustom, IconEngineered, IconApplication, IconProtection, IconQuality } from "./Icon";

const ICONS = [IconEngineered, IconQuality, IconApplication, IconProtection, IconCustom];

export function TrustStrip() {
  return (
    <section className="border-y border-slate-200 bg-white">
      <div className="home-section-container">
        <div className="grid divide-y divide-slate-200 sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-5">
          {trustPillars.map((pillar, i) => {
            const Icon = ICONS[i] ?? IconEngineered;
            return (
              <div
                key={pillar.title}
                className="flex items-start gap-4 px-4 py-6 sm:px-6 lg:border-r lg:border-slate-200 lg:px-6 lg:py-8 last:lg:border-r-0"
              >
                <div className="h-10 w-10 shrink-0 text-brand-700">
                  <Icon className="h-10 w-10" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-brand-950">{pillar.title}</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">{pillar.text}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
