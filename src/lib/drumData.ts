export type DrumSpecRow = {
  label: string;
  values: string[];
};

export type DrumFeature = {
  text: string;
};

export const drumFeatures: DrumFeature[] = [
  { text: "High flow rate pumps" },
  { text: "Priming piston (shovel) type suction for high viscous fluids" },
  { text: "Auto shut off for pumps on drum empty" },
  { text: "Option for twin pail switchover system" },
  { text: "Drum capacity up to 200 liters." },
  { text: "Custom built system for non-standard drum size." },
  { text: "Dispensing/spraying nozzles to suit your application" },
];

export const drumApplications = [
  {
    title: "High Viscosity Material Handling",
    description:
      "Designed for dispensing and transferring grease, sealants, and other high-viscosity materials. Ensures efficient material flow directly from standard drums with minimal wastage.",
  },
];

export const drumSpecColumns = [
  "28:550",
  "28:920",
  "30:150",
  "40:110",
  "55:275",
  "60:350",
  "65:175",
  "75:210",
];

export const drumSpecRows: DrumSpecRow[] = [
  { label: "PRESSURE RATIO", values: ["28:1", "28:1", "30:1", "40:1", "55:1", "60:1", "65:1", "75:1"] },
  { label: "DISCHARGE PER CYCLE (CC)", values: ["550", "920", "150", "110", "275", "350", "175", "210"] },
  { label: "AIR MOTOR PISTON DIAMETER (MM)", values: ["300", "350", "160", "160", "300", "350", "250", "300"] },
  { label: "STROKE LENGTH (MM)", values: ["120", "200", "120", "120", "120", "120", "120", "120"] },
  { label: "RECOMMENDED DISPENSING VOLUME @10 CYCLES/MIN (LPM)", values: ["5.5", "9.2", "15", "1.1", "2.75", "3.5", "1.75", "2.1"] },
  { label: "AIR INLET PRESSURE MAXIMUM (BAR)", values: ["6", "6", "6", "6", "6", "6", "6", "6"] },
  { label: "MAXIMUM OUTPUT PRESSURE @ 6 BAR INLET", values: ["168", "168", "180", "240", "330", "360", "390", "450"] },
  { label: "AIR CONSUMPTION N LITRES/MIN @15 CYCLES/MINUTE", values: ["945", "2700", "340", "340", "1190", "825", "825", "1190"] },
];

export const drumCatalogue = {
  name: "DRUM PRESS",
  category: "Dispensing Equipment - Drum Press / Drum Press",
  catalogue: "/Catalogue/DRUM PRESS.pdf",
  description:
    "Medium & heavy duty heated and cold airless drum press dispensing/ transfer equipment. Equipped with medium duty or heavy duty range of pumps and suitable for semi-solid and pasty materials.",
};

export const drumSummarySpecifications = drumSpecRows.map((row) => ({
  label: row.label,
  value: row.values.join(" / "),
}));