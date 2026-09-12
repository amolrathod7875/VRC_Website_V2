export type TurbineSpecRow = {
  label: string;
  value: string;
};

export type TurbineApplication = {
  title: string;
  description: string;
};

export type TurbineFeature = {
  text: string;
};

export const turbineFeatures: TurbineFeature[] = [
  { text: "All wetted parts are made of stainless steel" },
  { text: "Electrical motors are IS standard (IP55 rated)" },
  { text: "Optional small Laboratory application stirrer with pneumatic motors" },
  { text: "Pneumatic actuated hoisting units for standard drum pails available separately" },
  { text: "Hand held stirrer for low viscous, lab applications" },
  { text: "Pneumatic motor driven stirrer with single post hoist for 20/25/50 Ltr pail (automated lifting)" },
  { text: "Electrically driven stirrer on twin post hoist for 20/50/200 Ltr pails (high viscous materials)" },
  { text: "TB-70 — best suited for hand held stirrer for smaller pails" },
  { text: "TB-110 — Medium duty turbine suited to fit on tank covers" },
  { text: "TB-180 — Heavy duty turbine suited for 200 Ltr hoist" },
  { text: "Rotary mixing stirrer driven by flameproof or EX-certified electric motor" },
  { text: "Efficient crushing and mixing due to unique blade construction" },
  { text: "Blending of all kinds of liquid and semi-solid products" },
  { text: "Eliminates vortex effect, avoiding air bubble inclusion" },
  { text: "Suitable for dissolving, dispersing and crushing of particulates" },
  { text: "Mounting options on pneumatic hoist (20/200 Ltr pail) for ease of operation" },
];

export const turbineApplications: TurbineApplication[] = [
  {
    title: "Paint Agitation & Mixing",
    description:
      "Efficient crushing and mixing of paint materials due to unique blade construction. Used for blending of all kinds of liquid and semi-solid products.",
  },
  {
    title: "Dissolving & Dispersing",
    description:
      "Especially suitable in dissolving, dispersing and crushing of particulates. Eliminates vortex effect, avoiding air bubble inclusion.",
  },
  {
    title: "Standard Pail Mixing",
    description:
      "Mounting options on pneumatic hoist (20/200 Ltr pail) for ease of operation. Can mix varying quantities of material in standard pails.",
  },
];

export const turbineSpecRows: TurbineSpecRow[] = [
  { label: "Wetted Parts Material", value: "Stainless Steel" },
  { label: "Electrical Motor Standard", value: "IS Standard (IP55 Rated)" },
  { label: "Available Motor Types", value: "Flameproof / EX-certified Electric / Pneumatic" },
  { label: "Turbine Blade Sizes", value: "TB-70, TB-110, TB-180" },
  { label: "TB-70 Application", value: "Hand held stirrer for smaller pails (low viscous, lab)" },
  { label: "TB-110 Application", value: "Medium duty turbine for tank covers" },
  { label: "TB-180 Application", value: "Heavy duty turbine for 200 Ltr hoist" },
  { label: "Stirrer Classifications", value: "Hand held / Pneumatic single post hoist / Electric twin post hoist" },
  { label: "Pneumatic Hoist Pail Sizes", value: "20/25/50 Ltr (single post) / 20/50/200 Ltr (twin post)" },
  { label: "Pneumatic Hoist Availability", value: "Standard drum pails available separately" },
  { label: "Lab Stirrer Option", value: "Small laboratory application with pneumatic motors" },
];

export const turbineCatalogue = {
  name: "TURBINE STIRRER",
  category: "Paint Agitation System - Turbine Stirrer",
  catalogue: "/Catalogue/turbine.pdf",
  description:
    "Turbine Stirrer Series — Rotary mixing stirrers driven by flameproof or EX-certified electric motors. Features efficient crushing and mixing due to unique blade construction. Eliminates vortex effect to avoid air bubble inclusion. Suitable for dissolving, dispersing and crushing particulates. Available in hand-held, pneumatic hoist, and electric hoist configurations for 20–200 Ltr pails.",
};