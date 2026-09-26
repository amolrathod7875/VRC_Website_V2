export function HeritageSince() {
  return (
    <section
      aria-labelledby="heritage-since"
      className="relative overflow-hidden bg-white"
    >
      <div className="home-section-container py-16 lg:py-24">
        <div className="flex flex-col items-start gap-4 sm:flex-row sm:items-end sm:gap-8">
          <p className="text-xs font-semibold uppercase tracking-[0.32em] text-[#1678C8]">
            Since
          </p>
          <h2
            id="heritage-since"
            className="font-semibold leading-[0.85] tracking-[-0.04em] text-[#1678C8] select-none"
            style={{
              fontSize: "clamp(6.5rem, 22vw, 18rem)",
              WebkitTextStroke: "1.2px #1678C8",
              WebkitTextFillColor: "transparent",
              color: "transparent",
            }}
          >
            1985
          </h2>
        </div>
      </div>
    </section>
  );
}

