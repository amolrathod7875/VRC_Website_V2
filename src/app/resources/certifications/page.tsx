import type { Metadata } from "next";
import { PageHero } from "@/components/PageHero";
import { IconCert, IconArrowRight } from "@/components/Icon";
import { certifications } from "@/lib/data";

export const metadata: Metadata = { title: "Certifications" };

export default function CertificationsPage() {
  return (
    <>
      <PageHero
        kicker="Resources"
        title="Certifications"
        text="Verified certification documents for quality management, ATEX, and CE compliance."
      />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-8">
          {certifications.map((cert) => (
            <article
              key={cert.name}
              className="group flex flex-col rounded-xl border border-slate-200 bg-white shadow-sm transition-shadow hover:shadow-md"
            >
              <a
                href={cert.file}
                target="_blank"
                rel="noopener noreferrer"
                className="relative block w-full overflow-hidden rounded-t-xl bg-surface-muted"
              >
                {cert.preview ? (
                  <img
                    src={cert.preview}
                    alt={cert.title ?? cert.name}
                    className="h-auto w-full object-contain"
                    loading="lazy"
                  />
                ) : (
                  <div className="flex h-48 w-full items-center justify-center">
                    <IconCert className="h-12 w-12 text-brand-600" />
                  </div>
                )}
              </a>
              <div className="p-5">
                <h3 className="text-sm font-semibold text-brand-900">{cert.title ?? cert.name}</h3>
                {cert.validTo && (
                  <p className="mt-1 text-xs text-slate-500">Valid until {cert.validTo}</p>
                )}
                {cert.body && <p className="mt-2 text-xs leading-5 text-slate-600">{cert.body}</p>}
                <a
                  href={cert.file}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-brand-700 hover:text-brand-800"
                >
                  View certificate
                  <IconArrowRight className="h-3 w-3 transition group-hover:translate-x-0.5" />
                </a>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
