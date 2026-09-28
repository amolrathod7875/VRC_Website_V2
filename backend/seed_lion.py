import uuid
import asyncio
from datetime import datetime
from sqlalchemy import insert
from app.core.database import engine
from app.models.media_asset import MediaAsset
from app.models.product import Product, ProductVariant


async def seed_lion():
    async with engine.begin() as conn:
        catalogue_asset_id = uuid.uuid4()
        product_id = uuid.uuid4()
        variant_id = uuid.uuid4()

        await conn.execute(
            insert(MediaAsset).values(
                id=catalogue_asset_id,
                filename="LION_Catalogue.pdf",
                original_filename="LION_Catalogue.pdf",
                media_type="catalogue",
                mime_type="application/pdf",
                storage_path="catalogues/LION_Catalogue.pdf",
                public_url="/media/catalogues/LION_Catalogue.pdf",
                alt_text="LION Catalogue",
                title="LION Catalogue",
                size_bytes=1037899,
                checksum=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )

        await conn.execute(
            insert(Product).values(
                id=product_id,
                name="LION",
                slug="lion",
                category="Paint Transfer Pumps",
                subcategory=None,
                short_description="Hydraulic high-volume fluid transfer pump for continuous circulation and feeding duties.",
                description="LION is a hydraulically driven, high-volume industrial fluid-transfer pump designed for continuous circulation and feeding duties. Its 4000 cc theoretical displacement and recommended delivery of 60 L/min at 15 cycles make it suitable for centralized coating and process-fluid handling systems.",
                catalogue_asset_id=catalogue_asset_id,
                primary_image_asset_id=None,
                is_active=True,
                display_order=2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )

        await conn.execute(
            insert(ProductVariant).values(
                id=variant_id,
                product_id=product_id,
                model_number=None,
                name="LION",
                description="Hydraulic high-volume fluid transfer pump with 4000 cc theoretical displacement and 60 L/min recommended delivery.",
                display_order=0,
                technical_specs={
                    "type": "Hydraulic Fluid Transfer Pump",
                    "pressure_ratio": "0.14:1",
                    "hydraulic_motor_type": "D66 (Ø66)",
                    "hydraulic_capacity_per_cycle": "4000 cc",
                    "dimensions": "Ø 500 x 1600 HEIGHT",
                    "recommended_spray_volume": "60 L/Min @ 15 Cycles",
                    "oil_consumption_per_cycle": "0.59 L/Cycle",
                    "oil_flow_rate": "8.85 L/Min @ 10 Bar & 15 Cycles",
                    "maximum_oil_inlet_pressure": "120 Bar",
                    "maximum_fluid_outlet_pressure": "16.8 Bar @ 120 Bar Oil Inlet",
                    "maximum_fluid_temp": "(II 2G Ex h IIB T4 Gb)",
                    "wetted_parts": "Carbon Steel Chrome Plated Cylinder & Piston, Tungsten Carbide Seat, PTFE seal rings",
                    "weight": "~132 kg (net weight, std pump)",
                },
                features=[
                    "Hydraulic drive for stable, continuous industrial transfer duty",
                    "4000 cc theoretical hydraulic capacity per cycle",
                    "Recommended delivery of 60 L/min at 15 cycles",
                    "Maximum oil inlet pressure of 120 bar",
                    "Heavy-duty wetted parts with chrome-plated and carbide components",
                    "Floor-mounted construction for fixed industrial installations",
                ],
                applications=[
                    {
                        "title": "Bulk Paint & Coating Transfer",
                        "description": "High-volume movement of primers, topcoats and compatible coating materials between storage and process equipment.",
                    },
                    {
                        "title": "Central Paint-Kitchen Circulation",
                        "description": "Suitable for continuous circulation and feeding in centralized paint supply installations.",
                    },
                    {
                        "title": "Production-Line Fluid Feeding",
                        "description": "Feeds compatible process fluids to dispensing, coating or finishing stations where steady volume is required.",
                    },
                    {
                        "title": "Tank / Drum Unloading",
                        "description": "Supports transfer from bulk containers into day tanks, circulation loops or downstream process equipment.",
                    },
                ],
                image_asset_id=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )

        await conn.commit()
        print("LION seed data inserted successfully")


if __name__ == "__main__":
    asyncio.run(seed_lion())
