export type DragonVariant = {
  id: string;
  name: string;
  pressureRatio: string;
  dischargePerCycle: string;
  pumpCombination: string;
  maxInletAirPressure: string;
  maxOutputPressure: string;
  mixingRatio: string;
  supply: string;
  referenceMaterial: string;
};

export type DragonFeature = {
  text: string;
};

export type DragonApplication = {
  title: string;
  description: string;
};

export const dragonFeatures: DragonFeature[] = [
  { text: "High duty Airless Plural component Passive Fire protection (PFP) spraying equipment" },
  { text: "Specially designed for seamless application of intumescent paint coating" },
  { text: "Modular configuration to operate custom mixing ratios" },
  { text: "Essential measured temperature and pressures, along with analog reference gauges" },
  { text: "Devices displayed on panel for smooth operation and monitoring" },
  { text: "Mixing block and Outlet manifold direct flush option" },
  { text: "Flush type pressure transmitter to cutoff system in case of unhealthy spray conditions" },
  { text: "Speed of the agitators controlled as per requirement" },
  { text: "Special VPR to protect the equipment from voltage surges and fluctuations" },
  { text: "Individual controlled heaters for material tanks to adjust as per material heating requirements" },
  { text: "High discharge transfer pumps for efficient transfer of material from pails to individual tanks" },
  { text: "Enhanced high flow inline heaters with individual temperature control" },
  { text: "Double static mixture to ensure precise and 100% material mixing" },
];

export const dragonApplications: DragonApplication[] = [
  {
    title: "Fireproof Coating Application System",
    description:
      "Designed for applying intumescent fireproof coatings with high build and precision. Ideal for passive fire protection in structural steel and industrial projects.",
  },
  {
    title: "Intumescent Paint Coating Application",
    description:
      "Specifically designed for seamless application of intumescent paint coatings with modular configuration for custom mixing ratios.",
  },
  {
    title: "Passive Fire Protection for Structural Steel",
    description:
      "Ideal for passive fire protection of structural steel in industrial and infrastructure projects.",
  },
  {
    title: "Passive Fire Protection for Industrial Projects",
    description:
      "Suitable for fire protection of industrial facilities including oil & gas, petrochemical, and offshore platforms.",
  },
];

export const dragonVariants: DragonVariant[] = [
  {
    id: "dragon-1-1",
    name: "Dragon 1:1",
    pressureRatio: "73:1",
    dischargePerCycle: "302 CC",
    pumpCombination: "350 - (151/151)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "438 BAR",
    mixingRatio: "1:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "Jot char 1709,Carboline3000SP, Carbolinethermo lag-E100,Chartek- 2218",
  },
  {
    id: "dragon-2-28-1",
    name: "Dragon 2.28:1",
    pressureRatio: "58:1",
    dischargePerCycle: "371CC",
    pumpCombination: "350 - (145-113/113)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "348 BAR",
    mixingRatio: "2.28:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "PITT CHAR - NX",
  },
  {
    id: "dragon-2-33-1",
    name: "Dragon 2.33:1",
    pressureRatio: "58:1",
    dischargePerCycle: "377CC",
    pumpCombination: "350 - (151-113/113)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "348 BAR",
    mixingRatio: "2.33:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "PITT CHAR -XP, Chartek 7E, Chartek-1960CSP",
  },
  {
    id: "dragon-2-35-1",
    name: "Dragon 2.35:1",
    pressureRatio: "58:1",
    dischargePerCycle: "377CC",
    pumpCombination: "350 - (151-113/113)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "348 BAR",
    mixingRatio: "2.35:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "Jotun Steel Master 1200HPE",
  },
  {
    id: "dragon-2-5-1",
    name: "Dragon 2.5:1",
    pressureRatio: "57:1",
    dischargePerCycle: "395CC",
    pumpCombination: "350 - (169-113/113)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "342 BAR",
    mixingRatio: "2.5:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "Hempafire XTR 100",
  },
  {
    id: "dragon-2-1",
    name: "Dragon 2:1",
    pressureRatio: "67:1",
    dischargePerCycle: "339CC",
    pumpCombination: "350 - (113-113/113)",
    maxInletAirPressure: "6 BAR",
    maxOutputPressure: "402 BAR",
    mixingRatio: "2:1",
    supply: "415V/3Ø/50HZ",
    referenceMaterial: "Firetex M90/02",
  },
];

export const dragonCatalogue = {
  name: "DRAGON",
  category: "Spray Painting Equipment / Dragon",
  catalogue: "/media/catalogues/dragon.pdf",
  description:
    "Passive fire protection High performance airless spray system. High duty Airless Plural component Passive Fire protection (PFP) spraying equipment. This range is specifically designed for seamless application of intumescent paint coating, with modular configuration to operate custom mixing ratios.",
};
