"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  faqCategories,
  faqCategoryOrder,
  faqCategorySlugs,
  faqCategoryDescriptions,
  featuredFaqSlugs,
  findFaqItem,
  slugifyQuestion,
  type FaqCategory,
  type FaqItem,
} from "@/lib/faqs";

export function FaqPage() {
  const [query, setQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [openId, setOpenId] = useState<string | null>(null);
  const sectionRefs = useRef<Record<string, HTMLElement | null>>({});

  const visibleCategories = faqCategoryOrder
    .map((title) => faqCategories.find((c) => c.title === title))
    .filter((c): c is FaqCategory => Boolean(c));

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) return [];
    return visibleCategories
      .map((category) => ({
        category,
        questions: category.questions.filter(
          (item) =>
            item.q.toLowerCase().includes(q) ||
            item.a.toLowerCase().includes(q) ||
            category.title.toLowerCase().includes(q)
        ),
      }))
      .filter((entry) => entry.questions.length > 0);
  }, [query, visibleCategories]);

  const noResults = query.trim().length >= 2 && filtered.length === 0;

  useEffect(() => {
    if (!activeCategory) return;
    const id = sectionRefs.current[activeCategory];
    if (!id) return;
    const y = id.getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top: y, behavior: "smooth" });
  }, [activeCategory]);

  const handleCategoryClick = (title: string) => {
    setActiveCategory((prev) => (prev === title ? null : title));
  };

  const handleToggle = (id: string) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  const handleFeaturedClick = (slug: string) => {
    const found = findFaqItem(slug);
    if (!found) return;
    setActiveCategory(found.category.title);
    setTimeout(() => handleToggle(slug), 50);
  };

  const registerSection = (title: string) => (el: HTMLElement | null) => {
    sectionRefs.current[title] = el;
  };

  return (
    <div className="bg-[#F4F7FA] text-[#111827]">
      <FaqHero query={query} onQuery={setQuery} />

      <div className="mx-auto w-full max-w-[1280px] px-4 sm:px-6">
        <CategoryNav
          categories={visibleCategories}
          active={activeCategory}
          onClick={handleCategoryClick}
        />

        <FeaturedSection
          onQuestionClick={handleFeaturedClick}
          activeId={openId}
          onToggle={handleToggle}
        />

        {query.trim().length >= 2 && (
          <SearchResults
            query={query}
            entries={filtered}
            noResults={noResults}
            onToggle={handleToggle}
            activeId={openId}
          />
        )}

        <div className="space-y-16">
{visibleCategories.map((category, index) => (
            <FaqCategorySection
              key={category.title}
              category={category}
              index={index + 1}
              sectionRef={registerSection(category.title)}
              query={query}
              openId={openId}
              onToggle={handleToggle}
            />
          ))}
        </div>

        <StillNeedHelp />
      </div>
    </div>
  );
}
function FaqHero({ query, onQuery }: { query: string; onQuery: (v: string) => void }) {
  return (
    <section className="relative overflow-hidden bg-[#082B4C] text-white">
      <div className="mx-auto grid max-w-[1280px] px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-20">
        <div className="max-w-xl">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">Resources</p>
          <h1 className="mt-3 text-4xl font-semibold leading-[1.05] sm:text-5xl">
            Frequently Asked Questions
          </h1>
          <p className="mt-4 text-base leading-7 text-slate-200">
            Find answers about VR Coatings products, applications, technical support, sales, exports and service.
          </p>
          <div className="mt-7 flex w-full max-w-md items-center rounded-xl border border-white/15 bg-white/5 px-4 py-3 focus-within:border-[#1678C8] focus-within:bg-white/10">
            <input
              value={query}
              onChange={(e) => onQuery(e.target.value)}
              placeholder="Search FAQs..."
              className="w-full bg-transparent text-sm text-white placeholder:text-slate-300 outline-none"
              aria-label="Search FAQs"
            />
            <svg viewBox="0 0 24 24" className="h-5 w-5 shrink-0 text-slate-300" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="7" />
              <path d="M20 20l-3-3" strokeLinecap="round" />
            </svg>
          </div>
        </div>

        <div className="relative mt-10 hidden lg:mt-0 lg:flex lg:items-center lg:justify-end">
          <div className="grid w-full max-w-sm grid-cols-2 gap-4">
            <InfoGlyph>
              <svg viewBox="0 0 48 48" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M24 4a20 20 0 1 0 20 20A20 20 0 0 0 24 4zm0 6a14 14 0 1 1-14 14A14 14 0 0 1 24 10z" strokeLinejoin="round" />
                <path d="M18 24h12M18 30h8" strokeLinecap="round" />
              </svg>
            </InfoGlyph>
            <InfoGlyph>
              <svg viewBox="0 0 48 48" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1.8">
                <rect x="6" y="8" width="36" height="28" rx="3" strokeLinejoin="round" />
                <path d="M6 14h36" />
                <path d="M14 22h10M14 28h16" strokeLinecap="round" />
              </svg>
            </InfoGlyph>
            <InfoGlyph>
              <svg viewBox="0 0 48 48" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1.8">
                <circle cx="24" cy="24" r="16" />
                <path d="M24 8v8M24 32v8" strokeLinecap="round" />
                <path d="M8 24h8M32 24h8" strokeLinecap="round" />
                <path d="M14 14l6 6M28 28l6 6M14 34l6-6M28 14l6 6" strokeLinecap="round" />
              </svg>
            </InfoGlyph>
            <InfoGlyph>
              <svg viewBox="0 0 48 48" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M24 8a16 16 0 0 0-16 16c0 8 5 12 10 14l-2 6 4-2 2 2 2-2 2 2 2-2 2 2 2-2-2-6c5-2 10-6 10-14a16 16 0 0 0-16-16z" strokeLinejoin="round" />
                <path d="M18 24h12M18 30h8" strokeLinecap="round" />
              </svg>
            </InfoGlyph>
          </div>
        </div>
      </div>
    </section>
  );
}

