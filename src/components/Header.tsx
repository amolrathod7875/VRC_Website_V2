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

const MEGA_MENU_LABELS = new Set(["About", "Our Assets", "Resources"]);

const MEGA_MENU_CONFIG: Record<
  string,
  {
    width?: string;
    columns: { title?: string; links: { label: string; href: string }[] }[];
    image?: { src: string; alt: string };
    cta?: { label: string; href: string };
  }
> = {
  About: {
    width: "720px",
    columns: [
      {
        title: "Company",
        links: [
          { label: "About VR Coatings", href: "/about" },
          { label: "Why Choose Us", href: "/about/why-choose-us" },
          { label: "Global Presence", href: "/about/global-presence" },
        ],
      },
    ],
    image: {
      src: "/VR-Coatings-Pvt-Ltd-Factory.png",
      alt: "VR Coatings facility",
    },
    cta: {
      label: "Contact Us",
      href: "/contact",
    },
  },
  "Our Assets": {
    width: "640px",
    columns: [
      {
        title: "Assets",
        links: [
          { label: "Partners", href: "/assets/partners" },
          { label: "Clients", href: "/assets/clients" },
          { label: "Industries We Serve", href: "/assets/industries" },
        ],
      },
    ],
    image: {
      src: "/VR-Coatings-Pvt-Ltd-Factory.png",
      alt: "VR Coatings operations",
    },
    cta: {
      label: "Contact Us",
      href: "/contact",
    },
  },
  Resources: {
    width: "680px",
    columns: [
      {
        title: "Learn",
        links: [
          { label: "Blog", href: "/resources/blog" },
          { label: "News", href: "/resources/news" },
        ],
      },
      {
        title: "Support",
        links: [
          { label: "Certifications", href: "/resources/certifications" },
          { label: "Career", href: "/resources/career" },
          { label: "FAQs", href: "/resources/faqs" },
        ],
      },
    ],
    image: {
      src: "/BLOGS/Blog_1.png",
      alt: "VR Coatings resources",
    },
    cta: {
      label: "View Catalog",
      href: "/catalog",
    },
  },
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
  compact?: boolean;
  mega?: boolean;
  open?: boolean;
};

