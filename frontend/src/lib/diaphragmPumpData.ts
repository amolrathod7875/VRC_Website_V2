export type DiaphragmPumpFeature = {
  text: string;
};

export type DiaphragmPumpApplication = {
  title: string;
  description: string;
};

export type DiaphragmPumpSpecRow = {
  label: string;
  values: string[];
};

export const diaphragmPumpFeatures: DiaphragmPumpFeature[] = [
  { text: "Double diaphragm design for smooth, pulse-free flow" },
  { text: "Self-priming — can run dry without damage" },
  { text: "Variable flow via air pressure regulation" },
  { text: "Handles abrasive and corrosive fluids" },
  { text: "No heat buildup" },
  { text: "BF-PTFE diaphragms available for hot materials" },
  { text: "Diaphragm Type: PTFE / Santropen / FKM" },
];

export const diaphragmPumpApplications: DiaphragmPumpApplication[] = [
  {
    title: "Pulsation-Free Paint Spray Applications",
    description:
      "Specially designed for pulsation-free paint spray applications ensuring smooth finish.",
  },
  {
    title: "Oil, Paint, Chemicals & Industrial Fluids Transfer",
    description:
      "Used for transferring oil, paint, chemicals, and other industrial fluids efficiently.",
  },
  {
    title: "Water-Based & Light Chemical Fluids Transfer",
    description:
      "Suitable for water-based and light chemical fluids with corrosion-resistant build and consistent output.",
  },
  {
    title: "Smooth Fluid Transfer in Industrial Environments",
    description:
      "Compact, high-efficiency design for smooth fluid transfer under moderate pressure and temperature conditions.",
  },
];

export const diaphragmPumpSpecColumns = ["Diaphragm Pump"];

export const diaphragmPumpSpecRows: DiaphragmPumpSpecRow[] = [
  { label: "TYPE", values: ["Air-Operated Double Diaphragm"] },
  { label: "PRESSURE RATIO", values: ["1:1 (standard), 2:1 (high pressure variant)"] },
  { label: "MAX FLOW RATE", values: ["4.2 LPM (252 L/h)"] },
  { label: "OPERATING PRESSURE", values: ["0.4–0.6 MPa (4–6 bar)"] },
  { label: "FLUID PORT", values: ["1/2\""] },
  { label: "WETTED PARTS", values: ["304 Stainless Steel / PTFE / EPDM / FKM"] },
  { label: "TEMPERATURE RANGE", values: ["-20°C to +135°C (T4 rating)"] },
];

export const diaphragmPumpSpecs: { label: string; value: string }[] = [
  { label: "Type", value: "Air-Operated Double Diaphragm" },
  { label: "Pressure Ratio", value: "1:1 (standard), 2:1 (high pressure variant)" },
  { label: "Max Flow Rate", value: "4.2 LPM (252 L/h)" },
  { label: "Operating Pressure", value: "0.4–0.6 MPa (4–6 bar)" },
  { label: "Fluid Port", value: "1/2\"" },
  { label: "Wetted Parts", value: "304 Stainless Steel / PTFE / EPDM / FKM" },
  { label: "Temperature Range", value: "-20°C to +135°C (T4 rating)" },
];

export const diaphragmPumpCatalogue = {
  name: "DIAPHRAGM PUMP",
  category: "Paint Transfer Pumps / Diaphragm Pump",
  catalogue: "/media/catalogues/diaphragm pump.pdf",
  description:
    "Air-operated double diaphragm pump for low-pressure transfer of paints, coatings, chemicals, and water-based materials.",
};