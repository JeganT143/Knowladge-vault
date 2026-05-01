import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Note title must be between 1 and 200 characters long.",
    )
    content: str | None = Field(
        None,
        min_length=1,
        description="`Note content must be at least 1 character long if provided.",
    )


class NoteUpdate(BaseModel):
    title: str | None = Field(
        None,
        min_length=1,
        max_length=200,
        description="Note title must be between 1 and 200 characters long.",
    )
    content: str | None = Field(
        None,
        min_length=1,
        description="`Note content must be at least 1 character long if provided.",
    )


class NotePublic(BaseModel):
    id: uuid.UUID
    title: str
    content: str | None
    created_at: datetime
    project_id: uuid.UUID
    updated_at: datetime | None = None
    is_chunked: bool = False

    model_config = {
        "from_attributes": True,  # Allow creating from ORM models
    }
