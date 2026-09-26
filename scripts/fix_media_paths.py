import re
import os
from pathlib import Path
from urllib.parse import quote

# Build actual storage file set
storage = Path('/home/vr-coatings/Desktop/website_V2/backend/storage')
actual_files = set()
for f in storage.rglob('*'):
    if f.is_file():
        rel = f.relative_to(storage)
        actual_files.add('/media/' + str(rel))

frontend = Path('/home/vr-coatings/Desktop/website_V2/frontend/src')

# Replacement rules: (pattern, replacement)
# Order matters - more specific first
replacements = [
    # About - missing About/ subdir
    ('/media/images/about/Global_Presence.png', '/media/images/about/About/Global_Presence.png'),
    ('/media/images/about/HEAD OFFICE.jpg', '/media/images/about/About/HEAD OFFICE.jpg'),
    ('/media/images/about/MANUFACTURING.jpg', '/media/images/about/About/MANUFACTURING.jpg'),
    ('/media/images/about/NORTH AMERICA.jpg', '/media/images/about/About/NORTH AMERICA.jpg'),
    ('/media/images/about/WAI MIDC.jpg', '/media/images/about/About/WAI MIDC.jpg'),
    
    # Applications - missing applications/ subdir
    ('/media/images/applications/automotive.jpg', '/media/images/applications/applications/automotive.jpg'),
    ('/media/images/applications/defence-aerospace.jpg', '/media/images/applications/applications/defence-aerospace.jpg'),
    ('/media/images/applications/electronics.jpg', '/media/images/applications/applications/electronics.jpg'),
    ('/media/images/applications/energy-process.jpg', '/media/images/applications/applications/energy-process.jpg'),
    ('/media/images/applications/infrastructure.jpg', '/media/images/applications/applications/infrastructure.jpg'),
    ('/media/images/applications/marine.jpg', '/media/images/applications/applications/marine.jpg'),
    
    # Blogs - missing BLOGS/ subdir
    ('/media/images/blogs/Blog_1.png', '/media/images/blogs/BLOGS/Blog_1.png'),
    ('/media/images/blogs/Blog_2.png', '/media/images/blogs/BLOGS/Blog_2.png'),
    ('/media/images/blogs/Blog_3.png', '/media/images/blogs/BLOGS/Blog_3.png'),
    ('/media/images/blogs/Blog_4.png', '/media/images/blogs/BLOGS/Blog_4.png'),
    ('/media/images/blogs/Blog_5.png', '/media/images/blogs/BLOGS/Blog_5.png'),
    ('/media/images/blogs/Blog_6.png', '/media/images/blogs/BLOGS/Blog_6.png'),
    
    # Certifications - missing certifications/ subdir
    ('/media/images/certifications/iso-9001-certificate.jpg', '/media/images/certifications/certifications/iso-9001-certificate.jpg'),
    ('/media/images/certifications/atex-acknowledgement.jpg', '/media/images/certifications/certifications/atex-acknowledgement.jpg'),
    ('/media/images/certifications/ce-certificate-of-conformity.jpg', '/media/images/certifications/certifications/ce-certificate-of-conformity.jpg'),
    ('/media/images/certifications/atex-eu-type-exam.jpg', '/media/images/certifications/certifications/atex-eu-type-exam.jpg'),
    
    # Clients - remove industry subdirs (Manufacturing, Automotive, etc.)
    # These are flat in storage
    ('/media/images/clients/Automotive/Ashok-Leyland.png', '/media/images/clients/Ashok-Leyland.png'),
    ('/media/images/clients/Automotive/BajajAutomotive.png', '/media/images/clients/BajajAutomotive.png'),
    ('/media/images/clients/Automotive/Daimler-Chrysler.png', '/media/images/clients/Daimler-Chrysler.png'),
    ('/media/images/clients/Automotive/EicherAutomotive.png', '/media/images/clients/EicherAutomotive.png'),
    ('/media/images/clients/Automotive/Farmtrac.png', '/media/images/clients/Farmtrac.png'),
    ('/media/images/clients/Automotive/FiatAutomotive.png', '/media/images/clients/FiatAutomotive.png'),
    ('/media/images/clients/Automotive/Ford.png', '/media/images/clients/Ford.png'),
    ('/media/images/clients/Automotive/General-Motors.png', '/media/images/clients/General-Motors.png'),
    ('/media/images/clients/Automotive/Godrej-Boyce.png', '/media/images/clients/Godrej-Boyce.png'),
    ('/media/images/clients/Automotive/HondaAutomotive-1.png', '/media/images/clients/HondaAutomotive-1.png'),
    ('/media/images/clients/Automotive/HondaAutomotive.png', '/media/images/clients/HondaAutomotive.png'),
    ('/media/images/clients/Automotive/Hyundai.png', '/media/images/clients/Hyundai.png'),
    ('/media/images/clients/Automotive/LTAutomotive.png', '/media/images/clients/LTAutomotive.png'),
    ('/media/images/clients/Automotive/Mahindra.png', '/media/images/clients/Mahindra.png'),
    ('/media/images/clients/Automotive/MercedesAutomotive.png', '/media/images/clients/MercedesAutomotive.png'),
    ('/media/images/clients/Automotive/Piaggio.png', '/media/images/clients/Piaggio.png'),
    ('/media/images/clients/Automotive/SurinAutomotive.png', '/media/images/clients/SurinAutomotive.png'),
    ('/media/images/clients/Automotive/TATAAutomotive.png', '/media/images/clients/TATAAutomotive.png'),
    ('/media/images/clients/Automotive/Tata-Motors.png', '/media/images/clients/Tata-Motors.png'),
    ('/media/images/clients/Automotive/Toyota.png', '/media/images/clients/Toyota.png'),
    ('/media/images/clients/Automotive/Vw.png', '/media/images/clients/Vw.png'),
    ('/media/images/clients/Defence & Aerospace/ArmyDefence.png', '/media/images/clients/ArmyDefence.png'),
    ('/media/images/clients/Defence & Aerospace/BSLShipyard.png', '/media/images/clients/BSLShipyard.png'),
    ('/media/images/clients/Defence & Aerospace/DDefence.png', '/media/images/clients/DDefence.png'),
    ('/media/images/clients/Defence & Aerospace/DRDODefence.png', '/media/images/clients/DRDODefence.png'),
    ('/media/images/clients/Defence & Aerospace/Defence-FactoryDefence.png', '/media/images/clients/Defence-FactoryDefence.png'),
    ('/media/images/clients/Defence & Aerospace/Defence-Shipyard.png', '/media/images/clients/Defence-Shipyard.png'),
    ('/media/images/clients/Defence & Aerospace/ISRODefence.png', '/media/images/clients/ISRODefence.png'),
    ('/media/images/clients/Defence & Aerospace/Indian-ArmyDefence.png', '/media/images/clients/Indian-ArmyDefence.png'),
    ('/media/images/clients/Electronics/ABBElectro.png', '/media/images/clients/ABBElectro.png'),
    ('/media/images/clients/Electronics/BHELElectronics.png', '/media/images/clients/BHELElectronics.png'),
    ('/media/images/clients/Electronics/Electrosteel-1.png', '/media/images/clients/Electrosteel-1.png'),
    ('/media/images/clients/Electronics/GKC.png', '/media/images/clients/GKC.png'),
    ('/media/images/clients/Electronics/HavellsElectro.png', '/media/images/clients/HavellsElectro.png'),
    ('/media/images/clients/Electronics/Twin-EngineersElectro.png', '/media/images/clients/Twin-EngineersElectro.png'),
    ('/media/images/clients/Electronics/ZaubaCorpElectro.png', '/media/images/clients/ZaubaCorpElectro.png'),
    ('/media/images/clients/Manufacturing/Anabond.png', '/media/images/clients/Anabond.png'),
    ('/media/images/clients/Manufacturing/BMTManufacture.png', '/media/images/clients/BMTManufacture.png'),
    ('/media/images/clients/Manufacturing/BelriseManufacture.png', '/media/images/clients/BelriseManufacture.png'),
    ('/media/images/clients/Manufacturing/Carro-IndiaManufacture.png', '/media/images/clients/Carro-IndiaManufacture.png'),
    ('/media/images/clients/Manufacturing/CumminsManufacture.png', '/media/images/clients/CumminsManufacture.png'),
    ('/media/images/clients/Manufacturing/DowManufacture.png', '/media/images/clients/DowManufacture.png'),
    ('/media/images/clients/Manufacturing/EnduranceManufacture.png', '/media/images/clients/EnduranceManufacture.png'),
    ('/media/images/clients/Manufacturing/Escort-Manufacture-1.png', '/media/images/clients/Escort-Manufacture-1.png'),
    ('/media/images/clients/Manufacturing/FleetGaurdManufacture.png', '/media/images/clients/FleetGaurdManufacture.png'),
    ('/media/images/clients/Manufacturing/GMManufacture.png', '/media/images/clients/GMManufacture.png'),
    ('/media/images/clients/Manufacturing/GSKManufacture.png', '/media/images/clients/GSKManufacture.png'),
    ('/media/images/clients/Manufacturing/General-MotorsManufacture.png', '/media/images/clients/General-MotorsManufacture.png'),
    ('/media/images/clients/Manufacturing/GlobalEngManufacture.png', '/media/images/clients/GlobalEngManufacture.png'),
    ('/media/images/clients/Manufacturing/GraniteManufacture.png', '/media/images/clients/GraniteManufacture.png'),
    ('/media/images/clients/Manufacturing/Jindal New Logo (1).jpg', '/media/images/clients/Jindal New Logo (1).jpg'),
    ('/media/images/clients/Manufacturing/JostsManufacture.png', '/media/images/clients/JostsManufacture.png'),
    ('/media/images/clients/Manufacturing/LeoManufacture.png', '/media/images/clients/LeoManufacture.png'),
    ('/media/images/clients/Manufacturing/LumaxManufacture.png', '/media/images/clients/LumaxManufacture.png'),
    ('/media/images/clients/Manufacturing/MSLManufacture.png', '/media/images/clients/MSLManufacture.png'),
    ('/media/images/clients/Manufacturing/Reliance-Manufacture.png', '/media/images/clients/Reliance-Manufacture.png'),
    ('/media/images/clients/Manufacturing/SpicerManufacture.png', '/media/images/clients/SpicerManufacture.png'),
    ('/media/images/clients/Manufacturing/SwathiEngManufacture.png', '/media/images/clients/SwathiEngManufacture.png'),
    ('/media/images/clients/Manufacturing/TMTLManufacture.png', '/media/images/clients/TMTLManufacture.png'),
    ('/media/images/clients/Manufacturing/Tata-Metaliks-1.png', '/media/images/clients/Tata-Metaliks-1.png'),
    ('/media/images/clients/Manufacturing/Toyota.png', '/media/images/clients/Toyota.png'),
    ('/media/images/clients/Manufacturing/VarrocManufacture.png', '/media/images/clients/VarrocManufacture.png'),
    ('/media/images/clients/Manufacturing/VolvoManufacture.png', '/media/images/clients/VolvoManufacture.png'),
    ('/media/images/clients/Manufacturing/WelspunCorp.png', '/media/images/clients/WelspunCorp.png'),
    ('/media/images/clients/Manufacturing/ZF-IndiaManufacture.png', '/media/images/clients/ZF-IndiaManufacture.png'),
    ('/media/images/clients/Manufacturing/bhushan.png', '/media/images/clients/bhushan.png'),
    ('/media/images/clients/Manufacturing/tata-steel.png', '/media/images/clients/tata-steel.png'),
    ('/media/images/clients/Manufacturing/tech-steel.png', '/media/images/clients/tech-steel.png'),
    ('/media/images/clients/Oil & Gas/b-L.png', '/media/images/clients/b-L.png'),
    ('/media/images/clients/Oil & Gas/conares.png', '/media/images/clients/conares.png'),
    ('/media/images/clients/Oil & Gas/indian-oil.png', '/media/images/clients/indian-oil.png'),
    ('/media/images/clients/Oil & Gas/jazeera.png', '/media/images/clients/jazeera.png'),
    ('/media/images/clients/Oil & Gas/man.png', '/media/images/clients/man.png'),
    ('/media/images/clients/Oil & Gas/msl.png', '/media/images/clients/msl.png'),
    ('/media/images/clients/Oil & Gas/psl.png', '/media/images/clients/psl.png'),
    ('/media/images/clients/Oil & Gas/welspun-corp.png', '/media/images/clients/welspun-corp.png'),
    ('/media/images/clients/Others/Ace-Construction.png', '/media/images/clients/Ace-Construction.png'),
    ('/media/images/clients/Others/AnweshaPackaging.png', '/media/images/clients/AnweshaPackaging.png'),
    ('/media/images/clients/Others/Aplapollo.png', '/media/images/clients/Aplapollo.png'),
    ('/media/images/clients/Others/BalmerPackaging.png', '/media/images/clients/BalmerPackaging.png'),
    ('/media/images/clients/Others/Cracker-Barrel.png', '/media/images/clients/Cracker-Barrel.png'),
    ('/media/images/clients/Others/DB-1.png', '/media/images/clients/DB-1.png'),
    ('/media/images/clients/Others/DM_Resources.png', '/media/images/clients/DM_Resources.png'),
    ('/media/images/clients/Others/Electrosteel.png', '/media/images/clients/Electrosteel.png'),
    ('/media/images/clients/Others/Essar.png', '/media/images/clients/Essar.png'),
    ('/media/images/clients/Others/Gcl.png', '/media/images/clients/Gcl.png'),
    ('/media/images/clients/Others/InsiderBiz.png', '/media/images/clients/InsiderBiz.png'),
    ('/media/images/clients/Others/JSL.png', '/media/images/clients/JSL.png'),
    ('/media/images/clients/Others/Kumar Containers Pvt. Ltd..png', '/media/images/clients/Kumar Containers Pvt. Ltd..png'),
    ('/media/images/clients/Others/MM BARELS Logo.webp', '/media/images/clients/MM BARELS Logo.webp'),
    ('/media/images/clients/Others/Meil-1.png', '/media/images/clients/Meil-1.png'),
    ('/media/images/clients/Others/Movers-and-Equipments.png', '/media/images/clients/Movers-and-Equipments.png'),
    ('/media/images/clients/Others/PARI-Automation.png', '/media/images/clients/PARI-Automation.png'),
    ('/media/images/clients/Others/Railway.png', '/media/images/clients/Railway.png'),
    ('/media/images/clients/Others/Ratnamani.png', '/media/images/clients/Ratnamani.png'),
    ('/media/images/clients/Others/Shipyard-3.png', '/media/images/clients/Shipyard-3.png'),
    ('/media/images/clients/Others/Siva Ram Barrel Industries Logo.webp', '/media/images/clients/Siva Ram Barrel Industries Logo.webp'),
    ('/media/images/clients/Others/Surya.png', '/media/images/clients/Surya.png'),
    ('/media/images/clients/Others/WMI.png', '/media/images/clients/WMI.png'),
    ('/media/images/clients/Others/genix-automation.png', '/media/images/clients/genix-automation.png'),
    
    # Logo
    ('/media/images/misc/VRC Logo_nobg (2).png', '/media/images/misc/logo/VRC Logo_nobg (2).png'),
    
    # Partners - missing partners/ subdir
    ('/media/images/partners/ASAHI_SUNAC.svg', '/media/images/partners/partners/ASAHI_SUNAC.svg'),
    ('/media/images/partners/timmer_logo_white_(14).svg', '/media/images/partners/partners/timmer_logo_white_(14).svg'),
    ('/media/images/partners/wst-logo-color.svg', '/media/images/partners/partners/wst-logo-color.svg'),
    
    # Products - Category_wise_products missing Product_png_s/ prefix
    ('/media/images/products/Category_wise_products/Barrel Pump/Barrel Transfer Pump 14419.jpg', '/media/images/products/Product_png_s/Category_wise_products/Barrel Transfer Pump 14419.jpg'),
    ('/media/images/products/Category_wise_products/Cheetah/Cheetah 14301.jpg', '/media/images/products/Product_png_s/Category_wise_products/Cheetah 14301.jpg'),
    ('/media/images/products/Category_wise_products/Cub/Cub pump.jpg', '/media/images/products/Product_png_s/Category_wise_products/Cub pump.jpg'),
    ('/media/images/products/Category_wise_products/Diaphragm Pump/Diaphragm pump.jpg', '/media/images/products/Product_png_s/Category_wise_products/Diaphragm pump.jpg'),
    ('/media/images/products/Category_wise_products/Elephant Pump/Elephant 14398.jpg', '/media/images/products/Product_png_s/Category_wise_products/Elephant 14398.jpg'),
    ('/media/images/products/Category_wise_products/Hippo Pump/Hippo 14311.jpg', '/media/images/products/Product_png_s/Category_wise_products/Hippo 14311.jpg'),
    ('/media/images/products/Category_wise_products/Leopard - ELECTRIC PUMP/Electric pump.jpg', '/media/images/products/Product_png_s/Category_wise_products/Electric pump.jpg'),
    ('/media/images/products/Category_wise_products/PFP DRAGON/PFP 4017.jpg', '/media/images/products/Product_png_s/Category_wise_products/PFP 4017.jpg'),
    ('/media/images/products/Category_wise_products/Polyurea/Polyurea.jpg', '/media/images/products/Product_png_s/Category_wise_products/Polyurea.jpg'),
    ('/media/images/products/Category_wise_products/Pressure Feed Pot/VRC 4295 (1).jpg', '/media/images/products/Product_png_s/Category_wise_products/VRC 4295 (1).jpg'),
    ('/media/images/products/Category_wise_products/Rhino Pump/Rhino 4040.jpg', '/media/images/products/Product_png_s/Category_wise_products/Rhino 4040.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/BLue (1).png', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/BLue (1).png'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Kingfisher gold gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Kingfisher gold gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Kingfisher silver gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Kingfisher silver gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Conventional Spray Painting Guns/Red (1).png', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Red (1).png'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/AM250 gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/AM250 gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Airless manual dispensing gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Airless manual dispensing gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Cartridge Gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Cartridge Gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/EXT Gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/EXT Gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Eagle gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Eagle gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Falcon gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Falcon gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/Pole Gun 14422 (1).jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Pole Gun 14422 (1).jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/VRC HAWK 8156 (1).jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/VRC HAWK 8156 (1).jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/airless manual spray gun VRIL.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/airless manual spray gun VRIL.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/Manual airless Spray Painting Guns/wax gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/wax gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/400B .jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/400B .jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/Automatic Dispensing gun VRIAD.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic Dispensing gun VRIAD.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/Automatic air assisted airless spray gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic air assisted airless spray gun.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/Automatic airless spray gun VRIA Alu.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic airless spray gun VRIA Alu.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/Automatic airless spray gun VRIA SS.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Automatic airless spray gun VRIA SS.jpg'),
    ('/media/images/products/Category_wise_products/Spray Painting Guns/automatic airless Spray Painting Guns/Holt melt Gun.jpg', '/media/images/products/Product_png_s/Category_wise_products/Spray Painting Guns/Holt melt Gun.jpg'),
    ('/media/images/products/Category_wise_products/Tiger Mini/VRC 4101.jpg', '/media/images/products/Product_png_s/Category_wise_products/VRC 4101.jpg'),
    ('/media/images/products/Category_wise_products/Tiger Pump/Tiger 14326.jpg', '/media/images/products/Product_png_s/Category_wise_products/Tiger 14326.jpg'),
    ('/media/images/products/Category_wise_products/Turbine Stirrer/Turbinr Stirrer.jpg', '/media/images/products/Product_png_s/Category_wise_products/Turbinr Stirrer.jpg'),
    ('/media/images/products/Category_wise_products/VRC MIX HP/VRCoatings 0964.jpg', '/media/images/products/Product_png_s/Category_wise_products/VRCoatings 0964.jpg'),
    ('/media/images/products/Category_wise_products/VRC MIX LP/VRC 4734.jpg', '/media/images/products/Product_png_s/Category_wise_products/VRC 4734.jpg'),
    
    # Filters - missing Product_png_s/ prefix and wrong dir name
    ('/media/images/products/filter/BAG TYPE INLINE FILTER .png', '/media/images/products/Product_png_s/BAG TYPE INLINE FILTER .png'),
    ('/media/images/products/filter/CARTRIDGE TYPE INLINE FILTER.png', '/media/images/products/Product_png_s/CARTRIDGE TYPE INLINE FILTER.png'),
    ('/media/images/products/filter/FILTER CASSETTE L145.jpg', '/media/images/products/Product_png_s/FILTER CASSETTE L145.jpg'),
    ('/media/images/products/filter/HIGH PRESSURE FILTER 450 bar.jpg', '/media/images/products/Product_png_s/HIGH PRESSURE FILTER 450 bar.jpg'),
    ('/media/images/products/filter/LOW PRESSURE FILTER (STAINLESS STEEL).png', '/media/images/products/Product_png_s/LOW PRESSURE FILTER (STAINLESS STEEL).png'),
    ('/media/images/products/filter/TIP FILTER ASSEMBLY.jpg', '/media/images/products/Product_png_s/TIP FILTER ASSEMBLY.jpg'),
]

# Also fix generic patterns
generic_replacements = [
    # Product image fallback in products/[slug]/page.tsx
    ('/media/images/products/Flamingo 11817.png', '/media/images/products/Flamingo 11817.png'),  # already correct
    ('/media/images/products/Hippo.png', '/media/images/products/Hippo.png'),  # already correct
]

def fix_file(path):
    content = path.read_text()
    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
    if content != original:
        path.write_text(content)
        return True
    return False

changed = []
for f in sorted(frontend.rglob('*')):
    if f.is_file() and f.suffix in ['.ts', '.tsx']:
        if fix_file(f):
            changed.append(f)

print(f'Fixed {len(changed)} files:')
for f in changed:
    print(f'  {f.relative_to(frontend)}')
