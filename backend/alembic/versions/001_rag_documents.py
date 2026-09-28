"""add_rag_documents_and_rag_ingestion_runs

Revision ID: 001_rag_documents
Revises:
Create Date: 2026-09-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001_rag_documents"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rag_documents",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("document_name", sa.String(length=512), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("product_slug", sa.String(length=256), nullable=True),
        sa.Column("storage_path", sa.String(length=1024), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("qdrant_document_id", sa.String(length=256), nullable=True),
        sa.Column("chunk_count", sa.Integer(), nullable=True),
        sa.Column("last_ingested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), server_onupdate=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("document_name"),
    )
    op.create_index(op.f("ix_rag_documents_status"), "rag_documents", ["status"], unique=False)
    op.create_index(op.f("ix_rag_documents_source_type"), "rag_documents", ["source_type"], unique=False)

    op.create_table(
        "rag_ingestion_runs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("document_id", UUID(as_uuid=True), nullable=True),
        sa.Column("document_name", sa.String(length=512), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("chunks_created", sa.Integer(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("rag_ingestion_runs")
    op.drop_index(op.f("ix_rag_documents_source_type"), table_name="rag_documents")
    op.drop_index(op.f("ix_rag_documents_status"), table_name="rag_documents")
    op.drop_table("rag_documents")
