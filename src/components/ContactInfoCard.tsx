import Link from "next/link";

type OfficeLike = {
  title: string;
  lines?: string[];
  phone?: string;
  phoneHref?: string;
};

const iconMap: Record<string, (props: { className?: string }) => React.ReactElement> = {
  "Head Office": ({ className }) => (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M8 42V20l10-6 10 6v22z" strokeLinejoin="round" />
      <path d="M4 42h16" strokeLinecap="round" />
      <path d="M10 28v6M14 28v6" strokeLinecap="round" />
      <path d="M8 14h8" strokeLinecap="round" />
    </svg>
  ),
  Factory: ({ className }) => (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M6 40V20l10 6V20l10 6v20z" strokeLinejoin="round" />
      <path d="M4 40h16M12 40v-6M18 40v-6" strokeLinecap="round" />
      <path d="M8 14h8M8 18h8" strokeLinecap="round" />
    </svg>
  ),
  "North America": ({ className }) => (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18M12 3c-3 3-3 18 0 21M12 3c3 3 3 18 0 21" strokeLinecap="round" />
    </svg>
  ),
};

function MailIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="M3 7l9 7 9-7" strokeLinejoin="round" />
    </svg>
  );
}

function PhoneIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.6">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.94 19.94 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.94 19.94 0 0 1 2.12 4.18 2 2 0 0 1 4.12 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" strokeLinejoin="round" />
    </svg>
  );
}

export function ContactInfoCard({
  title,
  lines,
  phone,
  phoneHref,
  email,
  type = "address",
}: {
  title: string;
  lines?: string[];
  phone?: string;
  phoneHref?: string;
  email?: string;
  type?: "address" | "email" | "phone";
}) {
  const IconComp = iconMap[title];
  const isLink = type === "phone" || type === "email";
  const href = type === "phone" ? phoneHref : type === "email" ? `mailto:${email}` : undefined;

  const content = (
    <div className="flex gap-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#EEF5FB] text-[#1678C8]">
        {type === "email" ? (
          <MailIcon className="h-5 w-5" />
        ) : type === "phone" ? (
          <PhoneIcon className="h-5 w-5" />
        ) : IconComp ? (
          <IconComp className="h-5 w-5" />
        ) : null}
      </div>
      <div className="flex-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#1678C8]">{title}</p>
        {lines && lines.length > 0 && (
          <div className="mt-1.5 space-y-0.5">
            {lines.map((line) => (
              <p key={line} className="text-sm leading-6 text-[#082B4C]">
                {line}
              </p>
            ))}
          </div>
        )}
        {phone && (
          <a
            href={phoneHref}
            className="mt-1.5 inline-block text-sm font-semibold text-[#0B5C97] transition-colors hover:text-[#082B4C]"
          >
            {phone}
          </a>
        )}
        {email && (
          <a
            href={`mailto:${email}`}
            className="mt-1.5 inline-block text-sm font-semibold text-[#0B5C97] transition-colors hover:text-[#082B4C]"
          >
            {email}
          </a>
        )}
      </div>
    </div>
  );

  if (isLink && href) {
    return (
      <a
        href={href}
        className="block rounded-xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgba(8,43,76,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:border-[#1678C8]/30 hover:shadow-[0_8px_30px_rgba(8,43,76,0.10)]"
      >
        {content}
      </a>
    );
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgba(8,43,76,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:border-[#1678C8]/30 hover:shadow-[0_8px_30px_rgba(8,43,76,0.10)]">
      {content}
    </div>
  );
}
