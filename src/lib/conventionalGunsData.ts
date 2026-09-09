export type GunSpec = {
  label: string;
  value: string;
};

export type GunVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  catalogueNote?: string;
  specifications: GunSpec[];
};

export const conventionalGunVariants: GunVariant[] = [
  {
    id: "kingfisher-silver",
    name: "KINGFISHER SILVER",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Kingfisher silver gun.jpg",
    alt: "Kingfisher Silver conventional spray painting gun",
    specifications: [
      { label: "PAINT NOZZLE", value: "1.4, 1.6, 1.8" },
      { label: "AIR PRESSURE RECOMMENDED", value: "4 BAR" },
      { label: "AIR CONSUMPTION", value: "250 – 700 L/MIN" },
      { label: "TYPICAL FAN PATTERN", value: "350 MM" },
      { label: "AIR INLET", value: '1/4" BSP' },
      { label: "MATERIAL INLET PORT", value: 'GRAVITY CUP 1/4" BSP (600 ML)' },
      { label: "GUN BODY", value: "ALUMINIUM PRESSURE DIE CAST" },
    ],
  },
  {
    id: "kingfisher-blue",
    name: "KINGFISHER BLUE",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/BLue (1).png",
    alt: "Kingfisher Blue conventional spray painting gun",
    specifications: [
      { label: "PAINT NOZZLE", value: "1.2, 1.4, 1.6, 1.8" },
      { label: "AIR PRESSURE RECOMMENDED", value: "4 BAR" },
      { label: "AIR CONSUMPTION", value: "250 – 700 L/MIN" },
      { label: "TYPICAL FAN PATTERN", value: "50 TO 250 MM" },
      { label: "AIR INLET", value: '1/4" BSP' },
      { label: "MATERIAL INLET PORT", value: 'GRAVITY CUP 1/4" BSP (600 ML)' },
      { label: "GUN BODY", value: "LIGHT ALUMINIUM FORGED" },
    ],
  },
  {
    id: "kingfisher-gold",
    name: "KINGFISHER GOLD",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Kingfisher gold gun.jpg",
    alt: "Kingfisher Gold conventional spray painting gun",
    specifications: [
      { label: "PAINT NOZZLE", value: "0.8, 1.0, 1.2" },
      { label: "AIR PRESSURE RECOMMENDED", value: "4 BAR" },
      { label: "AIR CONSUMPTION", value: "250 – 700 L/MIN" },
      { label: "TYPICAL FAN PATTERN", value: "50 TO 250 MM" },
      { label: "AIR INLET", value: '1/4" BSP' },
      { label: "MATERIAL INLET PORT", value: 'PRESSURE FEED POT 3/8" BSP' },
      { label: "GUN BODY", value: "LIGHT ALUMINIUM FORGED" },
    ],
  },
  {
    id: "kingfisher-red",
    name: "KINGFISHER RED",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Red (1).png",
    alt: "Kingfisher Red conventional spray painting gun",
    specifications: [
      { label: "PAINT NOZZLE", value: "0.8, 1.0, 1.2" },
      { label: "AIR PRESSURE RECOMMENDED", value: "4 BAR" },
      { label: "AIR CONSUMPTION", value: "250 – 700 L/MIN" },
      { label: "TYPICAL FAN PATTERN", value: "50 TO 250 MM" },
      { label: "AIR INLET", value: '1/4" BSP' },
      { label: "MATERIAL INLET PORT", value: 'PRESSURE FEED POT 3/8" BSP' },
      { label: "GUN BODY", value: "LIGHT ALUMINIUM FORGED ANODIZED" },
    ],
  },
];

export const conventionalGunCatalogue = {
  name: "CONVENTIONAL SPRAY PAINTING GUN",
  category: "Spray Painting Guns / Conventional Guns",
  catalogue: "/Catalogue/CONVENTIONAL GUNS_f.pdf",
  description:
    "The Kingfisher family of conventional spray painting guns delivers reliable finish quality for industrial coating applications. Each variant is engineered for specific coating viscosities and finish requirements.",
};
