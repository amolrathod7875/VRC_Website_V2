from typing import Dict, List, Any
from app.rag.constants import (
    CHUNK_TYPE_SECTION,
    CHUNK_TYPE_PRODUCT_MASTER,
    COMPANY_AUTHORITY_PRIORITY,
    SOURCE_TYPE_COMPANY_MASTER,
)
from app.rag.utils.text import normalize_text


def chunk_company_sections(sections: List[Dict[str, Any]], document_id: str) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    chunk_index = 0
    for section in sections:
        section_number = section.get("section_number", "")
        section_title = section.get("section_title", "")
        lines = [normalize_text(line) for line in section.get("lines", []) if normalize_text(line)]
        if not lines:
            continue
        text = "\n".join(lines)
        chunk_size = 700
        overlap = 100
        start = 0
        while start < len(text):
            end = start + chunk_size
            window = text[start:end]
            line_start = 1
            line_end = window.count("\n") + 1
            chunks.append({
                "document_id": document_id,
                "chunk_id": f"{document_id}::chunk::{chunk_index}",
                "source_type": SOURCE_TYPE_COMPANY_MASTER,
                "source_authority": "primary_company_knowledge",
                "authority_priority": COMPANY_AUTHORITY_PRIORITY,
                "document_name": "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt",
                "product": None,
                "product_slug": None,
                "section": section_title,
                "content_type": CHUNK_TYPE_SECTION,
                "page_number": None,
                "line_start": line_start,
                "line_end": line_end,
                "text": window,
            })
            chunk_index += 1
            start = end - overlap
    return chunks
