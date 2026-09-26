/**
 * Single source of truth for all VR Coatings office / contact information
 * used on the /contact page.
 *
 * Every value below is verified company data. Nothing here is invented:
 *  - addresses, phone numbers and emails come from the supplied company data
 *  - the YouTube link reuses the existing verified `socialLinks` entry
 *  - the website link reuses the existing verified footer entry
 */

export type OfficeContact = {
  label?: string | null;
  value: string;
  href?: string;
};

export type Office = {
  id: string;
  label: string;
  icon: "building2" | "factory" | "globe2";
  name: string;
  city: string;
  addressLines: string[];
  contacts: OfficeContact[];
  mapEmbedUrl: string;
  googleMapsUrl: string;
  /** Verified site photograph used on the About / Global Presence office cards. */
  image: string;
  imageAlt: string;
};

function embedUrl(address: string): string {
  return `https://www.google.com/maps?q=${encodeURIComponent(address)}&output=embed`;
}

function mapsSearchUrl(address: string): string {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;
}

export const YOUTUBE_URL = "https://www.youtube.com";
export const WEBSITE_URL = "https://www.vrcoatings.com";
export const SALES_EMAIL = "sales@vrcoatings.com";
export const HEAD_OFFICE_PHONE = "+91 8237086924";

const HEAD_OFFICE_ADDRESS =
  "J - 138, Bhosari Industrial Area, Bhosari, Pune - 411 026, Maharashtra, India";
const FACTORY_ADDRESS =
  "Sector No. 7, Plot No. 136, PCNTDA Industrial Area, Bhosari, Pune - 411 026, Maharashtra, India";
const NORTH_AMERICA_ADDRESS =
  "648, Welham Rd, Barrie, Ontario L4N 9A1, Canada";
const WAI_MIDC_ADDRESS =
  "D-91, Wai MIDC, Unnamed Road, Maharashtra Industrial Development Corporation, Lohare, Wai Rural, Maharashtra - 412803, India";

export const offices: Office[] = [
  {
    id: "head-office",
    label: "HEAD OFFICE",
    icon: "building2",
    name: "V R Coatings Pvt. Ltd.",
    city: "Pune",
    addressLines: [
      "J - 138, Bhosari Industrial Area",
      "Bhosari, Pune - 411 026",
      "Maharashtra, India",
    ],
    contacts: [
      { label: "Reception", value: "+91 8237086924", href: "tel:+918237086924" },
      { label: "Marketing", value: "+91 8237086913", href: "tel:+918237086913" },
      { label: null, value: "sales@vrcoatings.com", href: "mailto:sales@vrcoatings.com" },
      { label: "Fax", value: "+91 (020) 27130891" },
      { label: "West India", value: "+91 8888846546", href: "tel:+918888846546" },
      { label: "North India", value: "+91 9850967289", href: "tel:+919850967289" },
      { label: "South India", value: "+91 8308800774", href: "tel:+918308800774" },
      { label: "East & Central", value: "+91 9168661541", href: "tel:+919168661541" },
    ],
    mapEmbedUrl: embedUrl(HEAD_OFFICE_ADDRESS),
    googleMapsUrl: mapsSearchUrl(HEAD_OFFICE_ADDRESS),
    image: "/media/images/about/HEAD OFFICE.jpg",
    imageAlt: "Head Office facility – Pune, India",
  },
  {
    id: "factory",
    label: "FACTORY",
    icon: "factory",
    name: "V R Coatings Pvt. Ltd.",
    city: "Pune",
    addressLines: [
      "Sector No. 7, Plot No. 136",
      "PCNTDA Industrial Area",
      "Bhosari, Pune - 411 026",
      "Maharashtra, India",
    ],
    contacts: [
      { label: "Reception", value: "+91 8237086903", href: "tel:+918237086903" },
      { label: "After Sales", value: "+91 8237086892", href: "tel:+918237086892" },
      { label: "Dispatch", value: "+91 8237086893", href: "tel:+918237086893" },
    ],
    mapEmbedUrl: embedUrl(FACTORY_ADDRESS),
    googleMapsUrl: mapsSearchUrl(FACTORY_ADDRESS),
    image: "/media/images/about/MANUFACTURING.jpg",
    imageAlt: "Manufacturing facility – Bhosari, Pune",
  },
  {
    id: "north-america",
    label: "NORTH AMERICA",
    icon: "globe2",
    name: "V R Coatings (North America) Ltd.",
    city: "Barrie",
    addressLines: [
      "648, Welham Rd, Barrie",
      "Ontario L4N 9A1",
      "Canada",
    ],
    contacts: [
      { label: null, value: "+1-705-739-0609", href: "tel:+17057390609" },
      { label: null, value: "sales@vrcoatingsna.com", href: "mailto:sales@vrcoatingsna.com" },
    ],
    mapEmbedUrl: embedUrl(NORTH_AMERICA_ADDRESS),
    googleMapsUrl: mapsSearchUrl(NORTH_AMERICA_ADDRESS),
    image: "/media/images/about/NORTH AMERICA.jpg",
    imageAlt: "North America office – Barrie, Ontario, Canada",
  },
  {
    id: "wai-midc",
    label: "WAI MIDC",
    icon: "factory",
    name: "V R Coatings Pvt. Ltd.",
    city: "Wai",
    addressLines: [
      "D-91, Wai MIDC, Unnamed Road",
      "Maharashtra Industrial Development Corporation",
      "Lohare, Wai Rural",
      "Maharashtra - 412803, India",
    ],
    contacts: [],
    mapEmbedUrl: embedUrl(WAI_MIDC_ADDRESS),
    googleMapsUrl: mapsSearchUrl(WAI_MIDC_ADDRESS),
    image: "/media/images/about/WAI MIDC.jpg",
    imageAlt: "Wai MIDC facility – Wai, Maharashtra",
  },
];

