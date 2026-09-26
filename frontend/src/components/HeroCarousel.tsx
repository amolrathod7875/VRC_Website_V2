"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { upcomingProducts } from "@/lib/data";

export function HeroCarousel() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => {
      setIndex((i) => (i + 1) % upcomingProducts.length);
    }, 5500);
    return () => window.clearInterval(id);
  }, []);

  const slide = upcomingProducts[index];

  return (
    <section className="bg-[#062746] text-white">
      <div className="mx-auto grid max-w-7xl items-stretch gap-0 lg:grid-cols-2">
        <div className="flex flex-col justify-center px-4 py-14 sm:px-6 lg:px-8">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand-100">Upcoming Products</p>
          <div key={slide.id} className="hero-slide-enter">
            <h1 className="mt-4 max-w-xl text-4xl font-semibold leading-tight text-white sm:text-5xl">
              {slide.title}
            </h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-slate-200">{slide.summary}</p>
          </div>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              href="/#products"
              className="rounded-md bg-[#1678C8] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#1269A8]"
            >
              Explore Products
            </Link>
          </div>
          <div className="mt-10 flex gap-2">
            {upcomingProducts.map((item, i) => (
              <button
                key={item.id}
                type="button"
                aria-label={`Show ${item.title}`}
                onClick={() => setIndex(i)}
                className={`h-2.5 rounded-full transition ${i === index ? "w-8 bg-white" : "w-2.5 bg-white/40"}`}
              />
            ))}
          </div>
        </div>
        <div className="relative min-h-[280px] overflow-hidden lg:min-h-[460px]">
          <Image
            src="/landing-industrial-coatings.jpg"
            alt="Industrial coating manufacturing facility with chimneys, tanks, and cranes"
            fill
            priority
            sizes="(max-width: 1024px) 100vw, 50vw"
            className="object-cover object-center"
          />
        </div>
      </div>
    </section>
  );
}
