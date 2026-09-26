export type PartnerProduct = {
  title: string;
  description: string;
};

export type Partner = {
  id: string;
  order: string;
  name: string;
  country: string;
  location: string;
  partnerType: string;
  description: string;
  tagline?: string;
  about: string;
  products: PartnerProduct[];
  highlights: string[];
  website: string;
  logo: string;
  logoDark?: string;
  logoBackground?: "light" | "dark";
  logoFit?: "contain" | "cover";
};

export const partners: Partner[] = [
  {
    id: "asahi-sunac",
    order: "01",
    name: "Asahi Sunac Corporation",
    country: "Japan",
    location: "Nagoya, Japan",
    partnerType: "Technology Partner",
    description: "Japan's Leading Coating Equipment & Atomization Technology Manufacturer",
    about:
      "Asahi Sunac Corporation, headquartered in Nagoya, Japan, is a globally recognised leader in coating equipment engineering, forging machinery, and new components technology. Their expertise in atomization science has made them a trusted partner for industrial coating solutions worldwide. VR Coatings distributes and supports Asahi Sunac products in India.",
    products: [
      {
        title: "Coating Equipment & Engineering",
        description: "Advanced airless, air-assisted and electrostatic spray coating systems for industrial applications.",
      },
      {
        title: "Forging Machinery",
        description: "High-precision forging machines and engineering systems for metal forming industries.",
      },
      {
        title: "Precision Spray Coater",
        description: "Precision spray coating equipment for electronics, semiconductors and specialty applications.",
      },
      {
        title: "Precision Cleaning Equipment",
        description: "Industrial cleaning systems for manufacturing environments requiring high cleanliness standards.",
      },
    ],
    highlights: [
      "Internationally certified coating equipment",
      "70+ years of manufacturing excellence from Japan",
      "Advanced atomization technology for optimal coating films",
      "Available in India through VR Coatings — sales, service & spares",
    ],
    website: "https://www.sunac.co.jp/en/",
    logo: "/media/images/partners/ASAHI_SUNAC.svg",
  },
  {
    id: "walther-systemtechnik",
    order: "02",
    name: "Walther Systemtechnik GmbH",
    country: "Germany",
    location: "Germany",
    partnerType: "Technology Partner",
    description: "German Precision Dosing & Fluid Handling Technology",
    tagline: "Precision Dosing Technology",
    about:
      "Walther Systemtechnik GmbH, based in Germany, specialises in high-precision dosing and dispensing technology for industrial and production environments. Their systems cover the complete fluid handling chain — from pumping and conveying to precision dosing and application. VR Coatings brings Walther Systemtechnik's German engineering to India.",
    products: [
      {
        title: "Pump Systems",
        description: "Complete pump systems for conveying and providing fluids — single pumps, small-volume dispensers, pressure vessels.",
      },
      {
        title: "Material Pressure Regulators",
        description: "Precision pressure regulators, flow limiters, pressure amplifiers and media storage for fluid control.",
      },
      {
        title: "Dosing Valves",
        description: "Spray valves, pulse/jet valves, chamber dosing valves and outlet valves for precise application.",
      },
      {
        title: "Nozzle Extensions & Systems",
        description: "Dosing devices, nozzle extensions and complete dispensing systems — including the RotoStream series for volumetric dosing.",
      },
    ],
    highlights: [
      "RotoStream Series — volumetric dosing & spraying with highest precision",
      "Complete fluid handling solutions from source to application point",
      "German engineering — ideal for automotive, electronics, pharma industries",
      "Available in India through VR Coatings — sales, service & spares",
    ],
    website: "https://www.walther-systemtechnik.com",
    logo: "/media/images/partners/wst-logo-color.svg",
  },
  {
    id: "timmer",
    order: "03",
    name: "Timmer GmbH",
    country: "Germany",
    location: "Germany",
    partnerType: "Technology Partner",
    description: "German Premium Pumps — Highest Quality, Compact & Low-Maintenance",
    tagline: "Premium Pump Technology",
    about:
      "Timmer GmbH, Germany, is a premium manufacturer of industrial pumps and fluid handling technology. Their product range covers double diaphragm pumps, piston pumps, vacuum technology, and intelligent sensor systems. Timmer is known for compact, reliable, and low-maintenance pumps that excel in industrial production environments. VR Coatings is an authorised partner for Timmer products in India.",
    products: [
      {
        title: "Double Diaphragm Pumps",
        description: "timPRO, timCLASSIC, timCHEM (1:1) and timBOOST (3.5:1) — for paint, coatings, adhesives & chemicals.",
      },
      {
        title: "Piston Pumps",
        description: "tim ECO electric piston pumps, tim COA coagulant pumps and tim GLUE glue pumps for production lines.",
      },
      {
        title: "Intelligent Sensor Technology",
        description: "tim TRON intelligent sensor, tim LINK pump monitoring — real-time pump health and performance data.",
      },
      {
        title: "fluidFIT Connectors",
        description: "Metric and imperial hose connectors, steelFIT metal pipe fittings and pneumatic accessories.",
      },
    ],
    highlights: [
      "timPRO & timCLASSIC — double diaphragm pumps with 40+ year reliability track record",
      "tim TRON intelligent sensor technology for Industry 4.0 ready pump monitoring",
      "Compact, low-maintenance design — ideal for paint, coating, glue, chemical transfer",
      "Available in India through VR Coatings — sales, service & spares",
    ],
    website: "https://www.timmer.de/en/pumps/",
    logo: "/media/images/partners/timmer_logo_white_(14).svg",
    logoBackground: "dark",
    logoFit: "contain",
  },
];
