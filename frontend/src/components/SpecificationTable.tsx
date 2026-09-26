type Spec = {
  label: string;
  value: string;
};

type SpecificationTableProps = {
  specifications: Spec[];
};

export function SpecificationTable({ specifications }: SpecificationTableProps) {
  if (!specifications || specifications.length === 0) return null;

  return (
    <div className="mt-6 w-full overflow-x-auto">
      <table className="w-full border-collapse text-left text-sm">
        <tbody>
          {specifications.map((spec, i) => (
            <tr key={spec.label} className="border-b border-slate-200 last:border-b-0">
              <td
                className="whitespace-nowrap px-4 py-2.5 font-semibold uppercase tracking-wide text-[#082B4C]"
                style={{ backgroundColor: "#BFE3F4" }}
              >
                {spec.label}
              </td>
              <td
                className="px-4 py-2.5 text-slate-700"
                style={{ backgroundColor: "#F1F3F5" }}
              >
                {spec.value}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
