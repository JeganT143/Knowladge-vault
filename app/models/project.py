# app/models/project.py
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.models.base_mixin import TimestampMixin


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ForeignKey is the chain link between tables.
    # "users.id" = the 'id' column of the 'users' table.
    # ondelete="CASCADE" means: if the parent user row is deleted,
    # the database itself deletes all child project rows.
    # This is a safety net — our cascade="all, delete-orphan" on the
    # relationship does the same at the ORM level, but DB-level cascade
    # ensures integrity even if someone runs raw SQL.
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,  # we'll query "all projects for user X" constantly
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Many-to-one: this project belongs to one owner
    # lazy="joined" — when we load a Project, also load its User in the same query
    # This makes sense for many-to-one: one extra JOIN vs one extra query
    owner: Mapped["User"] = relationship(
        "User", back_populates="projects", lazy="joined"
    )

    # One-to-many: this project has many notes
    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    query_logs: Mapped[list["QueryLog"]] = relationship(
        "QueryLog",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"
