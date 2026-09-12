import type { Metadata } from "next";
import { offices, type Office } from "@/lib/contactData";
import { ContactInfoCard } from "@/components/ContactInfoCard";
import { InquiryForm } from "@/components/InquiryForm";
import { ContactFindUs } from "@/components/ContactFindUs";

export const metadata: Metadata = { title: "Contact Us" };

function officeToInfoCard(office: Office) {
  const phoneContact = office.contacts.find((c) => c.href?.startsWith("tel:"));
  return {
    title: office.label,
    lines: office.addressLines,
    phone: phoneContact?.value,
    phoneHref: phoneContact?.href,
  };
}

export default function ContactPage() {
  return (
    <>
      <section className="relative overflow-hidden bg-[#082B4C]">
        <div className="mx-auto max-w-[1280px] px-4 py-16 sm:px-6 lg:px-8">
          <div className="max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#1678C8]">Get in touch</p>
            <h1 className="mt-3 text-3xl font-semibold text-white sm:text-4xl">Contact Us</h1>
            <p className="mt-4 text-base leading-7 text-slate-200">
              Send an inquiry or reach a regional office directly. Our team is available to discuss coating
              requirements, applications, and support.
            </p>
          </div>
        </div>
        <div className="absolute inset-y-0 right-0 hidden w-1/3 bg-gradient-to-l from-white/[0.03] to-transparent lg:block" />
      </section>

      <ContactFindUs />

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-[1200px] px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-[38%_1fr] lg:gap-10">
            <div className="space-y-4">
              {offices.map((office) => (
                <ContactInfoCard key={office.id} {...officeToInfoCard(office)} />
              ))}
            </div>

            <div className="mt-10 lg:mt-0">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_10px_40px_rgba(8,43,76,0.08)] sm:p-8">
                <div className="mb-6 sm:mb-8">
                  <h2 className="text-xl font-semibold text-[#082B4C] sm:text-2xl">Inquiry Form</h2>
                  <p className="mt-1.5 text-sm text-slate-500">
                    Fill out the form below and our team will get back to you.
                  </p>
                </div>
                <InquiryForm />
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}