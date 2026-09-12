export type BarrelPumpSpecRow = {
  label: string;
  values: string[];
};

export type BarrelPumpApplication = {
  title: string;
  description: string;
};

export type BarrelPumpFeature = {
  text: string;
};

export const barrelPumpFeatures: BarrelPumpFeature[] = [
  { text: "Pneumatically operated transfer pump for 200L steel drums and 210L plastic barrels" },
  { text: "High pressure with 4:1 to 60:1 pressure ratio variants" },
  { text: "Stainless steel rust-proof hydraulic body" },
  { text: "Four-foot ram pump with follower plate for minimal waste" },
  { text: "Easy maintenance and cleaning" },
  { text: "Durable and rugged design for industrial use" },
];

export const barrelPumpApplications: BarrelPumpApplication[] = [
  {
    title: "Drum and Barrel Transfer",
    description:
      "Extracting paint and viscous fluids from 200L steel drums and 210L plastic barrels with minimal waste and residue.",
  },
  {
    title: "Industrial Paint Supply",
    description:
      "Reliable transfer of industrial coatings, primers, and finish paints from containers to spray equipment.",
  },
  {
    title: "Viscous Fluid Handling",
    description:
      "Handles high-viscosity liquids efficiently, making it ideal for heavy-duty coating applications.",
  },
  {
    title: "Hazardous Area Operations",
    description:
      "Pneumatically operated design ensures safe operation in environments where electrical equipment is restricted.",
  },
];

export const barrelPumpSpecColumns = ["4:24", "6:36", "12:72", "60:360"];

export const barrelPumpSpecRows: BarrelPumpSpecRow[] = [
  { label: "TYPE", values: ["4:24", "6:36", "12:72", "60:360"] },
  { label: "PRESSURE RATIO", values: ["4:1", "6:1", "12:1", "60:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["230", "230", "230", "230"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["80", "100", "125", "160"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120", "120"] },
  { label: "MAXIMUM INLET AIR PRESSURE (BAR)", values: ["6", "6", "6", "6"] },
  { label: "OUTPUT PRESSURE @ 6 BAR AIR INLET (BAR)", values: ["24", "36", "72", "360"] },
  { label: "AIR CONSUMPTION N-LPM @ 15 CYCLES/MINUTE", values: ["127", "96", "309", "506"] },
  { label: "CFM AT 6 BAR @ 15 CYCLES", values: ["45", "6.7", "10.9", "17.9"] },
];

export const barrelPumpCatalogue = {
  name: "BARREL PUMP",
  category: "Paint Transfer Pumps / Barrel Pump",
  catalogue: "/Catalogue/Barrel Pump.pdf",
  description:
    "Pneumatically operated barrel transfer pump for extracting paint and viscous fluids from 200L steel drums and 210L plastic barrels with minimal waste. Available in multiple pressure ratio variants from 4:1 to 60:1.",
};
