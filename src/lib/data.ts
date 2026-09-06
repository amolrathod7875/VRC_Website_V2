export type NavItem = {
  label: string;
  href: string;
  children?: { label: string; href: string }[];
};

export const navItems: NavItem[] = [
  { label: "Home", href: "/" },
  {
    label: "About",
    href: "/about",
    children: [
      { label: "About Us", href: "/about" },
      { label: "Why Choose Us", href: "/about/why-choose-us" },
      { label: "Global Presence", href: "/about/global-presence" },
    ],
  },
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
      { label: "News", href: "/resources/news" },
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
      "VR Coatings Pvt. Ltd.",
      "Plot 42, Industrial Estate, MIDC",
      "Pune, Maharashtra 411019, India",
    ],
    phone: "+91 20 2741 2200",
    phoneHref: "tel:+912027412200",
  },
  {
    title: "Factory",
    lines: [
      "VR Coatings Manufacturing Unit",
      "Gat No. 318, Chakan Industrial Area",
      "Pune, Maharashtra 410501, India",
    ],
    phone: "+91 20 2768 4410",
    phoneHref: "tel:+912027684410",
  },
  {
    title: "North America",
    lines: [
      "VR Coatings NA Inc.",
      "1850 Commerce Drive, Suite 210",
      "Troy, MI 48083, USA",
    ],
    phone: "+1 248 555 0148",
    phoneHref: "tel:+12485550148",
  },
];

export const companyEmail = "info@vrcoatings.com";

export const socialLinks = [
  { name: "LinkedIn", href: "https://www.linkedin.com", icon: "in" },
  { name: "YouTube", href: "https://www.youtube.com", icon: "yt" },
  { name: "Instagram", href: "https://www.instagram.com", icon: "ig" },
  { name: "Facebook", href: "https://www.facebook.com", icon: "fb" },
  { name: "WhatsApp", href: "https://wa.me/912027412200", icon: "wa" },
];

export type FooterLink = { label: string; href: string };
export type FooterColumn = { title: string; links: FooterLink[] };

export const footerProductColumns: FooterColumn[] = [
  {
    title: "SPRAY SYSTEMS",
    links: [
      { label: "DRAGON \u2014 PFP System", href: "/products" },
      { label: "CHEETAH \u2014 2K Hot Airless", href: "/products" },
      { label: "RHINO \u2014 Heavy Duty", href: "/products" },
      { label: "TIGER \u2014 Low/Medium Duty", href: "/products" },
      { label: "MINI TIGER \u2014 Air-Assisted", href: "/products" },
      { label: "POLYUREA System", href: "/products" },
      { label: "VRC-MIX HP", href: "/products" },
      { label: "VRC MIX (L/M)", href: "/products" },
      { label: "LEOPARD \u2014 Electric Pump", href: "/products" },
      { label: "TUBE/VARNISH COATING", href: "/products" },
    ],
  },
  {
    title: "TRANSFER PUMPS",
    links: [
      { label: "ELEPHANT \u2014 High Volume", href: "/products" },
      { label: "HIPPO \u2014 Low Pressure", href: "/products" },
      { label: "BARREL PUMP \u2014 20L", href: "/products" },
      { label: "CUB \u2014 Four-Ball Piston", href: "/products" },
      { label: "DRUM PRESS", href: "/products" },
    ],
  },
  {
    title: "SPRAY GUNS",
    links: [
      { label: "Manual Spray Guns", href: "/products" },
      { label: "Automatic Spray Guns", href: "/products" },
      { label: "KINGFISHER \u2014 Conventional", href: "/products" },
    ],
  },
  {
    title: "ACCESSORIES",
    links: [
      { label: "Ball Valves \u2014 up to 500 BAR", href: "/products" },
      { label: "Pressure Regulators HP/LP", href: "/products" },
      { label: "Inline Filters HP/LP", href: "/products" },
      { label: "Turbine Stirrers", href: "/products" },
      { label: "Pneumatic Stirrer", href: "/products" },
      { label: "Pressure Feed Pot", href: "/products" },
      { label: "Pulsation Dampner", href: "/products" },
    ],
  },
];

export const footerCompanyLinks: FooterLink[] = [
  { label: "About VR Coatings", href: "/about" },
  { label: "Industries Served", href: "/assets/industries" },
  { label: "Product Videos", href: "/products" },
  { label: "Careers", href: "/resources/career" },
  { label: "Vendor Registration", href: "/contact" },
  { label: "Contact Us", href: "/contact" },
  { label: "Visit Original Site", href: "https://www.vrcoatings.com" },
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
};

