import {
  offices,
  defaultOfficeId,
  type Office,
  type OfficeContact,
} from "@/lib/contactData";

function Building2Icon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 22V10l6-4 6 4v12" />
      <path d="M4 22h16" />
      <path d="M10 18v4M14 18v4" />
      <path d="M10 14h4" />
    </svg>
  );
}

function FactoryIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 22V12l6 4V10l6 4V6h6v16" />
      <path d="M10 22v-4M14 22v-4M18 22v-4" />
      <path d="M8 16h8" />
    </svg>
  );
}

function Globe2Icon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18" />
      <path d="M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" />
    </svg>
  );
}

function MapPinIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
      <circle cx="12" cy="10" r="2.5" />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12h14M11 6l6 6-6 6" />
    </svg>
  );
}

function officeIcon(icon: Office["icon"]) {
  if (icon === "factory") return FactoryIcon;
  if (icon === "globe2") return Globe2Icon;
  return Building2Icon;
}

export function OfficeCard({
  office,
  selected,
  onSelect,
}: {
  office: Office;
  selected: boolean;
  onSelect: (id: string) => void;
}) {
  const Icon = officeIcon(office.icon);

  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={() => onSelect(office.id)}
      className={
        "group flex w-full flex-col rounded-xl border bg-white text-left transition-all duration-200 " +
        (selected
          ? "border-[#1678C8] bg-[#F4F7FA] shadow-[0_10px_30px_rgba(22,120,200,0.18)]"
          : "border-slate-200 shadow-[0_4px_20px_rgba(8,43,76,0.06)] hover:-translate-y-0.5 hover:border-[#1678C8]/40 hover:shadow-[0_10px_30px_rgba(8,43,76,0.10)]")
      }
    >
      <div
        className={
          "flex items-center gap-2 rounded-t-xl px-4 py-2.5 text-[11px] font-bold uppercase tracking-[0.18em] " +
          (selected ? "bg-[#1678C8] text-white" : "bg-[#EEF5FB] text-[#0B5C97]")
        }
      >
        <Icon className="h-4 w-4" />
        {office.label}
      </div>

      <div className="flex flex-1 flex-col gap-3 p-4">
        <div>
          <p className="text-[15px] font-bold leading-5 text-[#082B4C]">{office.name}</p>
          <div className="mt-1 space-y-0.5">
            {office.addressLines.map((line) => (
              <p key={line} className="text-[12.5px] leading-5 text-slate-500">
                {line}
              </p>
            ))}
          </div>
        </div>

        {office.contacts.length > 0 && (
          <div className="space-y-1.5 border-t border-slate-100 pt-2.5">
            {office.contacts.map((contact: OfficeContact, index: number) =>
              contact.href ? (
                <a
                  key={`${contact.value}-${index}`}
                  href={contact.href}
                  onClick={(event) => event.stopPropagation()}
                  className="flex items-center gap-2 text-[12.5px] leading-5"
                >
                  <MapPinIcon className="h-3.5 w-3.5 shrink-0 text-[#1678C8]" />
                  <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-400">
                    {contact.label ?? ""}
                  </span>
                  <span className="font-medium text-[#082B4C] transition-colors hover:text-[#1678C8]">
                    {contact.value}
                  </span>
                </a>
              ) : (
                <div
                  key={`${contact.value}-${index}`}
                  className="flex items-center gap-2 text-[12.5px] leading-5"
                >
                  <MapPinIcon className="h-3.5 w-3.5 shrink-0 text-[#1678C8]" />
                  <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-400">
                    {contact.label ?? ""}
                  </span>
                  <span className="font-medium text-[#082B4C]">{contact.value}</span>
                </div>
              )
            )}
          </div>
        )}

        <span className="mt-auto inline-flex items-center gap-1.5 text-[12px] font-semibold text-[#1678C8] transition-colors group-hover:text-[#0B5C97]">
          <MapPinIcon className="h-3.5 w-3.5" />
          Click to view on map
          <ArrowRightIcon className="h-3 w-3 transition-transform duration-200 group-hover:translate-x-0.5" />
        </span>
      </div>
    </button>
  );
}

export function OfficeGrid({
  selectedId,
  onSelect,
}: {
  selectedId: string;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {offices.map((office) => (
        <OfficeCard
          key={office.id}
          office={office}
          selected={office.id === selectedId}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}

export { defaultOfficeId, offices };