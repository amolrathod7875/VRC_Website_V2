type CareerRole = {
  id: string;
  title: string;
  responsibilities?: string[];
  fullDescription?: string;
};

function DetailBlock({ title, items }: { title: string; items?: string[] }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="border-t border-slate-100 pt-5 first:border-t-0 first:pt-0">
      <h4 className="text-xs font-semibold uppercase tracking-[0.14em] text-[#1678C8]">
        {title}
      </h4>
      <ul className="mt-2 space-y-1.5">
        {items.map((item, idx) => (
          <li key={idx} className="flex gap-2.5 text-sm leading-6 text-slate-600">
            <span aria-hidden className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1678C8]/60" />
            <span className="pt-px">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function JobDetails({ role }: { role: CareerRole }) {
  const hasResponsibilities = role.responsibilities && role.responsibilities.length > 0;
  const hasFullDescription = Boolean(role.fullDescription);

  if (!hasResponsibilities && !hasFullDescription) return null;

  return (
    <div className="mt-5 scroll-mt-32 space-y-5 border-t border-slate-100 pt-5">
      {hasResponsibilities && (
        <DetailBlock title="Key Responsibilities" items={role.responsibilities} />
      )}
      {hasFullDescription && (
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-[0.14em] text-[#1678C8]">
            Full Description
          </h4>
          <p className="mt-2 text-sm leading-6 text-slate-600">{role.fullDescription}</p>
        </div>
      )}
    </div>
  );
}