import { getFeaturedClients } from "@/lib/clients";

export function LogoSlider() {
  const featured = getFeaturedClients();
  const logos = [...featured, ...featured];
  return (
    <section className="border-y border-slate-200 bg-surface py-10">
      <div className="home-section-container">
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
                    className="max-h-10 max-w-[120px] object-contain"
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
