export type ValveSpec = {
  label: string;
  value: string;
};

export type ValveProduct = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: ValveSpec[];
  description?: string;
};

export const valveProducts: ValveProduct[] = [
  {
    id: "colour-change-valve-double-disc-ccv-250",
    name: "COLOUR CHANGE VALVE (DOUBLE DISC) CCV 250",
    image: "/media/images/products/vrc.png",
    alt: "Colour change valve double disc CCV 250",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "250 BAR" },
      { label: "VALVE SEAT ID", value: "2 MM" },
      { label: "INLET/CIRCULATION PORT", value: '1/4" BSP(F)' },
      { label: "WETTED PARTS", value: "304, STAINLESS STEEL, PTFE, VITON" },
      { label: "VALVE SEATS & BALL", value: "TUNGSTEN CARBIDE" },
      { label: "CONTROL SYSTEM", value: "PLC-BASED ELECTRO-PNEUMATIC OR COMPLETE PNEUMATIC CONTROL" },
    ],
    description: "Suitable for colour change application in airless and air-assisted airless systems. Fast easy colour changing.",
  },
  {
    id: "colour-change-valve-double-disc-ccv-400",
    name: "COLOUR CHANGE VALVE (DOUBLE DISC) CCV 400",
    image: "/media/images/products/vrc.png",
    alt: "Colour change valve double disc CCV 400",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "400 BAR" },
      { label: "VALVE SEAT ID", value: "2 MM" },
      { label: "INLET/CIRCULATION PORT", value: '1/4" BSP(F)' },
      { label: "WETTED PARTS", value: "304, STAINLESS STEEL, PTFE, VITON" },
      { label: "VALVE SEATS & BALL", value: "TUNGSTEN CARBIDE" },
      { label: "CONTROL SYSTEM", value: "PLC-BASED ELECTRO-PNEUMATIC OR COMPLETE PNEUMATIC CONTROL" },
    ],
    description: "Suitable for colour change application in airless and air-assisted airless systems. Fast easy colour changing.",
  },
  {
    id: "colour-change-valve-single-disc",
    name: "COLOUR CHANGE VALVE (SINGLE DISC)",
    image: "/media/images/products/vrc.png",
    alt: "Colour change valve single disc",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "300 BAR" },
      { label: "INLET/CIRCULATION PORT", value: '1/4" BSP (F)' },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL/TUNGSTEN" },
      { label: "VALVE SEATS & BALL", value: "TUNGSTEN CARBIDE" },
      { label: "CONTROL SYSTEM", value: "PLC-BASED ELECTRO-PNEUMATIC OR COMPLETE PNEUMATIC CONTROL" },
    ],
    description: "Suitable for water based materials. Compact, easy to maintain and service, fast efficient valve action. Fully Stainless Steel.",
  },
  {
    id: "colour-change-valve-low-pressure",
    name: "COLOUR CHANGE VALVE (LOW PRESSURE)",
    image: "/media/images/products/vrc.png",
    alt: "Colour change valve low pressure",
    specifications: [
      { label: "RESULTANT FLUID PATH", value: "EQUIVALENT TO 4 MM HOLE (12.56 MM²)" },
      { label: "FULLY STAINLESS STEEL", value: "YES" },
      { label: "MAXIMUM WORKING PRESSURE", value: "40 BAR" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE, DELRIN" },
      { label: "CONTROL SYSTEM", value: "PLC-BASED ELECTRO-PNEUMATIC OR COMPLETE PNEUMATIC CONTROL" },
    ],
    description: "Suitable for water based materials. Compact, easy to maintain and service, fast efficient valve action.",
  },
  {
    id: "automatic-feeding-valve",
    name: "AUTOMATIC FEEDING (ON/OFF) VALVE 3.0MM, 6.5MM, 10MM",
    image: "/media/images/products/vrc.png",
    alt: "Automatic feeding on/off valve",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "500 BAR (FOR 3 MM), 225 BAR (FOR 6.5 MM), 240 BAR (FOR 10MM)" },
      { label: "OUTLET HOLE SIZE", value: "3.0 MM, 6.5 MM, 10MM" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "UP TO 8 BAR (DOUBLE ACTING)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP(F) FOR 3 MM, 3/8" BSP(F) FOR 6.5 MM, 1/2 BSP(F) FOR 10MM' },
      { label: "OUTLET PORT", value: '3/8" BSP(F) SWIVEL, 1/2" BSP(F) SWIVEL' },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, TUNGSTEN CARBIDE VALVE, PTFE" },
    ],
    description: "Suitable for colour change application in air assisted spray systems. Basic Module consists of three valves, two for colour and one for solvent valve. Add on module consists of two colour valves. Any number of colours possible. Fast easy colour changing.",
  },
];

export const valveCatalogue = {
  name: "VALVES",
  category: "Accessories / Valves",
  catalogue: "/media/catalogues/Valves.pdf",
  description:
    "Valves for colour change and automatic feeding applications in air assisted and airless spray systems.",
};
