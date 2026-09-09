export type FilterSpec = {
  label: string;
  value: string;
};

export type FilterProduct = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: FilterSpec[];
  description?: string;
};

export const filterProducts: FilterProduct[] = [
  {
    id: "cartridge-type-inline-filter",
    name: "CARTRIDGE TYPE INLINE FILTER 1\"",
    image: "/Product_png_s/slimline filter.png",
    alt: "Cartridge type inline filter",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR" },
      { label: "INLET, OUTLET, DRAIN PORTS", value: '1/2" BSP(F), 3/8"BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "Ø27MM X 145MM LONG" },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE SEAL RING" },
    ],
  },
  {
    id: "bag-type-inline-filter",
    name: "BAG TYPE INLINE FILTER 9\"/13\"",
    image: "/Product_png_s/Bag type filter.png",
    alt: "Bag type inline filter",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "30 BAR" },
      { label: "INLET, OUTLET, GAUGE PORTS", value: '1" BSP(F), 1"BSP(F), 1/4" BSP(F)' },
      { label: "BAG SIZE", value: '4" O.D. X 13" LONG, 4" O.D. X 9" LONG' },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE RING" },
    ],
  },
  {
    id: "filter-cassette-l145",
    name: "FILTER CASSETTE L145",
    image: "/Product_png_s/slimline filter.png",
    alt: "Filter cassette L145",
    specifications: [
      { label: "SIZE", value: "Ø 27MM X L 145 MM" },
      { label: "TOTAL FILL VOLUME", value: "83 CC" },
      { label: "MESH SIZES", value: "60, 80, 100, 120, 125, 150, 200, 250, 400, 600" },
      { label: "CONSTRUCTION MATERIAL", value: "304 STAINLESS STEEL" },
    ],
    description: "Note: Filters as on request.",
  },
  {
    id: "tip-filter-assembly",
    name: "TIP FILTER ASSEMBLY",
    image: "/Product_png_s/slimline filter.png",
    alt: "Tip filter assembly",
    specifications: [
      { label: "INLET, OUTLET", value: 'M18 X 1(F), M18 X 1(M) / 7/8" (F), 7/8" (M)' },
      { label: "MESH SIZES", value: "30, 60, 100" },
      { label: "CONSTRUCTION MATERIAL", value: "304 STAINLESS STEEL" },
    ],
  },
  {
    id: "high-pressure-filter",
    name: "HIGH PRESSURE FILTER",
    image: "/Product_png_s/hp filter 350 bar.png",
    alt: "High pressure filter",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR" },
      { label: "INLET, OUTLET, DRAIN PORTS", value: '1/2" BSP(F), 3/8"BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "Ø27MM X 145MM LONG" },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE SEAL RING" },
    ],
  },
  {
    id: "low-pressure-filter-ss",
    name: "LOW PRESSURE FILTER (STAINLESS STEEL)",
    image: "/Product_png_s/slimline filter.png",
    alt: "Low pressure filter stainless steel",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 BAR" },
      { label: "INLET, OUTLET, DRAIN PORTS", value: '1/2 BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "Ø27MM X 114MM LONG" },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE SEAL RING" },
    ],
  },
  {
    id: "low-pressure-filter-aluminium",
    name: "LOW PRESSURE FILTER (ALUMINIUM)",
    image: "/Product_png_s/slimline filter.png",
    alt: "Low pressure filter aluminium",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "120 BAR" },
      { label: "INLET, OUTLET, DRAIN PORTS", value: '3/8" BSP(F), 3/8" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "Ø27MM X 145MM LONG" },
      { label: "WETTED PARTS", value: "304 STAINLESS STEEL, PTFE SEAL RING" },
    ],
  },
  {
    id: "low-pressure-filter-aluminium-24bar",
    name: "LOW PRESSURE FILTER (ALUMINIUM) 24 BAR",
    image: "/Product_png_s/slimline filter.png",
    alt: "Low pressure filter aluminium 24 bar",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "24 BAR" },
      { label: "INLET, OUTLET, DRAIN PORTS", value: '3/8" BSP(F), 3/8" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "Ø27MM X 145MM LONG" },
      { label: "WETTED PARTS", value: "ALUMINIUM, PTFE RING" },
    ],
  },
];

export const filterCatalogue = {
  name: "FILTERS",
  category: "Accessories / Filters",
  catalogue: "/Catalogue/filters.pdf",
  description:
    "Complete range of filters for paint spray systems including cartridge type, bag type, filter cassette, tip filter, high pressure, and low pressure filters.",
};
