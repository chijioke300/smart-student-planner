"""
Task model.

Each task represents a single item of student work (lecture revision,
coursework, lab activity and so on). Tasks are serialised to JSON via
``to_dict`` and reconstructed through ``from_dict``.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    """A single student task."""

    title: str
    module: str = ""
    due_date: str = ""           # YYYY-MM-DD
    priority: str = "Medium"     # High / Medium / Low
    notes: str = ""
    completed: bool = False
    task_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    owner_email: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Rehydrate a task from its dictionary form."""
        return cls(
            title=data.get("title", ""),
            module=data.get("module", ""),
            due_date=data.get("due_date", ""),
            priority=data.get("priority", "Medium"),
            notes=data.get("notes", ""),
            completed=data.get("completed", False),
            task_id=data.get("task_id", uuid4().hex),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            owner_email=data.get("owner_email", ""),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def matches(self, keyword: str) -> bool:
        """Case-insensitive search across the user-visible fields."""
        if not keyword:
            return True
        k = keyword.lower().strip()
        return (
            k in self.title.lower()
            or k in self.module.lower()
            or k in self.notes.lower()
        )
