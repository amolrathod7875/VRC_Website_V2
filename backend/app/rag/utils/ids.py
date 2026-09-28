import uuid


def generate_document_id() -> str:
    return str(uuid.uuid4())


def generate_chunk_id(document_id: str, index: int) -> str:
    return f"{document_id}::chunk::{index}"
