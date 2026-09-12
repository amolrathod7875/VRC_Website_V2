export type NavItem = {
  label: string;
  href: string;
  children?: { label: string; href: string }[];
};

export type Application = {
  slug: string;
  name: string;
  text: string;
  icon: React.FC<IconProps>;
  image?: string;
  video?: string;
};

export const navItems: NavItem[] = [
  { label: "Home", href: "/" },
{ label: "About", href: "/about" },
  { label: "Products", href: "/products" },
  { label: "Applications", href: "/applications" },
  {
    label: "Our Assets",
    href: "/assets/clients",
    children: [
      { label: "Partners", href: "/assets/partners" },
      { label: "Clients", href: "/assets/clients" },
      { label: "Industries We Serve", href: "/assets/industries" },
    ],
  },
  {
    label: "Resources",
    href: "/resources/blog",
    children: [
      { label: "Blog", href: "/resources/blog" },
      { label: "Certifications", href: "/resources/certifications" },
      { label: "Career", href: "/resources/career" },
      { label: "FAQs", href: "/resources/faqs" },
    ],
  },
  { label: "Catalog", href: "/catalog" },
  { label: "Contact Us", href: "/contact" },
];

export const offices = [
  {
    title: "Head Office",
    lines: [
      "V R Coatings Pvt. Ltd.",
      "J - 138, Bhosari Industrial Area",
      "Bhosari, Pune - 411 026, Maharashtra, India",
    ],
    phone: "+91 8237086924",
    phoneHref: "tel:+918237086924",
  },
  {
    title: "Factory",
    lines: [
      "V R Coatings Pvt. Ltd.",
      "Sector No. 7, Plot No. 136",
      "PCNTDA Industrial Area, Bhosari, Pune - 411 026, Maharashtra, India",
    ],
    phone: "+91 8237086903",
    phoneHref: "tel:+918237086903",
  },
  {
    title: "North America",
    lines: [
      "V R Coatings (North America) Ltd.",
      "648, Welham Rd, Barrie",
      "Ontario L4N 9A1, Canada",
    ],
    phone: "+1-705-739-0609",
    phoneHref: "tel:+17057390609",
  },
  {
    title: "Wai MIDC",
    lines: [
      "V R Coatings Pvt. Ltd.",
      "D-91, Wai MIDC, Unnamed Road",
      "Maharashtra Industrial Development Corporation, Lohare, Wai Rural, Maharashtra - 412803, India",
    ],
    phone: "",
    phoneHref: "",
  },
];

export const upcomingProducts = [
  {
    id: "up-1",
    title: "VR-Shield XT",
    tag: "Upcoming",
    summary:
      "Next-generation high-build epoxy for coastal infrastructure with extended salt-spray resistance.",
  },
  {
    id: "up-2",
    title: "ThermoGuard 900",
    tag: "Upcoming",
    summary:
      "High-temperature silicone coating engineered for exhaust systems, furnaces, and process equipment.",
  },
  {
    id: "up-3",
    title: "AeroClear E-Coat",
    tag: "Upcoming",
    summary:
      "Low-VOC electrocoat primer designed for aerospace and defence component lines.",
  },
];

export const solutions = [
  {
    title: "Protective Systems",
    text: "Multi-coat corrosion protection for steel structures, tanks, and process plants.",
  },
  {
    title: "Industrial Finishes",
    text: "Durable powder and liquid finishes for OEM parts with consistent colour and film build.",
  },
  {
    title: "Specialty Coatings",
    text: "Chemical, thermal, and dielectric solutions for demanding operating environments.",
  },
];

export const featuredProducts = [
  { slug: "vr-epoxy-510", name: "VR Epoxy 510", category: "Protective" },
  { slug: "vr-pu-720", name: "VR PU 720", category: "Protective" },
  { slug: "vr-powder-arch", name: "VR Powder Architectural", category: "Powder" },
  { slug: "vr-zinc-prime", name: "VR Zinc Prime 90", category: "Primers" },
  { slug: "vr-marine-hs", name: "VR Marine HS", category: "Marine" },
  { slug: "vr-dielectric", name: "VR Dielectric 40", category: "Electronics" },
];

export type LandingProduct = {
  slug: string;
  name: string;
  category?: string;
  description: string;
  catalogue?: string;
  image?: string | null;
  overview?: string;
  features?: string[];
  specs?: { label: string; value: string }[];
  applications?: string[];
};

