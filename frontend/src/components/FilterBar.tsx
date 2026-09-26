type FilterBarProps = {
  departments: string[];
  active: string;
  onChange: (dept: string) => void;
  total: number;
  filtered: number;
};

export function FilterBar({ departments, active, onChange, total, filtered }: FilterBarProps) {
  const label = active === "All" ? "All Departments" : active;
  const countLabel = active === "All" ? `${total} openings` : `${filtered} openings`;

  return (
    <section className="bg-white">
      <div className="mx-auto max-w-[1320px] px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex flex-1 items-center gap-2 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            <button
              type="button"
              onClick={() => onChange("All")}
              className={`whitespace-nowrap rounded-md border px-3.5 py-2 text-sm font-medium transition-colors duration-200 ${
                active === "All"
                  ? "border-transparent bg-[#1678C8] text-white"
                  : "border-slate-200 bg-white text-slate-700 hover:border-[#1678C8]/40 hover:bg-[#F4F7FA]"
              }`}
            >
              All Departments
            </button>
            {departments.map((dept) => (
              <button
                key={dept}
                type="button"
                onClick={() => onChange(dept)}
                className={`whitespace-nowrap rounded-md border px-3.5 py-2 text-sm font-medium transition-colors duration-200 ${
                  active === dept
                    ? "border-transparent bg-[#1678C8] text-white"
                    : "border-slate-200 bg-white text-slate-700 hover:border-[#1678C8]/40 hover:bg-[#F4F7FA]"
                }`}
              >
                {dept}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <span className="font-semibold text-[#082B4C]">{countLabel}</span>
            <span>in</span>
            <span className="font-medium text-slate-600">{label}</span>
          </div>
        </div>
      </div>
    </section>
  );
}