function NavLink({ label, href, active, hasChildren, onMouseEnter, onMouseLeave, compact, mega, open }: NavLinkProps) {
  const px = compact ? "2.5" : "3";
  return (
    <Link
      href={href}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      aria-current={active ? "page" : undefined}
      className={`group relative inline-flex items-center gap-1 transition-colors duration-200 ease-out ${compact ? `px-${px} py-2 text-xs font-medium` : `px-${px} py-3 text-sm font-medium`}`}
    >
      <span
        className={`transition-colors duration-200 ease-out ${
          active || open ? "text-[#1678C8]" : "text-slate-900 group-hover:text-[#1678C8]"
        }`}
      >
        {label}
      </span>
      {hasChildren && mega && (
        <svg
          viewBox="0 0 20 20"
          className={`h-3.5 w-3.5 transition-all duration-200 ease-out ${
            open ? "rotate-180 text-[#1678C8]" : "text-slate-700 group-hover:text-[#1678C8]"
          }`}
          fill="currentColor"
          aria-hidden
        >
          <path d="M5.5 7.5 10 12l4.5-4.5" />
        </svg>
      )}
      {hasChildren && !mega && (
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
        className={`pointer-events-none absolute left-${px} right-${px} -bottom-px h-[2px] origin-left rounded-full bg-[#1678C8] transition-transform duration-300 ease-out ${
          active
            ? "scale-x-100"
            : "scale-x-0 group-hover:scale-x-100"
        }`}
      />
    </Link>
  );
}

function MegaMenuPanel({ label, onClose }: { label: string; onClose: () => void }) {
  const config = MEGA_MENU_CONFIG[label];
  if (!config) return null;

  const columns = config.columns ?? [];
  const colCount = columns.length;

  return (
    <div
      className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_12px_40px_rgba(0,0,0,0.10)]"
      style={{ width: config.width ?? "auto" }}
      onMouseEnter={() => {}}
      onMouseLeave={onClose}
    >
      <div className={`grid gap-8 p-6 ${config.image ? "lg:grid-cols-[1fr_220px]" : ""}`}>
        <div className={`grid gap-6 ${colCount === 2 ? "grid-cols-2" : "grid-cols-1"}`}>
          {columns.map((col) => (
            <div key={col.title ?? col.links[0]?.label}>
              {col.title && (
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                  {col.title}
                </p>
              )}
              <ul className="space-y-2">
                {col.links.map((link) => (
                  <li key={link.href + link.label}>
                    <Link
                      href={link.href}
                      onClick={onClose}
                      className="group flex items-center gap-2 text-sm font-medium text-slate-700 transition-colors duration-200 hover:text-[#1678C8]"
                    >
                      <span className="h-1 w-1 rounded-full bg-slate-300 transition-colors duration-200 group-hover:bg-[#1678C8]" />
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {config.image && (
          <div className="hidden lg:flex flex-col gap-4">
            <div className="relative overflow-hidden rounded-xl bg-slate-100">
              <Image
                src={config.image.src}
                alt={config.image.alt}
                width={220}
                height={160}
                className="h-40 w-full object-cover"
              />
            </div>
            {config.cta && (
              <Link
                href={config.cta.href}
                onClick={onClose}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#082B4C] px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
              >
                {config.cta.label}
                <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </Link>
            )}
          </div>
        )}

        {!config.image && config.cta && (
          <div className="hidden lg:flex items-center">
            <Link
              href={config.cta.href}
              onClick={onClose}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#082B4C] px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
            >
              {config.cta.label}
              <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<string | null>(null);
  const [scrolled, setScrolled] = useState(false);
  const [megaOpen, setMegaOpen] = useState(false);
  const [megaLabel, setMegaLabel] = useState<string | null>(null);
  const hoverTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const megaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMobileOpen(false);
    setOpenMenu(null);
    setMegaOpen(false);
    setMegaLabel(null);
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

  useEffect(() => {
    if (pathname !== "/") return;
    const handleScroll = () => setScrolled(window.scrollY > 24);
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [pathname]);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setMegaOpen(false);
        setMegaLabel(null);
        setOpenMenu(null);
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [pathname]);

  const isHome = pathname === "/";

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

  const desktopNavItems = navItems.filter((item) => item.label !== "Contact Us");

  const openMega = (label: string) => {
    if (hoverTimer.current) clearTimeout(hoverTimer.current);
    setMegaLabel(label);
    setMegaOpen(true);
    setOpenMenu(null);
  };

  const closeMega = () => {
    hoverTimer.current = setTimeout(() => {
      setMegaOpen(false);
      setMegaLabel(null);
    }, 120);
  };

  const keepMegaOpen = () => {
    if (hoverTimer.current) clearTimeout(hoverTimer.current);
  };

  const closeMegaNow = () => {
    if (hoverTimer.current) clearTimeout(hoverTimer.current);
    setMegaOpen(false);
    setMegaLabel(null);
  };

  if (isHome) {
    return (
      <header
        className={`fixed inset-x-0 z-50 pointer-events-none transition-all duration-300 ${
          scrolled ? "top-3" : "top-6"
        }`}
      >
        <div className="mx-auto max-w-[1200px] px-4 pointer-events-auto">
          <div
            className={`overflow-hidden rounded-2xl bg-white transition-all duration-300 ${
              scrolled
                ? "shadow-[0_4px_20px_rgba(0,0,0,0.08)]"
                : "shadow-[0_8px_30px_rgba(0,0,0,0.10)]"
            }`}
          >
            <div className="flex items-center justify-between gap-3 px-5 py-3">
              <Link href="/" className="flex items-center gap-2.5 shrink-0">
                <Image
                  src="/vrc-logo.png"
                  alt="VR Coatings logo"
                  width={140}
                  height={36}
                  priority
                  className="h-9 w-auto"
                />
              </Link>

              <div className="hidden md:block h-7 w-px bg-black/[0.08]" />

              <nav className="hidden lg:flex items-center gap-0.5">
                {desktopNavItems.map((item) => {
                  const active = isRouteActive(item) || isSectionActive(item.label);
                  const isMega = MEGA_MENU_LABELS.has(item.label);
                  const isOpen = megaOpen && megaLabel === item.label;
                  return (
                      <div
                        key={item.label}
                        className="relative"
                        onMouseEnter={() => (isMega ? openMega(item.label) : item.children ? setOpenMenu(item.label) : undefined)}
                        onMouseLeave={() => {
                          if (isMega) closeMega();
                          else if (item.children) setOpenMenu(null);
                        }}
                      >
                      <NavLink
                        label={item.label}
                        href={item.href}
                        active={active}
                        hasChildren={Boolean(item.children)}
                        compact
                        mega={isMega}
                        open={isOpen}
                      />
                    </div>
                  );
                })}
              </nav>

              <div className="hidden lg:block h-7 w-px bg-black/[0.08]" />

              <div className="flex items-center gap-2">
                <SearchControl />
                <Link
                  href="/contact"
                  className="hidden sm:inline-flex items-center gap-1.5 rounded-lg bg-[#082B4C] px-4 py-2 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
                >
                  Contact Us
                </Link>
                <button
                  type="button"
                  className="lg:hidden flex h-9 w-9 items-center justify-center rounded-md text-brand-900"
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
          </div>

          {megaOpen && megaLabel && (
            <div
              ref={megaRef}
              className="mt-2 mx-auto origin-top transition-all duration-200 ease-out"
              style={{ maxWidth: MEGA_MENU_CONFIG[megaLabel]?.width ?? "auto" }}
              onMouseEnter={keepMegaOpen}
              onMouseLeave={closeMega}
            >
              <MegaMenuPanel label={megaLabel} onClose={closeMegaNow} />
            </div>
          )}

          {mobileOpen && (
            <div className="mt-2 overflow-hidden rounded-2xl bg-white shadow-[0_8px_30px_rgba(0,0,0,0.10)] lg:hidden">
              <div className="space-y-1 p-4">
                {navItems.map((item) => {
                  const active = isRouteActive(item) || isSectionActive(item.label);
                  return (
                    <div key={item.label} className="border-b border-slate-200 py-2 last:border-b-0">
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
            </div>
          )}
        </div>
      </header>
    );
  }

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
