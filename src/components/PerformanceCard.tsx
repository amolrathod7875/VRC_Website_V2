import type { ReactNode } from "react";

type AttributeProps = {
  icon: ReactNode;
  title: string;
  text: string;
};

export function PerformanceCard({ icon, title, text }: AttributeProps) {
  return (
    <div className="flex flex-col rounded-lg border border-slate-200 bg-white p-6">
      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-md bg-brand-50 text-brand-800">
        {icon}
      </div>
      <h3 className="text-base font-semibold text-brand-950">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-600">{text}</p>
    </div>
  );
}
