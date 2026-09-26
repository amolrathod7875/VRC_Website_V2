export type TubeVarnishSpecRow = {
  label: string;
  values: string[];
};

export type TubeVarnishApplication = {
  title: string;
  description: string;
};

export type TubeVarnishFeature = {
  text: string;
};

export const tubeVarnishFeatures: TubeVarnishFeature[] = [
  { text: "Basic Airless spray coating system for continuous line production" },
  { text: "Closed spray chamber with suction chamber and over-sprayed coating material re-cycling system" },
  { text: "Fumes exhaust system with water spraying chamber to remove traces of coating material" },
  { text: "Coating material tank, solvent tank and water tank" },
  { text: "Airless pump with double filter system — two high pressure cassette filters in series with drain ball valves" },
  { text: "In-line heater and two auto on/off valves — one for paint and one for solvent" },
  { text: "Spray ring for different type of pipe sizes" },
  { text: "Fume collection and filtration system with water shower, metal filter and exhaust blower" },
];

export const tubeVarnishApplications: TubeVarnishApplication[] = [
  {
    title: "External Pipe Coating",
    description:
      "External pipe coating line complete with material handling. Suitable for diameter 1/2\" to 8\" and length 4mtr to 8mtr. This system comes with single pipe at a time. Single pipe sizes = 5\" to 12\".",
  },
  {
    title: "Internal and External Pipe Coating",
    description:
      "Internal and external pipe coating line complete with material handling. Suitable for diameter 1/2\" to 8\" and length 4mtr to 8mtr. This system comes with single / double pipe at a time. Double pipe sizes = 2\" to 4\". Single pipe sizes = 5\" to 8\".",
  },
  {
    title: "External Varnish / Enamel / Water Solvent Based Pipe Coating",
    description:
      "External pipe coating application for varnish, enamel and water solvent based pipe coatings.",
  },
  {
    title: "Post Heating Oven for Pipe Coating",
    description:
      "Customised design post heating oven as per pipe size and length. Suitable for diameter 1\" to 8\" & length 4mtr to 8mtr, up to 4\" to 12\" & length 4mtr to 12mtr.",
  },
];

export const tubeVarnishSpecColumns = ["Parameter"];

export const tubeVarnishSpecRows: TubeVarnishSpecRow[] = [
  { label: "DUCT FLANGE SIZE (OUT SIDE)", values: ["440x340x4mm"] },
  { label: "DUCT FLANGE SIZE (IN SIDE)", values: ["375x275"] },
  { label: "WATER COLLECTION TANK WATER LEVEL", values: ["200 mm (H)"] },
  { label: "COATING TYPE", values: ["External varnish / enamel / water solvent based pipe coating"] },
  { label: "SYSTEM TYPE", values: ["Basic Airless spray coating system for continuous line production"] },
];

export const tubeVarnishCatalogue = {
  name: "TUBE / VARNISH COATING",
  category: "Spray Painting Equipment / Tube / Varnish Coating",
  catalogue: "/media/catalogues/TUBE VARNISH COATING SYSTEM.pdf",
  description:
    "Tube coating system for continuous line production. Basic Airless spray coating system with a closed spray chamber equipped with spray chambers, suction chamber, over-sprayed coating material re-cycling system, fumes exhaust system and a water spraying chamber to remove traces of coating material. Includes coating material tank, solvent tank and water tank.",
};