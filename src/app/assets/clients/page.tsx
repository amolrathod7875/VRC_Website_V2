import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { ClientsTabs } from "@/components/ClientsTabs";

export const metadata: Metadata = { title: "Clients" };

export default function ClientsPage() {
  return (
    <>
      <PageHero
        kicker="Our Assets"
        title="Our clients"
        text="Representative customers grouped by industry. Replace logos when brand assets are ready."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <ClientsTabs />
      </section>
    </>
  );
}
