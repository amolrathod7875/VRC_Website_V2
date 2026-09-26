export type MiniTigerSpecRow = {
  label: string;
  values: string[];
};

export type MiniTigerApplication = {
  title: string;
  description: string;
};

export type MiniTigerFeature = {
  text: string;
};

export const miniTigerFeatures: MiniTigerFeature[] = [
  { text: "Pneumatically sensed high-performance air motor" },
  { text: "High pressure with medium output discharge" },
  { text: "Stainless steel rust-proof hydraulic body" },
  { text: "Easy maintenance" },
  { text: "Ice-free air motor technology" },
  { text: "Durable and rugged, easy to handle" },
  { text: "Compliance with EC and Atex norms" },
];

export const miniTigerApplications: MiniTigerApplication[] = [
  {
    title: "Precision Spray System for Wood Finishing",
    description:
      "Airless and air-assisted spray system ideal for woodworking applications. Perfect for spraying lacquer, clear coat, varnish, and sealer coats with fine finish.",
  },
  {
    title: "Sprayable Primers & Finishing Paints",
    description:
      "Suitable for spraying all kinds of sprayable primers and finish paints with consistent results.",
  },
  {
    title: "Medium-Viscosity Liquid Coatings",
    description:
      "Purpose-built for reliable and efficient spraying of medium-viscosity liquids containing medium-sized particles.",
  },
  {
    title: "Air-Assisted Airless Fine Finish Applications",
    description:
      "Delivers fine finish quality for lacquer, clear coat, and sealer applications in workshop environments.",
  },
];

export const miniTigerSpecColumns = ["15:16", "15:30", "25:16", "28:20", "28:40", "30:70"];

export const miniTigerSpecRows: MiniTigerSpecRow[] = [
  { label: "TYPE", values: ["15:16", "15:30", "25:16", "28:20", "28:40", "30:70"] },
  { label: "PRESSURE RATIO", values: ["15:1", "15:1", "25:1", "28:1", "28:1", "30:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["16", "30", "16", "20", "40", "70"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["60", "80", "80", "80", "80", "125"] },
  { label: "STROKE LENGTH (MM)", values: ["50", "50", "50", "70", "120", "120"] },
  { label: "RECOMMENDED SPRAY VOLUME @15 CYCLES/MIN (LPM)", values: ["0.24", "0.45", "0.24", "0.3", "0.6", "1.05"] },
  { label: "AIR INLET PRESSURE MAXIMUM (BAR)", values: ["6", "6", "6", "6", "6", "6"] },
  { label: "MAXIMUM OUTPUT PRESSURE @ 6 BAR AIR INLET", values: ["90", "90", "150", "168", "168", "210"] },
  { label: "AIR CONSUMPTION N-LPM @15 CYCLES/MINUTE", values: ["17.8", "10.9", "17.8", "27.9", "17.8", "27.9"] },
];

export const miniTigerCatalogue = {
  name: "MINI TIGER",
  category: "Spray Painting Equipment / Mini Tiger",
  catalogue: "/media/catalogues/Tiger_mini.pdf",
  description:
    "Airless Air Assisted Spray Painting Equipment. The MINI TIGER series is purpose-built for reliable and efficient spraying of medium-viscosity liquids. Whether you're working with sprayable primers, finishing paints, or coatings containing medium-sized particles, MINI TIGER equipment delivers consistent results with minimal maintenance.",
};
