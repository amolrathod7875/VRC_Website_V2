export type AutomaticGunSpec = {
  label: string;
  value: string;
};

export type AutomaticGunProduct = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: AutomaticGunSpec[];
  description?: string;
};

export const automaticGunProducts: AutomaticGunProduct[] = [
  {
    id: "vria-ss",
    name: "AUTOMATIC AIRLESS SPRAY GUN (VRIA) STAINLESS STEEL",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic airless spray gun VRIA SS.jpg",
    alt: "VRIA stainless steel automatic airless spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "450 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR (SPRING RETURN)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "M18 X 1 (M)" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "400b",
    name: "AUTOMATIC AIRLESS SPRAY GUN (400B) ALUMINIUM",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/400B .jpg",
    alt: "400B aluminium automatic airless spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "400 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 2 BAR" },
      { label: "INLET/CIRCULATION PORTS", value: '1/8" BSP' },
      { label: "TIP CONNECTION", value: "11/16 - UNF" },
      { label: "WETTED PARTS", value: "Aluminium, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "vriad-ss",
    name: "AUTOMATIC DISPENSING GUN VRIAD (STAINLESS STEEL)",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic Dispensing gun VRIAD.jpg",
    alt: "VRIAD stainless steel automatic dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "350 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR (SPRING RETURN)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "M18 X 1.5 (M)" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide seat, PTFE" },
    ],
    description: "*MORE PRESSURE ON REQUEST",
  },
  {
    id: "vria-aluminium",
    name: "AUTOMATIC AIRLESS SPRAY GUN (VRIA) ALUMINIUM",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic airless spray gun VRIA Alu.jpg",
    alt: "VRIA aluminium automatic airless spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "250 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR (SPRING RETURN)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "M18 X 1 (M)" },
      { label: "WETTED PARTS", value: "Aluminium, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "vriad-aluminium",
    name: "AUTOMATIC DISPENSING GUN VRIAD (ALUMINIUM)",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic Dispensing gun VRIAD.jpg",
    alt: "VRIAD aluminium automatic dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "200 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR (SPRING RETURN)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "M18 X 1.5 (M)" },
      { label: "WETTED PARTS", value: "Aluminium, Tungsten Carbide needle, PTFE" },
    ],
    description: "*MORE PRESSURE ON REQUEST",
  },
  {
    id: "flamingo-auto",
    name: "AUTOMATIC AIR ASSISTED AIRLESS SPRAY GUN (FLAMINGO)",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic air assisted airless spray gun.jpg",
    alt: "Flamingo automatic air assisted airless spray gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "250 BARS" },
      { label: "INLET PORTS", value: '1/4" BSP (M)' },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR" },
      { label: "WETTED PARTS", value: "304 Stainless steel, Tungsten Carbide seat, PTFE" },
    ],
  },
  {
    id: "hotmelt",
    name: "HOTMELT DISPENSING GUN",
    image: "/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Holt melt Gun.jpg",
    alt: "Hotmelt dispensing gun",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "200 BARS" },
      { label: "SWITCHING AIR INLET PRESSURE", value: "MINIMUM 4 BAR (SPRING RETURN)" },
      { label: "INLET/CIRCULATION PORTS", value: '1/4" BSP (F)' },
      { label: "TIP CONNECTION", value: "M18 X 1.5 (M)" },
      { label: "WETTED PARTS", value: "Aluminium, Tungsten Carbide needle, PTFE" },
    ],
    description: "*MORE PRESSURE ON REQUEST",
  },
];

export const automaticGunCatalogue = {
  name: "AUTOMATIC SPRAY PAINTING GUNS",
  category: "Spray Painting Guns / Automatic Guns",
  catalogue: "/media/catalogues/AUTOMATIC_gun.pdf",
  description:
    "The Automatic Spray Painting Guns catalogue covers automatic airless spray guns, dispensing guns, air assisted spray guns, and hotmelt dispensing guns for high-volume industrial coating lines.",
};