export const landingProducts: LandingProduct[] = [
  {
    slug: "barrel-pump",
    name: "Barrel Pump",
    description: "Pneumatically operated transfer pump for extracting paint and viscous fluids from 200L steel drums and 210L plastic barrels with minimal waste.",
    catalogue: "/Catalogue/Barrel Pump.pdf",
    image: "/Product_png_s/Category_wise_products/Barrel Pump/Barrel Transfer Pump 14419.jpg",
    overview: "The Barrel Pump is a pneumatically operated transfer pump designed for extracting paint and viscous fluids from 200L steel drums and 210L plastic barrels with minimal waste. Available in four variants with pressure ratios from 4:1 to 60:1, providing output pressures up to 360 bar at 6 bar air inlet.",
    features: [
      "Pneumatically operated transfer pump for 200L steel drums and 210L plastic barrels",
      "Pressure ratio variants from 4:1 to 60:1",
      "Stainless steel rust-proof hydraulic body",
      "Four-foot ram pump with follower plate for minimal waste",
      "Easy maintenance and cleaning",
      "Durable and rugged design for industrial use",
    ],
    specs: [
      { label: "System Type", value: "Pneumatic Barrel Transfer Pump" },
      { label: "Pressure Ratio", value: "4:1 to 60:1 (4 variants)" },
      { label: "Max Output Pressure", value: "Up to 360 bar @ 6 bar air inlet" },
      { label: "Discharge Per Cycle", value: "230 cc" },
      { label: "Air Motor Piston Diameter", value: "80, 100, 125, 160 mm" },
      { label: "Stroke Length", value: "120 mm" },
      { label: "Max Inlet Air Pressure", value: "6 bar" },
      { label: "Air Consumption", value: "127 to 506 N-LPM @ 15 cycles/min" },
    ],
    applications: [
      "200L steel drum paint extraction",
      "210L plastic barrel transfer",
      "Viscous fluid transfer from containers",
      "Industrial paint and coating supply",
    ],
  },
  {
    slug: "cheetah",
    name: "CHEETAH",
    description: "Two-Component Hot Airless Spray Painting Equipment designed for tough working conditions, suitable for two-component high viscosity, solventless coating, semi-solid coating, marine coating, and all types of protective coatings.",
    catalogue: "/Catalogue/Cheetah.pdf",
    image: "/Product_png_s/Category_wise_products/Cheetah/Cheetah 14301.jpg",
    overview: "The CHEETAH is a two-component hot airless spray painting equipment range designed for tough working conditions. It is suitable for two-component high viscosity, solventless coating, semi-solid coating, marine coating, and all types of protective coatings.",
    features: [
      "Pneumatically sensed high-performance air motor",
      "High discharge flow rates",
      "Stainless steel hydraulic body",
      "Easy maintenance",
      "Ice-free air motor technology",
      "Easy to operate mounted on a robust trolley/stand",
      "Fixed volume mixing ratio",
      "Modular design to achieve various mixing ratios",
      "Online ratio monitoring",
      "Electrically heated oil-jacketed tank",
    ],
    specs: [
      { label: "Mixing Ratio", value: "1:1, 1.4:1, 2:1, 2.6:1, 3:1, 4:1" },
      { label: "Transfer Ratio", value: "45:1, 55:1, 65:1, 55:1, 45:1, 35:1" },
      { label: "Pump Combination", value: "110×110/230, 110×110/161, 110×110/110, 100×100/155, 230×110/110, 230×230/110" },
      { label: "Discharge per Cycle", value: "450, 385, 330, 352, 450, 570 cc" },
      { label: "Air Motor Piston", value: "350" },
      { label: "Recommended Volume @ 15 cycles/min", value: "6.7, 3.5, 3.3, 3.5, 6.75, 8.55 L/min" },
      { label: "Air Inlet Pressure (Max)", value: "270, 330, 390, 330, 270, 210 bar" },
      { label: "Air Consumption @ 6 bar, 15 cycles/min", value: "85.6 CFM" },
    ],
    applications: [
      "High-Performance 2K Spray System",
      "Spraying challenging materials like solventless epoxy and polyurethane",
      "High-pressure two-component (2K) paint applications with precise ratio control",
    ],
  },
  {
    slug: "cub",
    name: "Cub",
    description: "Four-ball piston transfer pump with 100:1 pressure ratio for high-pressure fluid transfer.",
    catalogue: "/Catalogue/cub.pdf",
    image: "/Product_png_s/Category_wise_products/Cub/Cub pump.jpg",
    overview: "The CUB is a four-ball piston transfer pump with a 100:1 pressure ratio, designed for high-pressure transfer of paints, coatings, and viscous fluids. Delivers up to 4.2 LPM at 600 BAR maximum working pressure.",
    features: [
      "100:1 pressure ratio",
      "600 BAR (8700 psi) max working pressure",
      "Up to 4.2 LPM flow rate",
      "Four-ball piston technology",
      "304 SS / 316 SS / PTFE / Tungsten Carbide wetted parts",
      "In-built 5 micron filtration system",
      "Air-operated — safe for hazardous areas",
      "Compact and portable design",
    ],
    specs: [
      { label: "Pump Type", value: "Four-Ball Piston" },
      { label: "Pressure Ratio", value: "100:1" },
      { label: "Max Working Pressure", value: "600 BAR (8700 psi)" },
      { label: "Flow Rate", value: "Up to 4.2 LPM" },
      { label: "Air Supply", value: "6–8 bar" },
      { label: "Fluid Inlet", value: "1\" BSP" },
      { label: "Fluid Outlet", value: "3/8\" BSP" },
      { label: "Wetted Parts", value: "304 SS / 316 SS / PTFE / Tungsten Carbide" },
      { label: "Weight", value: "55 kg" },
      { label: "Dimensions", value: "900 × 450 × 550 mm" },
    ],
    applications: [
      "High-pressure fluid transfer",
      "Paint and coating supply to spray guns",
      "Transfer from drums and containers",
      "High-pressure circulation systems",
    ],
  },
  {
    slug: "diaphragm-pump",
    name: "Diaphragm Pump",
    description: "Air-operated double diaphragm pump for low-pressure transfer of paints, coatings, chemicals, and water-based materials.",
    catalogue: "/Catalogue/pulsing dampner.pdf",
    image: "/Product_png_s/Category_wise_products/Diaphragm Pump/Diaphragm pump.jpg",
    overview: "Air-operated double diaphragm pump for low-pressure transfer of paints, coatings, chemicals, and water-based materials. Available in 1:1 and 2:1 pressure ratios. Handles corrosive and abrasive fluids with PTFE/Santropen/FKM diaphragms.",
    features: [
      "Double diaphragm design for smooth, pulse-free flow",
      "Self-priming — can run dry without damage",
      "Variable flow via air pressure regulation",
      "Handles abrasive and corrosive fluids",
      "No heat buildup",
      "BF-PTFE diaphragms available for hot materials",
      "Diaphragm Type: PTFE / Santropen / FKM",
    ],
    specs: [
      { label: "Type", value: "Air-Operated Double Diaphragm" },
      { label: "Pressure Ratio", value: "1:1 (standard), 2:1 (high pressure variant)" },
      { label: "Max Flow Rate", value: "4.2 LPM (252 L/h)" },
      { label: "Operating Pressure", value: "0.4–0.6 MPa (4–6 bar)" },
      { label: "Fluid Port", value: "1/2\"" },
      { label: "Wetted Parts", value: "304 Stainless Steel / PTFE / EPDM / FKM" },
      { label: "Temperature Range", value: "-20°C to +135°C (T4 rating)" },
    ],
    applications: [
      "Water-based paint transfer",
      "Solvent-based coating transfer",
      "Chemical dosing and transfer",
      "Adhesive and sealant dispensing",
      "Ink transfer",
      "Low-pressure circulation systems",
    ],
  },
  {
    slug: "drum-press",
    name: "DRUM PRESS",
    description: "Pneumatic drum press dispensing system for extracting paint and coatings from 200L drums.",
    catalogue: "/Catalogue/DRUM PRESS.pdf",
    image: "/Product_png_s/Drum press1.png",
    overview: "The DRUM PRESS is a pneumatic drum press dispensing system for extracting and dispensing paint, coatings, and sealants from 200L drums. Features a pneumatic follow plate system with 5L to 200L capacity range and 5\" and 8\" ram options.",
    features: [
      "Pneumatic operation — safe for hazardous areas",
      "Five-liter to 200-liter capacity range",
      "Follow plate system for minimum waste",
      "5\" and 8\" ram standard options",
      "Corrosion-resistant SS304 wetted parts",
      "Compatible with HIPPO, TIGER, Rhino, and CUB pumps",
    ],
    specs: [
      { label: "Pressure Type", value: "Pneumatic" },
      { label: "Fluid Volume", value: "5L to 200L" },
      { label: "Ram Size", value: "5\" and 8\" (standard)" },
      { label: "Air Supply", value: "6–8 bar" },
      { label: "Follow Plate", value: "Pneumatic, SS304" },
      { label: "Max Working Pressure", value: "8 BAR (116 psi)" },
      { label: "Weight", value: "35 kg (approx)" },
    ],
    applications: [
      "200L drum paint extraction",
      "Coating dispensing from drums",
      "Sealant and adhesive dispensing",
      "Continuous production feeding",
      "Industrial paint supply systems",
    ],
  },
  {
    slug: "elephant-pump",
    name: "Elephant Pump",
    description: "High-volume, low-pressure transfer pump for efficient supply of paints, coatings, and viscous fluids.",
    catalogue: "/Catalogue/Elephant.pdf",
    image: "/Product_png_s/Category_wise_products/Elephant Pump/Elephant 14398.jpg",
    overview: "The ELEPHANT is a high-volume, low-pressure transfer pump designed for efficient supply of paints, coatings, and viscous fluids to spray systems. Features a 2:1 pressure ratio, up to 60 LPM flow rate, and handles viscosities up to 2,000 Cp.",
    features: [
      "60 LPM max flow rate — high-volume transfer",
      "Low-pressure operation at 40 BAR",
      "2:1 pressure ratio",
      "Handles viscosities up to 2,000 Cp",
      "304 SS wetted parts — corrosion resistant",
      "Air-operated — safe for ATEX zones",
      "Compatible with HIPPO, TIGER, RHINO, DRAGON systems",
    ],
    specs: [
      { label: "Pump Type", value: "Transfer Pump" },
      { label: "Pressure Ratio", value: "2:1" },
      { label: "Max Working Pressure", value: "40 BAR (580 psi)" },
      { label: "Max Flow Rate", value: "Up to 60 LPM" },
      { label: "Viscosity Handling", value: "Up to 2,000 Centipoise" },
      { label: "Air Supply", value: "6–8 bar, 1,200 Nl/min" },
      { label: "Fluid Inlet", value: "1\" BSP" },
      { label: "Fluid Outlet", value: "3/8\" BSP" },
      { label: "Wetted Parts", value: "304 SS / PTFE / Silicon" },
      { label: "Weight", value: "75 kg" },
      { label: "Dimensions", value: "1200 × 500 × 600 mm" },
    ],
    applications: [
      "High-volume paint transfer",
      "Coating supply to spray systems",
      "Drum to pump transfer",
      "Industrial circulation systems",
      "Multi-gun painting line feed",
    ],
  },
  {
    slug: "hippo-pump",
    name: "Hippo Pump",
    description: "Low-pressure transfer pump for reliable transfer of paints, coatings, and viscous fluids.",
    catalogue: "/Catalogue/Hippo.pdf",
    image: "/Product_png_s/Category_wise_products/Hippo Pump/Hippo 14311.jpg",
    overview: "The HIPPO is a low-pressure transfer pump designed for reliable transfer of paints, coatings, and viscous fluids. Available in piston type (pressure ratios 1:170, 3:400, 5:900, 12:400) and diaphragm type (1:1 ratio, 6 bar max). Features 304 stainless steel wetted parts with PTFE/Silicon sealing.",
    features: [
      "Available in piston type (4 pressure ratios) and diaphragm type (1:1 ratio)",
      "Low pressure operation — ideal for water-based and chemical fluids",
      "304 SS wetted parts — chemically resistant",
      "Air-operated — safe for hazardous areas",
      "T4 temperature rating (135°C) — handles hot materials",
    ],
    specs: [
      { label: "Piston Type Pressure Ratios", value: "1:170, 3:400, 5:900, 12:400" },
      { label: "Max Working Pressure (Piston)", value: "Up to 400 BAR (12:400 model)" },
      { label: "Diaphragm Type Ratio", value: "1:1" },
      { label: "Max Output Pressure (Diaphragm)", value: "6 bar" },
      { label: "Fluid Temperature (Diaphragm)", value: "T4 (135°C max)" },
      { label: "Air Consumption (Diaphragm)", value: "30 N-LPM" },
      { label: "Wetted Parts", value: "304 SS / PTFE / Silicon" },
      { label: "Weight", value: "50–55 kg" },
    ],
    applications: [
      "Paint and coating transfer",
      "Water-based material transfer",
      "Chemical fluid handling",
      "Low-pressure circulation systems",
    ],
  },
  {
    slug: "leopard-electric",
    name: "Leopard - Electric",
    description: "Electric pump system for paint and fluid transfer with dual heating elements and programmable temperature control.",
    catalogue: "/Catalogue/Electric_pump.pdf",
    image: "/Product_png_s/Category_wise_products/Leopard - ELECTRIC PUMP/Electric pump.jpg",
    overview: "The LEOPARD is an electric pump system for paint and fluid transfer. Motor-driven pump with dual heating elements and programmable temperature control. Available in 20L and 210L configurations for 200L barrels and 210L plastic containers. Features stainless steel construction, 2.2 KW motor, 0–40 BAR operating pressure, and built-in filtration.",
    features: [
      "Electric motor-driven — clean, quiet operation",
      "2.2 KW motor power",
      "0–40 BAR operating pressure",
      "Dual heating system with programmable temperature control",
      "20L and 210L configurations",
      "415V / 3-phase power supply",
      "In-built 5 micron filtration",
      "CE & ATEX certified",
    ],
    specs: [
      { label: "Motor Power", value: "2.2 KW" },
      { label: "Max Operating Pressure", value: "0–40 BAR" },
      { label: "Power Supply", value: "415V / 3-Phase" },
      { label: "Fluid Volume", value: "20L & 210L" },
      { label: "Fluid Inlet", value: "1\" BSP" },
      { label: "Fluid Outlet", value: "3/8\" BSP" },
      { label: "Wetted Parts", value: "304 SS / 316 SS / PTFE" },
      { label: "Filtration", value: "5 micron (in-built)" },
      { label: "Weight", value: "180 kg" },
    ],
    applications: [
      "Paint and coating transfer",
      "Fluid circulation systems",
      "Industrial mixing and transfer",
      "Temperature-controlled material delivery",
      "Automated paint systems",
    ],
  },
  {
    slug: "pfp-dragon",
    name: "PFP DRAGON",
    description: "Passive Fire Protection (PFP) spray system for high-build intumescent coatings.",
    catalogue: "/Catalogue/dragon.pdf",
    image: "/Product_png_s/Category_wise_products/PFP DRAGON/PFP 4017.jpg",
    overview: "The DRAGON system is a passive fire protection (PFP) spray system designed for the application of high-build intumescent coatings. Engineered for heavy-duty industrial use, it ensures reliable and uniform coating performance to enhance fire resistance and protect critical steel structures.",
    features: [
      "Passive fire protection system",
      "High-build intumescent coating application",
      "Working Pressure: 250 BAR (piston) / 400 BAR (diaphragm variant)",
      "Pressure Ratio: 1:170 (piston), 2:1 (diaphragm)",
      "Up to 6 LPM flow rate",
      "Dual heating with 15m heated hose bundle",
      "Automatic temperature control",
      "304 SS / 316 SS / PTFE / Tungsten Carbide wetted parts",
    ],
    specs: [
      { label: "System Type", value: "Passive Fire Protection (PFP)" },
      { label: "Working Pressure", value: "250 BAR (standard) / 400 BAR (variant)" },
      { label: "Pressure Ratio", value: "1:170 (piston), 2:1 (diaphragm)" },
      { label: "Max Flow Rate", value: "Up to 6 LPM" },
      { label: "Air Supply", value: "6–8 bar, 600 Nl/min" },
      { label: "Power Supply", value: "415V / 3-Phase" },
      { label: "Fluid Temperature", value: "-20°C to +70°C" },
      { label: "Wetted Parts", value: "304 SS / 316 SS / PTFE / Tungsten Carbide" },
    ],
    applications: [
      "Fire-resistant steel structures",
      "Oil & Gas industry",
      "Petrochemical facilities",
      "Infrastructure (bridges, buildings)",
      "Steel structure protection",
      "Offshore platforms",
    ],
  },
  {
    slug: "polyurea",
    name: "Polyurea",
    description: "Two-component hot airless polyurea spray equipment for high viscosity, solvent-less coating, waterproofing, PU foam and insulation coatings.",
    catalogue: "/Catalogue/polyurea.pdf",
    image: "/Product_png_s/Category_wise_products/Polyurea/Polyurea.jpg",
    overview:
      "The POLYUREA system is a two-component hot airless spray equipment designed for tough working conditions. It is suitable for two-component high viscosity, solvent-less coating, waterproofing coating, PU foam and insulation coatings. Compact mounted on a robust trolley with accurate fixed volume 1:1 mixing ratio, double 3KW heaters and a polyurea wrap suff heated hose bundle of 15 metres.",
    features: [
      "Two-component hot airless technology",
      "Accurate fixed volume mixing ratio 1:1",
      "Double 3KW heaters for uniform and consistent heating",
      "Polyurea wrap suff heated hose bundle 15 meter",
      "12V flat copper heating element hose for long term even heating without abrupt hot spots",
      "Standard up to 3 set of hose bundle can be attached",
      "Special ISO barrel transfer pump for smooth and leak proof transfer",
      "Compatible with air purge fusion gun as well as durable manual static mixture type spray gun",
      "Pressure monitored to cut off pump in case of ratio faults",
      "Inbuilt fluid temperature sensor at inlet and add on block provisions for extended hoses",
      "Stainless steel hydraulic body compatible with isocyanates",
      "High discharge flow rates",
      "Easy to operate, compact mounted on robust trolley",
    ],
    specs: [
      { label: "System Type", value: "Two-Component Hot Airless Polyurea Spray Equipment" },
      { label: "Mixing Ratio", value: "1:1 (fixed volume)" },
      { label: "Heating System", value: "Double 3KW heaters" },
      { label: "Heated Hose", value: "Polyurea wrap suff heated hose bundle 15 meter; 12V flat copper heating element hose" },
      { label: "Maximum Output Pressure", value: "300 BAR @ 6 bar air inlet" },
      { label: "Maximum Inlet Air Pressure", value: "6 bar" },
      { label: "Air Motor Piston Diameter", value: "250 mm / 300 mm" },
      { label: "Discharge Per Cycle", value: "226 cc / 310 cc" },
      { label: "Recommended Spray Volume", value: "2.26 lpm / 3.1 lpm @ 10 cycles/min" },
      { label: "Stroke Length", value: "120 mm" },
      { label: "CFM @ 6 bar @ 10 cycles", value: "825 / 1188" },
      { label: "Hose Bundles", value: "Standard up to 3 set of hose bundle can be attached" },
    ],
    applications: [
      "High-Performance Coating & Insulation System",
      "Spraying polyurea paints for durable floor coatings and protective layers",
      "Spraying and dispensing polyurethane foam for insulation and sealing applications",
    ],
  },
  {
    slug: "portable-pressure-feed-pot",
    name: "Pressure Feed Pot",
    description: "Portable stainless steel pressure vessel for transferring paint, oils and explosive liquids to spray guns.",
    catalogue: "/Catalogue/PORTABLE PRESSURE FEED POT.pdf",
    image: "/Product_png_s/Category_wise_products/Pressure Feed Pot/VRC 4295 (1).jpg",
    overview:
      "The Pressure Feed Pot is a portable stainless steel pressure vessel suitable for transferring paint, oils, and explosive liquids. It is designed for single gun use and serves as a substitute for the suction pot and gravity pot of the spray gun.",
    features: [
      "Suitable for transferring paints, oils and explosive liquids",
      "Suitable for single gun",
      "Stainless steel rust proof pot",
      "Clamping arrangement with PTFE Gasket to avoid jamming due to Two Component Paints",
      "Safety valve to evacuate excess pressure",
      "Bend Outlet Tube in Nylon to use even last 20cc of paint",
      "Substitute for suction pot and gravity pot of the spray gun",
    ],
    specs: [
      { label: "Pot capacity", value: "2.5 ltrs Approx" },
      { label: "Max Working Pressure", value: "4 Bar" },
      { label: "Net Wt.", value: "3 Kg." },
      { label: "Pot Capacity Available", value: "2.5 ltrs, 5 ltrs, 10 ltrs, 20 ltrs, 40 ltrs" },
    ],
    applications: [
      "Transferring paint to spray guns",
      "Transferring oils",
      "Transferring explosive liquids",
    ],
  },
  {
    slug: "rhino-pump",
    name: "Rhino Pump",
    description: "Heavy-duty airless spray pump with 12:400 pressure ratio and 400 BAR max pressure.",
    catalogue: "/Catalogue/rhino.pdf",
    image: "/Product_png_s/Category_wise_products/Rhino Pump/Rhino 4040.jpg",
    overview: "The RHINO is a heavy-duty airless spray pump system designed for large-scale industrial coating applications. Features a 12:400 pressure ratio, 400 BAR max working pressure, 15 LPM flow rate, and 4.0 KW air motor. Equipped with dual 3KW heaters and 15m heated hose bundle.",
    features: [
      "400 BAR (5800 psi) max working pressure",
      "12:400 pressure ratio — highest in range",
      "15 LPM high flow rate",
      "4.0 KW air motor for powerful operation",
      "Dual 3KW heaters with 15m heated hose bundle",
      "Automatic temperature control",
      "100 mesh inlet / 40 mesh outlet filtration",
      "304 SS / 316 SS / PTFE / Tungsten Carbide wetted parts",
      "Compatible with all VR Coatings spray guns",
    ],
    specs: [
      { label: "Pump Type", value: "Airless, Piston" },
      { label: "Pressure Ratio", value: "12:400" },
      { label: "Max Working Pressure", value: "400 BAR (5800 psi)" },
      { label: "Max Flow Rate", value: "15 LPM" },
      { label: "Air Motor", value: "4.0 KW" },
      { label: "Power Supply", value: "415V / 3-Phase" },
      { label: "Air Supply", value: "6–8 bar, 800 Nl/min" },
      { label: "Heating System", value: "Dual 3KW heaters" },
      { label: "Heated Hose", value: "15m bundle" },
      { label: "Wetted Parts", value: "304 SS / 316 SS / PTFE / Tungsten Carbide" },
      { label: "Weight", value: "220 kg" },
      { label: "Dimensions", value: "1400 × 600 × 900 mm" },
    ],
    applications: [
      "Large-scale industrial coating",
      "Protective coating application on steel structures",
      "Marine and offshore coating",
      "Bridge and infrastructure coating",
      "High-volume paint application",
    ],
  },
  {
    slug: "spray-painting-guns",
    name: "Spray Painting Guns",
    description: "Comprehensive range of manual spray guns for airless and air-assisted spraying applications.",
    catalogue: "/Catalogue/manual_GUNS.pdf",
    image: "/Product_png_s/Flamingo 11817.png",
    overview: "VR Coatings offers a comprehensive range of manual spray guns for airless and air-assisted spraying applications. Pressure ratings from 250 to 500 BAR, with models for general finishing, heavy-duty applications, fine wood finishing, cavity waxing, and precision dispensing.",
    features: [
      "Pressure range: 250 BAR (AM250) to 500 BAR (EAGLE)",
      "Tungsten Carbide valve seats on all airless guns",
      "304 SS wetted parts for corrosion resistance",
      "Composite body option (AM250) for quick cleaning",
      "Air and paint controls for fine adjustment",
      "CE & ATEX certified throughout",
    ],
    specs: [
      { label: "Gun Models", value: "EAGLE (500 BAR), FALCON (450/350 BAR), VRIL (350 BAR), AM250 (250 BAR), FLAMINGO (250 BAR), POLE GUN (2345 BAR), WAX SPRAY (350 BAR), HAWK (350 BAR), EXT-1 (350 BAR)" },
      { label: "Body Materials", value: "304 Stainless Steel, Aluminium, Aluminium Forged" },
      { label: "Tip Connections", value: "7/8\" UNF, M18×1" },
      { label: "Air Inlet", value: "¼\" BSP" },
    ],
    applications: [
      "Structural and protective coatings",
      "General purpose spraying",
      "Fine wood finishing and furniture",
      "Cavity waxing and underbody",
      "Painting at height / internal pipe coating",
      "Precision sealant/adhesive dispensing",
      "High-viscosity extrusion",
    ],
  },
  {
    slug: "tiger-mini",
    name: "Tiger Mini",
    description: "Air-assisted airless spray pump system for fine finish and medium-duty applications.",
    catalogue: "/Catalogue/Tiger_mini.pdf",
    image: "/Product_png_s/Category_wise_products/Tiger Mini/VRC 4101.jpg",
    overview: "The MINI TIGER is an air-assisted airless spray pump system for fine finish and medium-duty applications. Features a 2:150 pressure ratio, 150 BAR working pressure, and 4.2 LPM flow rate. Designed for use with the FLAMINGO air-assisted airless spray gun.",
    features: [
      "150 BAR working pressure — air-assisted airless system",
      "2:150 pressure ratio",
      "4.2 LPM flow rate",
      "Dual 3KW heaters with automatic temperature control",
      "304 SS wetted parts — chemically compatible",
      "Compatible gun: FLAMINGO",
      "CE & ATEX certified",
      "Compact design for workshop use",
    ],
    specs: [
      { label: "Pump Type", value: "Air-Assisted Airless" },
      { label: "Pressure Ratio", value: "2:150" },
      { label: "Max Working Pressure", value: "150 BAR (2175 psi)" },
      { label: "Max Flow Rate", value: "4.2 LPM" },
      { label: "Air Supply", value: "6–8 bar, 600 Nl/min" },
      { label: "Power Supply", value: "415V / 3-Phase" },
      { label: "Heating System", value: "Dual 3KW heaters" },
      { label: "Compatible Gun", value: "FLAMINGO (air-assisted airless)" },
      { label: "Wetted Parts", value: "304 SS / PTFE" },
      { label: "Weight", value: "110 kg" },
    ],
    applications: [
      "Fine finish airless spraying",
      "Wood finishing and furniture",
      "Lacquer application",
      "Medium production lines",
      "High-quality finish coat application",
    ],
  },
  {
    slug: "tiger-pump",
    name: "Tiger Pump",
    description: "Low to medium-duty airless spray pump with 2:150 pressure ratio and up to 2 spray guns support.",
    catalogue: "/Catalogue/Tiger.pdf",
    image: "/Product_png_s/Category_wise_products/Tiger Pump/Tiger 14326.jpg",
    overview: "The TIGER is a low to medium-duty airless spray pump system for industrial coating applications. Features a 2:150 pressure ratio, 150 BAR max working pressure, 4.2 LPM flow rate, and 2.2 KW air motor. Compatible with up to 2 spray guns.",
    features: [
      "150 BAR (2175 psi) working pressure — medium-duty airless",
      "2:150 pressure ratio",
      "4.2 LPM max flow rate",
      "Supports up to 2 spray guns",
      "2.2 KW air motor",
      "304 SS wetted parts — chemically compatible",
      "100 mesh filtration",
      "CE & ATEX certified",
    ],
    specs: [
      { label: "Pump Type", value: "Airless, Piston" },
      { label: "Pressure Ratio", value: "2:150" },
      { label: "Max Working Pressure", value: "150 BAR (2175 psi)" },
      { label: "Max Flow Rate", value: "4.2 LPM" },
      { label: "Guns Supported", value: "Up to 2 spray guns" },
      { label: "Air Supply", value: "6–8 bar, 600 Nl/min" },
      { label: "Air Motor", value: "2.2 KW" },
      { label: "Power Supply", value: "415V / 3-Phase" },
      { label: "Wetted Parts", value: "304 SS / PTFE" },
      { label: "Weight", value: "120 kg" },
      { label: "Dimensions", value: "1000 × 450 × 650 mm" },
    ],
    applications: [
      "Medium-duty industrial spraying",
      "Paint and coating application",
      "Primer and finish coat spraying",
      "Compatible with manual and automatic spray guns",
    ],
  },
  {
    slug: "turbine-stirrer",
    name: "Turbine Stirrer",
    description: "Air-operated turbine agitation system for paint mixing, circulation, and material preparation.",
    catalogue: "/Catalogue/turbine.pdf",
    image: "/Product_png_s/Category_wise_products/Turbine Stirrer/Turbinr Stirrer.jpg",
    overview: "VR Coatings Turbine Stirrers are air-operated agitation systems for paint mixing, circulation, and material preparation. Available in three tank sizes: TB-70 (70L), TB-110 (110L), and TB-180 (180L). Features 6-blade turbine impellers and 304 stainless steel wetted parts.",
    features: [
      "Three tank sizes: TB-70, TB-110, TB-180",
      "6-blade turbine impellers for efficient mixing",
      "0–1400 RPM variable speed control",
      "304 SS wetted parts — chemically compatible",
      "Air-operated — safe for hazardous areas",
      "Compatible with HIPPO, ELEPHANT, TIGER, RHINO systems",
      "CE & ATEX certified",
    ],
    specs: [
      { label: "Tank Capacity", value: "TB-70: 70L, TB-110: 110L, TB-180: 180L" },
      { label: "Speed", value: "0–1400 RPM" },
      { label: "Air Supply", value: "6 bar" },
      { label: "Wetted Parts", value: "304 Stainless Steel" },
      { label: "Impeller", value: "6-blade turbine (200mm, 250mm, 300mm)" },
      { label: "Power", value: "2.2–5.5 KW (depending on size)" },
    ],
    applications: [
      "Paint mixing and homogenisation",
      "Viscosity adjustment",
      "Solid particle suspension",
      "Temperature control circulation",
      "Tank agitation for spray systems",
    ],
  },
  {
    slug: "vrc-mix-hp",
    name: "VRC MIX HP",
    description: "Electronic variable ratio 2K mixing system for high-pressure spray applications at 450 bar.",
    catalogue: "/Catalogue/VRC - MIX HP.pdf",
    image: "/Product_png_s/Category_wise_products/VRC MIX HP/VRCoatings 0964.jpg",
    overview: "The VRC-MIX HP is an electronic two-component mixing system with variable ratio control for high-pressure spray applications. Features 450 bar max working pressure, adjustable mix ratio up to 10.0:1 in 0.1 increments, 240V AC single-phase power supply, and RS 232 + Modbus communication.",
    features: [
      "Electronic variable ratio 2K mixing system",
      "450 bar max working pressure",
      "Variable mix ratio up to 10.0:1 in 0.1 increments",
      "240V AC 50Hz single phase power supply",
      "RS 232 + Modbus communication interface",
      "Touch screen and hardware key control",
      "Audio and visual alarms with auto shut-off",
      "Flow rate 6.8 L/min",
      "Air supply 4-7 bar",
    ],
    specs: [
      { label: "System Type", value: "2-Component Electronic Mixing" },
      { label: "Max Working Pressure", value: "450 BAR" },
      { label: "Power Supply", value: "240V AC 50Hz Single Phase" },
      { label: "Air Supply", value: "4-7 bar" },
      { label: "Flow Rate", value: "6.8 L/min" },
      { label: "Communication", value: "RS 232 + Modbus" },
      { label: "Control System", value: "Touch screen + hardware key" },
      { label: "Alarms", value: "Audio + Visual with auto shut-off" },
    ],
    applications: [
      "All types of two component paints with moderate pot life",
    ],
  },
  {
    slug: "vrc-mix-lp",
    name: "VRC MIX LP",
    description: "Variable ratio electronic 2K mixing system for low to medium pressure spray at 30 bar.",
    catalogue: "/Catalogue/VRC MIX (LOW-MEDIUM) PRESSURE.pdf",
    image: "/Product_png_s/Category_wise_products/VRC MIX LP/VRC 4734.jpg",
    overview: "The VRC MIX (L/M) is a variable ratio electronic two-component mixing system designed for low to medium pressure spray applications. Features a 30 bar max working pressure, variable mixing ratio up to 15.0:1 in 0.1 increments, 230V AC single-phase power, and advanced alarm system with audio/visual alerts.",
    features: [
      "Electronic variable ratio 2K mixing system",
      "30 bar max working pressure (air spray system)",
      "Mixing ratio range up to 15.0 in 0.1 increments",
      "Accuracy tolerance down to 1% (user settable)",
      "Flow rate 0.1 to 4 liters per minute",
      "230V AC 50Hz single phase power supply",
      "Air pressure requirement 0-7 bars",
      "RS 232 + Modbus communication",
      "Touch screen graphical operator interface",
      "Audio + Visual alarms with auto shut-off",
      "Pot life monitoring",
      "Material usage reporting",
      "Online system health checking",
    ],
    specs: [
      { label: "System Type", value: "2-Component Electronic Mixing" },
      { label: "Max Working Pressure", value: "30 bar" },
      { label: "Mixing Ratio Range", value: "Up to 15.0 (in 0.1 increments)" },
      { label: "Accuracy Tolerance", value: "Down to 1% (user settable)" },
      { label: "Flow Rate", value: "0.1 to 4 liters per minute" },
      { label: "Air Pressure Requirement", value: "0-7 bars" },
      { label: "Power Supply", value: "230V AC 50Hz Single Phase" },
      { label: "Communication", value: "RS 232 + Modbus" },
      { label: "Control Interface", value: "Touch screen graphical display" },
      { label: "Alarm System", value: "Audio + Visual with auto shut-off" },
    ],
    applications: [
      "Two-component coating application (low/medium pressure)",
      "Colour, hardeners, solvents (modular system for different recipes)",
      "Colour change configuration and setup",
      "Auto flushing cycle with programmable sequential air/solvent purge",
    ],
  },
];

