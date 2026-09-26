export type RhinoSpecRow = {
  label: string;
  values: string[];
};

export type RhinoApplication = {
  title: string;
  description: string;
};

export type RhinoFeature = {
  text: string;
};

export const rhinoFeatures: RhinoFeature[] = [
  { text: "Pneumatically sensed high performance air motor" },
  { text: "High pressure with high output discharge" },
  { text: "Stainless steel rust proof hydraulic body" },
  { text: "Easy maintenance" },
  { text: "Ice free air motor technology" },
  { text: "Durable and rugged, easy to handle" },
  { text: "Compliance to EC and Atex norms" },
];

export const rhinoApplications: RhinoApplication[] = [
  {
    title: "Heavy Structural Painting",
    description:
      "Used for high-viscosity coating on large steel structures like bridges and towers.",
  },
  {
    title: "Railways (Bogies & Wagons)",
    description:
      "Ideal for efficient spray painting of railway bogies and wagons with uniform coverage.",
  },
  {
    title: "Oil and Natural Gas Industries (Pipes/Valves)",
    description:
      "Applies protective coatings on pipes and valves to resist corrosion in harsh environments.",
  },
  {
    title: "Water Pipeline",
    description:
      "Used for coating water pipelines internally and externally to prevent rust and degradation.",
  },
];

export const rhinoSpecColumns = ["28:550", "35:275", "50:210", "55:275", "60:180", "60:350", "70:150", "75:210", "100:210"];

export const rhinoSpecRows: RhinoSpecRow[] = [
  { label: "TYPE", values: ["28:550", "35:275", "50:210", "55:275", "60:180", "60:350", "70:150", "75:210", "100:210"] },
  { label: "PRESSURE RATIO", values: ["28:1", "35:1", "50:1", "55:1", "60:1", "60:1", "70:1", "75:1", "100:1"] },
  { label: "OUTPUT PER CYCLE (CC)", values: ["550", "275", "210", "275", "180", "350", "150", "210", "210"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["300", "250", "250", "300", "250", "350", "250", "300", "350"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120", "120", "120", "120", "120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES PER MINUTE (LITRES)", values: ["5.25", "4.121", "3.15", "4.12", "2.7", "5.25", "2.25", "3.15", "3.15"] },
  { label: "AIR INLET PRESSURE MAXIMUM (BAR)", values: ["6", "6", "6", "6", "6", "6", "6", "6", "6"] },
  { label: "OUTPUT PRESSURE (BAR)", values: ["168", "210", "300", "330", "360", "360", "420", "450", "600"] },
  { label: "AIR CONSUMPTION N LITRES/MIN @15 CYCLES/MINUTE", values: ["1780", "1237", "1237", "1782", "1237", "2424", "1237", "1782", "2424"] },
  { label: "CFM AT 6 BAR @15 CYCLES", values: ["62.96", "43.71", "43.71", "62.96", "43.71", "85.65", "43.7", "62.96", "85.65"] },
];

export const rhinoCatalogue = {
  name: "RHINO",
  category: "Spray Painting Equipment / Rhino",
  catalogue: "/media/catalogues/rhino.pdf",
  description:
    "Heavy Duty Airless Spray Painting Equipment. This range is designed for tough working conditions and suitable for high viscosity, solvent less, low solvent coating, semisolid coating, marine coating etc applications.",
};
