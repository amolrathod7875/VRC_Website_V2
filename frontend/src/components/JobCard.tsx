import { IconArrowRight } from "./Icon";
import { JobDetails } from "./JobDetails";
import type { CareerRole } from "@/lib/careerData";

function Badge({ type }: { type: CareerRole["type"] }) {
  const styles: Record<CareerRole["type"], string> = {
    "Full-time": "bg-[#DCEAF7] text-[#0B5C97]",
    Internship: "bg-[#E2F3E7] text-[#1F7A45]",
    "Part-time": "bg-[#F1ECE4] text-[#7A6B4F]",
    Contract: "bg-[#F1ECE4] text-[#7A6B4F]",
  };
  return (
    <span
      className={`inline-flex items-center rounded-md px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.08em] ${styles[type]}`}
    >
      {type}
    </span>
  );
}

function MetaRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0">
      <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-400">
        {label}
      </p>
      <p className="mt-0.5 text-sm font-semibold text-[#082B4C]">{value}</p>
    </div>
  );
}

function IconCircle({ children }: { children: React.ReactNode }) {
  return (
    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-[#EEF4FB] text-[#1678C8]">
      <svg
        viewBox="0 0 24 24"
        className="h-4 w-4"
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

function LocationLabel({ role }: { role: CareerRole }) {
  if (role.locations && role.locations.length > 1) {
    return (
      <span className="inline-flex items-center gap-1.5">
        <IconCircle>
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z" />
          <circle cx="12" cy="10" r="3" />
        </IconCircle>
        <span>Multiple Locations</span>
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5">
      <IconCircle>
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z" />
        <circle cx="12" cy="10" r="3" />
      </IconCircle>
      <span>{role.location}</span>
    </span>
  );
}

export function JobCard({
  role,
  expanded = false,
  onToggle,
  onApply,
}: {
  role: CareerRole;
  expanded?: boolean;
  onToggle?: (id: string) => void;
  onApply?: (role: CareerRole) => void;
}) {
  const handleToggle = () => {
    if (onToggle) onToggle(role.id);
  };

  const handleApply = () => {
    if (onApply) onApply(role);
  };

  const showSalary = Boolean(role.salary && role.salary.trim().length > 0);

  return (
    <article
      id={`job-${role.id}`}
      className="scroll-mt-28 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-[0_1px_2px_rgba(8,43,76,0.04)] transition-all duration-250 hover:-translate-y-[4px] hover:border-[#1678C8]/40 hover:shadow-[0_12px_30px_rgba(8,43,76,0.12)]"
    >
      <div className="p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge type={role.type} />
            {role.posted ? (
              <>
                <span className="text-xs text-slate-400">|</span>
                <span className="inline-flex items-center gap-1.5 text-xs text-slate-500">
                  <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={1.9} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                    <rect x="3" y="4" width="18" height="18" rx="2" />
                    <path d="M3 10h18M8 2v4M16 2v4" />
                  </svg>
                  {role.posted}
                </span>
              </>
            ) : null}
          </div>
        </div>

        <h3 className="mt-4 text-xl font-semibold leading-tight text-[#082B4C] sm:text-[22px]">
          {role.title}
        </h3>

        <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-slate-600">
          <span className="inline-flex items-center gap-1.5">
            <IconCircle>
              <path d="M3 21h18M5 21V8l7-5 7 5v13" />
            </IconCircle>
            <span>{role.department}</span>
          </span>
          <LocationLabel role={role} />
        </div>

        <div className="mt-5 grid grid-cols-1 gap-3 border-t border-slate-100 pt-4 sm:grid-cols-3">
          <MetaRow label="Experience" value={role.experience} />
          {showSalary ? <MetaRow label="Salary" value={role.salary as string} /> : null}
          <MetaRow label="Qualification" value={role.qualification} />
        </div>

<p className="mt-4 text-sm leading-6 text-slate-600 line-clamp-2">
          {role.summary}
        </p>

<div className="mt-3 flex flex-wrap gap-1.5">
          {role.skills.slice(0, 6).map((skill) => (
            <span
              key={skill}
              className="rounded-md border border-slate-200 bg-[#F7F9FC] px-2.5 py-1 text-[11px] font-medium text-slate-600"
            >
              {skill}
            </span>
          ))}
        </div>

        <JobDetails role={role} expanded={expanded} />

        <div className="mt-5 flex items-center gap-3 border-t border-slate-100 pt-4">
          <button
            type="button"
            onClick={handleApply}
            className="inline-flex items-center gap-1.5 rounded-md bg-[#082B4C] px-4 py-2 text-xs font-semibold text-white transition-colors duration-200 hover:bg-[#1678C8]"
          >
            Apply Now
            <IconArrowRight className="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            onClick={handleToggle}
            className="inline-flex items-center gap-1.5 rounded-md border border-[#082B4C] bg-white px-4 py-2 text-xs font-semibold text-[#082B4C] transition-colors duration-200 hover:bg-[#F4F7FA]"
          >
            {expanded ? "Hide details" : "View Details"}
            <svg viewBox="0 0 20 20" className="h-3.5 w-3.5 transition-transform duration-200" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" style={{ transform: expanded ? "rotate(180deg)" : "rotate(0deg)" }}>
              <path d="M5 8l5 5 5-5" />
            </svg>
          </button>
        </div>
      </div>
    </article>
  );
}
