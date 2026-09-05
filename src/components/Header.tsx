"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useMemo, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import { navItems, searchIndex } from "@/lib/data";

const SECTION_TO_NAV: Record<string, string> = {
  products: "Products",
  applications: "Applications",
};

function SearchControl() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  useEffect(() => {
    setOpen(false);
    setQuery("");
  }, [pathname]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return searchIndex
      .filter((item) => `${item.title} ${item.keywords}`.toLowerCase().includes(q))
      .slice(0, 8);
  }, [query]);

  return (
    <div className="relative">
      <div className="flex items-center justify-end">
        <label className="sr-only" htmlFor="site-search">
          Search
        </label>
        <input
          id="site-search"
          ref={inputRef}
          value={query}
          autoComplete="off"
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search products, pages..."
          className={`h-10 rounded-md border border-brand-100 bg-white px-3 text-sm text-slate-800 outline-none transition-all duration-300 focus:border-brand-600 ${
            open ? "w-44 opacity-100 sm:w-64" : "w-0 border-transparent p-0 opacity-0"
          }`}
        />
        <button
          type="button"
          aria-expanded={open}
          aria-label={open ? "Close search" : "Open search"}
          onClick={() => {
            setOpen((v) => !v);
            if (open) setQuery("");
          }}
          className="ml-2 flex h-10 w-10 items-center justify-center rounded-md text-brand-900 hover:bg-brand-50"
        >
          <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="7" />
            <path d="M20 20l-3-3" />
          </svg>
        </button>
      </div>
      {open && query && (
        <div className="absolute right-0 z-50 mt-2 w-72 overflow-hidden rounded-md border border-slate-200 bg-white shadow-lg sm:w-80">
          {results.length === 0 ? (
            <p className="px-4 py-3 text-sm text-slate-500">No matches found.</p>
          ) : (
            results.map((item) => (
              <Link
                key={item.href + item.title}
                href={item.href}
                className="block px-4 py-2.5 text-sm text-slate-700 hover:bg-brand-50 hover:text-brand-800"
              >
                {item.title}
              </Link>
            ))
          )}
        </div>
      )}
    </div>
  );
}

type NavLinkProps = {
  label: string;
  href: string;
  active: boolean;
  hasChildren: boolean;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
};

