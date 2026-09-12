import type { Metadata } from "next";
import { FaqPage } from "@/components/FaqPage";
import { faqSchema } from "@/lib/faqs";

export const metadata: Metadata = {
  title: "FAQs",
  description:
    "Find answers about VR Coatings products, applications, technical support, sales, exports and service.",
};

export default function FaqsPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      <FaqPage />
    </>
  );
}