export const landingProducts: LandingProduct[] = [
  { slug: "barrel-pump", name: "Barrel pump", description: "" },
  { slug: "cheetah", name: "Cheetah", description: "" },
  { slug: "cub", name: "Cub", description: "" },
  { slug: "diaphragm-pump", name: "Diaphragm Pump", description: "" },
  { slug: "drum-press", name: "DRUM PRESS", description: "" },
  { slug: "elephant-pump", name: "Elephant Pump", description: "" },
  { slug: "hippo-pump", name: "Hippo Pump", description: "" },
  { slug: "leopard-electric", name: "Leopard - ELECTRIC\u2026", description: "" },
  { slug: "pfp-dragon", name: "PFP DRAGON", description: "" },
  { slug: "polyurea", name: "Polyurea", description: "" },
  { slug: "pressure-feed-pot", name: "Pressure Feed Pot", description: "" },
  { slug: "rhino-pump", name: "Rhino Pump", description: "" },
  { slug: "spray-painting-guns", name: "Spray Painting Guns", description: "" },
  { slug: "tiger-mini", name: "Tiger Mini", description: "" },
  { slug: "tiger-pump", name: "Tiger Pump", description: "" },
  { slug: "turbine-stirrer", name: "Turbine Stirrer", description: "" },
  { slug: "vrc-mix-hp", name: "VRC MIX HP", description: "" },
  { slug: "vrc-mix-lp", name: "VRC MIX LP", description: "" },
];

