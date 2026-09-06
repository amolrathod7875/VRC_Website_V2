export type FaqItem = { q: string; a: string };
export type FaqCategory = { title: string; questions: FaqItem[] };

export const FAQ_VISIBLE = 6;

export const faqCategories: FaqCategory[] = [
  {
    title: "General",
    questions: [
      {
        q: "What does VR Coatings do?",
        a: "We manufacture and export dispensing machines, spray painting equipment, pumps, and fluid handling systems.",
      },
      {
        q: "Where is VR Coatings based?",
        a: "Our HQ and plant are in Pune, India, with a German subsidiary (DOT) for global operations.",
      },
      {
        q: "How long has VR Coatings been in business?",
        a: "We've been serving industries with innovative coating and dispensing solutions for over 30 years.",
      },
      {
        q: "Which industries use your products?",
        a: "Automotive, railways, aerospace, heavy engineering, adhesives & sealants, electronics, pharma, and more.",
      },
      {
        q: "Do you serve both large enterprises and small businesses?",
        a: "Yes, we work with OEMs, Tier-1s, SMEs, and specialized manufacturers.",
      },
      {
        q: "Are your machines made in India?",
        a: "Yes, our machines are designed and manufactured in India with German collaboration.",
      },
      {
        q: "Do you have international certifications?",
        a: "Yes, our systems comply with CE and other industry standards.",
      },
      {
        q: "Do you have a German office?",
        a: "Yes, through DOT (Germany), ensuring fast support across Europe.",
      },
      {
        q: "Do you attend exhibitions or trade shows?",
        a: "Yes, we regularly participate in global industrial summits and expos.",
      },
      {
        q: "What makes VR Coatings unique?",
        a: "Customized engineering, robust after-sales support, and proven global trust.",
      },
    ],
  },
  {
    title: "Products & Solutions",
    questions: [
      {
        q: "What types of spray painting equipment do you offer?",
        a: "Airless systems, electrostatic spray guns, auto painting machines, and complete solutions.",
      },
      {
        q: "Do you provide cartridge filling systems?",
        a: "Yes, we offer cartridge fillers for adhesives, sealants, and other materials.",
      },
      {
        q: "What are your dispensing machines used for?",
        a: "For accurate metering, mixing, and dispensing of adhesives, sealants, and coatings.",
      },
      {
        q: "What are transfer pumps used for?",
        a: "They handle viscous materials like sealants, paints, and adhesives with high efficiency.",
      },
      {
        q: "Do you offer hydraulic dosing systems?",
        a: "Yes, we provide hydraulic and pneumatic dosers for precision applications.",
      },
      {
        q: "Do you supply spares and consumables?",
        a: "Yes, we stock spares and consumables for long-term machine support.",
      },
      {
        q: "Do you manufacture standard and customized machines?",
        a: "Yes, we offer both standard models and tailor-made solutions.",
      },
      {
        q: "Can your machines handle high-viscosity materials?",
        a: "Yes, our pumps and dosers are built for high-viscosity adhesives and coatings.",
      },
      {
        q: "Do you supply complete paint shop setups?",
        a: "Yes, we design and supply turnkey painting solutions.",
      },
      {
        q: "Can your machines integrate with automation lines?",
        a: "Yes, our systems can be integrated into robotic and automated production lines.",
      },
      {
        q: "Do you provide fluid handling solutions beyond coatings?",
        a: "Yes, we serve adhesives, sealants, resins, inks, and specialty chemicals.",
      },
      {
        q: "Are your products energy-efficient?",
        a: "Yes, our machines are designed for high efficiency and reduced wastage.",
      },
    ],
  },
  {
    title: "Sales & Exports",
    questions: [
      {
        q: "Do you export internationally?",
        a: "Yes, to Europe, Asia, Middle East, Africa, and beyond.",
      },
      {
        q: "Can I order directly from Germany?",
        a: "Yes, DOT Germany supports EU customers for faster delivery.",
      },
      {
        q: "Do you work with OEMs?",
        a: "Yes, we supply directly to OEMs and Tier-1 companies.",
      },
      {
        q: "Can I request a product demo?",
        a: "Yes, live or virtual demos are available.",
      },
      {
        q: "How can I request a quote?",
        a: "Fill out the inquiry form or email sales@vrcoatings.com.",
      },
      {
        q: "Do you handle bulk orders?",
        a: "Yes, we manage bulk, custom, and repeat orders globally.",
      },
      {
        q: "What are your delivery timelines?",
        a: "Lead times vary by product but are communicated clearly at order.",
      },
      {
        q: "Do you offer trial machines?",
        a: "In some cases, yes—contact our sales team for details.",
      },
      {
        q: "What are your payment terms?",
        a: "We offer flexible terms depending on project size and client profile.",
      },
      {
        q: "Do you have distributors abroad?",
        a: "Yes, we have partners in Europe, Asia, and other regions.",
      },
      {
        q: "Do you offer Incoterms flexibility (EXW, FOB, DDP)?",
        a: "Yes, we can ship as per your preferred Incoterms.",
      },
      {
        q: "Can I visit your plant before ordering?",
        a: "Yes, we welcome customer visits to our Pune facility.",
      },
    ],
  },
  {
    title: "Service & Support",
    questions: [
      {
        q: "Do you provide installation and commissioning?",
        a: "Yes, our engineers handle installation and setup at your site.",
      },
      {
        q: "Do you offer operator training?",
        a: "Yes, we train your staff to ensure smooth operation and safety.",
      },
      {
        q: "What kind of maintenance services do you provide?",
        a: "Preventive maintenance, breakdown support, and performance audits.",
      },
      {
        q: "Can I get remote support?",
        a: "Yes, we provide virtual troubleshooting and guidance.",
      },
      {
        q: "Do you provide annual maintenance contracts (AMC)?",
        a: "Yes, we offer flexible AMC packages for peace of mind.",
      },
      {
        q: "Do you provide spare parts support globally?",
        a: "Yes, we ship spares worldwide and ensure availability through DOT Germany.",
      },
      {
        q: "Do you provide a quick turnaround for repairs?",
        a: "Yes, our service teams ensure minimum downtime.",
      },
      {
        q: "Can you service competitor machines?",
        a: "Yes, in many cases we can repair or retrofit third-party systems.",
      },
      {
        q: "Do you provide safety compliance checks?",
        a: "Yes, we perform safety audits and ensure standards compliance.",
      },
      {
        q: "Do you provide warranty on products?",
        a: "Yes, all machines come with a standard warranty and extended options.",
      },
      {
        q: "Do you provide calibration services?",
        a: "Yes, we calibrate dosers, pumps, and spray systems for accuracy.",
      },
      {
        q: "How do I contact support?",
        a: "Email us at sales@vrcoatings.com or use the website contact form.",
      },
    ],
  },
];