export type ProductNode = {
  slug: string;
  name: string;
  summary: string;
  catalogue?: string;
  children?: ProductNode[];
  image?: string | null;
};

export const productTree: ProductNode[] = [
  {
    slug: "protective-coatings",
    name: "Protective Coatings",
    summary: "High-performance systems for corrosion, abrasion, and chemical attack.",
    children: [
      {
        slug: "epoxy",
        name: "Epoxy Systems",
        summary: "High-build epoxies for tanks, structures, and industrial flooring.",
        children: [
          { slug: "vr-epoxy-510", name: "VR Epoxy 510", summary: "Surface-tolerant epoxy mastic for maintenance work." },
          { slug: "vr-epoxy-tank", name: "VR Epoxy Tank Lining", summary: "Solvent-free lining for chemical storage." },
        ],
      },
      {
        slug: "polyurethane",
        name: "Polyurethane Finishes",
        summary: "UV-stable topcoats with excellent gloss retention.",
        children: [
          { slug: "vr-pu-720", name: "VR PU 720", summary: "Aliphatic polyurethane for exterior steel." },
        ],
      },
      {
        slug: "zinc-primers",
        name: "Zinc-Rich Primers",
        summary: "Cathodic protection primers for blasted steel.",
        children: [
          { slug: "vr-zinc-prime", name: "VR Zinc Prime 90", summary: "Inorganic zinc silicate primer." },
        ],
      },
    ],
  },
  {
    slug: "powder-coatings",
    name: "Powder Coatings",
    summary: "Architectural and industrial powders with consistent film quality.",
    children: [
      {
        slug: "architectural",
        name: "Architectural",
        summary: "Weathering-grade powders for façades and aluminium profiles.",
        children: [
          { slug: "vr-powder-arch", name: "VR Powder Architectural", summary: "AAMA-aligned architectural powder range." },
        ],
      },
      {
        slug: "industrial-powder",
        name: "Industrial",
        summary: "Functional powders for racks, cabinets, and heavy equipment.",
        children: [
          { slug: "vr-powder-ind", name: "VR Powder Industrial", summary: "Hybrid and polyester industrial grades." },
        ],
      },
    ],
  },
  {
    slug: "specialty",
    name: "Specialty Coatings",
    summary: "Purpose-built chemistries for extreme duty cycles.",
    children: [
      { slug: "marine", name: "Marine", summary: "Immersion and atmospheric marine systems.", children: [{ slug: "vr-marine-hs", name: "VR Marine HS", summary: "High-solids marine epoxy." }] },
      { slug: "high-temperature", name: "High Temperature", summary: "Silicone and inorganic systems up to 600°C." },
      { slug: "electronics", name: "Electronics", summary: "Conformal and dielectric coatings.", children: [{ slug: "vr-dielectric", name: "VR Dielectric 40", summary: "Moisture-resistant dielectric coating." }] },
    ],
  },
];

