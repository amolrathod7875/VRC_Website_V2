export type OtherAccessorySpec = {
  label: string;
  value: string;
};

export type OtherAccessoryVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: OtherAccessorySpec[];
  description?: string;
  variantTable?: {
    columns: string[];
    rows: { name: string; values: string[] }[];
  };
};

export const otherAccessoryVariants: OtherAccessoryVariant[] = [
  {
    id: "quick-release-coupling",
    name: "QUICK RELEASE COUPLING",
    image: "",
    alt: "Quick Release Coupling",
    description: "Quick release coupling for high-pressure fluid connections.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "150 BAR" },
      { label: "INLET / OUTLET PORTS", value: '3/8" BSP(M), 3/8" BSP(F)' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, Nylon, UHMWPE, Tungsten Carbide" },
    ],
  },
  {
    id: "y-restrictor-swivel",
    name: "Y RESTRICTOR",
    image: "",
    alt: "Y Restrictor with Swivel Outlet",
    description: "Y restrictor with swivel outlet for circulation systems.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "10 BAR" },
      { label: "CIRCULATION PORTS", value: '1/4" BSP(M)' },
      { label: "OUTLET PORT", value: '3/8" BSP(F) SWIVEL' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, Aluminium, Viton / PTFE" },
    ],
  },
  {
    id: "y-restrictor-socket",
    name: "Y RESTRICTOR",
    image: "",
    alt: "Y Restrictor with Socket Outlet",
    description: "Y restrictor with socket outlet suitable for male nipple or QRC.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "10 BAR" },
      { label: "CIRCULATION PORTS", value: '1/4" NPS(M)' },
      { label: "OUTLET PORT", value: "Socket suitable for male nipple or QRC" },
      { label: "WETTED PARTS", value: "304 Stainless Steel, Aluminium, Viton, PTFE" },
    ],
  },
  {
    id: "high-pressure-gun-swivel",
    name: "HIGH PRESSURE GUN SWIVEL",
    image: "",
    alt: "High Pressure Gun Swivel",
    description: "High pressure gun swivel for fluid handling up to 450 BAR.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR" },
      { label: "INLET / OUTLET PORTS", value: '1/4" BSP (M) X 1/4" BSP (F) SWIVEL' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE" },
    ],
  },
  {
    id: "high-pressure-z-swivel",
    name: 'HIGH PRESSURE "Z" SWIVEL',
    image: "",
    alt: 'High Pressure "Z" Swivel',
    description: 'High pressure "Z" swivel for fluid handling up to 450 BAR.',
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR" },
      { label: "INLET / OUTLET PORTS", value: '1/4" BSP (M) X 1/4" BSP (F)' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE" },
    ],
  },
  {
    id: "non-return-valve",
    name: "NON RETURN VALVE",
    image: "",
    alt: "Non Return Valve Family",
    description: "Non return valve family with multiple size variants for various pressure ratings.",
    specifications: [
      { label: "WETTED PARTS (COMMON)", value: "304 Stainless Steel, Tungsten Carbide Valve Seat" },
    ],
    variantTable: {
      columns: ["PART NAME", "INLET / OUTLET PORT", "MAXIMUM WORKING PRESSURE", "VALVE SEAT HOLES"],
      rows: [
        {
          name: "NON RETURN VALVE 3/8\"",
          values: ['3/8" BSPM X 3/8" BSPM', "210 BAR", "10 MM"],
        },
        {
          name: "NON RETURN VALVE 1/2\"",
          values: ['1/2" BSPM X 1/2" BSPM', "210 BAR", "10 MM"],
        },
        {
          name: "NON RETURN VALVE 3/4\"",
          values: ['3/4" BSPM X 3/4" BSPM', "450 BAR", "15 MM"],
        },
        {
          name: "NON RETURN VALVE 1\"",
          values: ['1" BSPF X 1" BSPF', "450 BAR", "19 MM"],
        },
        {
          name: "NON RETURN VALVE 1 1/2\"",
          values: ['1 1/2" BSPF X 1 1/2" BSPF', "200 BAR", "32 MM"],
        },
        {
          name: 'NON RETURN VALVE 1/2" SWIVEL',
          values: ['1/2" BSPM X 1/2" BSPF SWIVEL', "350 BAR", "5 MM"],
        },
        {
          name: 'NON RETURN VALVE 3/4" SWIVEL',
          values: ['3/4" BSPM X 3/4" BSPF SWIVEL', "450 BAR", "8.5 MM"],
        },
      ],
    },
  },
];

export const otherAccessoryCatalogue = {
  name: "OTHER ACCESSORIES",
  category: "Accessories / Other Accessories",
  catalogue: "/Catalogue/Other Accessories.pdf",
  description:
    "Complete range of other accessories including quick release couplings, Y restrictors, high pressure gun swivels, high pressure Z swivels, and non return valves in multiple size variants.",
};