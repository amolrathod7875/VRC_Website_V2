"use client";

import { useState, useEffect, useCallback } from "react";
import { clientFeedback } from "@/lib/data";
import { Eyebrow } from "@/components/SectionHeading";

const PER_PAGE_DESKTOP = 2;
const TRANSITION_MS = 500;

function getInitials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

export function ClientFeedback() {
  const [page, setPage] = useState(0);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(max-width: 767px)");
    setIsMobile(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const perPage = isMobile ? 1 : PER_PAGE_DESKTOP;
  const totalPages = Math.ceil(clientFeedback.length / perPage);

  const canGoPrevious = page > 0;
  const canGoNext = page < totalPages - 1;

  const prev = useCallback(() => {
    setPage((p) => Math.max(0, p - 1));
  }, []);

  const next = useCallback(() => {
    setPage((p) => Math.min(totalPages - 1, p + 1));
  }, [totalPages]);

  const cardWidthPercent = (100 / clientFeedback.length) * perPage;
  const shiftPercent = page * (100 / clientFeedback.length) * perPage;

  const buttonBase =
    "flex h-11 w-11 items-center justify-center rounded-lg border border-slate-200 bg-white text-[#1678C8] transition-colors duration-200";

  return (
    <section className="bg-white py-28 sm:py-32 lg:py-36">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-[24%_1fr] lg:gap-12">
          <div className="flex flex-col justify-between">
            <Eyebrow>CLIENT FEEDBACK</Eyebrow>
            <div className="mt-8 flex gap-2.5">
              <button
                type="button"
                onClick={prev}
                aria-label="Previous testimonials"
                disabled={!canGoPrevious}
                className={`${buttonBase} ${
                  !canGoPrevious
                    ? "pointer-events-none opacity-40"
                    : "hover:bg-[#1678C8] hover:text-white"
                }`}
              >
                <svg
                  viewBox="0 0 20 20"
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    d="M12 4l-6 6 6 6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
              <button
                type="button"
                onClick={next}
                aria-label="Next testimonials"
                disabled={!canGoNext}
                className={`${buttonBase} ${
                  !canGoNext
                    ? "pointer-events-none opacity-40"
                    : "hover:bg-[#1678C8] hover:text-white"
                }`}
              >
                <svg
                  viewBox="0 0 20 20"
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    d="M8 4l6 6-6 6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>

          <div>
            <h2 className="max-w-[820px] text-[40px] sm:text-[44px] font-semibold leading-[1.1] text-gray-900">
              Industrial companies rely on VR Coatings for equipment that{" "}
              <span className="text-[#1678C8]">performs reliably</span> under real operational
              conditions.
            </h2>

            <div className="relative mt-10 overflow-hidden">
              <div
                className="flex"
                style={{
                  transform: `translateX(-${shiftPercent}%)`,
                  transition: `transform ${TRANSITION_MS}ms ease-out`,
                }}
              >
                {clientFeedback.map((item) => (
                  <div
                    key={item.id}
                    className="flex-shrink-0 px-3"
                    style={{ width: `${cardWidthPercent}%` }}
                  >
                    <div className="flex h-full min-h-[240px] flex-col rounded-xl border border-slate-200 bg-[#F4F4F4] p-6">
                      <div className="flex items-center gap-4">
                        {item.image ? (
                          <img
                            src={item.image}
                            alt={item.name}
                            className="h-14 w-14 rounded-lg object-cover"
                          />
                        ) : (
                          <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-slate-300 text-lg font-semibold text-white">
                            {getInitials(item.name)}
                          </div>
                        )}
                        <div>
                          <p className="text-sm font-semibold text-gray-900">{item.name}</p>
                          <p className="text-xs text-slate-500">{item.role}</p>
                          <p className="mt-0.5 flex items-center gap-1 text-[12px] text-slate-400">
                            <svg
                              viewBox="0 0 20 20"
                              className="h-3 w-3"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={1.6}
                            >
                              <path
                                d="M10 2C6.5 2 4 4.8 4 8.2c0 4.3 3.3 7.4 6 9.6.5.4 1.5.4 2 0 2.7-2.2 6-5.3 6-9.6C16 4.8 13.5 2 10 2z"
                                strokeLinejoin="round"
                              />
                              <circle cx="10" cy="8.2" r="1.8" />
                            </svg>
                            {item.location}
                          </p>
                        </div>
                      </div>
                      <p className="mt-4 text-sm leading-6 text-gray-700">{item.feedback}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}