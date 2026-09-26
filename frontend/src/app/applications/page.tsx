import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { ApplicationsShowcase } from "@/components/ApplicationsShowcase";

export const metadata: Metadata = { title: "Applications" };

export default function ApplicationsPage() {
  return (
    <>
      <PageHero
        kicker="Markets"
        title="Applications"
        text="Industry uses for VR coating systems—from OEM lines to infrastructure maintenance."
      />
      <ApplicationsShowcase />
    </>
  );
}