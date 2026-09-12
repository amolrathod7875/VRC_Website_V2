import { type Office } from "@/lib/contactData";

function MapPinIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
      <circle cx="12" cy="10" r="2.5" />
    </svg>
  );
}

export function OfficeMap({ office }: { office: Office }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_10px_40px_rgba(8,43,76,0.08)]">
      <iframe
        title={`Map location for ${office.name} — ${office.city}`}
        src={office.mapEmbedUrl}
        className="h-[340px] w-full border-0 sm:h-[420px]"
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      />
      <div className="pointer-events-none absolute left-4 top-4 z-10">
        <span className="inline-flex items-center gap-2 rounded-full bg-[#082B4C]/90 px-3.5 py-1.5 text-xs font-semibold text-white shadow-lg">
          <MapPinIcon className="h-3.5 w-3.5 text-[#1678C8]" />
          {office.label} — {office.city}
        </span>
      </div>
    </div>
  );
}