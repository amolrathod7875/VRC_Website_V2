export type ElephantSpecRow = {
  label: string;
  values: string[];
};

export type ElephantApplication = {
  title: string;
  description: string;
};

export type ElephantFeature = {
  text: string;
};

export const elephantFeatures: ElephantFeature[] = [
  { text: "Pneumatically sensed high-performance air motor" },
  { text: "High Flow Delivery" },
  { text: "Stainless Steel Hydraulic Body" },
  { text: "Easy Maintenance" },
  { text: "Ice-Free Air Motor Technology" },
  { text: "Non-turbulent flow" },
];

export const elephantApplications: ElephantApplication[] = [
  {
    title: "Paint Materials, Oils & Explosive Liquids Transfer",
    description:
      "Engineered for reliable transfer of paint materials, oils, and explosive liquids in industrial environments.",
  },
  {
    title: "Multiple Spray Guns & Paint Circulation Systems Feed",
    description:
      "Ideal for feeding multiple spray guns and supporting paint circulation systems with high-volume delivery up to 120 L/min.",
  },
  {
    title: "Large Volume Fluid Transfer",
    description:
      "Designed for transferring large volumes of fluids like paints, adhesives, solvents, petrol, and diesel with ease.",
  },
  {
    title: "High-Volume Delivery for Demanding Environments",
    description:
      "Rugged construction ensures reliable performance in demanding industrial environments with delivery up to 120+ L/min.",
  },
];

export const elephantSpecColumns = ["2:1000", "2:2000", "3:2000", "2:4000", "2:6500"];

export const elephantSpecRows: ElephantSpecRow[] = [
  { label: "TYPE", values: ["2:1000", "2:2000", "3:2000", "2:4000", "2:6500"] },
  { label: "PRESSURE RATIO", values: ["2.5:1", "2:1", "3:1", "2:1", "2:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["1000", "2000", "2000", "4000", "6500"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["125", "160", "202", "250", "250"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES/MIN (LPM)", values: ["20", "40", "40", "40", "130"] },
  { label: "MAXIMUM INLET AIR PRESSURE (BAR)", values: ["6", "6", "6", "6", "6"] },
  { label: "MAXIMUM OUTPUT PRESSURE @ 6 BAR AIR INLET", values: ["15", "18", "18", "18", "18"] },
  { label: "AIR CONSUMPTION N-LPM @15 CYCLES/MINUTE", values: ["213", "676", "1050", "1650", "2749"] },
  { label: "CFM @ 6 BAR @15 CYCLES", values: ["14.6", "23.9", "37.3", "58.3", "97.1"] },
];

export const elephantCatalogue = {
  name: "ELEPHANT",
  category: "Paint Transfer Pumps / Elephant",
  catalogue: "/media/catalogues/Elephant.pdf",
  description:
    "Low Pressure Paint Transfer Pumps. Engineered for reliable transfer of paint materials, oils, and explosive liquids. Ideal for feeding multiple spray guns and supporting paint circulation systems. High-volume delivery up to 120 liters per minute and beyond.",
};