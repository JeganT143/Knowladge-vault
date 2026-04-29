# app/models/user.py
import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from app.models.base_mixin import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    # Mapped[uuid.UUID] is SQLAlchemy 2.0's type-annotated column style.
    # It replaces the old Column(UUID, primary_key=True) syntax.
    # The type annotation IS the column definition — cleaner, fully type-checked.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # Python generates the UUID before INSERT
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,  # we'll query by email frequently (login), so index it
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships — this is where SQLAlchemy earns its keep
    # "I own many projects" — back_populates links this to Project.owner
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete-orphan",  # if user is deleted, delete all their projects
        lazy="selectin",  # explained below
    )

    query_logs: Mapped[list["QueryLog"]] = relationship(
        "QueryLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