export function flattenProducts(nodes: ProductNode[] = productTree, trail: ProductNode[] = []): { node: ProductNode; trail: ProductNode[] }[] {
  return nodes.flatMap((node) => {
    const next = [...trail, node];
    const self = [{ node, trail: next }];
    return node.children ? [...self, ...flattenProducts(node.children, next)] : self;
  });
}

export function findProduct(slug: string) {
  return flattenProducts().find((entry) => entry.node.slug === slug);
}

export function findIndustry(slug: string) {
  return industries.find((item) => item.slug === slug);
}

import type { IconProps } from "@/components/Icon";
import {
  IconApplication,
  IconBadgeCheck,
  IconBuilding,
  IconCar,
  IconCircuit,
  IconFactory,
  IconFlask,
  IconGlobe,
  IconPlane,
  IconShield,
  IconShip,
  IconSupport,
  IconZap,
} from "@/components/Icon";

export const applications: Application[] = [
  {
    slug: "automotive",
    name: "Automotive",
    text: "E-coat, primers, and durable topcoats for body and underbody parts.",
    icon: IconCar,
    image: "/applications/automotive.jpg",
    video: "/automotive.mp4",
  },
  {
    slug: "defence-aerospace",
    name: "Defence & Aerospace",
    text: "Spec-driven coatings for airframes, ground systems, and components.",
    icon: IconPlane,
    image: "/applications/defence-aerospace.jpg",
    video: "/Aerospace.mp4",
  },
  {
    slug: "electronics",
    name: "Electronics",
    text: "Protective dielectric films for boards, housings, and connectors.",
    icon: IconCircuit,
    image: "/applications/electronics.jpg",
    video: "/Electronics.mp4",
  },
  {
    slug: "infrastructure",
    name: "Infrastructure",
    text: "Bridges, tanks, and industrial structures requiring long-term barrier protection.",
    icon: IconBuilding,
    image: "/applications/infrastructure.jpg",
    video: "/Infrastructure.mp4",
  },
  {
    slug: "marine",
    name: "Marine",
    text: "Hull, deck, and offshore steel protection in saline environments.",
    icon: IconShip,
    image: "/applications/marine.jpg",
    video: "/Marine.mp4",
  },
  {
    slug: "energy-process",
    name: "Energy & Process",
    text: "Coatings for pipelines, refineries, and power generation assets.",
    icon: IconFactory,
    image: "/applications/energy-process.jpg",
    video: "/Energy.mp4",
  },
];

