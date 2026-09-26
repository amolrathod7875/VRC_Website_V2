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
  { name: "Tata Steel", industry: "Manufacturing", logo: "/media/images/clients/tata-steel.png", tier: 1, globalPriority: 1 },
  { name: "Tata Motors", industry: "Automotive", logo: "/media/images/clients/Tata-Motors.png", tier: 2, globalPriority: 2 },
  { name: "Toyota", industry: "Manufacturing", logo: "/media/images/clients/Toyota.png", tier: 1, globalPriority: 3 },
  { name: "Toyota Kirloskar", industry: "Automotive", logo: "/media/images/clients/Toyota.png", tier: 1, globalPriority: 4 },
  { name: "Mercedes", industry: "Automotive", logo: "/media/images/clients/MercedesAutomotive.png", tier: 1, globalPriority: 5 },
  { name: "Daimler Chrysler (Mercedes Benz)", industry: "Automotive", logo: "/media/images/clients/Daimler-Chrysler.png", tier: 2, globalPriority: 6 },
  { name: "Mahindra & Mahindra", industry: "Automotive", logo: "/media/images/clients/Mahindra.png", tier: 1, globalPriority: 7 },
  { name: "Honda", industry: "Automotive", logo: "/media/images/clients/HondaAutomotive.png", tier: 1, globalPriority: 8 },
  { name: "Honda Siel Cars", industry: "Automotive", logo: "/media/images/clients/HondaAutomotive-1.png", tier: 3, globalPriority: 9 },
  { name: "Hyundai Motors", industry: "Automotive", logo: "/media/images/clients/Hyundai.png", tier: 1, globalPriority: 10 },
  { name: "Bajaj", industry: "Automotive", logo: "/media/images/clients/BajajAutomotive.png", tier: 1, globalPriority: 11 },
  { name: "Volkswagen", industry: "Automotive", logo: "/media/images/clients/Vw.png", tier: 1, globalPriority: 12 },
  { name: "Ford Motors", industry: "Automotive", logo: "/media/images/clients/Ford.png", tier: 1, globalPriority: 13 },
  { name: "Fiat", industry: "Automotive", logo: "/media/images/clients/FiatAutomotive.png", tier: 2, globalPriority: 14 },
  { name: "Ashok Leyland", industry: "Automotive", logo: "/media/images/clients/Ashok-Leyland.png", tier: 1, globalPriority: 15 },
  { name: "General Motors", industry: "Automotive", logo: "/media/images/clients/General-Motors.png", tier: 1, globalPriority: 16 },
  { name: "GM", industry: "Manufacturing", logo: "/media/images/clients/GMManufacture.png", tier: 2, globalPriority: 17 },
  { name: "Indian Oil Corporation (IOC)", industry: "Oil & Gas", logo: "/media/images/clients/indian-oil.png", tier: 1, globalPriority: 18 },
  { name: "DRDO", industry: "Defence & Aerospace", logo: "/media/images/clients/DRDODefence.png", tier: 1, globalPriority: 19 },
  { name: "ISRO", industry: "Defence & Aerospace", logo: "/media/images/clients/ISRODefence.png", tier: 1, globalPriority: 20 },

  // ─── Global Priority 21–35: Major industrial brands ────────────────────
  { name: "Reliance", industry: "Manufacturing", logo: "/media/images/clients/Reliance-Manufacture.png", tier: 1, globalPriority: 21 },
  { name: "Cummins", industry: "Manufacturing", logo: "/media/images/clients/CumminsManufacture.png", tier: 1, globalPriority: 22 },
  { name: "Volvo", industry: "Manufacturing", logo: "/media/images/clients/VolvoManufacture.png", tier: 1, globalPriority: 23 },
  { name: "ABB", industry: "Electronics", logo: "/media/images/clients/ABBElectro.png", tier: 1, globalPriority: 24 },
  { name: "BHEL", industry: "Electronics", logo: "/media/images/clients/BHELElectronics.png", tier: 1, globalPriority: 25 },
  { name: "Dow", industry: "Manufacturing", logo: "/media/images/clients/DowManufacture.png", tier: 1, globalPriority: 26 },
  { name: "ZF India", industry: "Manufacturing", logo: "/media/images/clients/ZF-IndiaManufacture.png", tier: 1, globalPriority: 27 },
  { name: "Tata Metaliks", industry: "Manufacturing", logo: "/media/images/clients/Tata-Metaliks-1.png", tier: 1, globalPriority: 28 },
  { name: "Jindal", industry: "Manufacturing", logo: "/media/images/clients/Jindal New Logo (1).jpg", tier: 2, globalPriority: 29 },
  { name: "TATA", industry: "Automotive", logo: "/media/images/clients/TATAAutomotive.png", tier: 4, globalPriority: 30 },
  { name: "Varroc", industry: "Manufacturing", logo: "/media/images/clients/VarrocManufacture.png", tier: 2, globalPriority: 31 },
  { name: "Endurance", industry: "Manufacturing", logo: "/media/images/clients/EnduranceManufacture.png", tier: 2, globalPriority: 32 },
  { name: "Essar", industry: "Others", logo: "/media/images/clients/Essar.png", tier: 1, globalPriority: 33 },
  { name: "Welspun Corp", industry: "Manufacturing", logo: "/media/images/clients/WelspunCorp.png", tier: 1, globalPriority: 34 },
  { name: "Welspun Corp Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/welspun-corp.png", tier: 1, globalPriority: 35 },

  // ─── Global Priority 36–50: Established industrial companies ───────────
  { name: "Bhushan Steel", industry: "Manufacturing", logo: "/media/images/clients/bhushan.png", tier: 2, globalPriority: 36 },
  { name: "Godrej Boyce", industry: "Automotive", logo: "/media/images/clients/Godrej-Boyce.png", tier: 2, globalPriority: 37 },
  { name: "LT", industry: "Automotive", logo: "/media/images/clients/LTAutomotive.png", tier: 2, globalPriority: 38 },
  { name: "Maharashtra Seamless Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/msl.png", tier: 2, globalPriority: 39 },
  { name: "Balmer Lawrie & Co. Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/b-L.png", tier: 2, globalPriority: 40 },
  { name: "Havells", industry: "Electronics", logo: "/media/images/clients/HavellsElectro.png", tier: 1, globalPriority: 41 },
  { name: "Electrosteel", industry: "Electronics", logo: "/media/images/clients/Electrosteel-1.png", tier: 2, globalPriority: 42 },
  { name: "Electrosteel Castings Ltd.", industry: "Others", logo: "/media/images/clients/Electrosteel.png", tier: 1, globalPriority: 43 },
  { name: "Man Industries Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/man.png", tier: 2, globalPriority: 44 },
  { name: "PSL Ltd.", industry: "Oil & Gas", logo: "/media/images/clients/psl.png", tier: 2, globalPriority: 45 },
  { name: "Ratnamani Metals & Tubes Ltd.", industry: "Others", logo: "/media/images/clients/Ratnamani.png", tier: 1, globalPriority: 46 },
  { name: "Surya Roshni Ltd.", industry: "Others", logo: "/media/images/clients/Surya.png", tier: 1, globalPriority: 47 },
  { name: "Zauba Corp", industry: "Electronics", logo: "/media/images/clients/ZaubaCorpElectro.png", tier: 3, globalPriority: 48 },
  { name: "GKC", industry: "Electronics", logo: "/media/images/clients/GKC.png", tier: 3, globalPriority: 49 },
  { name: "Twin Engineers", industry: "Electronics", logo: "/media/images/clients/Twin-EngineersElectro.png", tier: 3, globalPriority: 50 },

  // ─── Global Priority 51–70: Industry-recognized companies ──────────────
  { name: "Piaggio", industry: "Automotive", logo: "/media/images/clients/Piaggio.png", tier: 3, globalPriority: 51 },
  { name: "ISMT Ltd.", industry: "Automotive", tier: 3, globalPriority: 52 },
  { name: "Eicher", industry: "Automotive", logo: "/media/images/clients/EicherAutomotive.png", tier: 3, globalPriority: 53 },
  { name: "Lumax", industry: "Manufacturing", logo: "/media/images/clients/LumaxManufacture.png", tier: 2, globalPriority: 54 },
  { name: "Escort", industry: "Manufacturing", logo: "/media/images/clients/Escort-Manufacture-1.png", tier: 2, globalPriority: 55 },
  { name: "BMT", industry: "Manufacturing", logo: "/media/images/clients/BMTManufacture.png", tier: 3, globalPriority: 56 },
  { name: "Spicer", industry: "Manufacturing", logo: "/media/images/clients/SpicerManufacture.png", tier: 2, globalPriority: 57 },
  { name: "Anabond", industry: "Manufacturing", logo: "/media/images/clients/Anabond.png", tier: 3, globalPriority: 58 },
  { name: "Belrise", industry: "Manufacturing", logo: "/media/images/clients/BelriseManufacture.png", tier: 3, globalPriority: 59 },
  { name: "Carro India", industry: "Manufacturing", logo: "/media/images/clients/Carro-IndiaManufacture.png", tier: 3, globalPriority: 60 },
  { name: "Tech Steel", industry: "Manufacturing", logo: "/media/images/clients/tech-steel.png", tier: 4, globalPriority: 61 },
  { name: "Swathi Eng", industry: "Manufacturing", logo: "/media/images/clients/SwathiEngManufacture.png", tier: 4, globalPriority: 62 },
  { name: "TMTL", industry: "Manufacturing", logo: "/media/images/clients/TMTLManufacture.png", tier: 4, globalPriority: 63 },
  { name: "General Motors", industry: "Manufacturing", logo: "/media/images/clients/General-MotorsManufacture.png", tier: 2, globalPriority: 64 },
  { name: "GSK", industry: "Manufacturing", logo: "/media/images/clients/GSKManufacture.png", tier: 2, globalPriority: 65 },
  { name: "Josts", industry: "Manufacturing", logo: "/media/images/clients/JostsManufacture.png", tier: 4, globalPriority: 66 },
  { name: "Leo", industry: "Manufacturing", logo: "/media/images/clients/LeoManufacture.png", tier: 4, globalPriority: 67 },
  { name: "Sivshakti Engineering", industry: "Manufacturing", tier: 4, globalPriority: 68 },
  { name: "MSL", industry: "Manufacturing", logo: "/media/images/clients/MSLManufacture.png", tier: 3, globalPriority: 69 },
  { name: "Fleet Gaurd", industry: "Manufacturing", logo: "/media/images/clients/FleetGaurdManufacture.png", tier: 3, globalPriority: 70 },

  // ─── Global Priority 71–90: Well-known within sectors ──────────────────
  { name: "Global Eng", industry: "Manufacturing", logo: "/media/images/clients/GlobalEngManufacture.png", tier: 3, globalPriority: 71 },
  { name: "Granite", industry: "Manufacturing", logo: "/media/images/clients/GraniteManufacture.png", tier: 4, globalPriority: 72 },
  { name: "Indian Army", industry: "Defence & Aerospace", logo: "/media/images/clients/Indian-ArmyDefence.png", tier: 1, globalPriority: 73 },
  { name: "Army", industry: "Defence & Aerospace", logo: "/media/images/clients/ArmyDefence.png", tier: 1, globalPriority: 74 },
  { name: "Defence Factory", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence-FactoryDefence.png", tier: 2, globalPriority: 75 },
  { name: "BSL", industry: "Defence & Aerospace", logo: "/media/images/clients/BSLShipyard.png", tier: 3, globalPriority: 76 },
  { name: "Defence", industry: "Defence & Aerospace", logo: "/media/images/clients/Defence-Shipyard.png", tier: 3, globalPriority: 77 },
  { name: "DDefence", industry: "Defence & Aerospace", logo: "/media/images/clients/DDefence.png", tier: 4, globalPriority: 78 },
  { name: "Conares (UAE)", industry: "Oil & Gas", logo: "/media/images/clients/conares.png", tier: 3, globalPriority: 79 },
  { name: "Al Jazeera Steel Products (Oman)", industry: "Oil & Gas", logo: "/media/images/clients/jazeera.png", tier: 4, globalPriority: 80 },
  { name: "APL Apollo", industry: "Others", logo: "/media/images/clients/Aplapollo.png", tier: 1, globalPriority: 81 },
  { name: "Gujarat Container Ltd.", industry: "Others", tier: 1, globalPriority: 82 },
  { name: "MM Barrel", industry: "Others", logo: "/media/images/clients/MM BARELS Logo.webp", tier: 3, globalPriority: 83 },
  { name: "Siva Ram Barrel Industries", industry: "Others", logo: "/media/images/clients/Siva Ram Barrel Industries Logo.webp", tier: 4, globalPriority: 84 },
  { name: "Movers and Equipments", industry: "Others", logo: "/media/images/clients/Movers-and-Equipments.png", tier: 3, globalPriority: 85 },
  { name: "Ace Construction", industry: "Others", logo: "/media/images/clients/Ace-Construction.png", tier: 2, globalPriority: 86 },
  { name: "Shipyard", industry: "Others", logo: "/media/images/clients/Shipyard-3.png", tier: 2, globalPriority: 87 },
  { name: "PARI Automation", industry: "Others", logo: "/media/images/clients/PARI-Automation.png", tier: 2, globalPriority: 88 },
  { name: "DM Resources", industry: "Others", logo: "/media/images/clients/DM_Resources.png", tier: 3, globalPriority: 89 },
  { name: "Anwesha Packaging", industry: "Others", logo: "/media/images/clients/AnweshaPackaging.png", tier: 2, globalPriority: 90 },

  // ─── Global Priority 91–109: Regional / specialized ────────────────────
  { name: "Balmer Packaging", industry: "Others", logo: "/media/images/clients/BalmerPackaging.png", tier: 2, globalPriority: 91 },
  { name: "Kumar Container Pvt. Ltd.", industry: "Others", logo: "/media/images/clients/Kumar Containers Pvt. Ltd..png", tier: 3, globalPriority: 92 },
  { name: "JSL", industry: "Others", logo: "/media/images/clients/JSL.png", tier: 3, globalPriority: 93 },
  { name: "Jindal Saw Ltd.", industry: "Others", tier: 1, globalPriority: 94 },
  { name: "Megha Engineering & Infrastructure Ltd. (MEIL)", industry: "Others", logo: "/media/images/clients/Meil-1.png", tier: 1, globalPriority: 95 },
  { name: "Hazira Pipe Mill Ltd.", industry: "Others", tier: 2, globalPriority: 96 },
  { name: "Insider Biz", industry: "Others", logo: "/media/images/clients/InsiderBiz.png", tier: 3, globalPriority: 97 },
  { name: "DB", industry: "Others", logo: "/media/images/clients/DB-1.png", tier: 3, globalPriority: 98 },
  { name: "GCL", industry: "Others", logo: "/media/images/clients/Gcl.png", tier: 3, globalPriority: 99 },
  { name: "Genix Automation", industry: "Others", logo: "/media/images/clients/genix-automation.png", tier: 3, globalPriority: 100 },
  { name: "Cracker Barrel", industry: "Others", logo: "/media/images/clients/Cracker-Barrel.png", tier: 2, globalPriority: 101 },
  { name: "Railway", industry: "Others", logo: "/media/images/clients/Railway.png", tier: 2, globalPriority: 102 },
  { name: "Royal Industrie", industry: "Others", tier: 4, globalPriority: 103 },
  { name: "Vinora Industrie", industry: "Others", tier: 4, globalPriority: 104 },
  { name: "Cetury Barrel", industry: "Others", tier: 4, globalPriority: 105 },
  { name: "WMI", industry: "Others", logo: "/media/images/clients/WMI.png", tier: 4, globalPriority: 106 },
  { name: "Diti Resource Pvt. Ltd.", industry: "Others", tier: 4, globalPriority: 107 },
  { name: "Surin", industry: "Automotive", logo: "/media/images/clients/SurinAutomotive.png", tier: 3, globalPriority: 108 },
  { name: "Farmtrac", industry: "Automotive", logo: "/media/images/clients/Farmtrac.png", tier: 3, globalPriority: 109 },
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