import { IconArrowRight } from "./Icon";

type CultureItem = {
  title: string;
  description: string;
  icon: React.ReactNode;
};

type CultureStripProps = {
  items: CultureItem[];
};

function LucideIcon({
  children,
  className = "h-6 w-6",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-[#EEF4FB] text-[#1678C8]">
      <svg
        viewBox="0 0 24 24"
        className={className}
        fill="none"
        stroke="currentColor"
        strokeWidth={1.9}
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden
      >
        {children}
      </svg>
    </span>
  );
}

const ICONS: Record<string, React.ReactNode> = {
  wrench: (
    <>
      <path d="M14.3 6.3a2.1 2.1 0 0 1 3 3L8.6 18a2.1 2.1 0 0 1-3-3l.9-1L5 17l1.9-.9-.4-.4.4.4L9 15.4l7.3-7.3Z" />
      <path d="M12 14 5 21" />
    </>
  ),
  hand: (
    <>
      <path d="M11 4v12" />
      <path d="M7 8H4a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h1v5a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-5h1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-3V5a1 1 0 0 0-1-1h-3a1 1 0 0 0-1 1Z" />
      <path d="M11 8h4" />
    </>
  ),
  factory: (
    <>
      <path d="M2 21V8l6-4 6 4v6l6-4v13H2Z" />
      <path d="M13 21v-6M9 21v-4M5 21v-3" />
    </>
  ),
  book: (
    <>
      <path d="M4 19V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14" />
      <path d="M4 19a2 2 0 0 1 2-2h14" />
      <path d="M12 12v7" />
    </>
  ),
};

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
              <LucideIcon className="h-6 w-6">
                {ICONS[item.icon] ?? ICONS.book}
              </LucideIcon>
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