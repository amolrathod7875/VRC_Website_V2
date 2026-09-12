import type { Metadata } from "next";
import { PartnersPage } from "@/components/PartnersPage";

export const metadata: Metadata = {
  title: "Partners | Global Technology Partners — VR Coatings",
  description:
    "VR Coatings collaborates with leading manufacturers from Japan and Germany to bring advanced coating, dosing and fluid-handling technologies to India.",
};

export default function Page() {
  return <PartnersPage />;
}
