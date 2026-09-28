export type LionSpecRow = {
  label: string;
  values: string[];
};

export type LionApplication = {
  title: string;
  description: string;
};

export type LionFeature = {
  text: string;
};

export const lionFeatures: LionFeature[] = [
  { text: "Hydraulic drive for stable, continuous industrial transfer duty" },
  { text: "4000 cc theoretical hydraulic capacity per cycle" },
  { text: "Recommended delivery of 60 L/min at 15 cycles" },
  { text: "Maximum oil inlet pressure of 120 bar" },
  { text: "Heavy-duty wetted parts with chrome-plated and carbide components" },
  { text: "Floor-mounted construction for fixed industrial installations" },
];

export const lionApplications: LionApplication[] = [
  {
    title: "Bulk Paint & Coating Transfer",
    description:
      "High-volume movement of primers, topcoats and compatible coating materials between storage and process equipment.",
  },
  {
    title: "Central Paint-Kitchen Circulation",
    description:
      "Suitable for continuous circulation and feeding in centralized paint supply installations.",
  },
  {
    title: "Production-Line Fluid Feeding",
    description:
      "Feeds compatible process fluids to dispensing, coating or finishing stations where steady volume is required.",
  },
  {
    title: "Tank / Drum Unloading",
    description:
      "Supports transfer from bulk containers into day tanks, circulation loops or downstream process equipment.",
  },
];

export const lionSpecRows = [
  { label: "TYPE", value: "Hydraulic Fluid Transfer Pump" },
  { label: "PRESSURE RATIO", value: "0.14:1" },
  { label: "HYDRAULIC MOTOR TYPE", value: "D66 (Ø66)" },
  { label: "HYDRAULIC CAPACITY / CYCLE (THEORETICAL)", value: "4000 cc" },
  { label: "DIMENSION (D x H) MM", value: "Ø 500 x 1600 HEIGHT" },
  { label: "RECOMMENDED SPRAY VOLUME @ 15 CYCLES (L/MIN)", value: "60 L/Min" },
  { label: "OIL CONSUMPTION @ 1 CYCLE", value: "0.59 L/Cycle" },
  { label: "OIL FLOW RATE AT 10 BAR & @ 15 CYCLES", value: "8.85 L/Min" },
  { label: "MAXIMUM OIL INLET PRESSURE (PRESSURE SAFETY SET)", value: "120 Bar" },
  { label: "MAXIMUM FLUID OUTLET PRESSURE @ 120 BAR OIL INLET", value: "16.8 Bar" },
  { label: "MAXIMUM FLUID TEMP", value: "(II 2G Ex h IIB T4 Gb)" },
  { label: "WETTED PARTS", value: "Carbon Steel Chrome Plated Cylinder & Piston, Tungsten Carbide Seat, PTFE seal rings" },
  { label: "WEIGHT", value: "~132 kg (net weight, std pump)" },
];

export const lionCatalogue = {
  name: "LION",
  category: "Paint Transfer Pumps / LION",
  catalogue: "/media/catalogues/LION_Catalogue.pdf",
  description:
    "Hydraulic high-volume fluid transfer pump designed for continuous circulation and feeding duties. Suitable for centralized coating and process-fluid handling systems with 4000 cc theoretical displacement and 60 L/min recommended delivery.",
};
