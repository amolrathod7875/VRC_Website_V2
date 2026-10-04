from typing import Dict, Any, Optional


def build_catalogue_metadata(
    document_id: str,
    document_name: str,
    storage_path: str,
    sha256: str,
    product_slug: str,
    chunk: Dict[str, Any],
) -> Dict[str, Any]:
    metadata = {
        "document_id": document_id,
        "chunk_id": chunk.get("chunk_id"),
        "source_type": chunk.get("source_type"),
        "source_authority": chunk.get("source_authority"),
        "authority_priority": chunk.get("authority_priority"),
        "document_name": document_name,
        "storage_path": storage_path,
        "product": chunk.get("product"),
        "product_slug": chunk.get("product_slug") or product_slug,
        "parent_product_slug": chunk.get("parent_product_slug"),
        "variant": chunk.get("variant"),
        "category": None,
        "section": chunk.get("section"),
        "content_type": chunk.get("content_type"),
        "page_number": chunk.get("page_number"),
        "line_start": chunk.get("line_start"),
        "line_end": chunk.get("line_end"),
        "model": chunk.get("model"),
        "verification_status": None,
        "data_status": None,
        "version": None,
        "text": chunk.get("text"),
    }
    return metadata


def build_company_metadata(
    document_id: str,
    document_name: str,
    storage_path: str,
    sha256: str,
    chunk: Dict[str, Any],
) -> Dict[str, Any]:
    metadata = {
        "document_id": document_id,
        "chunk_id": chunk.get("chunk_id"),
        "source_type": chunk.get("source_type"),
        "source_authority": chunk.get("source_authority"),
        "authority_priority": chunk.get("authority_priority"),
        "document_name": document_name,
        "storage_path": storage_path,
        "product": chunk.get("product"),
        "product_slug": chunk.get("product_slug"),
        "category": None,
        "section": chunk.get("section"),
        "content_type": chunk.get("content_type"),
        "page_number": chunk.get("page_number"),
        "line_start": chunk.get("line_start"),
        "line_end": chunk.get("line_end"),
        "model": None,
        "verification_status": None,
        "data_status": None,
        "version": None,
        "text": chunk.get("text"),
    }
    return metadata