function InfoGlyph({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-center rounded-2xl border border-white/15 bg-white/5 text-[#1678C8]">
      {children}
    </div>
  );
}
function CategoryNav({
  categories,
  active,
  onClick,
}: {
  categories: FaqCategory[];
  active: string | null;
  onClick: (title: string) => void;
}) {
  return (
    <nav aria-label="FAQ categories" className="mt-10 -mx-1 px-1 sm:-mx-2">
      <div className="flex gap-2 overflow-x-auto pb-2 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {categories.map((category) => {
          const isActive = active === category.title;
          return (
            <button
              key={category.title}
              type="button"
              onClick={() => onClick(category.title)}
              className={`whitespace-nowrap rounded-full border px-4 py-2 text-sm font-semibold transition-colors duration-200 ${
                isActive
                  ? "border-transparent bg-[#1678C8] text-white"
                  : "border-slate-200 bg-white text-[#0B5C97] hover:border-[#1678C8] hover:text-[#1678C8]"
              }`}
              aria-pressed={isActive}
            >
              {category.title}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
function FeaturedSection({
  onQuestionClick,
  activeId,
  onToggle,
}: {
  onQuestionClick: (slug: string) => void;
  activeId: string | null;
  onToggle: (id: string) => void;
}) {
  const featured = featuredFaqSlugs
    .map((slug) => findFaqItem(slug))
    .filter((item): item is { category: FaqCategory; item: FaqItem } => Boolean(item));

  return (
    <section className="mt-14">
      <div className="flex items-center gap-3">
        <span className="h-px flex-1 bg-slate-200" />
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">Most Asked</p>
        <span className="h-px flex-1 bg-slate-200" />
      </div>
      <p className="mt-3 text-sm text-slate-500">Quick answers to common questions</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {featured.map((entry) => {
          const slug = `${entry.category.title}:${slugifyQuestion(entry.item.q)}`;
          const isActive = activeId === slug;
          return (
            <button
              key={slug}
              type="button"
              onClick={() => onQuestionClick(slug)}
              className="group relative flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-5 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-[#1678C8] hover:shadow-[0_8px_24px_rgba(22,120,200,0.12)]"
            >
              <div className="flex items-center justify-between">
                <span className="rounded-full bg-[#F4F7FA] px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wider text-[#0B5C97]">
                  {entry.category.title}
                </span>
                <span className="text-[#1678C8] transition-transform duration-200 group-hover:translate-x-1">
                  <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
              </div>
              <span className="text-base font-semibold text-[#111827] transition-colors duration-200 group-hover:text-[#1678C8]">
                {entry.item.q}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
function SearchResults({
  query,
  entries,
  noResults,
  onToggle,
  activeId,
}: {
  query: string;
  entries: { category: FaqCategory; questions: FaqItem[] }[];
  noResults: boolean;
  onToggle: (id: string) => void;
  activeId: string | null;
}) {
  return (
    <section className="mt-14">
      <div className="flex items-center gap-3">
        <span className="h-px flex-1 bg-slate-200" />
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">Search Results</p>
        <span className="h-px flex-1 bg-slate-200" />
      </div>
      <p className="mt-3 text-sm text-slate-500">
        Showing matches for &ldquo;{query}&rdquo;
      </p>

      {noResults ? (
        <div className="mt-8 rounded-2xl border border-dashed border-slate-200 bg-white p-10 text-center">
          <p className="text-lg font-semibold text-[#111827]">No matching questions found.</p>
          <p className="mt-2 text-sm text-slate-500">
            Try another keyword or contact our team.
          </p>
          <Link
            href="/contact"
            className="mt-5 inline-flex items-center rounded-lg bg-[#1678C8] px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-[#0B5C97]"
          >
            Contact Us
          </Link>
        </div>
      ) : (
        <div className="mt-6 space-y-10">
          {entries.map((entry) => (
            <div key={entry.category.title}>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-[#0B5C97]">
                {entry.category.title}
              </h3>
              <div className="mt-3 space-y-3">
                {entry.questions.map((item) => {
                  const slug = `${entry.category.title}:${slugifyQuestion(item.q)}`;
                  return (
                    <FaqAccordionItem
                      key={slug}
                      item={item}
                      categoryTitle={entry.category.title}
                      slug={slug}
                      isOpen={activeId === slug}
                      onToggle={() => onToggle(slug)}
                    />
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
function FaqCategorySection({
  category,
  index,
  sectionRef,
  query,
  openId,
  onToggle,
}: {
  category: FaqCategory;
  index: number;
  sectionRef: (el: HTMLElement | null) => void;
  query: string;
  openId: string | null;
  onToggle: (id: string) => void;
}) {
  const q = query.trim().toLowerCase();
  const visibleQuestions =
    q.length >= 2
      ? category.questions.filter(
          (item) =>
            item.q.toLowerCase().includes(q) ||
            item.a.toLowerCase().includes(q) ||
            category.title.toLowerCase().includes(q)
        )
      : category.questions;

  if (q.length >= 2 && visibleQuestions.length === 0) {
    return null;
  }

  return (
    <section ref={sectionRef} id={faqCategorySlugs[category.title]} className="scroll-mt-28">
      <div className="grid items-start gap-8 lg:grid-cols-[220px_1fr]">
        <div className="lg:sticky lg:top-28">
          <span className="text-3xl font-bold text-[#1678C8]">{String(index).padStart(2, "0")}</span>
          <h2 className="mt-1 text-2xl font-bold text-[#082B4C]">{category.title}</h2>
          {faqCategoryDescriptions[category.title] ? (
            <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
              {faqCategoryDescriptions[category.title]}
            </p>
          ) : null}
        </div>

        <div className="space-y-3">
          {visibleQuestions.map((item) => {
            const slug = `${category.title}:${slugifyQuestion(item.q)}`;
            return (
              <FaqAccordionItem
                key={slug}
                item={item}
                categoryTitle={category.title}
                slug={slug}
                isOpen={openId === slug}
                onToggle={() => onToggle(slug)}
              />
            );
          })}
        </div>
      </div>
    </section>
  );
}
function FaqAccordionItem({
  item,
  categoryTitle,
  slug,
  isOpen,
  onToggle,
}: {
  item: FaqItem;
  categoryTitle: string;
  slug: string;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const contentRef = useRef<HTMLDivElement>(null);
  const [maxHeight, setMaxHeight] = useState(isOpen ? "auto" : "0px");

  useEffect(() => {
    const el = contentRef.current;
    if (!el) return;
    setMaxHeight(isOpen ? `${el.scrollHeight}px` : "0px");
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const el = contentRef.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const update = () => setMaxHeight(`${el.scrollHeight}px`);
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, [isOpen]);

  const contentId = `faq-content-${slug.replace(/[: ]/g, "-")}`;

  return (
    <div
      className={`overflow-hidden rounded-xl border bg-white transition-all duration-200 ease-out ${
        isOpen ? "border-[#1678C8] shadow-[0_8px_24px_rgba(22,120,200,0.14)]" : "border-slate-200 hover:border-[#1678C8] hover:-translate-y-0.5 hover:shadow-[0_6px_18px_rgba(8,43,76,0.08)]"
      }`}
    >
      <button
        type="button"
        aria-expanded={isOpen}
        aria-controls={contentId}
        onClick={onToggle}
        className="flex w-full items-center gap-4 px-5 py-4 text-left"
      >
        <span
          className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full border transition-colors duration-200 ${
            isOpen ? "border-[#1678C8] bg-[#1678C8] text-white" : "border-slate-300 bg-white text-[#0B5C97]"
          }`}
        >
          {isOpen ? (
            <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2.4">
              <path d="M5 10h10" strokeLinecap="round" />
            </svg>
          ) : (
            <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2.4">
              <path d="M10 5v10M5 10h10" strokeLinecap="round" />
            </svg>
          )}
        </span>
        <span className="flex-1 text-base font-semibold leading-snug text-[#111827]">{item.q}</span>
        <span
          className={`shrink-0 text-slate-400 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
        >
          <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5.5 7.5 10 12l4.5-4.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </span>
      </button>
      <div
        id={contentId}
        ref={contentRef}
        className="overflow-hidden transition-max-height duration-250 ease-out"
        style={{ maxHeight, opacity: isOpen ? 1 : 0, transition: "max-height 0.25s ease, opacity 0.2s ease" }}
      >
        <div className="px-5 pb-5 pl-12">
          <p className="text-[15px] leading-[1.7] text-slate-600">{item.a}</p>
        </div>
      </div>
    </div>
  );
}
function StillNeedHelp() {
  return (
    <section className="mt-20">
      <div className="overflow-hidden rounded-2xl bg-[#082B4C]">
        <div className="grid items-center gap-6 px-7 py-9 sm:px-10 sm:py-10 lg:grid-cols-[1fr_auto]">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#1678C8]">Still Need Help</p>
            <h2 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">
              Still have a question?
            </h2>
            <p className="mt-2 max-w-xl text-sm leading-6 text-slate-200">
              Talk to our team about your product, application or service requirement.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/contact"
              className="inline-flex items-center rounded-lg bg-[#1678C8] px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-[#0B5C97]"
            >
              Contact Us
            </Link>
            <Link
              href="/products"
              className="inline-flex items-center rounded-lg border border-white/30 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-white/10"
            >
              Explore Products
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
