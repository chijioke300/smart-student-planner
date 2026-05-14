"""
Task controller.

Implements the five required task operations from the assignment brief:
``AddTask``, ``EditTask``, ``DeleteTask``, ``MarkTaskComplete`` /
``MarkTaskIncomplete`` and ``SearchTasks``.
"""

from __future__ import annotations
from typing import Iterable

from models.task import Task
from services.storage_service import StorageService
from utils.validators import (
    validate_task_title,
    validate_due_date,
    validate_priority,
)


class TaskController:
    """Application layer for everything to do with tasks."""

    def __init__(self, storage: StorageService) -> None:
        self.storage = storage

    # ------------------------------------------------------- create
    def add_task(
        self,
        owner_email: str,
        title: str,
        module: str,
        due_date: str,
        priority: str,
        notes: str,
    ) -> tuple[bool, str, Task | None]:
        """Validate the inputs then persist a new task."""
        ok, msg = validate_task_title(title)
        if not ok:
            return False, msg, None
        ok, msg = validate_due_date(due_date)
        if not ok:
            return False, msg, None
        ok, msg = validate_priority(priority)
        if not ok:
            return False, msg, None

        task = Task(
            title=title.strip(),
            module=module.strip(),
            due_date=due_date.strip(),
            priority=priority,
            notes=notes.strip(),
            owner_email=owner_email,
        )
        self.storage.tasks.append(task.to_dict())
        self.storage.save()
        return True, "Task added.", task

    # ------------------------------------------------------- read
    def list_tasks(self, owner_email: str, keyword: str = "") -> list[Task]:
        """Return tasks for the active user, optionally filtered by keyword."""
        items: Iterable[Task] = (
            Task.from_dict(t) for t in self.storage.tasks
            if t.get("owner_email") == owner_email
        )
        results = [t for t in items if t.matches(keyword)]
        # Outstanding tasks first, then by due date ascending.
        results.sort(key=lambda t: (t.completed, t.due_date or "9999-99-99"))
        return results

    def search_tasks(self, owner_email: str, keyword: str) -> list[Task]:
        """Explicit search helper. Delegates to :meth:`list_tasks`."""
        return self.list_tasks(owner_email, keyword)

    def get_task(self, task_id: str) -> Task | None:
        for record in self.storage.tasks:
            if record["task_id"] == task_id:
                return Task.from_dict(record)
        return None

    # ------------------------------------------------------- update
    def edit_task(self, task_id: str, **fields) -> tuple[bool, str]:
        """Modify selected fields on an existing task."""
        for record in self.storage.tasks:
            if record["task_id"] != task_id:
                continue

            # Validate any of the changed fields
            if "title" in fields:
                ok, msg = validate_task_title(fields["title"])
                if not ok:
                    return False, msg
            if "due_date" in fields:
                ok, msg = validate_due_date(fields["due_date"])
                if not ok:
                    return False, msg
            if "priority" in fields:
                ok, msg = validate_priority(fields["priority"])
                if not ok:
                    return False, msg

            # Apply
            for key in ("title", "module", "due_date", "priority", "notes"):
                if key in fields:
                    record[key] = fields[key].strip() if isinstance(fields[key], str) else fields[key]
            self.storage.save()
            return True, "Task updated."

        return False, "Task not found."

    def mark_complete(self, task_id: str) -> tuple[bool, str]:
        return self._set_completed(task_id, True)

    def mark_incomplete(self, task_id: str) -> tuple[bool, str]:
        return self._set_completed(task_id, False)

    def _set_completed(self, task_id: str, value: bool) -> tuple[bool, str]:
        for record in self.storage.tasks:
            if record["task_id"] == task_id:
                record["completed"] = value
                self.storage.save()
                return True, "Updated."
        return False, "Task not found."

    # ------------------------------------------------------- delete
    def delete_task(self, task_id: str) -> tuple[bool, str]:
        for index, record in enumerate(self.storage.tasks):
            if record["task_id"] == task_id:
                self.storage.tasks.pop(index)
                self.storage.save()
                return True, "Task deleted."
        return False, "Task not found."
