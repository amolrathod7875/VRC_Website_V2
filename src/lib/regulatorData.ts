export type RegulatorSpec = {
  label: string;
  value: string;
};

export type RegulatorVariant = {
  id: string;
  name: string;
  image: string;
  alt: string;
  specifications: RegulatorSpec[];
  description?: string;
};

export const regulatorVariants: RegulatorVariant[] = [
  {
    id: "model-01",
    name: "MODEL 01 — TO BE POPULATED FROM PDF",
    image: "",
    alt: "Regulator Model 01",
    description: "Specifications to be extracted from regulator.pdf catalogue.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "—" },
      { label: "REGULATING PRESSURE RANGE", value: "—" },
      { label: "INLET PORT", value: "—" },
      { label: "OUTLET PORT", value: "—" },
      { label: "WETTED PARTS", value: "—" },
      { label: "BODY MATERIAL", value: "—" },
      { label: "SEAL MATERIAL", value: "—" },
    ],
  },
  {
    id: "model-02",
    name: "MODEL 02 — TO BE POPULATED FROM PDF",
    image: "",
    alt: "Regulator Model 02",
    description: "Specifications to be extracted from regulator.pdf catalogue.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "—" },
      { label: "REGULATING PRESSURE RANGE", value: "—" },
      { label: "INLET PORT", value: "—" },
      { label: "OUTLET PORT", value: "—" },
      { label: "WETTED PARTS", value: "—" },
      { label: "BODY MATERIAL", value: "—" },
      { label: "SEAL MATERIAL", value: "—" },
    ],
  },
  {
    id: "model-03",
    name: "MODEL 03 — TO BE POPULATED FROM PDF",
    image: "",
    alt: "Regulator Model 03",
    description: "Specifications to be extracted from regulator.pdf catalogue.",
    specifications: [
      { label: "MAXIMUM WORKING PRESSURE", value: "—" },
      { label: "REGULATING PRESSURE RANGE", value: "—" },
      { label: "INLET PORT", value: "—" },
      { label: "OUTLET PORT", value: "—" },
      { label: "WETTED PARTS", value: "—" },
      { label: "BODY MATERIAL", value: "—" },
      { label: "SEAL MATERIAL", value: "—" },
    ],
  },
];

export const regulatorCatalogue = {
  name: "REGULATOR",
  category: "Accessories / Pressure Regulator / Regulator",
  catalogue: "/Catalogue/regulator.pdf",
  description:
    "Complete range of pressure regulators for industrial fluid handling systems. Refer to the catalogue PDF for detailed model specifications, pressure ranges, and technical data.",
};