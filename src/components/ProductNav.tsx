"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { productCategories, type ProductCategory } from "@/lib/data";

function ChevronRightIcon({ className = "h-4 w-4" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 20 20"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 10l5 5 5-5" />
    </svg>
  );
}

function AnimatedCollapse({
  isOpen,
  children,
}: {
  isOpen: boolean;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState<number>(0);

  useEffect(() => {
    if (!ref.current) return;
    const targetHeight = isOpen ? ref.current.scrollHeight : 0;
    setHeight(targetHeight);
  }, [isOpen]);

  return (
    <div
      ref={ref}
      className="overflow-hidden transition-all duration-200 ease-out"
      style={{ maxHeight: height, opacity: isOpen ? 1 : 0 }}
    >
      {children}
    </div>
  );
}

function CategoryDisplayName({ node }: { node: ProductCategory }) {
  if (!node.lineBreakAfter) return <>{node.name}</>;
  const parts = node.name.split(node.lineBreakAfter);
  if (parts.length !== 2 || !parts[1].trimStart().length) return <>{node.name}</>;
  return (
    <>
      {parts[0]}
      <br />
      {parts[1].trim()}
    </>
  );
}

function CategoryNodes({
  nodes,
  depth = 0,
  expanded,
  toggleNode,
  pathname,
}: {
  nodes: ProductCategory[];
  depth?: number;
  expanded: Set<string>;
  toggleNode: (slug: string) => void;
  pathname: string;
}) {
  const paddingLeft = depth === 0 ? 0 : depth * 12;
  const borderClass = depth === 0 ? "" : "border-l border-slate-200";

  return (
    <ul className={`mt-1 space-y-0.5 ${borderClass}`} style={{ paddingLeft }}>
      {nodes.map((node) => {
        const href = `/products/${node.slug}`;
        const isActive = pathname === href;
        const isParent = Boolean(node.children && node.children.length > 0);
        const isExpanded = expanded.has(node.slug);

        return (
          <li key={node.slug}>
            <div
              className={`flex items-center gap-1 rounded py-1.5 text-sm transition-colors duration-150 ${
                isActive
                  ? "bg-brand-50 text-brand-700"
                  : "hover:bg-slate-50"
              }`}
            >
              {isParent ? (
                <button
                  type="button"
                  onClick={() => toggleNode(node.slug)}
                  aria-expanded={isExpanded}
                  aria-controls={`category-${node.slug}`}
                  className="flex flex-1 items-center gap-1 font-semibold text-brand-800 outline-none hover:text-brand-900"
                >
                  <span
                    className="transition-transform duration-200 ease-out"
                    style={{ transform: isExpanded ? "rotate(90deg)" : "rotate(0)" }}
                  >
                    <ChevronRightIcon className="h-3.5 w-3.5 shrink-0 text-slate-500" />
                  </span>
                  <span className="leading-tight">
                    <CategoryDisplayName node={node} />
                  </span>
                </button>
              ) : depth === 0 ? (
                <Link
                  href={href}
                  className="ml-[22px] block flex-1 font-semibold text-brand-800 py-1 text-slate-700 hover:text-brand-700"
                >
                  <CategoryDisplayName node={node} />
                </Link>
              ) : (
                <Link
                  href={href}
                  className="ml-[22px] block flex-1 py-1 text-slate-700 hover:text-brand-700"
                >
                  <CategoryDisplayName node={node} />
                </Link>
              )}
            </div>
            {isParent && node.children && (
              <AnimatedCollapse isOpen={isExpanded}>
                <CategoryNodes
                  nodes={node.children}
                  depth={depth + 1}
                  expanded={expanded}
                  toggleNode={toggleNode}
                  pathname={pathname}
                />
              </AnimatedCollapse>
            )}
          </li>
        );
      })}
    </ul>
  );
}

function findPathToSlug(
  slug: string,
  nodes: ProductCategory[],
  trail: string[] = []
): string[] | null {
  for (const node of nodes) {
    if (node.slug === slug) {
      return [...trail, node.slug];
    }
    if (node.children) {
      const result = findPathToSlug(slug, node.children, [...trail, node.slug]);
      if (result) return result;
    }
  }
  return null;
}

function getExpandedFromPathname(pathname: string): Set<string> {
  const slug = pathname.split("/").pop();
  if (!slug || slug === "products") return new Set();
  const path = findPathToSlug(slug, productCategories);
  if (!path) return new Set();
  return new Set(path.slice(0, -1));
}

export function ProductNav() {
  const pathname = usePathname();
  const [userExpanded, setUserExpanded] = useState<Set<string>>(new Set());

  const toggleNode = (slug: string) => {
    setUserExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) {
        next.delete(slug);
      } else {
        next.add(slug);
      }
      return next;
    });
  };

  const expanded = new Set(userExpanded);
  const pathExpanded = getExpandedFromPathname(pathname);
  pathExpanded.forEach((slug) => expanded.add(slug));

  return (
    <aside
      className="product-sidebar overflow-y-auto"
      style={{ maxHeight: "70vh" }}
    >
      <h2 className="mb-4 text-xs font-semibold uppercase tracking-[0.18em] text-brand-800">
        Categories
      </h2>
      <nav aria-label="Product Categories">
        <CategoryNodes
          nodes={productCategories}
          expanded={expanded}
          toggleNode={toggleNode}
          pathname={pathname}
        />
      </nav>
    </aside>
  );
}
