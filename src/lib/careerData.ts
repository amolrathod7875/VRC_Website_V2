/**
 * Career listing data.
 *
 * Single source of truth for the VR Coatings careers page. The card grid,
 * department filters and opening count all derive from this array.
 *
 * Schema notes:
 *   - `summary` (string): compact 25-45 word role summary shown on the
 *     collapsed card. The long `description`/`sections` content is reserved
 *     for the expanded View Details panel.
 *   - `locations` (string[]): multi-location roles. `location` is the
 *     primary/summary string used on the card; `locations` lists every
 *     open city for the View Details section.
 *   - `salary` is optional. When absent the Salary block is hidden.
 *   - `posted` is optional. When absent the posted-date chip is hidden.
 *   - `sections` (long-form structured blocks) render only inside the
 *     expanded View Details panel.
 */

export type EmploymentType = "Full-time" | "Internship" | "Part-time" | "Contract";

export type JobSection = {
  title: string;
  items: string[];
};

export type CareerRole = {
  id: string;
  title: string;
  department: string;
  location: string;
  locations?: string[];
  type: EmploymentType;
  experience: string;
  salary?: string;
  qualification: string;
  posted?: string;
  summary: string;
  description: string;
  skills: string[];
  responsibilities?: string[];
  fullDescription?: string;
  sections?: JobSection[];
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
    id: "sales-engineer",
    title: "Sales Engineer",
    department: "Sales",
    location: "Multiple Locations",
    locations: ["Pune", "Chennai", "Bangalore", "Ahmedabad", "Delhi NCR"],
    type: "Full-time",
    experience: "2–5 years",
    salary: "3.5–6 LPA",
    qualification: "B.E. / MBA / Any Graduate",
    posted: "15 Mar 2026",
    summary:
      "Expand our industrial client base across multiple regions in India as a B2B sales professional, generating leads, negotiating industrial product deals and building long-term customer relationships.",
    description:
      "We are looking for a driven Sales Engineer to expand our industrial client base across multiple regions in India.",
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
    summary:
      "Design and develop mechanical components for our spray equipment range using SolidWorks and AutoCAD, working with the R&D team on product improvements, new product development and prototype coordination.",
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
    summary:
      "Manage daily operations at our Bhosari manufacturing facility, overseeing production planning, team management, quality control and shop-floor execution to meet delivery commitments.",
    description:
      "We are looking for an experienced Production Supervisor to manage daily operations at our Bhosari manufacturing facility.",
    skills: ["Production Planning", "Team Management", "Quality Control", "ERP/SAP", "5S / Lean"],
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
    summary:
      "Support day-to-day HR operations at VR Coatings, managing recruitment, onboarding, payroll and employee communication as the first point of contact for HR queries.",
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
    summary:
      "Support digital marketing, social media and content creation for an established industrial company, ideal for marketing students looking for hands-on experience.",
    description:
      "Exciting internship opportunity for marketing students to work on digital marketing, social media, and content creation for an established industrial company.",
    skills: ["Social Media", "Content Writing", "Canva", "MS Office", "Google Analytics"],
  },
  {
    id: "ppc-engineer",
    title: "PPC Engineer",
    department: "Production",
    location: "Pune",
    type: "Full-time",
    experience: "3–5 years",
    qualification:
      "Diploma / B.E. / B.Tech. – Mechanical / Production / Industrial Engineering",
summary:
      "Plan and control production schedules, materials and capacity using SAP-based production planning to support timely customer deliveries.",
    description:
      "The PPC Engineer will be responsible for planning, scheduling, monitoring and controlling production activities to ensure timely completion of customer orders while optimising manpower, machine capacity and material availability.",
    skills: ["PPC", "SAP", "MRP", "Capacity Planning", "Production Scheduling", "BOM / Routing"],
    sections: [
      {
        title: "Job Description",
        items: [
          "The PPC Engineer will be responsible for planning, scheduling, monitoring and controlling production activities to ensure timely completion of customer orders while optimising manpower, machine capacity and material availability.",
        ],
      },
      {
        title: "Key Responsibilities",
        items: [
          "Prepare daily, weekly and monthly production plans based on customer requirements and available capacity.",
          "Create and monitor production orders and schedules in SAP.",
          "Coordinate with Production, Stores, Purchase, Quality, Design and Dispatch for smooth production flow.",
          "Check material availability and identify shortages before production commencement.",
          "Monitor machine and manpower capacity and plan production accordingly.",
          "Track production progress against planned quantities and delivery schedules.",
          "Identify production delays, bottlenecks and capacity constraints.",
          "Monitor WIP and ensure timely movement of materials between processes.",
          "Coordinate with Stores and Purchase for timely availability of raw materials and bought-out components.",
          "Prepare daily, weekly and monthly PPC reports.",
          "Analyse plan vs. actual production and identify reasons for deviations.",
          "Maintain and monitor BOMs, routings, production orders and manufacturing lead times in SAP.",
          "Coordinate priority orders and delivery commitments with Sales and Production.",
          "Ensure accuracy and timely updating of PPC data in SAP.",
          "Support continuous improvement initiatives to reduce production lead times and improve machine and manpower utilisation.",
          "Provide management with production MIS, capacity reports and other planning-related information.",
        ],
      },
      {
        title: "Preferred Candidate Profile",
        items: [
          "Educational Qualification: Diploma / B.E. / B.Tech. in Mechanical Engineering, Production Engineering, Industrial Engineering or equivalent.",
          "UG Accepted: B.Tech / B.E. in Mechanical Engineering, Mechatronics, Manufacturing Engineering, Diploma in Mechanical Engineering, Mechatronics Engineering, Automobile Engineering.",
          "Experience Required: 3–5 years of relevant experience in Production Planning & Control in a manufacturing environment.",
          "Preferred Experience: Machine-shop manufacturing, Assembly manufacturing, SAP/ERP-based production planning.",
        ],
      },
      {
        title: "Technical Skills",
        items: [
          "Production Planning & Control (PPC)",
          "Production Scheduling",
          "Capacity Planning",
          "Material Requirement Planning (MRP)",
          "BOM",
          "Routing",
          "Production Orders",
          "SAP",
          "SAP S/4HANA",
          "SAP PP/MM",
          "Inventory Planning",
          "Material Availability Planning",
          "MS Excel",
          "Production Reporting",
          "CNC",
          "VMC",
          "Turning",
          "Milling",
          "Grinding",
          "Fabrication",
          "Assembly",
        ],
      },
      {
        title: "Other Requirements",
        items: [
          "Strong analytical and problem-solving skills",
          "Good communication and coordination skills",
          "Ability to coordinate with Production, Purchase, Stores, Quality, Design, Sales and Dispatch",
          "Ability to work under production deadlines",
          "Good understanding of shop-floor operations",
          "Good understanding of manufacturing lead times",
        ],
      },
    ],
  },
  {
    id: "sr-engineer-electrical-automation",
    title: "Sr. Engineer - Electrical & Automation",
    department: "Engineering",
    location: "Pune",
    type: "Full-time",
    experience: "6–10 years",
    qualification:
      "Degree / Diploma – Electrical / Electronics / Instrumentation / Automation",
    summary:
      "Lead electrical design, PLC/HMI/SCADA programming, machine automation, panel engineering, commissioning and technical support for industrial machine projects from concept design through customer-site commissioning.",
    description:
      "Sr. Engineer - Electrical & Automation is responsible for leading electrical design, control system development, PLC programming, panel engineering, machine automation, commissioning, and technical support activities for industrial machine manufacturing projects. The role includes complete responsibility from concept design to final machine commissioning at customer site.",
    skills: [
      "PLC",
      "Siemens TIA Portal",
      "HMI / SCADA",
      "Servo",
      "VFD",
      "AutoCAD Electrical",
    ],
    sections: [
      {
        title: "Job Description",
        items: [
          "Sr. Engineer - Electrical & Automation is responsible for leading electrical design, control system development, PLC programming, panel engineering, machine automation, commissioning, and technical support activities for industrial machine manufacturing projects.",
          "The role includes complete responsibility from concept design to final machine commissioning at customer site.",
        ],
      },
      {
        title: "Electrical Design & Engineering",
        items: [
          "Lead electrical design activities for industrial machines and automation systems.",
          "Prepare electrical schematics, GA drawings, IO lists, cable schedules, and BOM.",
          "Design control panels including MCC, PCC, PLC, VFD, and remote IO panels.",
          "Select electrical components such as PLC, HMI, servo systems, sensors, relays, safety devices, and field instruments.",
          "Ensure electrical design compliance with industrial standards and customer specifications.",
        ],
      },
      {
        title: "Automation & Control Systems",
        items: [
          "Develop and troubleshoot PLC, HMI, SCADA, and servo control programs.",
          "Integrate VFDs, servo drives, safety PLCs, and industrial communication systems.",
          "Handle machine sequencing, interlocks, alarms, recipe management, and data logging systems.",
          "Support motion control and synchronized automation applications.",
          "Maintain program backup and software revision control.",
        ],
      },
      {
        title: "Machine Manufacturing Support",
        items: [
          "Coordinate with mechanical, production, and assembly teams during machine manufacturing.",
          "Support panel wiring, machine wiring, and FAT activities.",
          "Resolve electrical and automation issues during machine assembly.",
          "Ensure machine readiness as per project schedule.",
        ],
      },
      {
        title: "Commissioning & Customer Support",
        items: [
          "Lead machine installation and commissioning activities at customer site.",
          "Conduct machine trials, tuning, and production validation.",
          "Provide customer training for machine operation and maintenance.",
          "Support troubleshooting during warranty and after-sales service period.",
          "Coordinate with customers for technical discussions and modification requirements.",
        ],
      },
      {
        title: "Project Management",
        items: [
          "Plan and monitor electrical and automation project timelines.",
          "Coordinate with vendors for procurement of electrical and automation components.",
          "Ensure project execution within budget and delivery schedule.",
          "Prepare project documentation and technical reports.",
        ],
      },
      {
        title: "Team Management",
        items: [
          "Lead electrical design engineers, PLC programmers, technicians, and commissioning engineers.",
          "Allocate project responsibilities and monitor team performance.",
          "Conduct technical training and skill development activities.",
          "Ensure proper documentation and engineering standards within department.",
        ],
      },
      {
        title: "Required Technical Skills",
        items: [
          "Industrial machine electrical systems",
          "PLC Programming",
          "PLC Troubleshooting",
          "HMI",
          "SCADA",
          "Servo Systems",
          "Motion Control",
          "VFD Systems",
          "Electrical Drawings",
          "Control Schematics",
          "Panel Manufacturing",
          "Machine Wiring",
          "Industrial Communication Protocols: Modbus, Profinet, Ethernet/IP, Profibus, CANopen",
          "Software / Platforms: Siemens TIA Portal, Allen-Bradley Studio 5000, Mitsubishi GX Works, Omron, AutoCAD Electrical, EPLAN",
          "Servo Experience: Mitsubishi, Panasonic, Festo",
          "Additional Knowledge: Machine safety systems, Electrical standards, Industrial automation, FAT, Commissioning",
        ],
      },
    ],
  },
];

export function getRoleById(id: string): CareerRole | undefined {
  return roles.find((role) => role.id === id);
}

export function listDepartments(): string[] {
  const present = new Set(roles.map((role) => role.department));
  return DEPARTMENTS.filter((dept) => present.has(dept));
}