const applicationIcons: Record<string, React.FC<IconProps>> = {
  car: IconCar,
  "defence-aerospace": IconPlane,
  circuit: IconCircuit,
  building: IconBuilding,
  ship: IconShip,
  "energy-process": IconFactory,
};

export function getApplicationIcon(name: string) {
  return applicationIcons[name] ?? IconApplication;
}

const weProvideIcons: Record<string, React.FC<IconProps>> = {
  support: IconSupport,
  flask: IconFlask,
  badgeCheck: IconBadgeCheck,
  globe: IconGlobe,
};

export function getWeProvideIcon(name: string) {
  return weProvideIcons[name] ?? IconApplication;
}

export function findApplication(slug: string) {
  return applications.find((item) => item.slug === slug);
}

export const industries = [
  { slug: "manufacturing", name: "Manufacturing", region: "Pune (Bhosari), India" },
  { slug: "automotive", name: "Automotive" },
  { slug: "shipyard-marine", name: "Shipyard & Marine" },
  { slug: "defence", name: "Defence" },
  { slug: "aerospace", name: "Aerospace" },
  { slug: "railways", name: "Railways" },
  { slug: "oil-gas", name: "Oil & Gas" },
  { slug: "construction", name: "Construction" },
  { slug: "wood-furniture", name: "Wood & Furniture" },
  { slug: "packaging", name: "Packaging" },
  { slug: "printing", name: "Printing" },
  { slug: "agriculture", name: "Agriculture" },
  { slug: "pharma-food", name: "Pharma & Food" },
  { slug: "electronics", name: "Electronics" },
  { slug: "wind-energy", name: "Wind Energy" },
  { slug: "infrastructure", name: "Infrastructure" },
  { slug: "north-america", name: "North America", region: "Barrie, Ontario, Canada" },
];

