from app.rag.ingestion.metadata_builder import build_catalogue_metadata, build_company_metadata


def test_catalogue_metadata_contains_document_id() -> None:
    chunk = {
        "chunk_id": "doc::chunk::0",
        "source_type": "catalogue",
        "source_authority": "primary",
        "authority_priority": 100,
        "product": "Rhino",
        "product_slug": "rhino",
        "section": "technical_model",
        "content_type": "technical_model",
        "page_number": 1,
        "line_start": 1,
        "line_end": 5,
        "model": "75:210",
        "text": "model: 75:210\npressure: 450 bar",
    }
    metadata = build_catalogue_metadata("doc-id", "rhino.pdf", "/app/storage/catalogues/rhino.pdf", "abc", "rhino", chunk)
    assert metadata["document_id"] == "doc-id"
    assert metadata["model"] == "75:210"
