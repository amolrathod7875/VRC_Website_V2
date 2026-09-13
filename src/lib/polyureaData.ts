export type PolyureaSpecRow = {
  label: string;
  values: string[];
};

export type PolyureaApplication = {
  title: string;
  description: string;
};

export type PolyureaFeature = {
  text: string;
};

export const polyureaFeatures: PolyureaFeature[] = [
  { text: "High discharge flow rates" },
  { text: "Stainless steel hydraulic body to compatible Isocyanates" },
  { text: "Easy to operate compact mounted on robust trolley" },
  { text: "Accurate fixed volume mixing ratio 1:1" },
  { text: "Double 3KW heaters for uniform and consistent heating" },
  { text: "Polyurea wrap suff heated hose bundle 15 meter" },
  { text: "12V- Flat Copper heating element hose for long term even heating without abrupt hot spots" },
  { text: "Standard up to 3 set of hose bundle can be attached" },
  { text: "Special ISO Barrel transfer pump, for smooth and leak proof transfer" },
  { text: "Compatible with Air purge fusion gun, as well as Durable manual static mixture type spray gun" },
  { text: "Pressure monitored to cut off pump in case of ratio faults" },
  { text: "Inbuilt Fluid temperature sensor at inlet and add on block provisions for extended hoses" },
];

export const polyureaApplications: PolyureaApplication[] = [
  {
    title: "High-Performance Coating & Insulation System",
    description:
      "Specialized in spraying polyurea paints for durable floor coatings and protective layers. Also used for spraying and dispensing polyurethane foam for insulation and sealing applications.",
  },
  {
    title: "Polyurea Floor Coatings & Protective Layers",
    description:
      "Spraying polyurea paints for durable floor coatings and protective layers in demanding environments.",
  },
  {
    title: "Polyurethane Foam Insulation & Sealing",
    description:
      "Spraying and dispensing polyurethane foam for insulation and sealing applications.",
  },
  {
    title: "Waterproofing Coating Application",
    description:
      "Suitable for two-component high-viscosity solvent-less waterproofing coatings and PU foam applications.",
  },
];

export const polyureaSpecColumns = ["50:1", "38:1", "72:1", "54:1"];

export const polyureaSpecRows: PolyureaSpecRow[] = [
  { label: "MIXING RATIO", values: ["1:1", "1:1", "1:1", "1:1"] },
  { label: "PRESSURE RATIO", values: ["50:1", "38:1", "72:1", "54:1"] },
  { label: "PUMP COMBINATION", values: ["113-113", "155-155", "110-110", "155-155"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["226", "310", "226", "310"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "120", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @10 CYCLES/MIN (LPM)", values: ["2.26", "3.1", "2.26", "3.1"] },
  { label: "MAXIMUM INLET AIR PRESSURE (BAR)", values: ["6", "6", "6", "6"] },
  { label: "MAXIMUM OUTPUT PRESSURE @ 6 BAR AIR INLET", values: ["300", "300", "300", "300"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["250", "250", "300", "300"] },
  { label: "CFM @ 6 BAR @ 10 CYCLES", values: ["825", "825", "1188", "1188"] },
];

export const polyureaCatalogue = {
  name: "POLYUREA",
  category: "Spray Painting Equipment / Polyurea",
  catalogue: "/Catalogue/polyurea.pdf",
  description:
    "Two component hot airless polyurea spray equipment. The range is designed for tough working conditions and is suitable for two component high viscosity, solvent-less coating, waterproofing coating PU foam and insulation coatings.",
};