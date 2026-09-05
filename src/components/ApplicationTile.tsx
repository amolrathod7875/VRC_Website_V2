import Link from "next/link";
import type { ReactNode } from "react";
import { IconArrowRight } from "./Icon";

type ApplicationTileProps = {
  icon: ReactNode;
  name: string;
  text: string;
  href?: string;
};

export function ApplicationTile({ icon, name, text, href = "/applications" }: ApplicationTileProps) {
  return (
    <Link
      href={href}
      className="group flex h-full flex-col rounded-lg border border-slate-200 bg-white p-6 transition hover:border-brand-200 hover:bg-brand-50"
    >
      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-md bg-brand-50 text-brand-800 transition group-hover:bg-white">
        {icon}
      </div>
      <h3 className="text-base font-semibold text-brand-950">{name}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-600">{text}</p>
      <span className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-700">
        Explore
        <IconArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
      </span>
    </Link>
  );
}
