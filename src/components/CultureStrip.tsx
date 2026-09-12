import { ReactElement } from "react";

type CultureItem = {
  title: string;
  description: string;
  icon: ReactElement;
};

type CultureStripProps = {
  items: CultureItem[];
};

function LucideIcon({ icon }: { icon: ReactElement }) {
  return (
    <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-[#EEF4FB] text-[#1678C8]">
      <svg
        viewBox="0 0 24 24"
        className="h-6 w-6"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.9}
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden
      >
        {icon}
      </svg>
    </span>
  );
}

export function CultureStrip({ items }: CultureStripProps) {
  return (
    <section className="border-y border-slate-200 bg-white">
      <div className="mx-auto max-w-[1320px] px-4 sm:px-6 lg:px-8">
        <div className="grid divide-y divide-slate-200 sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-4">
          {items.map((item) => (
            <div
              key={item.title}
              className="flex items-start gap-4 px-5 py-7 sm:px-6 lg:border-r lg:border-slate-200 lg:px-7 lg:py-8 last:lg:border-r-0"
            >
              <LucideIcon icon={item.icon} />
              <div>
                <p className="text-sm font-semibold text-[#082B4C]">{item.title}</p>
                <p className="mt-1 text-xs leading-5 text-slate-500">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}