import {
  YOUTUBE_URL,
  WEBSITE_URL,
  SALES_EMAIL,
  HEAD_OFFICE_PHONE,
} from "@/lib/contactData";

function PhoneIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.94 19.94 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.94 19.94 0 0 1 2.12 4.18 2 2 0 0 1 4.12 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z" />
    </svg>
  );
}

function MailIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="M3 7l9 7 9-7" />
    </svg>
  );
}

function YoutubeIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="6" width="16" height="12" rx="4" />
      <path d="M10 9l4 3-4 3z" fill="currentColor" stroke="none" />
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

function ExternalLinkIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M7 17h10M11 7l10 10M21 11V21H3V3h10" />
    </svg>
  );
}

function ActionCard({
  icon: Icon,
  title,
  value,
  href,
  ariaLabel,
}: {
  icon: (props: { className?: string }) => React.ReactElement;
  title: string;
  value: string;
  href: string;
  ariaLabel: string;
}) {
  return (
    <a
      href={href}
      aria-label={ariaLabel}
      className="group flex items-center gap-3 rounded-xl border border-slate-200 bg-[#F4F7FA] p-4 transition-all duration-200 hover:-translate-y-0.5 hover:border-[#1678C8]/40 hover:bg-white hover:shadow-[0_8px_24px_rgba(22,120,200,0.15)]"
    >
      <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-white text-[#1678C8] shadow-sm">
        <Icon className="h-5 w-5" />
      </span>
      <span className="flex flex-col">
        <span className="text-[11px] font-bold uppercase tracking-[0.16em] text-slate-400">
          {title}
        </span>
        <span className="text-[14px] font-semibold text-[#082B4C] transition-colors group-hover:text-[#1678C8]">
          {value}
        </span>
      </span>
    </a>
  );
}

export function QuickContactActions() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <ActionCard
        icon={PhoneIcon}
        title="Call Us"
        value={HEAD_OFFICE_PHONE}
        href={`tel:${HEAD_OFFICE_PHONE.replace(/[^0-9+]/g, "")}`}
        ariaLabel={`Call VR Coatings at ${HEAD_OFFICE_PHONE}`}
      />
      <ActionCard
        icon={MailIcon}
        title="Email Us"
        value={SALES_EMAIL}
        href={`mailto:${SALES_EMAIL}`}
        ariaLabel={`Email VR Coatings at ${SALES_EMAIL}`}
      />
      <ActionCard
        icon={YoutubeIcon}
        title="YouTube"
        value="VR Coatings"
        href={YOUTUBE_URL}
        ariaLabel="Open VR Coatings YouTube channel"
      />
      <ActionCard
        icon={Globe2Icon}
        title="Website"
        value="www.vrcoatings.com"
        href={WEBSITE_URL}
        ariaLabel="Open VR Coatings website"
      />
    </div>
  );
}

export function OpenInGoogleMapsButton({ office }: { office: { label: string; city: string; googleMapsUrl: string } }) {
  return (
    <a
      href={office.googleMapsUrl}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`Open ${office.label} — ${office.city} in Google Maps`}
      className="group inline-flex w-full items-center justify-center gap-2.5 rounded-lg bg-[#082B4C] px-5 py-3 text-sm font-semibold text-white transition-colors duration-200 hover:bg-[#0B5C97]"
    >
      <MapPinIcon className="h-4 w-4 text-[#1678C8]" />
      Open in Google Maps
      <ExternalLinkIcon className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
    </a>
  );
}