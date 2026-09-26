import Link from "next/link";
import { Eyebrow } from "./SectionHeading";
import { IconArrowRight } from "./Icon";

export function BrandStatement() {
  return (
    <section className="relative overflow-hidden bg-[#062746] text-white">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage:
            "linear-gradient(#9fc1e3 1px, transparent 1px), linear-gradient(90deg, #9fc1e3 1px, transparent 1px)",
          backgroundSize: "64px 64px",
        }}
      />
      <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
        <div className="grid items-end gap-12 lg:grid-cols-[1fr_auto]">
          <div className="max-w-3xl">
            <Eyebrow tone="white">About VR Coatings</Eyebrow>
            <h2 className="mt-4 text-4xl font-semibold leading-[1.05] tracking-tight text-white sm:text-5xl lg:text-6xl">
              Engineered coatings.
              <br />
              <span className="text-[#7FB1DC]">Built for industry.</span>
            </h2>
            <p className="mt-8 max-w-2xl text-base leading-8 text-slate-200 sm:text-lg">
              Solutions engineered around real-world performance. VR Coatings develops, manufactures, and
              supports industrial coating systems for OEM lines and maintenance programmes — pairing
              formulation science with application support so films perform in the field, not only in the lab.
            </p>
          </div>
          <div className="flex flex-col gap-3 text-sm uppercase tracking-[0.28em] text-slate-300">
            <span>Engineering</span>
            <span className="text-[#7FB1DC]">Protection</span>
            <span>Performance</span>
            <span>Reliability</span>
          </div>
        </div>

        <div className="mt-16 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="max-w-xl text-sm leading-6 text-slate-300">
            A serious industrial coatings company — specified by manufacturers who need predictable
            protection on critical surfaces.
          </p>
          <Link
            href="/about"
            className="inline-flex items-center gap-2 self-start rounded-md bg-white px-5 py-3 text-sm font-semibold text-[#062746] transition hover:bg-[#F4F7FA] sm:self-auto"
          >
            About VR Coatings
            <IconArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    </section>
  );
}
