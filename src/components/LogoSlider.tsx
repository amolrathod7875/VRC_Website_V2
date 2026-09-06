import { getTrustedClients } from "@/lib/clients";

export function LogoSlider() {
  const trusted = getTrustedClients();
  const logos = [...trusted, ...trusted];
  return (
    <section className="border-y border-slate-200 bg-surface py-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="mb-6 text-center text-xs font-semibold uppercase tracking-[0.24em] text-brand-800">
          Trusted by industrial partners
        </p>
        <div className="overflow-hidden">
          <div className="logo-marquee flex w-max gap-6">
            {logos.map((client, i) => (
              <div
                key={`${client.name}-${i}`}
                className="flex h-16 w-40 shrink-0 items-center justify-center rounded-md bg-white"
              >
                {client.logo ? (
                  <img
                    src={client.logo}
                    alt={client.name}
                    className="h-full w-full object-contain"
                  />
                ) : (
                  <span className="px-2 text-center text-xs font-medium uppercase tracking-wide text-slate-500">
                    {client.name}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
