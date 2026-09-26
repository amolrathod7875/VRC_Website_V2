import Link from "next/link";

type GetInTouchSectionProps = {
  eyebrow?: string;
  title?: string;
  text?: string;
  primaryHref?: string;
  primaryLabel?: string;
  secondaryHref?: string;
  secondaryLabel?: string;
};

/**
 * Single shared Get in Touch section used across the entire website.
 *
 * This is the MASTER version originally shipped on the homepage. It is kept
 * byte-for-byte identical so every page reuses the exact same video, overlay,
 * content, buttons, sizing and responsive behaviour. Do not create variants.
 */
export function GetInTouchSection({
  eyebrow = "Get in touch",
  title = "Ready to discuss your coating requirements?",
  text = "Talk to our team about the right coating system for your application, substrate and operating environment.",
  primaryHref = "/contact",
  primaryLabel = "Discuss Your Requirement",
  secondaryHref = "/contact",
  secondaryLabel = "Contact Us",
}: GetInTouchSectionProps) {
  return (
    <section className="relative bg-[#062746] text-white min-h-screen flex flex-col">
      <video
        autoPlay
        muted
        loop
        playsInline
        preload="metadata"
        className="absolute inset-0 z-0 h-full w-full object-cover"
      >
        <source src="/media/videos/homepage/get_in_touch.mp4" type="video/mp4" />
      </video>
      <div
        className="absolute inset-0 z-10"
        style={{ backgroundColor: "rgba(6, 31, 54, 0.65)" }}
      />
      <div className="home-section-container flex-1 flex items-center py-20 lg:py-32">
        <div className="max-w-[600px]">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">{eyebrow}</p>
          <h2 className="mt-4 text-4xl font-semibold leading-[1.1] text-white sm:text-5xl">{title}</h2>
          <p className="mt-5 max-w-2xl text-base leading-8 text-slate-200">{text}</p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              href={primaryHref}
              className="inline-flex rounded-md bg-[#1678C8] px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-[#1269A8]"
            >
              {primaryLabel}
            </Link>
            <Link
              href={secondaryHref}
              className="inline-flex rounded-md border border-white/30 px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-white/10"
            >
              {secondaryLabel}
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}