export type ProductNode = {
  slug: string;
  name: string;
  summary: string;
  children?: ProductNode[];
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

export const applications = [
  { slug: "automotive", name: "Automotive", text: "E-coat, primers, and durable topcoats for body and underbody parts." },
  { slug: "defence-aerospace", name: "Defence & Aerospace", text: "Spec-driven coatings for airframes, ground systems, and components." },
  { slug: "electronics", name: "Electronics", text: "Protective dielectric films for boards, housings, and connectors." },
  { slug: "infrastructure", name: "Infrastructure", text: "Bridges, tanks, and industrial structures requiring long-term barrier protection." },
  { slug: "marine", name: "Marine", text: "Hull, deck, and offshore steel protection in saline environments." },
  { slug: "energy", name: "Energy & Process", text: "Coatings for pipelines, refineries, and power generation assets." },
];

export const industries = [
  { slug: "manufacturing", name: "Manufacturing" },
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
];

export const weProvide = [
  { title: "Application Support", text: "On-site process guidance from surface prep to final inspection." },
  { title: "Custom Formulation", text: "Lab-backed recipes matched to substrate, climate, and duty cycle." },
  { title: "Quality Assurance", text: "Batch traceability, film testing, and documented QC protocols." },
  { title: "Global Supply", text: "Coordinated logistics from India and North America to your line." },
];

export const trustPillars = [
  { title: "Engineered for Performance", text: "Coating systems designed around real substrate and duty-cycle conditions." },
  { title: "Industrial-Grade Quality", text: "Documented batch traceability and lab-verified film performance." },
  { title: "Application Expertise", text: "Field engineers supporting OEM lines and maintenance programmes." },
  { title: "Consistent Protection", text: "Reproducible results from first trial through serial production." },
  { title: "Custom Engineering", text: "Formulations matched to substrate, climate and operating requirements." },
];

export const performanceAttributes = [
  {
    title: "Surface Protection",
    text: "Barrier and inhibitive systems for steel, aluminium and engineered substrates.",
  },
  {
    title: "Corrosion Resistance",
    text: "Zinc-rich primers and high-build epoxies for atmospheric and immersion service.",
  },
  {
    title: "Durability",
    text: "UV-stable polyurethanes and toughened finishes for long service life.",
  },
  {
    title: "Chemical Resistance",
    text: "Lining systems and high-crosslink-density films for aggressive media.",
  },
  {
    title: "Temperature Performance",
    text: "Silicone and inorganic coatings engineered for elevated operating temperatures.",
  },
  {
    title: "Application Precision",
    text: "Powder, liquid and electrocoat systems tuned to OEM process windows.",
  },
];

export const capabilityHighlights = [
  { title: "Resin Processing", text: "In-house resin blending for tight polymer specifications." },
  { title: "Mill Rooms", text: "Controlled dispersion for pigment and filler consistency." },
  { title: "Powder Extrusion", text: "Continuous extrusion lines for architectural and industrial grades." },
  { title: "Quality Laboratories", text: "Film, corrosion and mechanical testing against documented methods." },
  { title: "Application Labs", text: "Pilot lines that replicate customer spray, dip and e-coat processes." },
  { title: "Climate-Controlled Storage", text: "Raw material and finished-goods warehousing for batch integrity." },
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
  { title: "Manufacturing", region: "Chakan, India" },
  { title: "North America", region: "Troy, MI, USA" },
];

export type ProductCategory = {
  slug: string;
  name: string;
  children?: ProductCategory[];
  lineBreakAfter?: string;
};

export const productCategories: ProductCategory[] = [
  {
    slug: "spray-painting-guns",
    name: "Spray Painting Guns",
    children: [
      { slug: "conventional-guns", name: "Conventional Guns" },
      { slug: "manual-guns", name: "Manual Guns" },
      { slug: "automatic-guns", name: "Automatic Guns" },
      { slug: "pu-foam-gun", name: "PU Foam Gun" },
      { slug: "wax-spray-gun", name: "Wax Spray Gun" },
      { slug: "electrostatic-gun", name: "Electrostatic Gun" },
    ],
  },
  {
    slug: "spray-painting-equipment",
    name: "Spray Painting Equipment",
    children: [
      { slug: "tiger", name: "Tiger" },
      { slug: "mini-tiger", name: "Mini Tiger" },
      { slug: "rhino", name: "Rhino" },
      { slug: "hippo", name: "Hippo" },
      { slug: "cheetah", name: "Cheetah" },
      { slug: "dragon", name: "Dragon" },
      { slug: "polyurea", name: "Polyurea" },
      {
        slug: "electronic-two-component",
        name: "Electronic Two Component",
        children: [
          { slug: "vrc-mix-hp", name: "VRC - Mix HP" },
          { slug: "vrc-mix-lp", name: "VRC - Mix LP" },
        ],
      },
      {
        slug: "fixed-ratio-two-component",
        name: "Fixed Ratio Two Component",
        children: [
          { slug: "vrc-mix-hp-fixed", name: "VRC - Mix HP" },
          { slug: "vrc-mix-lp-fixed", name: "VRC - Mix LP" },
        ],
      },
      { slug: "lion", name: "Lion" },
    ],
  },
  {
    slug: "paint-transfer-pumps",
    name: "Paint Transfer Pumps",
    children: [
      { slug: "hippo-pump", name: "Hippo" },
      { slug: "elephant", name: "Elephant" },
      { slug: "cub", name: "Cub" },
      { slug: "barrel-pump", name: "Barrel Pump" },
      { slug: "portable-pressure-feed-pot", name: "Portable Pressure Feed Pot" },
    ],
  },
  {
    slug: "dispensing-equipment-drum-press",
    name: "Dispensing Equipment - Drum Press",
    children: [
      { slug: "drum-press", name: "Drum Press" },
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
  { slug: "painting-reciprocators", name: "Painting Reciprocators" },
  {
    slug: "paint-agitation-system-turbine-stirrer",
    name: "Paint Agitation System - Turbine Stirrer",
    lineBreakAfter: "Turbine",
    children: [
      { slug: "turbine-stirrer", name: "Turbine Stirrer" },
      { slug: "pneumatic-stirrer", name: "Pneumatic Stirrer" },
      { slug: "electrical-flame-proof-stirrer", name: "Electrical Flame Proof Stirrer" },
    ],
  },
  {
    slug: "accessories",
    name: "Accessories",
    children: [
      { slug: "valves", name: "Valves" },
      { slug: "two-component-mixers", name: "Two Component Mixers" },
      { slug: "filters", name: "Filters" },
      { slug: "heating-accessories", name: "Heating Accessories" },
      { slug: "guns", name: "Guns" },
      {
        slug: "pressure-regulator",
        name: "Pressure Regulator",
        children: [
          { slug: "back-pressure-regulator", name: "Back Pressure Regulator" },
        ],
      },
      {
        slug: "hoses",
        name: "Hoses",
        children: [
          { slug: "electrically-heated-hoses", name: "Electrically Heated Hoses" },
          { slug: "water-heated-hoses", name: "Water Heated Hoses" },
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
  { title: "News", href: "/resources/news", keywords: "news press" },
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
