import uuid

# Stable namespace for deterministic document identity.
# Using a fixed UUID (version 5) guarantees that the same source name
# always maps to the same document_id across backend restarts.
_DOCUMENT_NAMESPACE = uuid.UUID("d8b9a8b0-1234-5678-9abc-def012345678")

# Legacy namespace retained for backward-compatible point-id computation.
_POINT_ID_NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def generate_document_id() -> str:
    return str(uuid.uuid4())


def generate_document_id_for(document_name: str, source_type: str = "catalogue") -> str:
    """Deterministic document identity based on canonical source name.

    Produces a stable UUID5 so that the same physical file always resolves
    to the same document_id, regardless of backend restarts. This replaces
    the random UUID4 previously used for RagDocument/qdrant_document_id.
    """
    raw = f"{source_type}:{document_name}"
    return str(uuid.uuid5(_DOCUMENT_NAMESPACE, raw))


def generate_chunk_id(document_id: str, index: int) -> str:
    return f"{document_id}::chunk::{index}"


def stable_point_id(document_id: str, chunk_id: str) -> str:
    """Deterministic Qdrant point ID derived from document_id + chunk_id.

    Uses UUID5 over a fixed namespace so that the same chunk is always
    assigned the same point ID, preventing duplicates on re-ingestion.
    """
    raw = f"{document_id}:{chunk_id}"
    return str(uuid.uuid5(_POINT_ID_NAMESPACE, raw))
