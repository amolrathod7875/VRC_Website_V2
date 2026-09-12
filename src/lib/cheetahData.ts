export type CheetahSpecRow = {
  label: string;
  values: string[];
};

export type CheetahApplication = {
  title: string;
  description: string;
};

export type CheetahFeature = {
  text: string;
};

export const cheetahFeatures: CheetahFeature[] = [
  { text: "Pneumatically sensed high-performance air motor" },
  { text: "High discharge flow rates" },
  { text: "Stainless steel hydraulic body" },
  { text: "Easy maintenance" },
  { text: "Ice-free air motor technology" },
  { text: "Easy to operate mounted on a robust trolley/stand" },
  { text: "Fixed volume mixing ratio" },
  { text: "Modular design to achieve various mixing ratios" },
  { text: "Online ratio monitoring" },
  { text: "Electrically heated oil-jacketed tank" },
];

export const cheetahApplications: CheetahApplication[] = [
  {
    title: "High-Performance 2K Spray System",
    description:
      "Engineered for spraying challenging materials like solventless epoxy and polyurethane.",
  },
  {
    title: "High-Pressure Two-Component (2K) Paint Applications",
    description:
      "Ideal for high-pressure two-component (2K) paint applications with precise ratio control.",
  },
];

export const cheetahSpecColumns = [
  "1:1",
  "1.4:1",
  "2:1",
  "2.6:1",
  "3:1",
  "4:1",
];

export const cheetahSpecRows: CheetahSpecRow[] = [
  { label: "MIXING RATIO", values: ["1:1", "1.4:1", "2:1", "2.6:1", "3:1", "4:1"] },
  { label: "TRANSFER RATIO", values: ["45:1", "55:1", "65:1", "55:1", "45:1", "35:1"] },
  { label: "PUMP COMBINATION", values: ["110×110/230", "110×110/161", "110×110/110", "100×100/155", "230×110/110", "230×230/110"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["450", "385", "330", "352", "450", "570"] },
  { label: "AIR MOTOR PISTON (MM)", values: ["350", "350", "350", "350", "350", "350"] },
  { label: "RECOMMENDED VOLUME @15 CYCLES/MIN (LPM)", values: ["6.7", "3.5", "3.3", "3.5", "6.75", "8.55"] },
  { label: "AIR INLET PRESSURE MAX (BAR)", values: ["270", "330", "390", "330", "270", "210"] },
  { label: "AIR CONSUMPTION @6 BAR, 15 CYCLES/MIN (CFM)", values: ["85.6", "85.6", "85.6", "85.6", "85.6", "85.6"] },
];

export const cheetahCatalogue = {
  name: "CHEETAH",
  category: "Spray Painting Equipment / Cheetah",
  catalogue: "/Catalogue/Cheetah.pdf",
  description:
    "Two-Component Hot Airless Spray Painting Equipment designed for tough working conditions. Suitable for two-component high viscosity, solventless coating, semi-solid coating, marine coating, and all types of protective coatings.",
};