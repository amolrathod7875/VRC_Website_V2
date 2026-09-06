import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { FaqAccordion } from "@/components/FaqAccordion";

export const metadata: Metadata = { title: "FAQs" };

export default function FaqsPage() {
  return (
    <>
      <PageHero
        kicker="Resources"
        title="FAQs"
        text="Common questions about products, customization, and commercial engagement."
      />
      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <FaqAccordion />
      </section>
    </>
  );
}
