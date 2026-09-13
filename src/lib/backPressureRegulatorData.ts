export type BackPressureRegulatorSpec = {
  label: string;
  value: string;
};

export type BackPressureRegulatorFeature = {
  text: string;
};

export type BackPressureRegulatorApplication = {
  title: string;
  description: string;
};

export const backPressureRegulatorFeatures: BackPressureRegulatorFeature[] = [
  { text: "Precise back pressure control for consistent fluid delivery" },
  { text: "Suitable for high and low pressure applications" },
  { text: "Durable construction for industrial environments" },
  { text: "Easy adjustment and maintenance" },
];

export const backPressureRegulatorApplications: BackPressureRegulatorApplication[] = [
  {
    title: "Paint Circulation Systems",
    description: "Maintains consistent back pressure in paint circulation loops for uniform spray quality.",
  },
  {
    title: "Fluid Supply Lines",
    description: "Regulates pressure in fluid supply lines to prevent pressure spikes and ensure steady flow.",
  },
  {
    title: "Spray Painting Equipment",
    description: "Provides stable back pressure for airless and conventional spray systems.",
  },
];

export const backPressureRegulatorSpecs: BackPressureRegulatorSpec[] = [
  { label: "MODEL", value: "BPR-01" },
  { label: "MAXIMUM WORKING PRESSURE", value: "—" },
  { label: "REGULATING PRESSURE RANGE", value: "—" },
  { label: "INLET PORT", value: "—" },
  { label: "OUTLET PORT", value: "—" },
  { label: "WETTED PARTS", value: "—" },
  { label: "BODY MATERIAL", value: "—" },
  { label: "SEAL MATERIAL", value: "—" },
  { label: "FLOW RATE", value: "—" },
  { label: "WEIGHT", value: "—" },
  { label: "DIMENSIONS", value: "—" },
];

export const backPressureRegulatorCatalogue = {
  name: "BACK PRESSURE REGULATOR",
  category: "Accessories / Pressure Regulator / Back Pressure Regulator",
  catalogue: "/Catalogue/regulator.pdf",
  description:
    "Back pressure regulator designed for precise pressure control in paint circulation systems and fluid supply lines. Ensures consistent flow and prevents pressure fluctuations in industrial coating applications.",
};