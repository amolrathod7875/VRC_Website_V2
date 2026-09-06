"use client";

import { useState } from "react";
import { clients, clientIndustries, sortByGlobalPriority, sortByIndustryTier } from "@/lib/clients";
import type { Client } from "@/lib/clients";

const tabs = ["All", ...clientIndustries];

export function ClientsTabs() {
  const [active, setActive] = useState<string>("All");
  const [search, setSearch] = useState("");
  const [erroredImages, setErroredImages] = useState<Set<string>>(new Set());

  const displayedClients = (
    active === "All"
      ? sortByGlobalPriority(clients)
      : sortByIndustryTier(clients.filter((c) => c.industry === active))
  ).filter((c) => {
    if (search.trim()) {
      const q = search.toLowerCase().trim();
      return c.name.toLowerCase().includes(q) || c.industry.toLowerCase().includes(q);
    }
    return true;
  });

  const handleImageError = (logoPath: string) => {
    setErroredImages((prev) => new Set([...prev, logoPath]));
  };

  return (
    <div>
      <div className="mb-6">
        <label htmlFor="client-search" className="sr-only">
          Search clients
        </label>
        <input
          id="client-search"
          type="text"
          placeholder="Search by client name or industry..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 placeholder-slate-400 focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600/20"
        />
      </div>

      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        {tabs.map((tab) => {
          const count =
            tab === "All" ? clients.length : clients.filter((c) => c.industry === tab).length;
          return (
            <button
              key={tab}
              type="button"
              onClick={() => setActive(tab)}
              className={`rounded-md px-3 py-2 text-sm font-medium ${
                active === tab
                  ? "bg-[#1678C8] text-white"
                  : "bg-surface-muted text-slate-700 hover:bg-brand-50"
              }`}
            >
              {tab}{" "}
              <span className="opacity-75">
                ({count})
              </span>
            </button>
          );
        })}
      </div>

      <p className="mt-4 text-xs text-slate-500">
        {displayedClients.length} client{displayedClients.length === 1 ? "" : "s"}
        {search && <span> matching &quot;{search}&quot;</span>}
        {!search && active !== "All" && <span> in {active}</span>}
      </p>

      {displayedClients.length === 0 ? (
        <p className="mt-8 text-center text-sm text-slate-500">No clients found.</p>
      ) : (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {displayedClients.map((client) => {
            const key = client.name + "|" + client.industry + "|" + (client.logo || "");
            return (
              <div
                key={key}
                className="flex flex-col items-center gap-2 rounded-lg border border-slate-200 bg-white p-4"
              >
                {client.logo && !erroredImages.has(client.logo) ? (
                  <img
                    src={client.logo}
                    alt={client.name}
                    className="h-16 w-full object-contain"
                    loading="lazy"
                    onError={() => handleImageError(client.logo!)}
                  />
                ) : (
                  <div className="flex h-16 w-full items-center justify-center rounded-md bg-surface-muted">
                    <span className="px-2 text-center text-xs font-medium uppercase tracking-wider text-slate-500">
                      {client.name}
                    </span>
                  </div>
                )}
                <p className="text-center text-sm font-medium text-slate-800">{client.name}</p>
                {active === "All" && <p className="text-xs text-slate-500">{client.industry}</p>}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
