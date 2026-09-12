export type CubSpecRow = {
  label: string;
  values: string[];
};

export type CubApplication = {
  title: string;
  description: string;
};

export type CubFeature = {
  text: string;
};

export const cubFeatures: CubFeature[] = [
  { text: "Pneumatically sensed high-performance air motor" },
  { text: "Low shear output" },
  { text: "Very low & easy maintenance" },
  { text: "Compact & easy assembly" },
  { text: "Hard-coated piston & cylinder" },
  { text: "Minimal wear & tear" },
  { text: "Long-life small throat seal stuffing — fast & easily replaceable throat seals" },
  { text: "Stainless Steel Wet Part Versions" },
  { text: "Compliance with EC Norms" },
  { text: "Ice-free air motor technology" },
];

export const cubApplications: CubApplication[] = [
  {
    title: "Small Paint Circulation System",
    description:
      "Ideal for compact setups requiring continuous, smooth paint circulation. Provides pulsation-free transfer, ensuring consistent flow and finish quality.",
  },
];

export const cubSpecColumns = ["CUB 2:400", "CUB 4:400", "CUB 6:400"];

export const cubSpecRows: CubSpecRow[] = [
  { label: "TYPE", values: ["CUB 2:400", "CUB 4:400", "CUB 6:400"] },
  { label: "PRESSURE RATIO", values: ["2:1", "4:1", "6:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["400", "400", "400"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["80", "100", "125"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES/MIN (LPM)", values: ["6", "6", "6"] },
  { label: "MAXIMUM INLET AIR PRESSURE (BAR)", values: ["6", "6", "6"] },
  { label: "AIR CONSUMPTION N-LPM @15 CYCLES/MINUTE", values: ["127", "108", "309"] },
  { label: "CFM @ 6 BAR @15 CYCLES", values: ["4.4", "6.9", "10.91"] },
];

export const cubCatalogue = {
  name: "CUB",
  category: "Paint Transfer Pumps / CUB",
  catalogue: "/Catalogue/cub.pdf",
  description:
    "Four-Ball Piston Type Paint Transfer Pump. Suitable for transferring paint materials, oils, explosive liquids, and feeding multiple spray guns in paint circulation systems. Designed for high delivery up to 16 L/min.",
};