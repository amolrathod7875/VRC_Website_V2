export type HippoSpecRow = {
  label: string;
  values: string[];
};

export type HippoApplication = {
  title: string;
  description: string;
};

export type HippoFeature = {
  text: string;
};

export const hippoFeatures: HippoFeature[] = [
  { text: "Pneumatically sensed high-performance air motor" },
  { text: "High Flow Delivery" },
  { text: "Stainless Steel Hydraulic Body" },
  { text: "Easy Maintenance" },
  { text: "Ice-Free Air Motor Technology" },
  { text: "Lightweight & User-Friendly" },
  { text: "Compliant with EC Norms" },
];

export const hippoApplications: HippoApplication[] = [
  {
    title: "Transfer Application for Paints, Oil, Chemicals",
    description:
      "Designed for safe and efficient transfer of paints, oils, and industrial chemicals.",
  },
  {
    title: "Automobile Paint Application",
    description:
      "Used to feed paint reliably to spray guns in automotive painting processes.",
  },
  {
    title: "Paint Circulation Systems Feed",
    description:
      "Can feed multiple spray guns in paint circulation systems with high delivery up to 15 L/min.",
  },
  {
    title: "Explosive Liquids Transfer",
    description:
      "Suitable for transferring explosive liquids safely in hazardous area environments.",
  },
];

export const hippoSpecColumns = ["1:170", "3:400", "3:900", "5:900", "12:400"];

export const hippoSpecRows: HippoSpecRow[] = [
  { label: "TYPE", values: ["1:170", "3:400", "3:900", "5:900", "12:400"] },
  { label: "PRESSURE RATIO", values: ["1:1", "3:1", "3:1", "5:1", "12:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["170", "400", "900", "900", "400"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["-", "80", "125", "160", "80"] },
  { label: "STROKE LENGTH (MM)", values: ["-", "120", "120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES/MIN (LPM)", values: ["6.8 liter @40 cycle/min", "6", "13.5", "13.5", "6"] },
  { label: "MAXIMUM INLET AIR PRESSURE (BAR)", values: ["6", "6", "6", "6", "6"] },
  { label: "MAXIMUM OUTPUT PRESSURE @ 6 BAR AIR INLET", values: ["6", "18", "18", "30", "72"] },
  { label: "AIR CONSUMPTION N-LPM @15 CYCLES/MINUTE", values: ["-", "127", "309", "507", "127"] },
  { label: "CFM @ 6 BAR @15 CYCLES", values: ["13.5 cfm @ 30 lpm", "4.5", "10.91", "17.91", "4.4"] },
];

export const hippoCatalogue = {
  name: "HIPPO",
  category: "Paint Transfer Pumps / Hippo",
  catalogue: "/media/catalogues/Hippo.pdf",
  description:
    "Low Pressure Paint Transfer Pumps. This range is suitable for transferring paint materials, explosive liquids, and can feed multiple spray guns in paint circulation systems. It is designed for high delivery up to 15 liters/min.",
};
