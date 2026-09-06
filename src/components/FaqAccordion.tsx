"use client";

import { useEffect, useRef, useState } from "react";
import { IconArrowRight } from "@/components/Icon";
import { FAQ_VISIBLE, type FaqCategory, type FaqItem, faqCategories } from "@/lib/faqs";

export function FaqAccordion() {
  return (
    <div className="grid gap-10">
      {faqCategories.map((category) => (
        <FaqCategory key={category.title} category={category} />
      ))}
    </div>
  );
}

function FaqCategory({ category }: { category: FaqCategory }) {
  const [openId, setOpenId] = useState<string | null>(null);
  const [viewAll, setViewAll] = useState(false);

  const visible = viewAll ? category.questions : category.questions.slice(0, FAQ_VISIBLE);
  const hasMore = category.questions.length > FAQ_VISIBLE;

  const toggleViewAll = () => {
    if (viewAll) {
      setOpenId(null);
    }
    setViewAll((v) => !v);
  };

  return (
    <div className="space-y-3">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-brand-800">
        {category.title}
      </h2>
      <div className="space-y-2">
        {visible.map((item, i) => {
          const id = `${category.title}:${i}`;
          return (
            <FaqAccordionItem
              key={id}
              item={item}
              isOpen={openId === id}
              onToggle={() => setOpenId((prev) => (prev === id ? null : id))}
              contentId={`faq-content-${id.replace(/[: ]/g, "-")}`}
            />
          );
        })}
      </div>
      {hasMore && (
        <div className="pt-1 text-center">
          <button
            type="button"
            onClick={toggleViewAll}
            className="inline-flex items-center gap-1 text-sm font-semibold text-brand-700 hover:text-brand-800"
          >
            {viewAll ? "View Less" : "View More"}
          </button>
        </div>
      )}
    </div>
  );
}

function FaqAccordionItem({
  item,
  isOpen,
  onToggle,
  contentId,
}: {
  item: FaqItem;
  isOpen: boolean;
  onToggle: () => void;
  contentId: string;
}) {
  const contentRef = useRef<HTMLDivElement>(null);
  const [maxHeight, setMaxHeight] = useState("0px");

  useEffect(() => {
    const el = contentRef.current;
    if (!el) {
      return;
    }
    setMaxHeight(isOpen ? `${el.scrollHeight}px` : "0px");
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) {
      return;
    }
    const el = contentRef.current;
    if (!el || typeof ResizeObserver === "undefined") {
      return;
    }
    const update = () => setMaxHeight(`${el.scrollHeight}px`);
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, [isOpen]);

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
      <button
        type="button"
        aria-expanded={isOpen}
        aria-controls={contentId}
        onClick={onToggle}
        className="flex w-full items-center gap-3 px-5 py-4 text-left hover:bg-slate-50"
      >
        <span
          className={
            isOpen
              ? "shrink-0 rotate-90 transition-transform duration-200"
              : "shrink-0 transition-transform duration-200"
          }
        >
          <IconArrowRight className="h-4 w-4 text-brand-700" />
        </span>
        <span className="flex-1 font-semibold text-brand-900">{item.q}</span>
      </button>
      <div
        id={contentId}
        ref={contentRef}
        className="overflow-hidden px-5 text-sm leading-6 text-slate-600"
        style={{
          maxHeight,
          opacity: isOpen ? 1 : 0,
          transition: "max-height 0.3s ease, opacity 0.2s ease",
        }}
      >
        <div className="py-4">{item.a}</div>
      </div>
    </div>
  );
}
