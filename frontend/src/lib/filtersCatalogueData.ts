export type FilterSpec = {
  label: string;
  value: string;
};

export type FilterVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: FilterSpec[];
  description?: string;
};

export const filterVariants: FilterVariant[] = [
  {
    id: "high-pressure-filter-450",
    name: "HIGH PRESSURE FILTER — 450 BAR",
    image: "/media/images/products/Product_png_s/HIGH PRESSURE FILTER 450 bar.jpg",
    alt: "High Pressure Filter 450 BAR",
    description: "High-pressure inline filtration unit for industrial fluid handling.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 bar" },
      { label: "INLET / OUTLET / DRAIN PORTS", value: '1/2" BSP(F), 3/8" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "27 mm × 145 mm long" },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE Seal Ring" },
    ],
  },
  {
    id: "high-pressure-filter-350",
    name: "HIGH PRESSURE FILTER — 350 BAR",
    image: "/media/images/products/Product_png_s/HIGH PRESSURE FILTER 450 bar.jpg",
    alt: "High Pressure Filter 350 BAR",
    description: "High-pressure inline filtration unit for industrial fluid handling.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 bar" },
      { label: "INLET / OUTLET / DRAIN PORTS", value: '1/2" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "27 mm × 114 mm long" },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE Seal Ring" },
    ],
  },
  {
    id: "low-pressure-filter-ss",
    name: "LOW PRESSURE FILTER (STAINLESS STEEL)",
    image: "/media/images/products/Product_png_s/LOW PRESSURE FILTER (STAINLESS STEEL).png",
    alt: "Low Pressure Filter Stainless Steel",
    description: "Low-pressure inline filtration unit with stainless steel construction.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "120 bar" },
      { label: "INLET / OUTLET / DRAIN PORTS", value: '3/8" BSP(F), 3/8" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "27 mm × 145 mm long" },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE Seal Ring" },
    ],
  },
  {
    id: "low-pressure-filter-aluminium",
    name: "LOW PRESSURE FILTER (ALUMINIUM)",
    image: "/media/images/products/Product_png_s/LOW PRESSURE FILTER (STAINLESS STEEL).png",
    alt: "Low Pressure Filter Aluminium",
    description: "Low-pressure inline filtration unit with aluminium construction.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "24 bar" },
      { label: "INLET / OUTLET / DRAIN PORTS", value: '3/8" BSP(F), 3/8" BSP(F), 1/4" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: "27 mm × 145 mm long" },
      { label: "WETTED PARTS", value: "Aluminium, PTFE Ring" },
    ],
  },
  {
    id: "cartridge-type-inline-filter",
    name: "CARTRIDGE TYPE INLINE FILTER 1\"",
    image: "/media/images/products/Product_png_s/CARTRIDGE TYPE INLINE FILTER.png",
    alt: "Cartridge Type Inline Filter 1\"",
    description: "Cartridge-type inline filter for paint spray systems.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "28 bar" },
      { label: "INLET / OUTLET / DRAIN PORTS", value: '1" BSP(F), 1" BSP(F), 3/8" BSP(F)' },
      { label: "FILTER CASSETTE SIZE", value: '2 1/2" Dia. × 20" long' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE Ring / Viton" },
    ],
  },
  {
    id: "bag-type-inline-filter",
    name: "BAG TYPE INLINE FILTER 9\"/13\"",
    image: "/media/images/products/Product_png_s/BAG TYPE INLINE FILTER .png",
    alt: "Bag Type Inline Filter 9\"/13\"",
    description: "Bag-type inline filter for paint spray systems.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "30 bar" },
      { label: "INLET / OUTLET / GAUGE PORTS", value: '1" BSP(F), 1" BSP(F), 1/4" BSP(F)' },
      { label: "BAG SIZE", value: '4" O.D. × 13" long, 4" O.D. × 9" long' },
      { label: "WETTED PARTS", value: "304 Stainless Steel, PTFE Ring" },
    ],
  },
  {
    id: "filter-cassette-l145",
    name: "FILTER CASSETTE L145",
    image: "/media/images/products/Product_png_s/FILTER CASSETTE L145.jpg",
    alt: "Filter Cassette L145",
    description: "Filter cassette element with multiple mesh size options.",
    specifications: [
      { label: "SIZE", value: "27 mm × L145 mm" },
      { label: "TOTAL FILL VOLUME", value: "83 cc" },
      { label: "MESH SIZES", value: "60, 80, 100, 120, 125, 150, 200, 250, 400, 600" },
      { label: "CONSTRUCTION MATERIAL", value: "304 Stainless Steel" },
      { label: "NOTE", value: "Other sizes on request" },
    ],
  },
  {
    id: "tip-filter-assembly",
    name: "TIP FILTER ASSEMBLY",
    image: "/media/images/products/Product_png_s/TIP FILTER ASSEMBLY.jpg",
    alt: "Tip Filter Assembly",
    description: "Disc tip filter assembly for spray guns.",
    specifications: [
      { label: "INLET / OUTLET", value: "M18 × 1(F), M18 × 1(M), 7/8\"(F), 7/8\"(M)" },
      { label: "MESH SIZES", value: "30, 60, 100" },
      { label: "CONSTRUCTION MATERIAL", value: "304 Stainless Steel" },
      { label: "TYPE", value: "Disc tip filter" },
    ],
  },
];

export const filterCatalogue = {
  name: "FILTERS",
  category: "Accessories / Filters",
  catalogue: "/media/catalogues/filters.pdf",
  description:
    "Complete range of filters for paint spray systems including high pressure filters (up to 450 BAR), low pressure filters (stainless steel & aluminium), cartridge type inline filters, bag type inline filters, filter cassettes with multiple mesh sizes, and tip filter assemblies for spray guns.",
};

export type FilterFeature = {
  text: string;
};

export const filterFeatures: FilterFeature[] = [
  { text: "Complete range for paint spray systems" },
  { text: "High pressure filters up to 450 BAR" },
  { text: "Low pressure filters (stainless steel & aluminium)" },
  { text: "Cartridge type inline filters" },
  { text: "Bag type inline filters" },
  { text: "Filter cassette with multiple mesh sizes" },
  { text: "Tip filter assembly for spray guns" },
  { text: "304 Stainless steel construction" },
  { text: "PTFE/Viton seal rings" },
  { text: "Customized filters available on request" },
];