# app/models/__init__.py
# Order matters for forward references — import parent models before children
from app.models.embedding import Embedding
from app.models.note import Note
from app.models.note_chunk import NoteChunk
from app.models.project import Project
from app.models.query_log import QueryLog
from app.models.user import User

__all__ = ["User", "Project", "Note", "NoteChunk", "Embedding", "QueryLog"]
