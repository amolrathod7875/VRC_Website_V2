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
  { name: "Tata Steel", industry: "Manufacturing", logo: "/client_list/Manufacturing/tata-steel.png", tier: 1, globalPriority: 1 },
  { name: "Tata Motors", industry: "Automotive", logo: "/client_list/Automotive/Tata-Motors.png", tier: 2, globalPriority: 2 },
  { name: "Toyota", industry: "Manufacturing", logo: "/client_list/Manufacturing/Toyota.png", tier: 1, globalPriority: 3 },
  { name: "Toyota Kirloskar", industry: "Automotive", logo: "/client_list/Automotive/Toyota.png", tier: 1, globalPriority: 4 },
  { name: "Mercedes", industry: "Automotive", logo: "/client_list/Automotive/MercedesAutomotive.png", tier: 1, globalPriority: 5 },
  { name: "Daimler Chrysler (Mercedes Benz)", industry: "Automotive", logo: "/client_list/Automotive/Daimler-Chrysler.png", tier: 2, globalPriority: 6 },
  { name: "Mahindra & Mahindra", industry: "Automotive", logo: "/client_list/Automotive/Mahindra.png", tier: 1, globalPriority: 7 },
  { name: "Honda", industry: "Automotive", logo: "/client_list/Automotive/HondaAutomotive.png", tier: 1, globalPriority: 8 },
  { name: "Honda Siel Cars", industry: "Automotive", logo: "/client_list/Automotive/HondaAutomotive-1.png", tier: 3, globalPriority: 9 },
  { name: "Hyundai Motors", industry: "Automotive", logo: "/client_list/Automotive/Hyundai.png", tier: 1, globalPriority: 10 },
  { name: "Bajaj", industry: "Automotive", logo: "/client_list/Automotive/BajajAutomotive.png", tier: 1, globalPriority: 11 },
  { name: "Volkswagen", industry: "Automotive", logo: "/client_list/Automotive/Vw.png", tier: 1, globalPriority: 12 },
  { name: "Ford Motors", industry: "Automotive", logo: "/client_list/Automotive/Ford.png", tier: 1, globalPriority: 13 },
  { name: "Fiat", industry: "Automotive", logo: "/client_list/Automotive/FiatAutomotive.png", tier: 2, globalPriority: 14 },
  { name: "Ashok Leyland", industry: "Automotive", logo: "/client_list/Automotive/Ashok-Leyland.png", tier: 1, globalPriority: 15 },
  { name: "General Motors", industry: "Automotive", logo: "/client_list/Automotive/General-Motors.png", tier: 1, globalPriority: 16 },
  { name: "GM", industry: "Manufacturing", logo: "/client_list/Manufacturing/GMManufacture.png", tier: 2, globalPriority: 17 },
  { name: "Indian Oil Corporation (IOC)", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/indian-oil.png", tier: 1, globalPriority: 18 },
  { name: "DRDO", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/DRDODefence.png", tier: 1, globalPriority: 19 },
  { name: "ISRO", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/ISRODefence.png", tier: 1, globalPriority: 20 },

  // ─── Global Priority 21–35: Major industrial brands ────────────────────
  { name: "Reliance", industry: "Manufacturing", logo: "/client_list/Manufacturing/Reliance-Manufacture.png", tier: 1, globalPriority: 21 },
  { name: "Cummins", industry: "Manufacturing", logo: "/client_list/Manufacturing/CumminsManufacture.png", tier: 1, globalPriority: 22 },
  { name: "Volvo", industry: "Manufacturing", logo: "/client_list/Manufacturing/VolvoManufacture.png", tier: 1, globalPriority: 23 },
  { name: "ABB", industry: "Electronics", logo: "/client_list/Electronics/ABBElectro.png", tier: 1, globalPriority: 24 },
  { name: "BHEL", industry: "Electronics", logo: "/client_list/Electronics/BHELElectronics.png", tier: 1, globalPriority: 25 },
  { name: "Dow", industry: "Manufacturing", logo: "/client_list/Manufacturing/DowManufacture.png", tier: 1, globalPriority: 26 },
  { name: "ZF India", industry: "Manufacturing", logo: "/client_list/Manufacturing/ZF-IndiaManufacture.png", tier: 1, globalPriority: 27 },
  { name: "Tata Metaliks", industry: "Manufacturing", logo: "/client_list/Manufacturing/Tata-Metaliks-1.png", tier: 1, globalPriority: 28 },
  { name: "Jindal", industry: "Manufacturing", logo: "/client_list/Manufacturing/Jindal New Logo (1).jpg", tier: 2, globalPriority: 29 },
  { name: "TATA", industry: "Automotive", logo: "/client_list/Automotive/TATAAutomotive.png", tier: 4, globalPriority: 30 },
  { name: "Varroc", industry: "Manufacturing", logo: "/client_list/Manufacturing/VarrocManufacture.png", tier: 2, globalPriority: 31 },
  { name: "Endurance", industry: "Manufacturing", logo: "/client_list/Manufacturing/EnduranceManufacture.png", tier: 2, globalPriority: 32 },
  { name: "Essar", industry: "Others", logo: "/client_list/Others/Essar.png", tier: 1, globalPriority: 33 },
  { name: "Welspun Corp", industry: "Manufacturing", logo: "/client_list/Manufacturing/WelspunCorp.png", tier: 1, globalPriority: 34 },
  { name: "Welspun Corp Ltd.", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/welspun-corp.png", tier: 1, globalPriority: 35 },

  // ─── Global Priority 36–50: Established industrial companies ───────────
  { name: "Bhushan Steel", industry: "Manufacturing", logo: "/client_list/Manufacturing/bhushan.png", tier: 2, globalPriority: 36 },
  { name: "Godrej Boyce", industry: "Automotive", logo: "/client_list/Automotive/Godrej-Boyce.png", tier: 2, globalPriority: 37 },
  { name: "LT", industry: "Automotive", logo: "/client_list/Automotive/LTAutomotive.png", tier: 2, globalPriority: 38 },
  { name: "Maharashtra Seamless Ltd.", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/msl.png", tier: 2, globalPriority: 39 },
  { name: "Balmer Lawrie & Co. Ltd.", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/b-L.png", tier: 2, globalPriority: 40 },
  { name: "Havells", industry: "Electronics", logo: "/client_list/Electronics/HavellsElectro.png", tier: 1, globalPriority: 41 },
  { name: "Electrosteel", industry: "Electronics", logo: "/client_list/Electronics/Electrosteel-1.png", tier: 2, globalPriority: 42 },
  { name: "Electrosteel Castings Ltd.", industry: "Others", logo: "/client_list/Others/Electrosteel.png", tier: 1, globalPriority: 43 },
  { name: "Man Industries Ltd.", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/man.png", tier: 2, globalPriority: 44 },
  { name: "PSL Ltd.", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/psl.png", tier: 2, globalPriority: 45 },
  { name: "Ratnamani Metals & Tubes Ltd.", industry: "Others", logo: "/client_list/Others/Ratnamani.png", tier: 1, globalPriority: 46 },
  { name: "Surya Roshni Ltd.", industry: "Others", logo: "/client_list/Others/Surya.png", tier: 1, globalPriority: 47 },
  { name: "Zauba Corp", industry: "Electronics", logo: "/client_list/Electronics/ZaubaCorpElectro.png", tier: 3, globalPriority: 48 },
  { name: "GKC", industry: "Electronics", logo: "/client_list/Electronics/GKC.png", tier: 3, globalPriority: 49 },
  { name: "Twin Engineers", industry: "Electronics", logo: "/client_list/Electronics/Twin-EngineersElectro.png", tier: 3, globalPriority: 50 },

  // ─── Global Priority 51–70: Industry-recognized companies ──────────────
  { name: "Piaggio", industry: "Automotive", logo: "/client_list/Automotive/Piaggio.png", tier: 3, globalPriority: 51 },
  { name: "ISMT Ltd.", industry: "Automotive", tier: 3, globalPriority: 52 },
  { name: "Eicher", industry: "Automotive", logo: "/client_list/Automotive/EicherAutomotive.png", tier: 3, globalPriority: 53 },
  { name: "Lumax", industry: "Manufacturing", logo: "/client_list/Manufacturing/LumaxManufacture.png", tier: 2, globalPriority: 54 },
  { name: "Escort", industry: "Manufacturing", logo: "/client_list/Manufacturing/Escort-Manufacture-1.png", tier: 2, globalPriority: 55 },
  { name: "BMT", industry: "Manufacturing", logo: "/client_list/Manufacturing/BMTManufacture.png", tier: 3, globalPriority: 56 },
  { name: "Spicer", industry: "Manufacturing", logo: "/client_list/Manufacturing/SpicerManufacture.png", tier: 2, globalPriority: 57 },
  { name: "Anabond", industry: "Manufacturing", logo: "/client_list/Manufacturing/Anabond.png", tier: 3, globalPriority: 58 },
  { name: "Belrise", industry: "Manufacturing", logo: "/client_list/Manufacturing/BelriseManufacture.png", tier: 3, globalPriority: 59 },
  { name: "Carro India", industry: "Manufacturing", logo: "/client_list/Manufacturing/Carro-IndiaManufacture.png", tier: 3, globalPriority: 60 },
  { name: "Tech Steel", industry: "Manufacturing", logo: "/client_list/Manufacturing/tech-steel.png", tier: 4, globalPriority: 61 },
  { name: "Swathi Eng", industry: "Manufacturing", logo: "/client_list/Manufacturing/SwathiEngManufacture.png", tier: 4, globalPriority: 62 },
  { name: "TMTL", industry: "Manufacturing", logo: "/client_list/Manufacturing/TMTLManufacture.png", tier: 4, globalPriority: 63 },
  { name: "General Motors", industry: "Manufacturing", logo: "/client_list/Manufacturing/General-MotorsManufacture.png", tier: 2, globalPriority: 64 },
  { name: "GSK", industry: "Manufacturing", logo: "/client_list/Manufacturing/GSKManufacture.png", tier: 2, globalPriority: 65 },
  { name: "Josts", industry: "Manufacturing", logo: "/client_list/Manufacturing/JostsManufacture.png", tier: 4, globalPriority: 66 },
  { name: "Leo", industry: "Manufacturing", logo: "/client_list/Manufacturing/LeoManufacture.png", tier: 4, globalPriority: 67 },
  { name: "Sivshakti Engineering", industry: "Manufacturing", tier: 4, globalPriority: 68 },
  { name: "MSL", industry: "Manufacturing", logo: "/client_list/Manufacturing/MSLManufacture.png", tier: 3, globalPriority: 69 },
  { name: "Fleet Gaurd", industry: "Manufacturing", logo: "/client_list/Manufacturing/FleetGaurdManufacture.png", tier: 3, globalPriority: 70 },

  // ─── Global Priority 71–90: Well-known within sectors ──────────────────
  { name: "Global Eng", industry: "Manufacturing", logo: "/client_list/Manufacturing/GlobalEngManufacture.png", tier: 3, globalPriority: 71 },
  { name: "Granite", industry: "Manufacturing", logo: "/client_list/Manufacturing/GraniteManufacture.png", tier: 4, globalPriority: 72 },
  { name: "Indian Army", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/Indian-ArmyDefence.png", tier: 1, globalPriority: 73 },
  { name: "Army", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/ArmyDefence.png", tier: 1, globalPriority: 74 },
  { name: "Defence Factory", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/Defence-FactoryDefence.png", tier: 2, globalPriority: 75 },
  { name: "BSL", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/BSLShipyard.png", tier: 3, globalPriority: 76 },
  { name: "Defence", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/Defence-Shipyard.png", tier: 3, globalPriority: 77 },
  { name: "DDefence", industry: "Defence & Aerospace", logo: "/client_list/Defence & Aerospace/DDefence.png", tier: 4, globalPriority: 78 },
  { name: "Conares (UAE)", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/conares.png", tier: 3, globalPriority: 79 },
  { name: "Al Jazeera Steel Products (Oman)", industry: "Oil & Gas", logo: "/client_list/Oil & Gas/jazeera.png", tier: 4, globalPriority: 80 },
  { name: "APL Apollo", industry: "Others", logo: "/client_list/Others/Aplapollo.png", tier: 1, globalPriority: 81 },
  { name: "Gujarat Container Ltd.", industry: "Others", tier: 1, globalPriority: 82 },
  { name: "MM Barrel", industry: "Others", logo: "/client_list/Others/MM BARELS Logo.webp", tier: 3, globalPriority: 83 },
  { name: "Siva Ram Barrel Industries", industry: "Others", logo: "/client_list/Others/Siva Ram Barrel Industries Logo.webp", tier: 4, globalPriority: 84 },
  { name: "Movers and Equipments", industry: "Others", logo: "/client_list/Others/Movers-and-Equipments.png", tier: 3, globalPriority: 85 },
  { name: "Ace Construction", industry: "Others", logo: "/client_list/Others/Ace-Construction.png", tier: 2, globalPriority: 86 },
  { name: "Shipyard", industry: "Others", logo: "/client_list/Others/Shipyard-3.png", tier: 2, globalPriority: 87 },
  { name: "PARI Automation", industry: "Others", logo: "/client_list/Others/PARI-Automation.png", tier: 2, globalPriority: 88 },
  { name: "DM Resources", industry: "Others", logo: "/client_list/Others/DM_Resources.png", tier: 3, globalPriority: 89 },
  { name: "Anwesha Packaging", industry: "Others", logo: "/client_list/Others/AnweshaPackaging.png", tier: 2, globalPriority: 90 },

  // ─── Global Priority 91–109: Regional / specialized ────────────────────
  { name: "Balmer Packaging", industry: "Others", logo: "/client_list/Others/BalmerPackaging.png", tier: 2, globalPriority: 91 },
  { name: "Kumar Container Pvt. Ltd.", industry: "Others", logo: "/client_list/Others/Kumar Containers Pvt. Ltd..png", tier: 3, globalPriority: 92 },
  { name: "JSL", industry: "Others", logo: "/client_list/Others/JSL.png", tier: 3, globalPriority: 93 },
  { name: "Jindal Saw Ltd.", industry: "Others", tier: 1, globalPriority: 94 },
  { name: "Megha Engineering & Infrastructure Ltd. (MEIL)", industry: "Others", logo: "/client_list/Others/Meil-1.png", tier: 1, globalPriority: 95 },
  { name: "Hazira Pipe Mill Ltd.", industry: "Others", tier: 2, globalPriority: 96 },
  { name: "Insider Biz", industry: "Others", logo: "/client_list/Others/InsiderBiz.png", tier: 3, globalPriority: 97 },
  { name: "DB", industry: "Others", logo: "/client_list/Others/DB-1.png", tier: 3, globalPriority: 98 },
  { name: "GCL", industry: "Others", logo: "/client_list/Others/Gcl.png", tier: 3, globalPriority: 99 },
  { name: "Genix Automation", industry: "Others", logo: "/client_list/Others/genix-automation.png", tier: 3, globalPriority: 100 },
  { name: "Cracker Barrel", industry: "Others", logo: "/client_list/Others/Cracker-Barrel.png", tier: 2, globalPriority: 101 },
  { name: "Railway", industry: "Others", logo: "/client_list/Others/Railway.png", tier: 2, globalPriority: 102 },
  { name: "Royal Industrie", industry: "Others", tier: 4, globalPriority: 103 },
  { name: "Vinora Industrie", industry: "Others", tier: 4, globalPriority: 104 },
  { name: "Cetury Barrel", industry: "Others", tier: 4, globalPriority: 105 },
  { name: "WMI", industry: "Others", logo: "/client_list/Others/WMI.png", tier: 4, globalPriority: 106 },
  { name: "Diti Resource Pvt. Ltd.", industry: "Others", tier: 4, globalPriority: 107 },
  { name: "Surin", industry: "Automotive", logo: "/client_list/Automotive/SurinAutomotive.png", tier: 3, globalPriority: 108 },
  { name: "Farmtrac", industry: "Automotive", logo: "/client_list/Automotive/Farmtrac.png", tier: 3, globalPriority: 109 },
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