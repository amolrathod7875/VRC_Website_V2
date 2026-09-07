import type { Metadata } from "next";
import Link from "next/link";
import { applications, getApplicationIcon } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { ApplicationTile } from "@/components/ApplicationTile";
import { IconArrowRight } from "@/components/Icon";

export const metadata: Metadata = { title: "Applications" };

export default function ApplicationsPage() {
  return (
    <>
      <PageHero
        kicker="Markets"
        title="Applications"
        text="Industry uses for VR coating systems—from OEM lines to infrastructure maintenance."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {applications.map((item) => {
            const Icon = getApplicationIcon(item.slug);
            return (
              <ApplicationTile
                key={item.slug}
                icon={<Icon className="h-7 w-7" />}
                name={item.name}
                text={item.text}
                href={`/applications/${item.slug}`}
              />
            );
          })}
        </div>
      </section>
    </>
  );
}
