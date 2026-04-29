# app/models/note.py
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.models.base_mixin import TimestampMixin


class Note(TimestampMixin, Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    # Text is PostgreSQL's unlimited-length string type.
    # Never use String() without a length for large content — it'll work but
    # you lose the database's ability to enforce a reasonable limit.
    content: Mapped[str] = mapped_column(Text, nullable=False)

    project: Mapped["Project"] = relationship(
        "Project", back_populates="notes", lazy="joined"
    )

    # Chunks are loaded only when explicitly needed (they can be large)
    chunks: Mapped[list["NoteChunk"]] = relationship(
        "NoteChunk",
        back_populates="note",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="NoteChunk.chunk_index",  # always return chunks in order
    )
