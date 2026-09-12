export type FilterSpecRow = {
  label: string;
  values: string[];
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

export const filterSpecRows: FilterSpecRow[] = [
  { label: "FILTER TYPE", values: ["High Pressure Filter (450 BAR)", "High Pressure Filter (350 BAR)", "Low Pressure Filter (SS)", "Low Pressure Filter (Aluminium)", "Cartridge Type Inline Filter", "Bag Type Inline Filter", "Filter Cassette L145", "Tip Filter Assembly"] },
  { label: "MAX WORKING PRESSURE", values: ["450 BAR", "350 BAR", "120 BAR", "24 BAR", "28 BAR", "30 BAR", "\u2014", "\u2014"] },
  { label: "INLET PORT", values: ['1/2" BSP(F)', '1/2" BSP(F)', '3/8" BSP(F)', '3/8" BSP(F)', '1" BSP(F)', '1" BSP(F)', '\u2014', 'M18\u00D71(F) / 7/8" (F)'] },
  { label: "OUTLET PORT", values: ['3/8" BSP(F)', '1/4" BSP(F)', '3/8" BSP(F)', '3/8" BSP(F)', '1" BSP(F)', '1" BSP(F)', '\u2014', 'M18\u00D71(M) / 7/8" (M)'] },
  { label: "DRAIN / GAUGE PORT", values: ['1/4" BSP(F)', '\u2014', '1/4" BSP(F)', '1/4" BSP(F)', '3/8" BSP(F)', '1/4" BSP(F)', '\u2014', '\u2014'] },
  { label: "CASSETTE / ELEMENT SIZE", values: ["\u00D827mm \u00D7 145mm", "\u00D827mm \u00D7 114mm", "\u00D827mm \u00D7 145mm", "\u00D827mm \u00D7 145mm", '2\u00BD" Dia. \u00D7 20" long', 'Bag 4" O.D. \u00D7 13"/9" long', "\u00D827mm \u00D7 145mm", "Disc tip filter"] },
  { label: "WETTED PARTS", values: ["304 SS, PTFE Seal Ring", "304 SS, PTFE Seal Ring", "304 SS, PTFE Seal Ring", "Aluminium, PTFE Ring", "304 SS, PTFE/Viton Ring", "304 SS, PTFE Ring", "304 SS", "304 SS"] },
  { label: "MESH SIZES", values: ["\u2014", "\u2014", "\u2014", "\u2014", "\u2014", "\u2014", "60, 80, 100, 120, 125, 150, 200, 250, 400, 600", "30, 60, 100"] },
  { label: "TOTAL FILL VOLUME", values: ["\u2014", "\u2014", "\u2014", "\u2014", "\u2014", "\u2014", "83 CC", "\u2014"] },
];

export const filterCatalogue = {
  name: "FILTERS",
  category: "Accessories / Filters",
  catalogue: "/Catalogue/filters.pdf",
  description:
    "Complete range of filters for paint spray systems including high pressure filters (up to 450 BAR), low pressure filters (stainless steel & aluminium), cartridge type inline filters, bag type inline filters, filter cassettes with multiple mesh sizes, and tip filter assemblies for spray guns.",
};