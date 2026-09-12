/**
 * Career listing data.
 *
 * Single source of truth for the VR Coatings careers page. The card grid,
 * department filters and opening count all derive from this array.
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
  fullDescription?: string;
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
    id: "sales-executive",
    title: "Sales Executive",
    department: "Sales",
    location: "Pune",
    type: "Full-time",
    experience: "2–5 years",
    salary: "3.5–6 LPA",
    qualification: "B.E. / MBA / Any Graduate",
    posted: "15 Mar 2026",
    description:
      "We are looking for a driven Sales Executive to expand our industrial client base across Maharashtra and beyond.",
    skills: ["B2B Sales", "Lead Generation", "Industrial Products", "Negotiation", "MS Office"],
  },
  {
    id: "mechanical-design-engineer",
    title: "Mechanical Design Engineer",
    department: "Engineering",
    location: "Pune",
    type: "Full-time",
    experience: "1–4 years",
    salary: "4–8 LPA",
    qualification: "B.E. / Diploma in Mechanical Engineering",
    posted: "10 Mar 2026",
    description:
      "We seek a Mechanical Design Engineer to design and develop components for our spray equipment range. You will work with the R&D team on product improvements and new product development.",
    skills: ["SolidWorks", "AutoCAD", "GD&T", "Sheet Metal Design", "Manufacturing Processes"],
    responsibilities: [
      "Design mechanical components using SolidWorks / AutoCAD",
      "Prepare manufacturing drawings and BOMs",
      "Coordinate with production team for prototype development",
      "Conduct design reviews and FMEA analysis",
      "Support after-sales technical issues",
    ],
    fullDescription:
      "We seek a Mechanical Design Engineer to design and develop components for our spray equipment range. You will work with the R&D team on product improvements and new product development.",
  },
  {
    id: "production-supervisor",
    title: "Production Supervisor",
    department: "Production",
    location: "Pune (Bhosari)",
    type: "Full-time",
    experience: "3–7 years",
    salary: "4–7 LPA",
    qualification: "B.E. / Diploma in Mechanical / Production Engineering",
    posted: "08 Mar 2026",
    description:
      "We are looking for an experienced Production Supervisor to manage daily operations at our Bhosari manufacturing facility.",
    skills: ["Production Planning", "Team Management", "Quality Control", "ERP/SAP", "5S / Lean"],
  },
  {
    id: "web-developer-frontend",
    title: "Web Developer (Frontend)",
    department: "IT",
    location: "Pune / Remote",
    type: "Full-time",
    experience: "1–3 years",
    salary: "3–6 LPA",
    qualification: "B.E. / BCA / Any Computer Science degree",
    posted: "05 Mar 2026",
    description:
      "We are looking for a Frontend Web Developer to maintain and improve our company website and internal tools.",
    skills: ["HTML/CSS", "JavaScript", "Responsive Design", "SEO", "Git"],
  },
  {
    id: "hr-executive",
    title: "HR Executive",
    department: "HR",
    location: "Pune",
    type: "Full-time",
    experience: "1–3 years",
    salary: "2.5–4.5 LPA",
    qualification: "MBA HR / MSW / PGDM HR",
    posted: "01 Mar 2026",
    description:
      "We are hiring an HR Executive to manage recruitment, onboarding, and day-to-day HR operations at VR Coatings.",
    skills: ["Recruitment", "HRMS / Greytip", "Payroll", "MS Excel", "Communication"],
  },
  {
    id: "marketing-intern",
    title: "Marketing Intern",
    department: "Marketing",
    location: "Pune / Remote",
    type: "Internship",
    experience: "Fresher",
    salary: "8,000–12,000 / month",
    qualification: "BBA / MBA Marketing (Pursuing or Completed)",
    posted: "20 Feb 2026",
    description:
      "Exciting internship opportunity for marketing students to work on digital marketing, social media, and content creation for an established industrial company.",
    skills: ["Social Media", "Content Writing", "Canva", "MS Office", "Google Analytics"],
  },
];

export function getRoleById(id: string): CareerRole | undefined {
  return roles.find((role) => role.id === id);
}

export function listDepartments(): string[] {
  const present = new Set(roles.map((role) => role.department));
  return DEPARTMENTS.filter((dept) => present.has(dept));
}