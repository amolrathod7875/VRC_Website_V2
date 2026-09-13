export type DiaphragmPumpFeature = {
  text: string;
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
  catalogue: "/Catalogue/pulsing dampner.pdf",
  description:
    "Air-operated double diaphragm pump for low-pressure transfer of paints, coatings, chemicals, and water-based materials.",
};