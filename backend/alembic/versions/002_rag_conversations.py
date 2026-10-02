"""add_rag_conversations_and_rag_messages

Revision ID: 002_rag_conversations
Revises: 001_rag_documents
Create Date: 2026-10-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "002_rag_conversations"
down_revision: Union[str, None] = "001_rag_documents"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rag_conversations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), server_onupdate=sa.text("now()"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
    )

    op.create_table(
        "rag_messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("conversation_id", UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sources", sa.JSON(), nullable=True),
        sa.Column("retrieval_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), server_onupdate=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["rag_conversations.id"], ondelete="CASCADE"),
    )

    op.create_index(op.f("ix_rag_messages_conversation_id"), "rag_messages", ["conversation_id"], unique=False)
    op.create_index(op.f("ix_rag_messages_created_at"), "rag_messages", ["created_at"], unique=False)
    op.create_index(op.f("ix_rag_messages_conversation_created"), "rag_messages", ["conversation_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_rag_messages_conversation_created"), table_name="rag_messages")
    op.drop_index(op.f("ix_rag_messages_created_at"), table_name="rag_messages")
    op.drop_index(op.f("ix_rag_messages_conversation_id"), table_name="rag_messages")
    op.drop_table("rag_messages")
    op.drop_table("rag_conversations")
