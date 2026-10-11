"""
Generate candidate chunks for final 5 catalogues (dry-run, no DB/Qdrant writes).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import hashlib
import json
import logging
from pathlib import Path
from datetime import timezone
from collections import Counter

from app.core.config import settings
from app.core.database import async_session_factory
from app.rag.ingestion.pdf_parser import extract_pages
from app.rag.ingestion.new_chunker import chunk_catalogue
from app.rag.ingestion.metadata_builder import build_catalogue_metadata
from app.rag.product_identity import get_canonical_slug
from app.rag.utils.ids import generate_document_id
from app.rag.config import rag_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATALOGUE_DIR = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues")

FINAL_DOCS = {
    "dragon.pdf": "dragon",
    "polyurea.pdf": "polyurea",
    "TUBE VARNISH COATING SYSTEM.pdf": "tube-varnish-coating-system",
    "VRC MIX (LOW - MEDIUM) PRESSURE.pdf": "vrc-mix-low-medium-pressure",
    "Barrel Pump.pdf": "barrel-pump",
}

TIGER_SUSPICIOUS_RATIOS = {"30:150", "35:70", "40:110", "45:150", "60:70", "60:110"}

def calculate_sha256(file_path: Path) -> str:
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def analyze_chunks(chunks, product_slug, sha256):
    """Analyze chunks for quality metrics."""
    total = len(chunks)
    technical = 0
    application = 0
    components = 0
    suspicious = 0
    duplicate_texts = set()
    dup_count = 0
    unresolved = 0
    variants = set()
    
    for chunk in chunks:
        text = chunk.get("text", "")
        meta = chunk.get("metadata", {})
        
        chunk_type = meta.get("chunk_type", "")
        if chunk_type == "technical_specs":
            technical += 1
        elif chunk_type == "application":
            application += 1
        elif chunk_type == "component":
            components += 1
            
        # Check for variants/configurations
        variant = meta.get("variant") or meta.get("configuration")
        if variant:
            variants.add(variant)
            
        # Check for suspicious Tiger ratios
        for ratio in TIGER_SUSPICIOUS_RATIOS:
            if ratio in text:
                suspicious += 1
                break
                
        # Duplicate detection
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        if text_hash in duplicate_texts:
            dup_count += 1
        else:
            duplicate_texts.add(text_hash)
            
        # Unresolved content (short or low quality)
        if len(text.strip()) < 50:
            unresolved += 1
            
    return {
        "total_chunks": total,
        "technical_chunks": technical,
        "application_chunks": application,
        "component_chunks": components,
        "suspicious_chunks": suspicious,
        "duplicate_chunks": dup_count,
        "unresolved_chunks": unresolved,
        "variants_configurations": sorted(list(variants)),
    }

async def generate_candidates(file_path: Path, product_slug: str) -> dict:
    document_name = file_path.name
    sha256 = calculate_sha256(file_path)
    
    logger.info(f"Processing {document_name} (sha256: {sha256[:16]}...)...")
    
    pages, ocr_results = extract_pages(str(file_path), enable_ocr=True)
    if not pages:
        return {"status": "failed", "reason": "No pages extracted"}
    
    document_id = generate_document_id()
    chunks = chunk_catalogue(document_name, pages, [], product_slug, document_id, ocr_results=ocr_results)
    if not chunks:
        return {"status": "failed", "reason": "No chunks generated"}
    
    analysis = analyze_chunks(chunks, product_slug, sha256)
    
    # Build detailed chunk info
    chunk_details = []
    for idx, chunk in enumerate(chunks):
        meta = chunk.get("metadata", {})
        chunk_details.append({
            "index": idx,
            "chunk_type": meta.get("chunk_type", "unknown"),
            "variant": meta.get("variant") or meta.get("configuration"),
            "text_preview": chunk.get("text", "")[:200],
            "has_table": meta.get("has_table", False),
        })
    
    return {
        "status": "candidate_generated",
        "document_name": document_name,
        "product_slug": product_slug,
        "sha256": sha256,
        "identity": product_slug,
        "total_pages": len(pages),
        "analysis": analysis,
        "chunk_details": chunk_details,
    }

async def main() -> None:
    logger.info("=" * 60)
    logger.info("GENERATING CANDIDATES FOR FINAL 5 CATALOGUES")
    logger.info("=" * 60)
    
    results = {}
    for doc_name, product_slug in FINAL_DOCS.items():
        file_path = CATALOGUE_DIR / doc_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            results[doc_name] = {"status": "not_found"}
            continue
        
        result = await generate_candidates(file_path, product_slug)
        results[doc_name] = result
        
        if result["status"] == "candidate_generated":
            a = result["analysis"]
            logger.info(f"  {doc_name}:")
            logger.info(f"    identity: {result['identity']}")
            logger.info(f"    sha256: {result['sha256'][:16]}...")
            logger.info(f"    total chunks: {a['total_chunks']}")
            logger.info(f"    technical: {a['technical_chunks']}, application: {a['application_chunks']}, components: {a['component_chunks']}")
            logger.info(f"    variants: {a['variants_configurations']}")
            logger.info(f"    suspicious: {a['suspicious_chunks']}, duplicates: {a['duplicate_chunks']}, unresolved: {a['unresolved_chunks']}")
    
    # Save report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    report_path = Path("/home/vr-coatings/Desktop/website_V2/backend/rag_debug/final_candidates_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    logger.info(f"Report saved to {report_path}")

if __name__ == "__main__":
    asyncio.run(main())