function NavLink({ label, href, active, hasChildren, onMouseEnter, onMouseLeave }: NavLinkProps) {
  return (
    <Link
      href={href}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      aria-current={active ? "page" : undefined}
      className="group relative inline-flex items-center gap-1 px-3 py-3 text-sm font-medium transition-colors duration-200 ease-out"
    >
      <span
        className={`transition-colors duration-200 ease-out ${
          active ? "text-[#1678C8]" : "text-slate-900 group-hover:text-[#1678C8]"
        }`}
      >
        {label}
      </span>
      {hasChildren && (
        <svg
          viewBox="0 0 20 20"
          className={`h-3.5 w-3.5 transition-colors duration-200 ease-out ${
            active ? "text-[#1678C8]" : "text-slate-700 group-hover:text-[#1678C8]"
          }`}
          fill="currentColor"
        >
          <path d="M5.5 7.5 10 12l4.5-4.5" />
        </svg>
      )}
      <span
        aria-hidden
        className={`pointer-events-none absolute left-3 right-3 -bottom-px h-[2px] origin-left rounded-full bg-[#1678C8] transition-transform duration-300 ease-out ${
          active
            ? "scale-x-100"
            : "scale-x-0 group-hover:scale-x-100"
        }`}
      />
    </Link>
  );
}

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  useEffect(() => {
    setMobileOpen(false);
    setOpenMenu(null);
  }, [pathname]);

  useEffect(() => {
    if (pathname !== "/") {
      setActiveSection(null);
      return;
    }
    const sections = Object.keys(SECTION_TO_NAV)
      .map((id) => document.getElementById(id))
      .filter((el): el is HTMLElement => el !== null);
    if (sections.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]) {
          setActiveSection(visible[0].target.id);
        }
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: [0, 0.25, 0.5, 0.75, 1] }
    );
    sections.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [pathname]);

  const isRouteActive = (item: (typeof navItems)[number]) => {
    if (item.href === "/") {
      return pathname === "/" && activeSection === null;
    }
    return (
      pathname === item.href ||
      pathname.startsWith(`${item.href}/`) ||
      (item.children?.some((c) => pathname === c.href) ?? false)
    );
  };

  const isSectionActive = (label: string) =>
    pathname === "/" && activeSection !== null && SECTION_TO_NAV[activeSection] === label;

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white">
      <div className="mx-auto flex w-[94%] max-w-[1600px] items-center justify-between gap-6 px-4 py-3 sm:px-6 lg:px-10 xl:px-12">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/vrc-logo.png"
            alt="VR Coatings logo"
            width={176}
            height={44}
            priority
            className="h-11 w-auto"
          />
          <span className="leading-tight">
            <span className="block text-sm font-semibold tracking-wide text-brand-900">VR Coatings</span>
            <span className="block text-[11px] uppercase tracking-[0.18em] text-slate-500">Pvt. Ltd.</span>
          </span>
        </Link>
        <div className="flex items-center gap-2">
          <SearchControl />
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 text-brand-900 lg:hidden"
            aria-label="Toggle menu"
            onClick={() => setMobileOpen((v) => !v)}
          >
            <span className="sr-only">Menu</span>
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
              {mobileOpen ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
            </svg>
          </button>
        </div>
      </div>
      <nav className="border-t border-slate-200 bg-white">
        <div className="mx-auto hidden w-[94%] max-w-[1600px] items-center gap-2 px-4 lg:flex lg:px-10 xl:px-12">
          {navItems.map((item) => {
            const active = isRouteActive(item) || isSectionActive(item.label);
            return (
              <div
                key={item.label}
                className="relative"
                onMouseEnter={() => item.children && setOpenMenu(item.label)}
                onMouseLeave={() => setOpenMenu(null)}
              >
                <NavLink
                  label={item.label}
                  href={item.href}
                  active={active}
                  hasChildren={Boolean(item.children)}
                />
                {item.children && openMenu === item.label && (
                  <div className="absolute left-0 top-full min-w-56 overflow-hidden rounded-b-md border border-slate-200 bg-white shadow-xl">
                    {item.children.map((child) => {
                      const childActive = pathname === child.href;
                      return (
                        <Link
                          key={child.href}
                          href={child.href}
                          className={`block px-4 py-2.5 text-sm transition-colors duration-200 ${
                            childActive
                              ? "bg-brand-50 text-[#1678C8]"
                              : "text-slate-700 hover:bg-brand-50 hover:text-[#1678C8]"
                          }`}
                        >
                          {child.label}
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
        {mobileOpen && (
          <div className="space-y-1 border-t border-slate-200 bg-white px-4 py-3 lg:hidden">
            {navItems.map((item) => {
              const active = isRouteActive(item) || isSectionActive(item.label);
              return (
                <div key={item.label} className="border-b border-slate-200 py-1 last:border-b-0">
                  <Link
                    href={item.href}
                    className={`block py-2 text-sm font-medium transition-colors ${
                      active ? "text-[#1678C8]" : "text-slate-900 hover:text-[#1678C8]"
                    }`}
                  >
                    {item.label}
                  </Link>
                  {item.children?.map((child) => {
                    const childActive = pathname === child.href;
                    return (
                      <Link
                        key={child.href}
                        href={child.href}
                        className={`block py-1.5 pl-3 text-sm transition-colors ${
                          childActive ? "text-[#1678C8]" : "text-slate-600 hover:text-[#1678C8]"
                        }`}
                      >
                        {child.label}
                      </Link>
                    );
                  })}
                </div>
              );
            })}
          </div>
        )}
      </nav>
    </header>
  );
}
