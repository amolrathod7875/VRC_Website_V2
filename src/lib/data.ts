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

export const clients = [
  "Apex Steel",
  "Northwind OEM",
  "Helios Auto",
  "Pinnacle Defence",
  "Orbit Electronics",
  "Delta Fabrication",
  "Summit Rail",
  "Blue Harbor Marine",
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

export const applications = [
  { slug: "automotive", name: "Automotive", text: "E-coat, primers, and durable topcoats for body and underbody parts." },
  { slug: "defence-aerospace", name: "Defence & Aerospace", text: "Spec-driven coatings for airframes, ground systems, and components." },
  { slug: "electronics", name: "Electronics", text: "Protective dielectric films for boards, housings, and connectors." },
  { slug: "infrastructure", name: "Infrastructure", text: "Bridges, tanks, and industrial structures requiring long-term barrier protection." },
  { slug: "marine", name: "Marine", text: "Hull, deck, and offshore steel protection in saline environments." },
  { slug: "energy", name: "Energy & Process", text: "Coatings for pipelines, refineries, and power generation assets." },
];

export const clientTabs = {
  Manufacturing: ["Apex Steel", "Delta Fabrication", "Summit Rail", "ForgeWorks Ltd."],
  Automotive: ["Helios Auto", "Northwind OEM", "Gearline Components"],
  "Defence & Aerospace": ["Pinnacle Defence", "AeroVector Systems", "Skyline Avionics"],
  Electronics: ["Orbit Electronics", "Nexus PCB", "Voltara Devices"],
  Others: ["Blue Harbor Marine", "Civic Infra Group"],
} as const;

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

export const certifications = [
  { name: "ISO 9001:2015", scope: "Quality management" },
  { name: "ISO 14001:2015", scope: "Environmental management" },
  { name: "IATF 16949", scope: "Automotive quality" },
  { name: "Qualicoat aligned", scope: "Architectural powder processes" },
];

export const presenceLocations = [
  { title: "Head Office", region: "Pune, India" },
  { title: "Manufacturing", region: "Chakan, India" },
  { title: "North America", region: "Troy, MI, USA" },
];

export const faqs = [
  {
    q: "Do you supply both liquid and powder coatings?",
    a: "Yes. VR Coatings manufactures protective liquids, industrial powders, and specialty systems for OEM and maintenance markets.",
  },
  {
    q: "Can products be custom-matched?",
    a: "Colour, gloss, and performance can be tailored after a technical review of substrate, process, and environment.",
  },
  {
    q: "Where can I download the catalog?",
    a: "Visit the Catalog page to request the current product catalog. A download placeholder is provided until the PDF is uploaded.",
  },
  {
    q: "How do I become a distributor?",
    a: "Use the Contact Us form and select Partnership as the inquiry type. Our commercial team will follow up.",
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
