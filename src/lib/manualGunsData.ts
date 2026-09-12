export type ManualGunSpec = {
  label: string;
  value: string;
};

export type ManualGunProduct = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: ManualGunSpec[];
  description?: string;
};

export const manualGunProducts: ManualGunProduct[] = [
  {
    id: "am250",
    name: "AIRLESS MANUAL SPRAY GUN AM250",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/AM250 gun.jpg",
    alt: "AM250 airless manual spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "250 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "TIP CONNECTION", value: "M18 X 1 (M)" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Aluminium, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "vril",
    name: "AIRLESS MANUAL SPRAY GUN VRIL",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/airless manual spray gun VRIL.jpg",
    alt: "VRIL airless manual spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "TIP CONNECTION", value: "M18 X 1" },
      { label: "WETTED PARTS VRIL", value: "304 Stainless steel, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "falcon",
    name: "AIRLESS MANUAL SPRAY GUN FALCON",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Falcon gun.jpg",
    alt: "Falcon airless manual spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR(SS), 350 BAR(AL)" },
      { label: "INLET PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "7/8\" UNF" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Aluminium, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "flamingo",
    name: "AIRLESS AIR ASSISTED SPRAY GUN (FLAMINGO)",
    image: "/Product_png_s/Flamingo 11817.png",
    alt: "Flamingo airless air assisted spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "250 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "TIP CONNECTION", value: "6 BAR" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "eagle",
    name: "AIRLESS MANUAL SPRAY GUN EAGLE",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Eagle gun.jpg",
    alt: "Eagle airless manual spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "500 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "7/8\"UNF" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "wax-spray-gun",
    name: "WAX SPRAY GUN",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/wax gun.jpg",
    alt: "Wax spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "WETTED PARTS", value: "304 Stainless steel, Aluminium, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "pole-gun",
    name: "POLE GUN",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Pole Gun 14422 (1).jpg",
    alt: "Pole gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "2345 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "TIP CONNECTION", value: "M18 X 1 (M)" },
      { label: "WETTED PARTS VRIL", value: "304 Stainless steel, Aluminium, Tungsten Carbide valve, PTFE" },
      { label: "STANDARD SIZE", value: "1 METER LONG" },
      { label: "NOTE", value: "*Other length on request" },
    ],
  },
  {
    id: "vrid",
    name: "AIRLESS MANUAL DISPENSING GUN VRID",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Airless manual dispensing gun.jpg",
    alt: "VRID airless manual dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "325 BAR/150 BAR" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "TIP CONNECTION", value: "M18 X 1 (M)" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Aluminium, Tungsten Carbide valve, PTFE" },
      { label: "NOTE", value: "*Other length on request" },
    ],
  },
  {
    id: "hawk-350",
    name: "DISPENSING GUN HAWK",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/VRC HAWK 8156 (1).jpg",
    alt: "Hawk dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 BAR" },
      { label: "INLET PORTS", value: '3/8" BSP' },
      { label: "TIP CONNECTION", value: "M18 X 1.5" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "extrusion-gun",
    name: "EXTRUSION GUN (EXT- I)",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/EXT Gun.jpg",
    alt: "Extrusion gun EXT-I",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BAR" },
      { label: "INLET PORTS", value: '3/8" BSP' },
      { label: "TIP CONNECTION", value: "M18 X 1.5 (M)" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide valve, PTFE" },
    ],
  },
  {
    id: "cartridge-dispensing-gun",
    name: "CARTRIDGE DISPENSING GUN",
    image: "/Product_png_s/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Cartridge Gun.jpg",
    alt: "Cartridge dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "6 BAR" },
      { label: "AIR PORTS", value: '1/4" BSP (M)' },
    ],
  },
];

export const manualGunCatalogue = {
  name: "MANUAL SPRAY PAINTING GUNS",
  category: "Spray Painting Guns / Manual Guns",
  catalogue: "/Catalogue/manual_GUNS.pdf",
  description:
    "The Manual Spray Painting Guns catalogue covers airless manual spray guns, dispensing guns, wax spray guns, pole guns, and extrusion guns for precision coating applications.",
};
