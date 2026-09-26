export type VrcMixLpSpecRow = {
  label: string;
  value: string;
};

export type VrcMixLpApplication = {
  title: string;
  description: string;
};

export type VrcMixLpFeature = {
  text: string;
};

export type VrcMixLpFault = {
  fault: string;
  alarm: string;
  response: string;
};

export const vrcMixLpFeatures: VrcMixLpFeature[] = [
  { text: "Electronic variable ratio 2K mixing system" },
  { text: "30 bar max working pressure (air spray system)" },
  { text: "Mixing ratio range up to 15.0 in 0.1 increments" },
  { text: "Accuracy tolerance down to 1% (user settable)" },
  { text: "Flow rate 0.1 to 4 liters per minute" },
  { text: "230V AC 50Hz single phase power supply" },
  { text: "Air pressure requirement 0-7 bars" },
  { text: "RS 232 + Modbus communication" },
  { text: "Touch screen graphical operator interface" },
  { text: "Audio + Visual alarms with auto shut-off" },
  { text: "Pot life monitoring" },
  { text: "Material usage reporting" },
  { text: "Online system health checking" },
];

export const vrcMixLpApplications: VrcMixLpApplication[] = [
  {
    title: "Two-Component Coating Application (Low/Medium Pressure)",
    description:
      "Suitable for all types of two component paints with moderate pot life at low to medium pressure.",
  },
  {
    title: "Colour, Hardeners, Solvents (Modular System)",
    description:
      "Modular system for different recipes with colour, hardeners, and solvents.",
  },
  {
    title: "Colour Change Configuration and Setup",
    description:
      "Configurable colour change setup for flexible production requirements.",
  },
  {
    title: "Auto Flushing Cycle",
    description:
      "Programmable sequential air/solvent purge for automated cleaning cycles.",
  },
];

export const vrcMixLpSpecRows: VrcMixLpSpecRow[] = [
  { label: "System Type", value: "2-Component Electronic Mixing" },
  { label: "Max Working Pressure", value: "30 bar" },
  { label: "Mixing Ratio Range", value: "Up to 15.0 (in 0.1 increments)" },
  { label: "Accuracy Tolerance", value: "Down to 1% (user settable)" },
  { label: "Flow Rate", value: "0.1 to 4 liters per minute" },
  { label: "Air Pressure Requirement", value: "0-7 bars" },
  { label: "Power Supply", value: "230V AC 50Hz Single Phase" },
  { label: "Communication", value: "RS 232 + Modbus" },
  { label: "Control Interface", value: "Touch screen graphical display" },
  { label: "Alarm System", value: "Audio + Visual with auto shut-off" },
];

export const vrcMixLpFaults: VrcMixLpFault[] = [
  { fault: "Off-mixing ratio", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Pot life nearing to end", alarm: "Audio + Visual alarm with test message", response: "Alert" },
  { fault: "Pot life end", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Container nearing to empty", alarm: "Audio + Visual alarm with test message", response: "Alert" },
  { fault: "Container empty", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Surpass of set pressure limits", alarm: "Audio + Visual alarm with test message", response: "Auto shut off" },
  { fault: "Other systems faults & interlocks", alarm: "Audio + Visual alarm with test message", response: "Alert" },
];

export const vrcMixLpCatalogue = {
  name: "VRC - MIX LP",
  category: "Spray Painting Equipment / Electronic Two Component / VRC - Mix LP",
  catalogue: "/media/catalogues/VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
  description:
    "Variable ratio electronic two-component mixing system designed for low to medium pressure spray applications at 30 bar max working pressure. Features mixing ratio range up to 15.0:1 in 0.1 increments, accuracy tolerance down to 1%, flow rate 0.1-4 L/min, and comprehensive fault monitoring with audio-visual alarms and auto shut-off responses.",
};