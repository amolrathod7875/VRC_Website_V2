from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.utils.ids import generate_document_id


def test_catalogue_chunk_contains_document_id() -> None:
    pages = [{"page_number": 1, "text": "Tiger\nApplications: heavy structural painting"}]
    tables = []
    document_id = generate_document_id()
    chunks = chunk_catalogue("Tiger.pdf", pages, tables, "tiger", document_id)
    assert chunks
    assert all(chunk["document_id"] == document_id for chunk in chunks)
