import type { Metadata } from "next";
import { CareerPage } from "@/components/CareerPage";

export const metadata: Metadata = {
  title: "Career",
  description:
    "Explore current openings at VR Coatings across engineering, manufacturing, application support, sales and technology.",
};

export default function CareerRoutePage() {
  return <CareerPage />;
}