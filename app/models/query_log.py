# app/models/query_log.py
import uuid

from sqlalchemy import Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.models.base_mixin import TimestampMixin


class QueryLog(TimestampMixin, Base):
    __tablename__ = "query_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # The cosine similarity score of the best retrieved chunk — 0.0 to 1.0.
    # Useful later for analytics: "what percentage of queries had low confidence?"
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship(
        "User", back_populates="query_logs", lazy="joined"
    )
    project: Mapped["Project"] = relationship(
        "Project", back_populates="query_logs", lazy="joined"
    )
