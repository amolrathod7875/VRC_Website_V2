"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useMemo, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import { navItems, searchIndex } from "@/lib/data";

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

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);

  useEffect(() => {
    setMobileOpen(false);
    setOpenMenu(null);
  }, [pathname]);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
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
      <nav className="border-t border-slate-100 bg-brand-900">
        <div className="mx-auto hidden w-[94%] max-w-[1600px] items-center gap-2 px-4 lg:flex lg:px-10 xl:px-12">
          {navItems.map((item) => {
            const active =
              item.href === "/"
                ? pathname === "/"
                : pathname === item.href ||
                  pathname.startsWith(`${item.href}/`) ||
                  (item.children?.some((c) => pathname === c.href) ?? false);
            return (
              <div
                key={item.label}
                className="relative"
                onMouseEnter={() => item.children && setOpenMenu(item.label)}
                onMouseLeave={() => setOpenMenu(null)}
              >
                <Link
                  href={item.href}
                  className={`inline-flex items-center gap-1 px-3 py-3 text-sm font-medium ${
                    active ? "bg-brand-800 text-white" : "text-slate-100 hover:bg-brand-800"
                  }`}
                >
                  {item.label}
                  {item.children && (
                    <svg viewBox="0 0 20 20" className="h-3.5 w-3.5" fill="currentColor">
                      <path d="M5.5 7.5 10 12l4.5-4.5" />
                    </svg>
                  )}
                </Link>
                {item.children && openMenu === item.label && (
                  <div className="absolute left-0 min-w-52 overflow-hidden rounded-b-md bg-white shadow-xl">
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        className="block px-4 py-2.5 text-sm text-slate-700 hover:bg-brand-50 hover:text-brand-800"
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
        {mobileOpen && (
          <div className="space-y-1 px-4 py-3 lg:hidden">
            {navItems.map((item) => (
              <div key={item.label} className="border-b border-brand-800/70 py-1">
                <Link href={item.href} className="block py-2 text-sm font-medium text-white">
                  {item.label}
                </Link>
                {item.children?.map((child) => (
                  <Link key={child.href} href={child.href} className="block py-1.5 pl-3 text-sm text-brand-100">
                    {child.label}
                  </Link>
                ))}
              </div>
            ))}
          </div>
        )}
      </nav>
    </header>
  );
}
