"use client";

import { useState } from "react";
import { clientTabs } from "@/lib/data";
import { Placeholder } from "./Placeholder";

const tabs = Object.keys(clientTabs) as (keyof typeof clientTabs)[];

export function ClientsTabs() {
  const [active, setActive] = useState<(typeof tabs)[number]>("Manufacturing");
  const list = clientTabs[active];

  return (
    <div>
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        {tabs.map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setActive(tab)}
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              active === tab ? "bg-brand-800 text-white" : "bg-surface-muted text-slate-700 hover:bg-brand-50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {list.map((name) => (
          <div key={name} className="rounded-lg border border-slate-200 bg-white p-4">
            <Placeholder label={`${name} logo`} className="h-24 rounded-md" />
            <p className="mt-3 text-center text-sm font-medium text-slate-800">{name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
