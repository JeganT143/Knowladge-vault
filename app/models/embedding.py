# app/models/embedding.py
import uuid

from pgvector.sqlalchemy import Vector  # the pgvector SQLAlchemy integration
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.models.base_mixin import TimestampMixin


class Embedding(TimestampMixin, Base):
    __tablename__ = "embeddings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    chunk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("note_chunks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # one embedding per chunk — enforced at DB level
        index=True,
    )

    # Vector(1536) means a list of 1536 floats.
    # Why 1536? That's the dimension of OpenAI's text-embedding-3-small model.
    # Different models use different dimensions:
    #   text-embedding-3-small → 1536
    #   text-embedding-3-large → 3072
    #   nomic-embed-text (Ollama) → 768
    # The dimension is baked into the column — changing it requires a migration.
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="text-embedding-3-small",
    )

    chunk: Mapped["NoteChunk"] = relationship("NoteChunk", back_populates="embedding")
