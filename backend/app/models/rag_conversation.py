from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base import UUIDMixin, TimestampMixin


class RagConversation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "rag_conversations"

    status = Column(String(32), nullable=False, default="active")

    messages = relationship("RagMessage", back_populates="conversation", order_by="RagMessage.created_at")


class RagMessage(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "rag_messages"

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("rag_conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(16), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)
    retrieval_metadata = Column(JSON, nullable=True)

    conversation = relationship("RagConversation", back_populates="messages")
