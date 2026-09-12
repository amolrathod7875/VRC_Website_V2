/**
 * Career listing data.
 *
 * The three roles below are the original career listings. Their `title`,
 * `location` and `type` values are preserved byte-for-byte. The additional
 * fields (department, experience, salary, qualification, skills, description
 * and the supporting detail sections) are standard recruitment listing fields
 * used to render the redesigned premium cards. They contain no fabricated
 * company claims.
 */

export type EmploymentType = "Full-time" | "Internship" | "Part-time" | "Contract";

export type CareerRole = {
  id: string;
  title: string;
  department: string;
  location: string;
  type: EmploymentType;
  experience: string;
  salary: string;
  qualification: string;
  posted: string;
  description: string;
  skills: string[];
  responsibilities?: string[];
  requirements?: string[];
  preferredSkills?: string[];
  roleDescription?: string;
};

export const DEPARTMENTS = [
  "Engineering",
  "Sales",
  "Production",
  "IT",
  "HR",
  "Marketing",
] as const;

export const roles: CareerRole[] = [
  {
    id: "coatings-chemist",
    title: "Coatings Chemist",
    department: "Engineering",
    location: "Pune, India",
    type: "Full-time",
    experience: "3–5 years",
    salary: "4–7 LPA",
    qualification: "B.E. / B.Sc. (Chemistry / Chemical)",
    posted: "Posted 2 weeks ago",
    description:
      "Develop and refine coating formulations for protective, industrial and specialty systems. Work closely with manufacturing to ensure batch consistency and reliable field performance.",
    skills: ["Formulation", "Resin Systems", "QC Testing", "Technical Data Sheets"],
    responsibilities: [
      "Formulate and refine coating systems for protective, industrial and specialty applications.",
      "Support scale-up from lab batches to production volumes.",
      "Maintain formulation records and technical documentation.",
    ],
    requirements: [
      "B.E. or B.Sc. in Chemistry, Chemical Engineering or a related discipline.",
      "3–5 years of hands-on formulation or coatings R&D experience.",
      "Working knowledge of resin systems and curing chemistry.",
    ],
    preferredSkills: ["Epoxy Systems", "Polyurethane", "Lab Testing Equipment"],
    roleDescription:
      "The Coatings Chemist works inside our formulation group, turning substrate, climate and duty-cycle requirements into repeatable coating systems.",
  },
  {
    id: "application-engineer",
    title: "Application Engineer",
    department: "Engineering",
    location: "Troy, MI",
    type: "Full-time",
    experience: "2–5 years",
    salary: "5–8 LPA",
    qualification: "B.E. (Mechanical / Chemical)",
    posted: "Posted 1 week ago",
    description:
      "Support customers in selecting and applying spray equipment and coating systems. Provide on-site application guidance and troubleshoot field issues across the product range.",
    skills: ["Spray Systems", "Field Support", "Customer Training", "Troubleshooting"],
    responsibilities: [
      "Guide customers through spray equipment selection and system setup.",
      "Deliver on-site application training and technical support.",
      "Troubleshoot field application issues and recommend corrective actions.",
    ],
    requirements: [
      "B.E. in Mechanical, Chemical or a related engineering discipline.",
      "2–5 years in application engineering, field support or technical sales.",
      "Comfortable working on-site with spray and fluid handling equipment.",
    ],
    preferredSkills: ["Airless Systems", "2K Mixing", "Customer Demonstration"],
    roleDescription:
      "The Application Engineer is the technical link between our equipment range and the customer's production line, ensuring systems are specified and applied correctly.",
  },
  {
    id: "quality-analyst",
    title: "Quality Analyst",
    department: "Production",
    location: "Chakan Factory",
    type: "Full-time",
    experience: "1–3 years",
    salary: "3–5 LPA",
    qualification: "B.Sc. / Diploma (Quality)",
    posted: "Posted this week",
    description:
      "Perform film, adhesion and corrosion testing on incoming and finished batches. Maintain documented QC records and certification traceability across production runs.",
    skills: ["Film Testing", "Corrosion Testing", "Documentation", "ISO 9001"],
    responsibilities: [
      "Carry out film, adhesion and corrosion tests on incoming and finished batches.",
      "Record QC results and maintain certification traceability.",
      "Flag non-conforming material and coordinate corrective action.",
    ],
    requirements: [
      "B.Sc. or Diploma in a quality, chemical or materials discipline.",
      "1–3 years in manufacturing quality control.",
      "Familiarity with standard film and corrosion test methods.",
    ],
    preferredSkills: ["ISO 9001", "Lab Instrumentation", "Batch Records"],
    roleDescription:
      "The Quality Analyst works on the production floor, verifying that every batch meets documented film performance and traceability standards before release.",
  },
];

export function getRoleById(id: string): CareerRole | undefined {
  return roles.find((role) => role.id === id);
}

export function listDepartments(): string[] {
  const present = new Set(roles.map((role) => role.department));
  return DEPARTMENTS.filter((dept) => present.has(dept));
}