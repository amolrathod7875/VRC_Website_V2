export type PortablePressureFeedPotFeature = {
  text: string;
};

export type PortablePressureFeedPotApplication = {
  title: string;
  description: string;
};

export type PortablePressureFeedPotSpecRow = {
  label: string;
  value: string;
};

export const portablePressureFeedPotFeatures: PortablePressureFeedPotFeature[] = [
  { text: "Suitable for transferring paints, oils and explosive liquids" },
  { text: "Suitable for single gun" },
  { text: "Stainless steel rust proof pot" },
  { text: "Clamping arrangement with PTFE Gasket to avoid jamming due to Two Component Paints" },
  { text: "Safety valve to evacuate excess pressure" },
  { text: "Bend Outlet Tube in Nylon to use even last 20cc of paint" },
  { text: "Substitute for suction pot and gravity pot of the spray gun" },
  { text: "Portable design with wheel cart mounting" },
];

export const portablePressureFeedPotApplications: PortablePressureFeedPotApplication[] = [
  {
    title: "Spray Gun Paint Transfer",
    description:
      "Serves as a substitute for suction pot and gravity pot of spray guns, providing consistent paint feed for single-gun applications.",
  },
  {
    title: "Industrial Oils Transfer",
    description:
      "Safe transfer of oils in industrial finishing and coating operations.",
  },
  {
    title: "Explosive Liquids Handling",
    description:
      "Pneumatically operated design safe for transferring explosive liquids in hazardous environments.",
  },
  {
    title: "Two-Component Paint Handling",
    description:
      "Clamping arrangement with PTFE Gasket to avoid jamming due to two-component paints; Nylon outlet tube uses even last 20cc of paint.",
  },
];

export const portablePressureFeedPotSpecRows: PortablePressureFeedPotSpecRow[] = [
  { label: "Pot Capacity", value: "2.5 ltrs Approx" },
  { label: "Max Working Pressure", value: "4 Bar" },
  { label: "Net Weight", value: "3 Kg" },
  { label: "Pot Capacity Available", value: "2.5 ltrs, 5 ltrs, 10 ltrs, 20 ltrs, 40 ltrs" },
];

export const portablePressureFeedPotCatalogue = {
  name: "PORTABLE PRESSURE FEED POT",
  category: "Spray Painting Equipment / Pressure Feed Pot",
  catalogue: "/media/catalogues/PORTABLE PRESSURE FEED POT.pdf",
  description:
    "Portable stainless steel pressure vessel suitable for transferring paint, oils, and explosive liquids. Designed for single gun use as a substitute for suction pot and gravity pot of spray gun.",
};
