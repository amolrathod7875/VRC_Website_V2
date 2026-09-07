"use client";

import { useRef, useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import type { LandingProduct } from "@/lib/data";

const STICKY_TOP = 100;
const CARD_HEIGHT = 410;
const TRANSITIONS = 5;
const SECTION_VH = 520;
const SCALE_MIN = 0.97;
const SCALE_PEAK = 1.015;
const SCALE_PEAK_PROGRESS = 0.82;

function easeInOutCubic(t: number) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

export function ProductWheel({ products }: { products: LandingProduct[] }) {
  const [isDesktop, setIsDesktop] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [progress, setProgress] = useState(0);
  const sectionRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | undefined>(0);

  useEffect(() => {
    const checkDesktop = () => setIsDesktop(window.innerWidth >= 1024);
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const checkReducedMotion = () => setReducedMotion(mq.matches);

    checkDesktop();
    checkReducedMotion();
    mq.addEventListener("change", checkReducedMotion);
    window.addEventListener("resize", checkDesktop);

    return () => {
      mq.removeEventListener("change", checkReducedMotion);
      window.removeEventListener("resize", checkDesktop);
    };
  }, []);

  useEffect(() => {
    if (!isDesktop || reducedMotion) return;

    const section = sectionRef.current;
    if (!section) return;

    const handleScroll = () => {
      if (rafRef.current) return;

      rafRef.current = requestAnimationFrame(() => {
        const rect = section.getBoundingClientRect();
        const sectionTop = rect.top;
        const sectionHeight = rect.height;
        const viewportHeight = window.innerHeight;

        const scrollRange = sectionHeight - viewportHeight;
        const rawProgress = scrollRange > 0 ? (STICKY_TOP - sectionTop) / scrollRange : 0;
        const clampedProgress = Math.max(0, Math.min(1, rawProgress));

        setProgress(clampedProgress);
        rafRef.current = undefined;
      });
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isDesktop, reducedMotion, products.length]);

  if (!products.length) return null;

  if (!isDesktop || reducedMotion) {
    return (
      <div className="mt-12 space-y-6 lg:mt-0">
        {products.map((product) => (
          <div
            key={product.slug}
            className="overflow-hidden rounded-2xl bg-[#082B4C] shadow-[0_16px_40px_rgba(8,43,76,0.10)]"
          >
            <div className="grid grid-cols-1 md:grid-cols-[45%_1fr]">
              <div className="relative flex items-center justify-center bg-[#F4F7FA] p-6">
                {product.image && (
                  <Image
                    src={product.image}
                    alt={product.name}
                    width={480}
                    height={360}
                    className="max-h-56 w-auto object-contain md:max-h-64"
                  />
                )}
              </div>
              <div className="flex flex-col justify-center p-6 text-white md:p-8">
                <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#1678C8]">
                  {product.category}
                </p>
                <h3 className="mt-2 text-xl font-semibold text-white md:text-2xl">
                  {product.name}
                </h3>
                <p className="mt-3 text-sm leading-6 text-white/75 line-clamp-3">
                  {product.description}
                </p>
                <Link
                  href={`/products/${product.slug}`}
                  className="mt-5 inline-flex items-center gap-2 rounded-lg border border-white/15 px-4 py-2.5 text-sm font-semibold text-white transition-all duration-200 hover:border-[#1678C8] hover:bg-[#1678C8] w-fit"
                >
                  View Full Details
                  <svg
                    viewBox="0 0 20 20"
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      d="M5 10h10M11 5l5 5-5 5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const totalProgress = progress * TRANSITIONS;
  const currentStep = Math.floor(totalProgress);
  const localProgress = totalProgress - currentStep;

  const sectionHeight = window.innerHeight + TRANSITIONS * CARD_HEIGHT * 1.25;

  return (
    <div
      ref={sectionRef}
      className="hidden lg:block relative"
      style={{ height: `${sectionHeight}px` }}
    >
      <div
        className="sticky overflow-hidden"
        style={{ top: STICKY_TOP, height: CARD_HEIGHT }}
      >
        <div className="relative h-full w-full max-w-[720px]">
          {products.map((product, i) => {
            let translateY = "100%";
            let scale = 1;

            if (i < currentStep) {
              translateY = "0%";
              scale = 1;
            } else if (i === currentStep) {
              translateY = "0%";
              scale = 1;
            } else if (i === currentStep + 1) {
              const easedLocalProgress = easeInOutCubic(localProgress);
              translateY = `${(1 - easedLocalProgress) * 100}%`;

              if (localProgress <= SCALE_PEAK_PROGRESS) {
                const t = easeInOutCubic(localProgress / SCALE_PEAK_PROGRESS);
                scale = SCALE_MIN + (SCALE_PEAK - SCALE_MIN) * t;
              } else {
                const t = easeInOutCubic((localProgress - SCALE_PEAK_PROGRESS) / (1 - SCALE_PEAK_PROGRESS));
                scale = SCALE_PEAK - (SCALE_PEAK - 1) * t;
              }
            } else {
              translateY = "100%";
              scale = 1;
            }

            return (
              <div
                key={product.slug}
                className="absolute inset-0"
                style={{
                  transform: `translateY(${translateY}) scale(${scale})`,
                  zIndex: i + 1,
                  willChange: "transform",
                }}
              >
                <ProductShowcaseCard product={product} />
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function ProductShowcaseCard({ product }: { product: LandingProduct }) {
  return (
    <div className="h-full w-full overflow-hidden rounded-2xl bg-[#082B4C] shadow-[0_16px_40px_rgba(8,43,76,0.10)]">
      <div className="grid h-full grid-cols-1 md:grid-cols-[45%_1fr]">
        <div className="relative flex items-center justify-center bg-[#F4F7FA] p-6">
          {product.image ? (
            <Image
              src={product.image}
              alt={product.name}
              width={480}
              height={360}
              className="max-h-56 w-auto object-contain md:max-h-64"
            />
          ) : (
            <div className="flex h-40 w-full items-center justify-center text-sm text-slate-400">
              {product.name}
            </div>
          )}
        </div>

        <div className="flex flex-col justify-center p-6 text-white md:p-8">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#1678C8]">
            {product.category}
          </p>
          <h3 className="mt-2 text-xl font-semibold text-white md:text-2xl">
            {product.name}
          </h3>
          <p className="mt-3 text-sm leading-6 text-white/75 line-clamp-3">
            {product.description}
          </p>
          <Link
            href={`/products/${product.slug}`}
            className="mt-5 inline-flex items-center gap-2 rounded-lg border border-white/15 px-4 py-2.5 text-sm font-semibold text-white transition-all duration-200 hover:border-[#1678C8] hover:bg-[#1678C8] w-fit"
          >
            View Full Details
            <svg
              viewBox="0 0 20 20"
              className="h-4 w-4"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                d="M5 10h10M11 5l5 5-5 5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </Link>
        </div>
      </div>
    </div>
  );
}
