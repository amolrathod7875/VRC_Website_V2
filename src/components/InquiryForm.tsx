"use client";

import { FormEvent, useState } from "react";

export function InquiryForm() {
  const [sent, setSent] = useState(false);

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSent(true);
  }

  if (sent) {
    return (
      <div className="rounded-lg border border-[#1678C8]/20 bg-[#EEF5FB] p-6 text-sm text-[#082B4C]">
        Thank you. Your inquiry has been recorded locally. Our team will respond after you connect this form to your mail service.
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <div className="grid gap-5 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Full name</span>
          <input
            required
            name="name"
            className="h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
          />
        </label>
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Company</span>
          <input
            name="company"
            className="h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
          />
        </label>
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Email</span>
          <input
            required
            type="email"
            name="email"
            className="h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
          />
        </label>
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Phone</span>
          <input
            type="tel"
            name="phone"
            className="h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
          />
        </label>
      </div>
      <label className="block">
        <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Inquiry type</span>
        <select
          name="type"
          className="h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
        >
          <option>Product inquiry</option>
          <option>Technical support</option>
          <option>Catalog request</option>
          <option>Partnership</option>
          <option>Career</option>
        </select>
      </label>
      <label className="block">
        <span className="mb-1.5 block text-sm font-medium text-[#082B4C]">Message</span>
        <textarea
          required
          name="message"
          rows={5}
          className="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-800 outline-none transition-all duration-200 focus:border-[#1678C8] focus:ring-4 focus:ring-[#1678C8]/10"
        />
      </label>
      <button
        type="submit"
        className="inline-flex items-center gap-2 rounded-lg bg-[#1678C8] px-6 py-3 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#0B5C97] hover:gap-3"
      >
        Send inquiry
        <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M5 10h10M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
    </form>
  );
}
