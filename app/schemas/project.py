import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Project name must be between 1 and 100 characters long.",
    )
    description: str | None = Field(
        None,
        max_length=2000,
        description="Project description must be between 0 and 2000 characters long.",
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Project name must be between 1 and 100 characters long.",
    )
    description: str | None = Field(
        None,
        max_length=2000,
        description="Project description must be between 0 and 2000 characters long.",
    )


class ProjectPublic(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    created_at: datetime
    user_id: uuid.UUID
    note_count: int = 0

    model_config = {
        "from_attributes": True,  # Allow creating from ORM models
    }


class ProjectDetail(ProjectPublic):
    """Extended version with note previews - for the project detail endpoint."""

    pass
