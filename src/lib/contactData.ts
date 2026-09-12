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
  },
];

export const defaultOfficeId = "head-office";

export function getOffice(id: string): Office | undefined {
  return offices.find((office) => office.id === id);
}