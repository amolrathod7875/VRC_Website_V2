from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class RagDocument(Base):
    __tablename__ = "rag_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_name = Column(String(512), nullable=False, unique=True)
    source_type = Column(String(64), nullable=False)
    product_slug = Column(String(256), nullable=True)
    storage_path = Column(String(1024), nullable=False)
    sha256 = Column(String(64), nullable=False)
    version = Column(String(64), nullable=True)
    status = Column(String(32), nullable=False, default="pending")
    qdrant_document_id = Column(String(256), nullable=True)
    chunk_count = Column(Integer, nullable=True)
    last_ingested_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RagIngestionRun(Base):
    __tablename__ = "rag_ingestion_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), nullable=True)
    document_name = Column(String(512), nullable=False)
    source_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    chunks_created = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
