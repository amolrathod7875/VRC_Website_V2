import Link from "next/link";
import {
  companyEmail,
  offices,
  socialLinks,
  footerProductColumns,
  footerCompanyLinks,
} from "@/lib/data";
import { IconArrowRight } from "./Icon";

function SocialIcon({ icon }: { icon: string }) {
  const common = "h-4 w-4";
  if (icon === "in") {
    return (
      <svg viewBox="0 0 24 24" className={common} fill="currentColor" aria-hidden>
        <path d="M6.5 9H3.7v11.3h2.8V9zM5.1 3.5A1.65 1.65 0 1 0 5.1 6.8 1.65 1.65 0 0 0 5.1 3.5zM20.3 13.2c0-3.6-1.9-5.3-4.5-5.3-2.1 0-3 1.1-3.6 1.9V9H9.5c0 1.9 0 11.3 0 11.3h2.8v-6.3c0-.3 0-.7.1-1 .3-.7.9-1.5 2-1.5 1.4 0 2 1.1 2 2.6v6.2h2.8c.1 0 .1-6.9.1-7.7z" />
      </svg>
    );
  }
  if (icon === "yt") {
    return (
      <svg viewBox="0 0 24 24" className={common} fill="currentColor" aria-hidden>
        <path d="M23 12.2s0-3.2-.4-4.6c-.2-.9-.9-1.6-1.8-1.8C19.2 5.4 12 5.4 12 5.4s-7.2 0-8.8.4c-.9.2-1.6.9-1.8 1.8C1 9 1 12.2 1 12.2s0 3.2.4 4.6c.2.9.9 1.6 1.8 1.8 1.6.4 8.8.4 8.8.4s7.2 0 8.8-.4c.9-.2 1.6-.9 1.8-1.8.4-1.4.4-4.6.4-4.6zM9.8 15.6V8.8l6.2 3.4-6.2 3.4z" />
      </svg>
    );
  }
  if (icon === "ig") {
    return (
      <svg viewBox="0 0 24 24" className={common} fill="currentColor" aria-hidden>
        <path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 1.8H7A2.2 2.2 0 0 0 4.8 7v10A2.2 2.2 0 0 0 7 19.2h10A2.2 2.2 0 0 0 19.2 17V7A2.2 2.2 0 0 0 17 4.8zM12 8.2A3.8 3.8 0 1 1 8.2 12 3.8 3.8 0 0 1 12 8.2zm0 1.6A2.2 2.2 0 1 0 14.2 12 2.2 2.2 0 0 0 12 9.8zM17.4 7.1a.9.9 0 1 1-.9.9.9.9 0 0 1 .9-.9z" />
      </svg>
    );
  }
  if (icon === "fb") {
    return (
      <svg viewBox="0 0 24 24" className={common} fill="currentColor" aria-hidden>
        <path d="M14.6 9.2V7.6c0-.7.5-1.1 1.2-1.1h1.4V3.5h-2.4c-2.6 0-4.3 1.6-4.3 4.4v1.3H8.4v3h2.1V20.5h4.1v-8.3h2.7l.4-3z" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" className={common} fill="currentColor" aria-hidden>
      <path d="M12.04 2C6.58 2 2.15 6.3 2.15 11.6c0 1.7.46 3.3 1.27 4.7L2 22l5.86-1.5A10.2 10.2 0 0 0 12.04 21c5.46 0 9.89-4.3 9.89-9.6C21.93 6.3 17.5 2 12.04 2zm5.74 13.6c-.24.67-1.18 1.22-1.93 1.38-.52.11-1.2.2-3.49-.73-2.93-1.19-4.82-4.1-4.96-4.29-.14-.19-1.16-1.51-1.16-2.88 0-1.37.74-2.04 1-2.32.24-.27.54-.34.72-.34h.52c.16 0 .39-.06.6.45.24.58.8 2 .87 2.14.07.15.12.32.02.51-.1.2-.15.32-.3.5-.14.17-.3.38-.43.51-.14.13-.29.28-.12.54.16.27.73 1.18 1.57 1.91 1.08.94 1.99 1.23 2.27 1.37.28.13.44.11.6-.07.17-.19.7-.8 1.88-1.07.19-.27.37-.23.62-.13.26.09 1.63.77 1.91.91.28.13.46.2.53.31.07.12.07.67-.17 1.34z" />
    </svg>
  );
}

function FooterAnchor({ label, href, productSlug }: { label: string; href: string; productSlug?: string }) {
  const isExternal = href.startsWith("http");
  const isProduct = Boolean(productSlug);
  const className =
    "group inline-flex items-center gap-1 text-sm text-slate-300 transition-colors duration-200 hover:text-[#1678C8]";

  if (isExternal) {
    return (
      <a href={href} target="_blank" rel="noreferrer" className={className}>
        <span>{label}</span>
      </a>
    );
  }

  if (!isProduct) {
    return <span className="text-sm text-slate-300">{label}</span>;
  }

  return (
    <Link href={href} className={className}>
      <span>{label}</span>
      <IconArrowRight className="h-3.5 w-3.5 -translate-x-1.5 opacity-0 transition-all duration-200 ease-out group-hover:translate-x-0 group-hover:opacity-100" />
    </Link>
  );
}

export function Footer() {
  const year = new Date().getFullYear();
  const headOffice = offices[0];
  const address = headOffice ? headOffice.lines.slice(1).join(", ") : "";
  const social = socialLinks.slice(0, 3);

  return (
    <footer className="mt-auto bg-brand-950 text-slate-200">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-12 px-4 py-12 sm:grid-cols-2 sm:px-6 lg:grid-cols-[1.4fr_1fr_1fr_1fr_1fr_1fr] lg:px-8">
        <div className="space-y-5">
          <h2 className="text-xl font-bold text-white">VR Coatings Pvt. Ltd.</h2>
          <p className="max-w-xs text-sm leading-6 text-slate-300">
            India&apos;s leading manufacturer of industrial spray painting equipment, dispensing
            machines, transfer pumps, and fluid handling systems. ISO, TUV, ATEX &amp; CE
            certified since 1985.
          </p>
          <div className="flex flex-wrap gap-3">
            {social.map((item) => (
              <a
                key={item.name}
                href={item.href}
                target="_blank"
                rel="noreferrer"
                aria-label={item.name}
                className="flex h-9 w-9 items-center justify-center rounded-full bg-brand-800 text-white transition-colors duration-200 hover:bg-brand-600"
              >
                <SocialIcon icon={item.icon} />
              </a>
            ))}
          </div>
        </div>

        {footerProductColumns.map((column) => (
          <div key={column.title} className="space-y-4">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-white">
              {column.title}
            </h3>
            <ul className="space-y-2.5">
              {column.links.map((link) => (
                <li key={link.label}>
                  <FooterAnchor
                    label={link.label}
                    href={link.href}
                    productSlug={link.productSlug}
                  />
                </li>
              ))}
            </ul>
          </div>
        ))}

        <div className="space-y-4">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-white">
            COMPANY
          </h3>
          <ul className="space-y-2.5">
            {footerCompanyLinks.map((link) => (
              <li key={link.label}>
                <FooterAnchor label={link.label} href={link.href} />
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="border-t border-slate-600">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-5 text-xs text-slate-400 sm:px-6 lg:px-8">
          <span>
            © {year} VR Coatings Pvt. Ltd. · {address}
          </span>
          <span className="flex flex-wrap items-center gap-2">
            <span>Made in India</span>
            <span className="text-slate-500">·</span>
            <a
              href="https://www.vrcoatings.com"
              target="_blank"
              rel="noreferrer"
              className="hover:text-[#1678C8]"
            >
              www.vrcoatings.com
            </a>
            <span className="text-slate-500">·</span>
            <a href={`mailto:${companyEmail}`} className="hover:text-[#1678C8]">
              {companyEmail}
            </a>
          </span>
        </div>
      </div>
    </footer>
  );
}
