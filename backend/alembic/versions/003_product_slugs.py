"""add_product_slugs_to_rag_documents

Revision ID: 003_product_slugs
Revises: 002_rag_conversations
Create Date: 2026-10-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "003_product_slugs"
down_revision: Union[str, None] = "002_rag_conversations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rag_documents", sa.Column("product_slugs", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("rag_documents", "product_slugs")
