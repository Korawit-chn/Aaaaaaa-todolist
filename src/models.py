"""Data models for the Todo List application."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from uuid import uuid4


class Priority(Enum):
    """Todo item priority levels."""
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    """Todo item completion status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """Represents a todo item in the application.
    
    Attributes:
        id: Unique identifier (UUID).
        title: The todo item title.
        details: Detailed description of the todo.
        priority: Priority level (HIGH, MID, LOW).
        status: Current status (PENDING, COMPLETED).
        owner: Username of the todo owner.
        created_at: ISO-8601 timestamp of creation.
        updated_at: ISO-8601 timestamp of last update.
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert TodoItem to dictionary format for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TodoItem from dictionary format."""
        return cls(
            id=data.get("id", str(uuid4())),
            title=data.get("title", ""),
            details=data.get("details", ""),
            priority=Priority(data.get("priority", "MID")),
            status=Status(data.get("status", "PENDING")),
            owner=data.get("owner", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )
