export type StirrerVariant = {
  id: string;
  name: string;
  motorType: string;
  containerSize: string;
  partNumber: string;
  shaftLength: string;
  fanDiameter: string;
};

export type StirrerFeature = {
  text: string;
};

export const stirrerFeatures: StirrerFeature[] = [
  { text: "Vane type pneumatic motor driven" },
  { text: "Axial piston type pneumatic motor driven" },
  { text: "Suitable for container 45-60 ltrs, 100, 200" },
  { text: "Customized specifications available on request" },
  { text: "Geared stirrers Pneumatic/Electrically driven available on request" },
];

export const stirrerVariants: StirrerVariant[] = [
  {
    id: "vane-45-60",
    name: "VANE TYPE PNEUMATIC STIRRER",
    motorType: "Vane type pneumatic motor driven",
    containerSize: "45-60 ltrs",
    partNumber: "16 045 000 00",
    shaftLength: "415",
    fanDiameter: "110",
  },
  {
    id: "vane-100",
    name: "VANE TYPE PNEUMATIC STIRRER",
    motorType: "Vane type pneumatic motor driven",
    containerSize: "100",
    partNumber: "16 100 000 00",
    shaftLength: "600",
    fanDiameter: "300",
  },
  {
    id: "vane-200",
    name: "VANE TYPE PNEUMATIC STIRRER",
    motorType: "Vane type pneumatic motor driven",
    containerSize: "200",
    partNumber: "16 200 000 00",
    shaftLength: "600",
    fanDiameter: "300",
  },
  {
    id: "axial-45-60",
    name: "AXIAL PISTON TYPE PNEUMATIC STIRRER",
    motorType: "Axial piston type pneumatic motor driven",
    containerSize: "45-60 ltrs",
    partNumber: "16 045 000 01",
    shaftLength: "415",
    fanDiameter: "110",
  },
  {
    id: "axial-100",
    name: "AXIAL PISTON TYPE PNEUMATIC STIRRER",
    motorType: "Axial piston type pneumatic motor driven",
    containerSize: "100",
    partNumber: "16 100 000 01",
    shaftLength: "600",
    fanDiameter: "300",
  },
  {
    id: "axial-200",
    name: "AXIAL PISTON TYPE PNEUMATIC STIRRER",
    motorType: "Axial piston type pneumatic motor driven",
    containerSize: "200",
    partNumber: "16 200 000 01",
    shaftLength: "600",
    fanDiameter: "300",
  },
];

export const stirrerCatalogue = {
  name: "PNEUMATIC STIRRER",
  category: "Paint Agitation System - Stirrer / Pneumatic Stirrer",
  catalogue: "/Catalogue/PNEUMATIC STIRRER.pdf",
  description:
    "Pneumatic stirrers for paint agitation and material mixing. Available in vane type and axial piston type pneumatic motor driven configurations for various container sizes.",
};