export const weProvide = [
  { title: "Application Support", text: "On-site process guidance from surface prep to final inspection.", icon: "support", image: "/we_provide/application-support.jpg" },
  { title: "Custom Formulation", text: "Lab-backed recipes matched to substrate, climate, and duty cycle.", icon: "flask", image: "/we_provide/custom-formulation.jpg" },
  { title: "Quality Assurance", text: "Batch traceability, film testing, and documented QC protocols.", icon: "badgeCheck", image: "/we_provide/quality-assurance.jpg" },
  { title: "Global Supply", text: "Coordinated logistics from India and North America to your line.", icon: "globe", image: "/we_provide/global-supply.jpg" },
];
 
export const companyStats = [
  { value: "1985", label: "FOUNDED" },
  { value: "40+", label: "YEARS EXPERIENCE" },
  { value: "30+", label: "PRODUCT LINES" },
  { value: "15+", label: "INDUSTRIES SERVED" },
  { value: "5", label: "GLOBAL CERTIFICATIONS" },
];

export const trustPillars = [
  { title: "Engineered for Performance", text: "Coating systems designed around real substrate and duty-cycle conditions." },
  { title: "Industrial-Grade Quality", text: "Documented batch traceability and lab-verified film performance." },
  { title: "Application Expertise", text: "Field engineers supporting OEM lines and maintenance programmes." },
  { title: "Consistent Protection", text: "Reproducible results from first trial through serial production." },
  { title: "Custom Engineering", text: "Formulations matched to substrate, climate and operating requirements." },
];

export const capabilityHighlights = [
  { title: "Resin Processing", text: "In-house resin blending for tight polymer specifications." },
  { title: "Mill Rooms", text: "Controlled dispersion for pigment and filler consistency." },
  { title: "Powder Extrusion", text: "Continuous extrusion lines for architectural and industrial grades." },
  { title: "Quality Laboratories", text: "Film, corrosion and mechanical testing against documented methods." },
  { title: "Application Labs", text: "Pilot lines that replicate customer spray, dip and e-coat processes." },
  { title: "Climate-Controlled Storage", text: "Raw material and finished-goods warehousing for batch integrity." },
];

export type ClientFeedback = {
  id: string;
  name: string;
  role: string;
  location: string;
  feedback: string;
  image: string | null;
};

export const clientFeedback: ClientFeedback[] = [
  {
    id: "sofia-ramirez",
    name: "Sofia Ramirez",
    role: "Logistics Lead",
    location: "Stuttgart, Germany",
    feedback:
      "The integration of VR Coatings equipment into our workflow significantly improved throughput and reduced manual handling.",
    image: "/Sofia Ramirez.avif",
  },
  {
    id: "laura-bennett",
    name: "Laura Bennett",
    role: "Tech Lead",
    location: "Munich, Germany",
    feedback:
      "Even under peak load conditions, the equipment operates seamlessly with minimal maintenance, ensuring consistent reliability.",
    image: "/Laura Bennett.avif",
  },
  {
    id: "tomasz-nowak",
    name: "Tomasz Nowak",
    role: "Compliance Officer",
    location: "Warsaw, Poland",
    feedback:
      "VR Coatings' certification process and records made deployment simple and fully compliant, ensuring complete regulatory standards overall.",
    image: "/Tomasz Nowak.avif",
  },
  {
    id: "hiroshi-tanaka",
    name: "Hiroshi Tanaka",
    role: "Engineering Consultant",
    location: "Eindhoven, Netherlands",
    feedback:
      "From design review to launch, the VR Coatings team delivered clear updates and strong technical support, ensuring smooth execution.",
    image: "/Hiroshi Tanaka.avif",
  },
  {
    id: "marcus-weber",
    name: "Marcus Weber",
    role: "Plant Manager",
    location: "Frankfurt, Germany",
    feedback:
      "The VR Coatings spray systems integrated cleanly into our existing production line, cutting coating cycle times and delivering a measurable ROI within the first quarter.",
    image: "/Marcus Weber.avif",
  },
];

export type Certification = {
  name: string;
  scope: string;
  title?: string;
  file?: string;
  preview?: string;
  body?: string;
  validTo?: string;
};

export const certifications: Certification[] = [
  {
    name: "ISO 9001:2015",
    scope: "Quality management",
    title: "ISO 9001:2015 Quality Management System Certificate",
    body:
      "Certificate No. AB22IS214430 issued by BMQR. Valid until 20 September 2027. Scope covers design, manufacturing, marketing, installation, sales and services of industrial spray painting and fluid handling equipments.",
    file: "/CERTIFICATES/V R COATINGS PVT LTD -9001-RCA - CERTIFICATE.pdf",
    preview: "/certifications/iso-9001-certificate.jpg",
    validTo: "20 September 2027",
  },
  {
    name: "ATEX Acknowledgement",
    scope: "Hazardous area equipment",
    title: "ATEX Acknowledgement of Receipt",
    body:
      "Document No. 2656/1/2018 issued by Technicka inspekcia, a.s. (Notified Body 1354). Acknowledges receipt of technical file documentation under Directive 2014/34/EU for non-electrical painting and fluid handling equipments. Technical documentation stored for 10 years.",
    file: "/CERTIFICATES/ATTEX CERTIFICATE.PDF",
    preview: "/certifications/atex-acknowledgement.jpg",
    validTo: "13 August 2028",
  },
  {
    name: "CE Certificate",
    scope: "Machine safety",
    title: "Certificate of Conformity (CE Marking)",
    body:
      "Certificate No. 3874-CI-32025 issued by CEPROM (Romania). Valid until 5 February 2030. Confirms compliance of industrial spray painting and fluid handling equipments with Directive 2006/42/EC. Reference standards: EN ISO 12100:2010, EN 60204-1:2006+A1:2009.",
    file: "/CERTIFICATES/3874-CI-32025 Industrial Spray Painting and Fluid Handling Equip.pdf",
    preview: "/certifications/ce-certificate-of-conformity.jpg",
    validTo: "5 February 2030",
  },
  {
    name: "ATEX EU-Type",
    scope: "Flameproof equipment",
    title: "EU-Type Examination Certificate (ATEX)",
    body:
      "Certificate No. TI19 ATEX 1308 X issued by Technicka inspekcia, a.s. (Notified Body 1354). EU-type examination for flameproof fluid heater under Directive 2014/34/EU. Compliance with EN 60079-0:2018 and EN 60079-1:2014.",
    file: "/CERTIFICATES/Certificate TI19 ATEX 1308 X.pdf",
    preview: "/certifications/atex-eu-type-exam.jpg",
  },
];

export const presenceLocations = [
  { title: "Head Office", region: "Pune, India" },
  { title: "Manufacturing", region: "Pune (Bhosari), India" },
  { title: "North America", region: "Barrie, Ontario, Canada" },
  { title: "Wai MIDC", region: "Wai, Maharashtra, India" },
];

export type ProductCategory = {
  slug: string;
  name: string;
  catalogue?: string;
  children?: ProductCategory[];
  lineBreakAfter?: string;
  image?: string | null;
};

