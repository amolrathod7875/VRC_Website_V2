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
      <div className="rounded-lg border border-brand-100 bg-brand-50 p-6 text-sm text-brand-900">
        Thank you. Your inquiry has been recorded locally. Our team will respond after you connect this form to your mail service.
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Full name</span>
          <input required name="name" className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600" />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Company</span>
          <input name="company" className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600" />
        </label>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Email</span>
          <input required type="email" name="email" className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600" />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Phone</span>
          <input type="tel" name="phone" className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600" />
        </label>
      </div>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-slate-700">Inquiry type</span>
        <select name="type" className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600">
          <option>Product inquiry</option>
          <option>Technical support</option>
          <option>Catalog request</option>
          <option>Partnership</option>
          <option>Career</option>
        </select>
      </label>
      <label className="block text-sm">
        <span className="mb-1 block font-medium text-slate-700">Message</span>
        <textarea required name="message" rows={5} className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-brand-600" />
      </label>
      <button type="submit" className="rounded-md bg-brand-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-600">
        Send inquiry
      </button>
    </form>
  );
}