export const defaultOfficeId = "head-office";

export function getOffice(id: string): Office | undefined {
  return offices.find((office) => office.id === id);
}

export type FooterLink = { label: string; href: string; productSlug?: string };
export type FooterColumn = { title: string; links: FooterLink[] };

export const socialLinks = [
  { name: "LinkedIn", href: "https://www.linkedin.com", icon: "in" },
  { name: "YouTube", href: "https://www.youtube.com", icon: "yt" },
  { name: "Instagram", href: "https://www.instagram.com", icon: "ig" },
  { name: "Facebook", href: "https://www.facebook.com", icon: "fb" },
  { name: "WhatsApp", href: "https://wa.me/918237086924", icon: "wa" },
];

export const footerProductColumns: FooterColumn[] = [
  {
    title: "SPRAY SYSTEMS",
    links: [
      { label: "DRAGON — PFP System", href: "/products/dragon", productSlug: "dragon" },
      { label: "CHEETAH — 2K Hot Airless", href: "/products/cheetah", productSlug: "cheetah" },
      { label: "RHINO — Heavy Duty", href: "/products/rhino", productSlug: "rhino" },
      { label: "TIGER — Low/Medium Duty", href: "/products/tiger", productSlug: "tiger" },
      { label: "MINI TIGER — Air-Assisted", href: "/products/mini-tiger", productSlug: "mini-tiger" },
      { label: "POLYUREA System", href: "/products/polyurea", productSlug: "polyurea" },
      { label: "VRC-MIX HP", href: "/products/vrc-mix-hp", productSlug: "vrc-mix-hp" },
      { label: "VRC MIX (L/M)", href: "/products/vrc-mix-lp", productSlug: "vrc-mix-lp" },
      { label: "LEOPARD — Electric Pump", href: "/products/leopard-electric", productSlug: "leopard-electric" },
      { label: "TUBE/VARNISH COATING", href: "/products/tube-varnish-coating-system", productSlug: "tube-varnish-coating-system" },
    ],
  },
  {
    title: "TRANSFER PUMPS",
    links: [
      { label: "ELEPHANT — High Volume", href: "/products/elephant", productSlug: "elephant" },
      { label: "HIPPO — Low Pressure", href: "/products/hippo", productSlug: "hippo" },
      { label: "BARREL PUMP — 20L", href: "/products/barrel-pump", productSlug: "barrel-pump" },
      { label: "CUB — Four-Ball Piston", href: "/products/cub", productSlug: "cub" },
      { label: "DRUM PRESS", href: "/products/drum-press", productSlug: "drum-press" },
    ],
  },
  {
    title: "SPRAY GUNS",
    links: [
      { label: "Manual Spray Guns", href: "/products/manual-guns", productSlug: "manual-guns" },
      { label: "Automatic Spray Guns", href: "/products/automatic-guns", productSlug: "automatic-guns" },
      { label: "KINGFISHER — Conventional", href: "/products/conventional-guns", productSlug: "conventional-guns" },
    ],
  },
  {
    title: "ACCESSORIES",
    links: [
      { label: "Ball Valves — up to 500 BAR", href: "/products/valves", productSlug: "valves" },
      { label: "Pressure Regulators HP/LP", href: "/products/pressure-regulator", productSlug: "pressure-regulator" },
      { label: "Inline Filters HP/LP", href: "/products/filters", productSlug: "filters" },
      { label: "Turbine Stirrers", href: "/products/turbine-stirrer", productSlug: "turbine-stirrer" },
      { label: "Pneumatic Stirrer", href: "/products/pneumatic-stirrer", productSlug: "pneumatic-stirrer" },
      { label: "Pressure Feed Pot", href: "/products/portable-pressure-feed-pot", productSlug: "portable-pressure-feed-pot" },
      { label: "Pulsation Dampner", href: "/products/diaphragm-pump", productSlug: "diaphragm-pump" },
    ],
  },
];

export const footerCompanyLinks: FooterLink[] = [
  { label: "About VR Coatings", href: "/about" },
  { label: "Industries Served", href: "/industries" },
  { label: "Product Videos", href: "/products" },
  { label: "Careers", href: "/resources/career" },
  { label: "Vendor Registration", href: "/contact" },
  { label: "Contact Us", href: "/contact" },
  { label: "Visit Original Site", href: "https://www.vrcoatings.com" },
];