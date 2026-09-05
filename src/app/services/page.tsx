import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { IndustryGrid } from "@/components/IndustryGrid";

export const metadata: Metadata = { title: "Services" };

export default function ServicesPage() {
  return (
    <>
      <PageHero
        kicker="Services"
        title="Industries we serve"
        text="Coating programmes, application support, and supply coverage for the industrial sectors we work with."
      />
      <IndustryGrid />
    </>
  );
}
