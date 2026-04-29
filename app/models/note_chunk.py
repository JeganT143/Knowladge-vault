# app/models/note_chunk.py
import uuid

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base


class NoteChunk(Base):
    # No TimestampMixin — chunks are write-once, never updated.
    # Only add what you actually need. Over-engineering timestamps
    # on immutable records wastes storage and adds noise.
    __tablename__ = "note_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    note_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Which chunk within the note? (0, 1, 2, ...)
    # Critical for reconstruction — when showing retrieved context to the LLM,
    # we want to present chunks in their original order.
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Approximate token count — useful for staying within LLM context windows
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    note: Mapped["Note"] = relationship("Note", back_populates="chunks")

    # A chunk has one embedding — one-to-one relationship
    # uselist=False makes SQLAlchemy return a single object, not a list
    embedding: Mapped["Embedding | None"] = relationship(
        "Embedding",
        back_populates="chunk",
        cascade="all, delete-orphan",
        uselist=False,  # ← this is what makes it one-to-one
        lazy="selectin",
    )
