export type VrcMixHpSpecRow = {
  label: string;
  value: string;
};

export type VrcMixHpApplication = {
  title: string;
  description: string;
};

export type VrcMixHpFeature = {
  text: string;
};

export const vrcMixHpFeatures: VrcMixHpFeature[] = [
  { text: "Accurate component metering by pump & precision metering valves" },
  { text: "Reliable online mixing ratio assurance" },
  { text: "Remote mixing manifold - can be kept closer to spray gun for minimum mixed material in the system" },
  { text: "Field proven pumps - high performance, easy to maintain pumps for material & flushing" },
  { text: "Simple & Easy to use - user friendly operator interface" },
  { text: "Portable - mounted on wheel cart including solvent pump, easy to move" },
  { text: "Mix ratio range up to 10:1 in 0.1 increments" },
  { text: "Material usage reporting - accumulative + daily consumption" },
  { text: "Pot life monitoring of mixed material with online system health checking by pressure monitoring" },
  { text: "Level monitoring - online container level monitoring based on material consumption" },
  { text: "Communication - RS 232 port for printer/network/PC, Protocol Modbus" },
  { text: "Operator interface - Hardware key for ratio setting / Touch screen graphical display with audio-visual alarm system" },
];

export const vrcMixHpApplications: VrcMixHpApplication[] = [
  {
    title: "Two-Component Paint Applications",
    description:
      "Suitable for all types of two component paints with moderate pot life.",
  },
  {
    title: "Airless / Air Assisted Airless Spraying",
    description:
      "Maximum flow rate 6.8 L/min, maximum fluid pressure 450 bar.",
  },
  {
    title: "High Viscosity Material Handling",
    description:
      "Designed for dispensing and transferring grease, sealants, and other high-viscosity materials. Ensures efficient material flow directly from standard drums with minimal wastage.",
  },
  {
    title: "Material Usage Reporting & Pot Life Monitoring",
    description:
      "Online system health checking with accumulative/daily consumption reporting and pot life monitoring of mixed material.",
  },
];

export const vrcMixHpSpecRows: VrcMixHpSpecRow[] = [
  { label: "System Type", value: "2-Component Electronic Mixing" },
  { label: "Max Working Pressure", value: "450 BAR" },
  { label: "Mix Ratio Range", value: "Up to 10:1 in 0.1 increments" },
  { label: "Application Type", value: "Airless / Air Assisted Airless" },
  { label: "Maximum Flow Rate", value: "6.8 L/min" },
  { label: "Air Pressure Requirement", value: "4-7 bar" },
  { label: "Electrical Power Requirement", value: "240V AC 50 Hz Single Phase" },
  { label: "Material Usage Reporting", value: "Accumulative + daily consumption" },
  { label: "Pot Life Monitoring", value: "Online system health checking by pressure monitoring" },
  { label: "Level Monitoring", value: "Online container level monitoring based on material consumption" },
  { label: "Communication", value: "RS 232 communication port for printer/network/PC, Protocol Modbus" },
  { label: "Operator Interface", value: "Hardware key for ratio setting / Touch screen graphical display with audio-visual alarm system" },
];

export const vrcMixHpFaults = [
  { fault: "Off-mixing ratio", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Pot life nearing to end", alarm: "Audio + Visual alarm with test message", response: "Alert" },
  { fault: "Pot life end", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Container nearing to empty", alarm: "Audio + Visual alarm with test message", response: "Alert" },
  { fault: "Container empty", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Surpass of set pressure limits", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Other systems faults & interlocks", alarm: "Audio + Visual alarm with test message", response: "Alert" },
];

export const vrcMixHpCatalogue = {
  name: "VRC MIX HP",
  category: "Spray Painting Equipment / Electronic Two Component / VRC - Mix HP",
  catalogue: "/Catalogue/VRC - MIX HP.pdf",
  description:
    "Advanced Variable Ratio Electronic Two Component Airless Spray Painting Equipment. Suitable for all types of two component paints with moderate pot life. Features accurate component metering, online mixing ratio assurance, remote mixing manifold, and comprehensive fault generation with system response.",
};