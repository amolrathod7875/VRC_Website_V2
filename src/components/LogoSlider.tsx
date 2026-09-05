import { clients } from "@/lib/data";
import { Placeholder } from "./Placeholder";

export function LogoSlider() {
  const logos = [...clients, ...clients];
  return (
    <section className="border-y border-slate-200 bg-surface py-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="mb-6 text-center text-xs font-semibold uppercase tracking-[0.24em] text-brand-800">
          Trusted by industrial partners
        </p>
        <div className="overflow-hidden">
          <div className="logo-marquee flex w-max gap-6">
            {logos.map((name, i) => (
              <Placeholder
                key={`${name}-${i}`}
                label={name}
                className="h-16 w-40 shrink-0 rounded-md"
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
