import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { ClientsTabs } from "@/components/ClientsTabs";
import { clients } from "@/lib/clients";

export const metadata: Metadata = { title: "Clients" };

export default function ClientsPage() {
  return (
    <>
      <PageHero
        kicker="Our Assets"
        title="Our clients"
        text={`Complete client portfolio of ${clients.length} companies organized by industry.`}
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <ClientsTabs />
      </section>
    </>
  );
}
