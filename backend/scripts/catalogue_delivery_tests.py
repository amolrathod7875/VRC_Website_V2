"""
Catalogue delivery tests for final 5 catalogues.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from app.core.database import async_session_factory
from app.rag.catalogue_resolver import CatalogueResolver
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_catalogue_delivery():
    async with async_session_factory() as db:
        resolver = CatalogueResolver(db)
        
        test_catalogues = [
            ("dragon", "dragon.pdf"),
            ("polyurea", "polyurea.pdf"),
            ("tube-varnish-coating-system", "TUBE VARNISH COATING SYSTEM.pdf"),
            ("vrc-mix-low-medium-pressure", "VRC MIX (LOW - MEDIUM) PRESSURE.pdf"),
            ("barrel-pump", "Barrel Pump.pdf"),
        ]
        
        print("=" * 60)
        print("CATALOGUE DELIVERY TESTS")
        print("=" * 60)
        
        for slug, expected_filename in test_catalogues:
            print(f"\n>>> Testing: {slug}")
            catalogues = await resolver.resolve(slug)
            
            if not catalogues:
                print(f"  FAIL: No catalogues resolved for {slug}")
                continue
            
            for cat in catalogues:
                doc_name = cat.get("document_name", "")
                url = cat.get("url", "")
                print(f"  Document: {doc_name}")
                print(f"  URL: {url}")
                
                if doc_name == expected_filename:
                    print(f"  PASS: Matches expected filename")
                else:
                    print(f"  FAIL: Expected {expected_filename}, got {doc_name}")
            
            if len(catalogues) > 1:
                print(f"  WARNING: Multiple catalogues returned ({len(catalogues)})")
        
        print("\n" + "=" * 60)
        print("CATALOGUE DELIVERY TESTS COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_catalogue_delivery())