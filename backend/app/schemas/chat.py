from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatRetrieval(BaseModel):
    chunks_used: int
    retrieval_duration_ms: float | None = None
    generation_duration_ms: float | None = None
    total_duration_ms: float | None = None


class ChatSource(BaseModel):
    source_type: str | None = None
    document: str | None = None
    product: str | None = None
    product_slug: str | None = None
    section: str | None = None
    page: int | None = None
    model: str | None = None
    url: str | None = None
    line_start: int | None = None
    line_end: int | None = None
    verification_status: str | None = None
    authority_priority: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource] = []
    retrieval: ChatRetrieval | None = None
