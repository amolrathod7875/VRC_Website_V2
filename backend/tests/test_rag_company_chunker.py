from app.rag.ingestion.company_chunker import chunk_company_sections
from app.rag.utils.ids import generate_document_id


def test_company_chunks_preserve_metadata() -> None:
    sections = [
        {
            "section_number": "4",
            "section_title": "Locations",
            "line_start": 1,
            "line_end": 3,
            "lines": ["Head Office — Pune", "Phone: +91 8237086924", "Email: sales@vrcoatings.com"],
        }
    ]
    document_id = generate_document_id()
    chunks = chunk_company_sections(sections, document_id)
    assert chunks
    assert chunks[0]["source_type"] == "company_master"
    assert chunks[0]["section"] == "Locations"
    assert chunks[0]["line_start"] == 1
    assert chunks[0]["line_end"] == 3
