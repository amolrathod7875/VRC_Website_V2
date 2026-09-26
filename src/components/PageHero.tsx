export function PageHero({
  kicker,
  title,
  text,
}: {
  kicker?: string;
  title: string;
  text?: string;
}) {
  return (
    <section className="bg-brand-900 text-white">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {kicker && (
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-brand-100">{kicker}</p>
        )}
        <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{title}</h1>
        {text && <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-200">{text}</p>}
      </div>
    </section>
  );
}
