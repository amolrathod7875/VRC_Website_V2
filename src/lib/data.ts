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
  catalogue?: string;
};

export const landingProducts: LandingProduct[] = [
  { slug: "barrel-pump", name: "Barrel pump", description: "", catalogue: "/Catalogue/Barrel Pump.pdf" },
  { slug: "cheetah", name: "Cheetah", description: "", catalogue: "/Catalogue/Cheetah.pdf" },
  { slug: "cub", name: "Cub", description: "", catalogue: "/Catalogue/cub.pdf" },
  { slug: "diaphragm-pump", name: "Diaphragm Pump", description: "", catalogue: "/Catalogue/diaphragm pump.pdf" },
  { slug: "drum-press", name: "DRUM PRESS", description: "", catalogue: "/Catalogue/DRUM PRESS.pdf" },
  { slug: "elephant-pump", name: "Elephant Pump", description: "", catalogue: "/Catalogue/Elephant.pdf" },
  { slug: "hippo-pump", name: "Hippo Pump", description: "", catalogue: "/Catalogue/Hippo.pdf" },
  { slug: "leopard-electric", name: "Leopard - ELECTRIC\u2026", description: "" },
  { slug: "pfp-dragon", name: "PFP DRAGON", description: "", catalogue: "/Catalogue/dragon.pdf" },
  { slug: "polyurea", name: "Polyurea", description: "", catalogue: "/Catalogue/polyurea.pdf" },
  { slug: "pressure-feed-pot", name: "Pressure Feed Pot", description: "", catalogue: "/Catalogue/PORTABLE PRESSURE FEED POT.pdf" },
  { slug: "rhino-pump", name: "Rhino Pump", description: "", catalogue: "/Catalogue/rhino.pdf" },
  { slug: "spray-painting-guns", name: "Spray Painting Guns", description: "" },
  { slug: "tiger-mini", name: "Tiger Mini", description: "", catalogue: "/Catalogue/Tiger_mini.pdf" },
  { slug: "tiger-pump", name: "Tiger Pump", description: "", catalogue: "/Catalogue/Tiger.pdf" },
  { slug: "turbine-stirrer", name: "Turbine Stirrer", description: "", catalogue: "/Catalogue/turbine.pdf" },
  { slug: "vrc-mix-hp", name: "VRC MIX HP", description: "", catalogue: "/Catalogue/VRC - MIX HP.pdf" },
  { slug: "vrc-mix-lp", name: "VRC MIX LP", description: "", catalogue: "/Catalogue/VRC MIX (LOW-MEDIUM) PRESSURE.pdf" },
];

export type ProductNode = {
  slug: string;
  name: string;
  summary: string;
  catalogue?: string;
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
  catalogue?: string;
  children?: ProductCategory[];
  lineBreakAfter?: string;
};

export const productCategories: ProductCategory[] = [
  {
    slug: "spray-painting-guns",
    name: "Spray Painting Guns",
    children: [
      { slug: "conventional-guns", name: "Conventional Guns", catalogue: "/Catalogue/CONVENTIONAL GUNS_f.pdf" },
      { slug: "manual-guns", name: "Manual Guns", catalogue: "/Catalogue/manual_GUNS.pdf" },
      { slug: "automatic-guns", name: "Automatic Guns", catalogue: "/Catalogue/AUTOMATIC_gun.pdf" },
      { slug: "pu-foam-gun", name: "PU Foam Gun" },
      { slug: "wax-spray-gun", name: "Wax Spray Gun" },
      { slug: "electrostatic-gun", name: "Electrostatic Gun" },
    ],
  },
  {
    slug: "spray-painting-equipment",
    name: "Spray Painting Equipment",
    children: [
      { slug: "tiger", name: "Tiger", catalogue: "/Catalogue/Tiger.pdf" },
      { slug: "mini-tiger", name: "Mini Tiger", catalogue: "/Catalogue/Tiger_mini.pdf" },
      { slug: "rhino", name: "Rhino", catalogue: "/Catalogue/rhino.pdf" },
      { slug: "hippo", name: "Hippo", catalogue: "/Catalogue/Hippo.pdf" },
      { slug: "cheetah", name: "Cheetah", catalogue: "/Catalogue/Cheetah.pdf" },
      { slug: "dragon", name: "Dragon", catalogue: "/Catalogue/dragon.pdf" },
      { slug: "polyurea", name: "Polyurea", catalogue: "/Catalogue/polyurea.pdf" },
      {
        slug: "electronic-two-component",
        name: "Electronic Two Component",
        children: [
          { slug: "vrc-mix-hp", name: "VRC - Mix HP", catalogue: "/Catalogue/VRC - MIX HP.pdf" },
          { slug: "vrc-mix-lp", name: "VRC - Mix LP", catalogue: "/Catalogue/VRC MIX (LOW-MEDIUM) PRESSURE.pdf" },
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
      { slug: "hippo-pump", name: "Hippo", catalogue: "/Catalogue/Hippo.pdf" },
      { slug: "elephant", name: "Elephant", catalogue: "/Catalogue/Elephant.pdf" },
      { slug: "cub", name: "Cub", catalogue: "/Catalogue/cub.pdf" },
      { slug: "barrel-pump", name: "Barrel Pump", catalogue: "/Catalogue/Barrel Pump.pdf" },
      { slug: "portable-pressure-feed-pot", name: "Portable Pressure Feed Pot", catalogue: "/Catalogue/PORTABLE PRESSURE FEED POT.pdf" },
    ],
  },
  {
    slug: "dispensing-equipment-drum-press",
    name: "Dispensing Equipment - Drum Press",
    children: [
      { slug: "drum-press", name: "Drum Press", catalogue: "/Catalogue/DRUM PRESS.pdf" },
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
      { slug: "turbine-stirrer", name: "Turbine Stirrer", catalogue: "/Catalogue/turbine.pdf" },
      { slug: "pneumatic-stirrer", name: "Pneumatic Stirrer", catalogue: "/Catalogue/PNEUMATIC STIRRER.pdf" },
      { slug: "electrical-flame-proof-stirrer", name: "Electrical Flame Proof Stirrer" },
    ],
  },
  {
    slug: "accessories",
    name: "Accessories",
    children: [
      { slug: "valves", name: "Valves", catalogue: "/Catalogue/Valves.pdf" },
      { slug: "two-component-mixers", name: "Two Component Mixers" },
      { slug: "filters", name: "Filters", catalogue: "/Catalogue/filters.pdf" },
      { slug: "heating-accessories", name: "Heating Accessories" },
      { slug: "guns", name: "Guns" },
      {
        slug: "pressure-regulator",
        name: "Pressure Regulator",
        children: [
          { slug: "back-pressure-regulator", name: "Back Pressure Regulator" },
        ],
        catalogue: "/Catalogue/regulator.pdf",
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
    image: null,
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
    image: null,
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
    image: null,
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
    image: null,
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
    image: null,
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
    image: null,
  },
];

export function findBlogPost(slug: string) {
  return blogPosts.find((post) => post.slug === slug);
}
