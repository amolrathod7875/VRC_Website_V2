export type TigerSpecRow = {
  label: string;
  values: string[];
};

export type TigerApplication = {
  title: string;
  description: string;
};

export type TigerFeature = {
  text: string;
};

export const tigerFeatures: TigerFeature[] = [
  { text: "Pneumatically sensed double spool stall free air motor" },
  { text: "High pressure with medium output discharge" },
  { text: "Stainless steel rust-proof hydraulic body" },
  { text: "Easy maintenance" },
  { text: "Ice-free air motors" },
];

export const tigerApplications: TigerApplication[] = [
  {
    title: "Medium Duty Paint Application",
    description:
      "Ideal for consistent spraying of medium-viscosity coatings across various surfaces.",
  },
  {
    title: "Structural Painting",
    description:
      "Suitable for painting small to mid-sized steel structures and industrial components.",
  },
  {
    title: "Automobile Paint Spray",
    description:
      "Used for primer and topcoat applications in vehicle body and part painting.",
  },
  {
    title: "Greasing & Lubrication",
    description:
      "Efficiently handles grease and lubricant dispensing in workshops and assembly lines.",
  },
];

export const tigerSpecColumns = ["30:150", "35:70", "40:110", "45:150", "60:70", "60:110"];

export const tigerSpecRows: TigerSpecRow[] = [
  { label: "TYPE", values: ["30:150", "35:70", "40:110", "45:150", "60:70", "60:110"] },
  { label: "PRESSURE RATIO", values: ["30:1", "35:1", "40:1", "45:1", "60:1", "60:1"] },
  { label: "OUTPUT PER CYCLE (CC)", values: ["150", "70", "110", "150", "70", "110"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["Ø 160", "Ø 125", "Ø 160", "Ø 200", "Ø 160", "Ø 200"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120", "120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES PER MINUTE (LITRES)", values: ["2.2", "1.0", "1.6", "2.2", "1.0", "1.6"] },
  { label: "AIR INLET PRESSURE MAXIMUM (BAR)", values: ["6", "6", "6", "6", "6", "6"] },
  { label: "OUTPUT PRESSURE (BAR)", values: ["180", "210", "240", "270", "360", "360"] },
  { label: "AIR CONSUMPTION N LITRES/MIN @15 CYCLES/MINUTE", values: ["506", "309", "506", "791", "506", "791"] },
  { label: "CFM AT 6 BAR @15 CYCLES", values: ["17.8", "10.9", "17.8", "27.9", "17.8", "27.9"] },
];

export const tigerCatalogue = {
  name: "TIGER",
  category: "Spray Painting Equipment / Tiger",
  catalogue: "/Catalogue/Tiger.pdf",
  description:
    "Low & medium duty airless spray painting equipment. This range is suitable for liquids of medium viscosities, all kinds of sprayable primers & finish paints, and paints of medium particle size.",
};