export const productCategories: ProductCategory[] = [
  {
    slug: "spray-painting-guns",
    name: "Spray Painting Guns",
    image: "/Product_png_s/Flamingo 11817.png",
    children: [
      { slug: "conventional-guns", name: "Conventional Guns", catalogue: "/Catalogue/CONVENTIONAL GUNS_f.pdf", image: "/Product_png_s/Flamingo 11817.png" },
      { slug: "manual-guns", name: "Manual Guns", catalogue: "/Catalogue/manual_GUNS.pdf", image: "/Product_png_s/king.png" },
      { slug: "automatic-guns", name: "Automatic Guns", catalogue: "/Catalogue/AUTOMATIC_gun.pdf", image: "/Product_png_s/Cartridge Gun.png" },
      { slug: "pu-foam-gun", name: "PU Foam Gun" },
      { slug: "wax-spray-gun", name: "Wax Spray Gun", image: "/Product_png_s/wax gun.png" },
      { slug: "electrostatic-gun", name: "Electrostatic Gun", image: "/Product_png_s/electro.png" },
    ],
  },
  {
    slug: "spray-painting-equipment",
    name: "Spray Painting Equipment",
    image: "/Product_png_s/Tiger.png",
    children: [
      { slug: "tiger", name: "Tiger", catalogue: "/Catalogue/Tiger.pdf", image: "/Product_png_s/Tiger.png" },
      { slug: "mini-tiger", name: "Mini Tiger", catalogue: "/Catalogue/Tiger_mini.pdf", image: "/Product_png_s/Tiger_mini.png" },
      { slug: "rhino", name: "Rhino", catalogue: "/Catalogue/rhino.pdf", image: "/Product_png_s/Rhino 4040 (1) copy.png" },
      { slug: "hippo", name: "Hippo", catalogue: "/Catalogue/Hippo.pdf", image: "/Product_png_s/Hippo.png" },
      { slug: "cheetah", name: "Cheetah", catalogue: "/Catalogue/Cheetah.pdf", image: "/Product_png_s/Cheetah.png" },
      { slug: "dragon", name: "Dragon", catalogue: "/Catalogue/dragon.pdf", image: "/Product_png_s/PFP.png" },
      { slug: "polyurea", name: "Polyurea", catalogue: "/Catalogue/polyurea.pdf", image: "/Product_png_s/Polyurea gun 4106.png" },
      {
        slug: "electronic-two-component",
        name: "Electronic Two Component",
        children: [
          { slug: "vrc-mix-hp", name: "VRC - Mix HP", catalogue: "/Catalogue/VRC - MIX HP.pdf", image: "/Product_png_s/VRC MIX HP 0964.png" },
          { slug: "vrc-mix-lp", name: "VRC - Mix LP", catalogue: "/Catalogue/VRC MIX (LOW-MEDIUM) PRESSURE.pdf", image: "/Product_png_s/VRC MIX LP.png" },
        ],
      },
      {
        slug: "fixed-ratio-two-component",
        name: "Fixed Ratio Two Component",
        children: [
          { slug: "vrc-mix-hp-fixed", name: "VRC - Mix HP", catalogue: "/Catalogue/VRC - MIX HP.pdf", image: "/Product_png_s/VRC MIX HP 0964.png" },
          { slug: "vrc-mix-lp-fixed", name: "VRC - Mix LP", catalogue: "/Catalogue/VRC MIX (LOW-MEDIUM) PRESSURE.pdf", image: "/Product_png_s/VRC MIX LP.png" },
        ],
      },
      { slug: "lion", name: "Lion", image: "/Product_png_s/VRC eagle.png" },
    ],
  },
  {
    slug: "paint-transfer-pumps",
    name: "Paint Transfer Pumps",
    image: "/Product_png_s/Elephant 14398.jpg",
    children: [
      { slug: "hippo-pump", name: "Hippo", catalogue: "/Catalogue/Hippo.pdf", image: "/Product_png_s/Hippo 14311.jpg" },
      { slug: "elephant", name: "Elephant", catalogue: "/Catalogue/Elephant.pdf", image: "/Product_png_s/Elephant 14398.jpg" },
      { slug: "cub", name: "Cub", catalogue: "/Catalogue/cub.pdf", image: "/Product_png_s/Category_wise_products/Cub/Cub pump.jpg" },
      { slug: "barrel-pump", name: "Barrel Pump", catalogue: "/Catalogue/Barrel Pump.pdf", image: "/Product_png_s/Barrel Transfer Pump.png" },
      { slug: "portable-pressure-feed-pot", name: "Portable Pressure Feed Pot", catalogue: "/Catalogue/PORTABLE PRESSURE FEED POT.pdf", image: "/Product_png_s/Category_wise_products/Pressure Feed Pot/VRC 4295 (1).jpg" },
    ],
  },
  {
    slug: "dispensing-equipment-drum-press",
    name: "Dispensing Equipment - Drum Press",
    image: "/Product_png_s/Drum press1.png",
    children: [
      { slug: "drum-press", name: "Drum Press", catalogue: "/Catalogue/DRUM PRESS.pdf", image: "/Product_png_s/Drum press1.png" },
      {
        slug: "doser",
        name: "Doser",
        children: [
          { slug: "single-component", name: "Single Component" },
          { slug: "two-component", name: "Two Component" },
        ],
      },
    ],
  },
  { slug: "painting-reciprocators", name: "Painting Reciprocators", image: "/Product_png_s/VRC HAWK.png" },
  {
    slug: "paint-agitation-system-turbine-stirrer",
    name: "Paint Agitation System - Turbine Stirrer",
    image: "/Product_png_s/Turbinr Stirrer.png",
    lineBreakAfter: "Turbine",
    children: [
      { slug: "turbine-stirrer", name: "Turbine Stirrer", catalogue: "/Catalogue/turbine.pdf", image: "/Product_png_s/Turbinr Stirrer.png" },
      { slug: "pneumatic-stirrer", name: "Pneumatic Stirrer", catalogue: "/Catalogue/PNEUMATIC STIRRER.pdf", image: "/Product_png_s/pneumatic_stirrer.png" },
      { slug: "electrical-flame-proof-stirrer", name: "Electrical Flame Proof Stirrer" },
    ],
  },
  {
    slug: "accessories",
    name: "Accessories",
    image: "/Product_png_s/slimline filter.png",
    children: [
      { slug: "valves", name: "Valves", catalogue: "/Catalogue/Valves.pdf", image: "/Product_png_s/vrc.png" },
      { slug: "two-component-mixers", name: "Two Component Mixers", image: "/Product_png_s/Mixing Manifold 14427.png" },
      { slug: "filters", name: "Filters", catalogue: "/Catalogue/filters.pdf", image: "/Product_png_s/slimline filter.png" },
      { slug: "heating-accessories", name: "Heating Accessories", image: "/Product_png_s/elecric3.png" },
      { slug: "guns", name: "Guns", catalogue: "/Catalogue/GUNS.pdf", image: "/Product_png_s/king.png" },
      {
        slug: "pressure-regulator",
        name: "Pressure Regulator",
        image: "/Product_png_s/LP regulator 4219.png",
        children: [
          { slug: "back-pressure-regulator", name: "Back Pressure Regulator", catalogue: "/Catalogue/regulator.pdf" },
        ],
        catalogue: "/Catalogue/regulator.pdf",
      },
      {
        slug: "hoses",
        name: "Hoses",
        children: [
          { slug: "electrically-heated-hoses", name: "Electrically Heated Hoses", image: "/Product_png_s/elecric.png" },
          { slug: "water-heated-hoses", name: "Water Heated Hoses", image: "/Product_png_s/elecric2.png" },
          {
            slug: "ptfe",
            name: "PTFE",
            children: [
              { slug: "ptfe-low-pressure-hoses", name: "Low Pressure Hoses" },
              { slug: "ptfe-high-pressure-hoses", name: "High Pressure Hoses" },
            ],
          },
          {
            slug: "thermoplastic-hoses",
            name: "Thermoplastic Hoses",
            children: [
              { slug: "thermoplastic-low-pressure-hoses", name: "Low Pressure Hoses" },
              { slug: "thermoplastic-high-pressure-hoses", name: "High Pressure Hoses" },
            ],
          },
          { slug: "suction-hoses", name: "Suction Hoses" },
          { slug: "air-hoses-for-spraying", name: "Air Hoses for Spraying" },
          { slug: "pneumatic-tube", name: "Pneumatic Tube" },
        ],
      },
      { slug: "other-accessories", name: "Other Accessories" },
    ],
  },
];

