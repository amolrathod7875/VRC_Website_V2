export type Client =
  | {
      name: string;
      industry: string;
      logo: string;
      tier: BrandTier;
      globalPriority: number;
    }
  | {
      name: string;
      industry: string;
      logo?: undefined;
      tier: BrandTier;
      globalPriority: number;
    };

export type BrandTier = 1 | 2 | 3 | 4;

export const clientIndustries = [
  "Manufacturing",
  "Automotive",
  "Defence & Aerospace",
  "Electronics",
  "Oil & Gas",
  "Others",
] as const;

export const industryOrder: Record<string, number> = {
  Manufacturing: 0,
  Automotive: 1,
  "Defence & Aerospace": 2,
  Electronics: 3,
  "Oil & Gas": 4,
  Others: 5,
};

export function sortByGlobalPriority(clients: Client[]): Client[] {
  return [...clients].sort((a, b) => a.globalPriority - b.globalPriority);
}

export function sortByIndustryTier(clients: Client[]): Client[] {
  return [...clients].sort((a, b) => a.tier - b.tier);
}

export const clients: Client[] = [
  // ─── Global Priority 1–20: Most recognizable brands ─────────────────────
  { name: "Tata Steel", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/tata-steel.png", tier: 1, globalPriority: 1 },
  { name: "Tata Motors", industry: "Automotive", logo: "/media/images/clients/Automotive/Tata-Motors.png", tier: 2, globalPriority: 2 },
  { name: "Toyota", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Toyota.png", tier: 1, globalPriority: 3 },
  { name: "Toyota Kirloskar", industry: "Automotive", logo: "/media/images/clients/Automotive/Toyota.png", tier: 1, globalPriority: 4 },
  { name: "Mercedes", industry: "Automotive", logo: "/media/images/clients/Automotive/MercedesAutomotive.png", tier: 1, globalPriority: 5 },
  { name: "Daimler Chrysler (Mercedes Benz)", industry: "Automotive", logo: "/media/images/clients/Automotive/Daimler-Chrysler.png", tier: 2, globalPriority: 6 },
  { name: "Mahindra & Mahindra", industry: "Automotive", logo: "/media/images/clients/Automotive/Mahindra.png", tier: 1, globalPriority: 7 },
  { name: "Honda", industry: "Automotive", logo: "/media/images/clients/Automotive/HondaAutomotive.png", tier: 1, globalPriority: 8 },
  { name: "Honda Siel Cars", industry: "Automotive", logo: "/media/images/clients/Automotive/HondaAutomotive-1.png", tier: 3, globalPriority: 9 },
  { name: "Hyundai Motors", industry: "Automotive", logo: "/media/images/clients/Automotive/Hyundai.png", tier: 1, globalPriority: 10 },
  { name: "Bajaj", industry: "Automotive", logo: "/media/images/clients/Automotive/BajajAutomotive.png", tier: 1, globalPriority: 11 },
  { name: "Volkswagen", industry: "Automotive", logo: "/media/images/clients/Automotive/Vw.png", tier: 1, globalPriority: 12 },
  { name: "Ford Motors", industry: "Automotive", logo: "/media/images/clients/Automotive/Ford.png", tier: 1, globalPriority: 13 },
  { name: "Fiat", industry: "Automotive", logo: "/media/images/clients/Automotive/FiatAutomotive.png", tier: 2, globalPriority: 14 },
  { name: "Ashok Leyland", industry: "Automotive", logo: "/media/images/clients/Automotive/Ashok-Leyland.png", tier: 1, globalPriority: 15 },
  { name: "General Motors", industry: "Automotive", logo: "/media/images/clients/Automotive/General-Motors.png", tier: 1, globalPriority: 16 },
  { name: "GM", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/GMManufacture.png", tier: 2, globalPriority: 17 },
  { name: "Indian Oil Corporation (IOC)", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/indian-oil.png", tier: 1, globalPriority: 18 },
  { name: "DRDO", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/DRDODefence.png", tier: 1, globalPriority: 19 },
  { name: "ISRO", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/ISRODefence.png", tier: 1, globalPriority: 20 },

  // ─── Global Priority 21–35: Major industrial brands ────────────────────
  { name: "Reliance", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Reliance-Manufacture.png", tier: 1, globalPriority: 21 },
  { name: "Cummins", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/CumminsManufacture.png", tier: 1, globalPriority: 22 },
  { name: "Volvo", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/VolvoManufacture.png", tier: 1, globalPriority: 23 },
  { name: "ABB", industry: "Electronics", logo: "/media/images/clients/Electronics/ABBElectro.png", tier: 1, globalPriority: 24 },
  { name: "BHEL", industry: "Electronics", logo: "/media/images/clients/Electronics/BHELElectronics.png", tier: 1, globalPriority: 25 },
  { name: "Dow", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/DowManufacture.png", tier: 1, globalPriority: 26 },
  { name: "ZF India", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/ZF-IndiaManufacture.png", tier: 1, globalPriority: 27 },
  { name: "Tata Metaliks", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Tata-Metaliks-1.png", tier: 1, globalPriority: 28 },
  { name: "Jindal", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Jindal New Logo (1).jpg", tier: 2, globalPriority: 29 },
  { name: "TATA", industry: "Automotive", logo: "/media/images/clients/Automotive/TATAAutomotive.png", tier: 4, globalPriority: 30 },
  { name: "Varroc", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/VarrocManufacture.png", tier: 2, globalPriority: 31 },
  { name: "Endurance", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/EnduranceManufacture.png", tier: 2, globalPriority: 32 },
  { name: "Essar", industry: "Others", logo: "/media/images/clients/Others/Essar.png", tier: 1, globalPriority: 33 },
  { name: "Welspun Corp", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/WelspunCorp.png", tier: 1, globalPriority: 34 },
  { name: "Welspun Corp Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/welspun-corp.png", tier: 1, globalPriority: 35 },

  // ─── Global Priority 36–50: Established industrial companies ───────────
  { name: "Bhushan Steel", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/bhushan.png", tier: 2, globalPriority: 36 },
  { name: "Godrej Boyce", industry: "Automotive", logo: "/media/images/clients/Automotive/Godrej-Boyce.png", tier: 2, globalPriority: 37 },
  { name: "LT", industry: "Automotive", logo: "/media/images/clients/Automotive/LTAutomotive.png", tier: 2, globalPriority: 38 },
  { name: "Maharashtra Seamless Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/msl.png", tier: 2, globalPriority: 39 },
  { name: "Balmer Lawrie & Co. Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/b-L.png", tier: 2, globalPriority: 40 },
  { name: "Havells", industry: "Electronics", logo: "/media/images/clients/Electronics/HavellsElectro.png", tier: 1, globalPriority: 41 },
  { name: "Electrosteel", industry: "Electronics", logo: "/media/images/clients/Electronics/Electrosteel-1.png", tier: 2, globalPriority: 42 },
  { name: "Electrosteel Castings Ltd.", industry: "Others", logo: "/media/images/clients/Others/Electrosteel.png", tier: 1, globalPriority: 43 },
  { name: "Man Industries Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/man.png", tier: 2, globalPriority: 44 },
  { name: "PSL Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/psl.png", tier: 2, globalPriority: 45 },
  { name: "Ratnamani Metals & Tubes Ltd.", industry: "Others", logo: "/media/images/clients/Others/Ratnamani.png", tier: 1, globalPriority: 46 },
  { name: "Surya Roshni Ltd.", industry: "Others", logo: "/media/images/clients/Others/Surya.png", tier: 1, globalPriority: 47 },
  { name: "Zauba Corp", industry: "Electronics", logo: "/media/images/clients/Electronics/ZaubaCorpElectro.png", tier: 3, globalPriority: 48 },
  { name: "GKC", industry: "Electronics", logo: "/media/images/clients/Electronics/GKC.png", tier: 3, globalPriority: 49 },
  { name: "Twin Engineers", industry: "Electronics", logo: "/media/images/clients/Electronics/Twin-EngineersElectro.png", tier: 3, globalPriority: 50 },

  // ─── Global Priority 51–70: Industry-recognized companies ──────────────
  { name: "Piaggio", industry: "Automotive", logo: "/media/images/clients/Automotive/Piaggio.png", tier: 3, globalPriority: 51 },
  { name: "ISMT Ltd.", industry: "Automotive", tier: 3, globalPriority: 52 },
  { name: "Eicher", industry: "Automotive", logo: "/media/images/clients/Automotive/EicherAutomotive.png", tier: 3, globalPriority: 53 },
  { name: "Lumax", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/LumaxManufacture.png", tier: 2, globalPriority: 54 },
  { name: "Escort", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Escort-Manufacture-1.png", tier: 2, globalPriority: 55 },
  { name: "BMT", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/BMTManufacture.png", tier: 3, globalPriority: 56 },
  { name: "Spicer", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/SpicerManufacture.png", tier: 2, globalPriority: 57 },
  { name: "Anabond", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Anabond.png", tier: 3, globalPriority: 58 },
  { name: "Belrise", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/BelriseManufacture.png", tier: 3, globalPriority: 59 },
  { name: "Carro India", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/Carro-IndiaManufacture.png", tier: 3, globalPriority: 60 },
  { name: "Tech Steel", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/tech-steel.png", tier: 4, globalPriority: 61 },
  { name: "Swathi Eng", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/SwathiEngManufacture.png", tier: 4, globalPriority: 62 },
  { name: "TMTL", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/TMTLManufacture.png", tier: 4, globalPriority: 63 },
  { name: "General Motors", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/General-MotorsManufacture.png", tier: 2, globalPriority: 64 },
  { name: "GSK", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/GSKManufacture.png", tier: 2, globalPriority: 65 },
  { name: "Josts", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/JostsManufacture.png", tier: 4, globalPriority: 66 },
  { name: "Leo", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/LeoManufacture.png", tier: 4, globalPriority: 67 },
  { name: "Sivshakti Engineering", industry: "Manufacturing", tier: 4, globalPriority: 68 },
  { name: "MSL", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/MSLManufacture.png", tier: 3, globalPriority: 69 },
  { name: "Fleet Gaurd", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/FleetGaurdManufacture.png", tier: 3, globalPriority: 70 },

  // ─── Global Priority 71–90: Well-known within sectors ──────────────────
  { name: "Global Eng", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/GlobalEngManufacture.png", tier: 3, globalPriority: 71 },
  { name: "Granite", industry: "Manufacturing", logo: "/media/images/clients/Manufacturing/GraniteManufacture.png", tier: 4, globalPriority: 72 },
  { name: "Indian Army", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/Indian-ArmyDefence.png", tier: 1, globalPriority: 73 },
  { name: "Army", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/ArmyDefence.png", tier: 1, globalPriority: 74 },
  { name: "Defence Factory", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/Defence-FactoryDefence.png", tier: 2, globalPriority: 75 },
  { name: "BSL", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/BSLShipyard.png", tier: 3, globalPriority: 76 },
  { name: "Defence", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/Defence-Shipyard.png", tier: 3, globalPriority: 77 },
  { name: "DDefence", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence & Aerospace/DDefence.png", tier: 4, globalPriority: 78 },
  { name: "Conares (UAE)", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/conares.png", tier: 3, globalPriority: 79 },
  { name: "Al Jazeera Steel Products (Oman)", industry: "Oil & Gas", logo: "/media/images/clients/Oil & Gas/jazeera.png", tier: 4, globalPriority: 80 },
  { name: "APL Apollo", industry: "Others", logo: "/media/images/clients/Others/Aplapollo.png", tier: 1, globalPriority: 81 },
  { name: "Gujarat Container Ltd.", industry: "Others", tier: 1, globalPriority: 82 },
  { name: "MM Barrel", industry: "Others", logo: "/media/images/clients/Others/MM BARELS Logo.webp", tier: 3, globalPriority: 83 },
  { name: "Siva Ram Barrel Industries", industry: "Others", logo: "/media/images/clients/Others/Siva Ram Barrel Industries Logo.webp", tier: 4, globalPriority: 84 },
  { name: "Movers and Equipments", industry: "Others", logo: "/media/images/clients/Others/Movers-and-Equipments.png", tier: 3, globalPriority: 85 },
  { name: "Ace Construction", industry: "Others", logo: "/media/images/clients/Others/Ace-Construction.png", tier: 2, globalPriority: 86 },
  { name: "Shipyard", industry: "Others", logo: "/media/images/clients/Others/Shipyard-3.png", tier: 2, globalPriority: 87 },
  { name: "PARI Automation", industry: "Others", logo: "/media/images/clients/Others/PARI-Automation.png", tier: 2, globalPriority: 88 },
  { name: "DM Resources", industry: "Others", logo: "/media/images/clients/Others/DM_Resources.png", tier: 3, globalPriority: 89 },
  { name: "Anwesha Packaging", industry: "Others", logo: "/media/images/clients/Others/AnweshaPackaging.png", tier: 2, globalPriority: 90 },

  // ─── Global Priority 91–109: Regional / specialized ────────────────────
  { name: "Balmer Packaging", industry: "Others", logo: "/media/images/clients/Others/BalmerPackaging.png", tier: 2, globalPriority: 91 },
  { name: "Kumar Container Pvt. Ltd.", industry: "Others", logo: "/media/images/clients/Others/Kumar Containers Pvt. Ltd..png", tier: 3, globalPriority: 92 },
  { name: "JSL", industry: "Others", logo: "/media/images/clients/Others/JSL.png", tier: 3, globalPriority: 93 },
  { name: "Jindal Saw Ltd.", industry: "Others", tier: 1, globalPriority: 94 },
  { name: "Megha Engineering & Infrastructure Ltd. (MEIL)", industry: "Others", logo: "/media/images/clients/Others/Meil-1.png", tier: 1, globalPriority: 95 },
  { name: "Hazira Pipe Mill Ltd.", industry: "Others", tier: 2, globalPriority: 96 },
  { name: "Insider Biz", industry: "Others", logo: "/media/images/clients/Others/InsiderBiz.png", tier: 3, globalPriority: 97 },
  { name: "DB", industry: "Others", logo: "/media/images/clients/Others/DB-1.png", tier: 3, globalPriority: 98 },
  { name: "GCL", industry: "Others", logo: "/media/images/clients/Others/Gcl.png", tier: 3, globalPriority: 99 },
  { name: "Genix Automation", industry: "Others", logo: "/media/images/clients/Others/genix-automation.png", tier: 3, globalPriority: 100 },
  { name: "Cracker Barrel", industry: "Others", logo: "/media/images/clients/Others/Cracker-Barrel.png", tier: 2, globalPriority: 101 },
  { name: "Railway", industry: "Others", logo: "/media/images/clients/Others/Railway.png", tier: 2, globalPriority: 102 },
  { name: "Royal Industrie", industry: "Others", tier: 4, globalPriority: 103 },
  { name: "Vinora Industrie", industry: "Others", tier: 4, globalPriority: 104 },
  { name: "Cetury Barrel", industry: "Others", tier: 4, globalPriority: 105 },
  { name: "WMI", industry: "Others", logo: "/media/images/clients/Others/WMI.png", tier: 4, globalPriority: 106 },
  { name: "Diti Resource Pvt. Ltd.", industry: "Others", tier: 4, globalPriority: 107 },
  { name: "Surin", industry: "Automotive", logo: "/media/images/clients/Automotive/SurinAutomotive.png", tier: 3, globalPriority: 108 },
  { name: "Farmtrac", industry: "Automotive", logo: "/media/images/clients/Automotive/Farmtrac.png", tier: 3, globalPriority: 109 },
];

export const clientsByIndustry = clientIndustries.reduce((acc, ind) => {
  acc[ind] = sortByIndustryTier(clients.filter((c) => c.industry === ind));
  return acc;
}, {} as Record<(typeof clientIndustries)[number], Client[]>);

export const trustedClientNames = [
  "Tata Steel",
  "Toyota Kirloskar",
  "Mercedes",
  "Mahindra & Mahindra",
  "Cummins",
  "Indian Oil Corporation (IOC)",
  "DRDO",
] as const;

export function getTrustedClients(): Client[] {
  const byName = new Map(clients.map((c) => [c.name.toLowerCase(), c]));
  return trustedClientNames
    .map((name) => byName.get(name.toLowerCase()))
    .filter((c): c is Client => c !== undefined)
    .filter((c): c is Client & { logo: string } => "logo" in c && typeof c.logo === "string");
}

export const featuredClientNames = [
  "Mercedes",
  "Volkswagen",
  "ZF India",
  "Toyota",
  "Honda",
  "Hyundai Motors",
  "Volvo",
  "Ford Motors",
  "General Motors",
  "Fiat",
  "Piaggio",
  "Cummins",
  "ABB",
  "Dow",
  "Tata Steel",
  "Tata Motors",
  "Mahindra & Mahindra",
  "Indian Oil Corporation (IOC)",
  "DRDO",
  "ISRO",
  "Reliance",
  "BHEL",
  "Bajaj",
  "Ashok Leyland",
  "Mercedes",
  "Volkswagen",
  "ZF India",
  "Toyota",
  "Honda",
  "Hyundai Motors",
  "Volvo",
  "Ford Motors",
  "General Motors",
] as const;

export function getFeaturedClients(): Client[] {
  const byName = new Map(clients.map((c) => [c.name.toLowerCase(), c]));
  return featuredClientNames
    .map((name) => byName.get(name.toLowerCase()))
    .filter((c): c is Client => c !== undefined)
    .filter((c): c is Client & { logo: string } => "logo" in c && typeof c.logo === "string");
}