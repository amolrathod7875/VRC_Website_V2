"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { productTree, type ProductNode } from "@/lib/data";

function Nodes({ nodes, depth = 0 }: { nodes: ProductNode[]; depth?: number }) {
  const pathname = usePathname();
  return (
    <ul className={depth === 0 ? "space-y-1" : "mt-1 space-y-1 border-l border-slate-200 pl-3"}>
      {nodes.map((node) => {
        const href = `/products/${node.slug}`;
        const active = pathname === href;
        return (
          <li key={node.slug}>
            <Link
              href={href}
              className={`block rounded-md px-2 py-1.5 text-sm ${
                active ? "bg-brand-50 font-semibold text-brand-800" : "text-slate-700 hover:bg-slate-50"
              }`}
            >
              {node.name}
            </Link>
            {node.children && <Nodes nodes={node.children} depth={depth + 1} />}
          </li>
        );
      })}
    </ul>
  );
}

export function ProductNav() {
  return (
    <aside className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-brand-800">Categories</h2>
      <Nodes nodes={productTree} />
    </aside>
  );
}