export const searchIndex = [
  { title: "Home", href: "/", keywords: "home coatings solutions" },
  { title: "About Us", href: "/about", keywords: "about company infrastructure" },
  { title: "Why Choose Us", href: "/about/why-choose-us", keywords: "quality why choose" },
  { title: "Global Presence", href: "/about/global-presence", keywords: "global offices export" },
  { title: "Products", href: "/products", keywords: "epoxy powder polyurethane zinc" },
  { title: "Applications", href: "/applications", keywords: "automotive aerospace marine" },
  { title: "Partners", href: "/assets/partners", keywords: "partners distributors" },
  { title: "Clients", href: "/assets/clients", keywords: "clients customers industries" },
  { title: "Industries We Serve", href: "/assets/industries", keywords: "industries served" },
  { title: "Blog", href: "/resources/blog", keywords: "blog articles" },
  { title: "Certifications", href: "/resources/certifications", keywords: "iso certification quality" },
  { title: "Career", href: "/resources/career", keywords: "jobs career hiring" },
  { title: "FAQs", href: "/resources/faqs", keywords: "faq questions" },
  { title: "Catalog", href: "/catalog", keywords: "catalog brochure pdf" },
  { title: "Contact Us", href: "/contact", keywords: "contact inquiry phone email" },
  ...flattenProducts().map(({ node }) => ({
    title: node.name,
    href: `/products/${node.slug}`,
    keywords: `${node.name} ${node.summary}`,
  })),
];

export type CatalogueEntry = {
  slug: string;
  name: string;
  category: string;
  catalogue: string;
};

export const cataloguePDFs: CatalogueEntry[] = [
  { slug: "ball-valves", name: "Ball Valves", category: "Accessories", catalogue: "/Catalogue/ball_valves.pdf" },
  { slug: "pulsation-dampner", name: "Pulsation Dampner", category: "Accessories", catalogue: "/Catalogue/PULSATION DAMPNER.pdf" },
  { slug: "paint-preparation-unit", name: "Paint Preparation Unit", category: "Special", catalogue: "/Catalogue/Paint Preparation Unit.pdf" },
  { slug: "tube-varnish-coating-system", name: "Tube Varnish Coating System", category: "Special", catalogue: "/Catalogue/TUBE VARNISH COATING SYSTEM.pdf" },
  { slug: "leopard-electric", name: "Leopard - Electric", category: "Paint Transfer Pumps", catalogue: "/Catalogue/Electric_pump.pdf" },
];

export function findCatalogue(slug: string): string | undefined {
  const cat = flattenCategories(productCategories).find((e) => e.node.slug === slug);
  if (cat?.node.catalogue) return cat.node.catalogue;

  const landing = landingProducts.find((p) => p.slug === slug);
  if (landing?.catalogue) return landing.catalogue;

  const special = cataloguePDFs.find((e) => e.slug === slug);
  if (special?.catalogue) return special.catalogue;

  return undefined;
}

function flattenCategories(
  nodes: ProductCategory[],
  trail: ProductCategory[] = []
): { node: ProductCategory; trail: ProductCategory[] }[] {
  return nodes.flatMap((node) => {
    const next = [...trail, node];
    const self = [{ node, trail: next }];
    return node.children
      ? [...self, ...flattenCategories(node.children, next)]
      : self;
  });
}

export type BlogPost = {
  slug: string;
  title: string;
  excerpt: string;
  content: string[];
  image: string | null;
};

export const blogPosts: BlogPost[] = [
  {
    slug: "the-day-it-all-began-1985",
    title: "The Day It All Began — 1985",
    excerpt:
      "The story of how VR Coatings began in Pune in 1985, driven by a simple idea: build reliable industrial equipment for Indian conditions.",
    content: [
      "If you want to build something that lasts, start with honesty and a screwdriver.",
      "It was 1985 in Pune. The Indian industry was waking up to new possibilities, but reliable fluid-handling equipment was still a distant dream for many. We were a small group of engineers and dreamers, with grease on our hands and fire in our hearts.",
      "The idea for VR Coatings came not from a business plan, but from a frustration. Imported machines were expensive, difficult to maintain, and ill-suited for Indian conditions. We thought: Why not make our own, better ones? Machines designed for India, in India — that could stand the dust, heat, and long working hours.",
      "The first few months were filled with sleepless nights. We worked out of a modest workshop in Pune, often making do with what we had. The first pump we built was tested in our backyard before it ever saw a factory floor. And when it worked — really worked — we knew we had something special.",
      "We didn\u2019t know then that VR Coatings would one day be a trusted name across India and even abroad. We only knew we wanted to make machines that never let our customers down.",
    ],
    image: "/BLOGS/Blog_1.png",
  },
  {
    slug: "learning-by-listening-our-first-customers",
    title: "Learning by Listening — Our First Customers",
    excerpt:
      "How early customers and shop-floor feedback shaped VR Coatings\u2019 approach to engineering and problem solving.",
    content: [
      "In our early years, our best teachers were not in classrooms — they were on shop floors.",
      "We made it a habit to listen. To watch how operators worked, how maintenance teams handled breakdowns, how production managers stressed over downtime. Every complaint was a clue, every request a challenge.",
      "Our first big break came when an automotive supplier took a chance on us. Their imported dispensing system was down for weeks, waiting for spares. We offered them a locally made solution that worked — and kept working. That customer is still with us today.",
      "From there, word spread. Industries from paints to adhesives to shipbuilding began calling us. Not because we were the cheapest, but because we understood their pain and solved it. Listening became our biggest strength — and it still is.",
    ],
    image: "/BLOGS/Blog_2.png",
  },
  {
    slug: "growing-roots-and-branches",
    title: "Growing Roots and Branches",
    excerpt:
      "How VR Coatings evolved from a workshop into a growing engineering organization.",
    content: [
      "By the mid-1990s, VR Coatings was no longer just a workshop — it was becoming an organization.",
      "We moved into larger facilities in Pune. We started building teams, training engineers, and investing in better tools. Our product line expanded from manual dispensing systems to automatic, servo-driven, and feedback-controlled machines.",
      "One of our proudest moments was when a customer told us: \u201cYour pump works better than the one we imported from Europe.\u201d That wasn\u2019t just praise — it was proof that Make in India could compete with the world.",
      "We didn\u2019t just grow in size; we grew in reputation. By the early 2000s, we were working with major names in automotive, construction, and manufacturing. And we were just getting started.",
    ],
    image: "/BLOGS/Blog_3.png",
  },
  {
    slug: "our-leap-into-the-global-arena",
    title: "Our Leap in to the Global Arena",
    excerpt:
      "The decision to set up a German assembly unit and carry Indian engineering to factories around the world.",
    content: [
      "Every business dreams of going global — but for us, it wasn\u2019t just a dream.",
      "Our reputation began reaching beyond India\u2019s borders. International companies started approaching us for machines that could withstand demanding industrial conditions yet be economical.",
      "That\u2019s when we decided to set up an assembly unit in Germany. It wasn\u2019t easy — new regulations, new market expectations — but it was worth it. The German presence allowed us to support European customers more closely and showcase Indian engineering on a global stage.",
      "From Pune to Germany, our machines began carrying the VR Coatings name to factories around the world. And each time a customer said, \u201cThis is better than what we had before,\u201d we knew our decision was right.",
    ],
    image: "/BLOGS/Blog_4.png",
  },
  {
    slug: "innovation-is-in-our-dna",
    title: "Innovation Is in Our DNA",
    excerpt:
      "From IoT-enabled dosing systems to electric pumps, how continuous innovation drives every VR Coatings solution.",
    content: [
      "If you walk through our factory floor today, you\u2019ll see machines that our younger selves could barely imagine in 1985.",
      "We now build IoT-enabled dosing systems, micro-dispensers accurate to 0.001 grams, and vacuum-assisted systems for high-precision applications. We\u2019ve even developed electric pumps that are clean, quiet, and energy-efficient.",
      "But innovation for us is not just about adding electronics. It\u2019s about making machines smarter, more reliable, and easier to maintain. Whether it\u2019s a high-viscosity adhesive or a delicate electronics potting compound, our solutions are engineered to perform.",
      "And we never stop learning — every new customer challenge is a chance to innovate again.",
    ],
    image: "/BLOGS/Blog_5.png",
  },
  {
    slug: "looking-back-moving-forward",
    title: "Looking Back, Moving Forward",
    excerpt:
      "From a small Pune workshop to a trusted global name, and the road ahead toward an IPO.",
    content: [
      "Today, VR Coatings stands as India\u2019s most trusted name in high-viscosity spraying and dispensing equipment. We serve industries from automotive to aerospace, pharmaceuticals to shipbuilding. Our clients include INS Vikrant, Mercedes-Benz, Tata Motors, Mahindra & Mahindra, and Indian Railways.",
      "We are preparing for our next big leap — a public offering (IPO) that will fund our R&D and global expansion.",
      "But even as we look ahead, we never forget where we came from — a small workshop, a few determined people, and a belief that Indian engineering could stand shoulder to shoulder with the world.",
      "And if there\u2019s one thing we\u2019ve learned in these decades, it\u2019s this: Machines may be made of steel, but trust is built in the hearts of customers. That\u2019s what keeps VR Coatings running strong — yesterday, today, and tomorrow.",
    ],
    image: "/BLOGS/Blog_6.png",
  },
];

export function findBlogPost(slug: string) {
  return blogPosts.find((post) => post.slug === slug);
}
