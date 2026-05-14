"""
Storage service: local JSON persistence.

A deliberately small file-based store keeps the project portable and
removes the need for any external database. Reads are cached in memory
while writes flush the whole object back to disk so saved data survives
between application launches.

JSON layout
-----------
{
  "users":   [ {...user dicts...} ],
  "tasks":   [ {...task dicts...} ],
  "session": { "email": "..." } or null,
  "settings": { "dark_mode": false, ... }
}

The atomic write technique (write to a temp file, then replace) protects
against partial writes if the application is killed mid-save (Liu et
al., 2024).
"""

from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path
from typing import Any


# Default location: <user-home>/.smart_student_planner/storage.json
DEFAULT_PATH = Path.home() / ".smart_student_planner" / "storage.json"


class StorageService:
    """Read and write the application's JSON store."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path or DEFAULT_PATH)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = self._load()

    # ------------------------------------------------------------------ I/O
    def _load(self) -> dict:
        """Load the JSON file, returning a fresh structure if absent or broken."""
        if not self.path.exists():
            return self._empty()
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
                # Guard against corrupt files by topping up missing keys.
                empty = self._empty()
                empty.update(payload)
                return empty
        except (json.JSONDecodeError, OSError):
            # Fail safe: never let bad data break the app.
            return self._empty()

    def _empty(self) -> dict:
        return {"users": [], "tasks": [], "session": None, "settings": {"dark_mode": False}}

    def save(self) -> None:
        """Atomically write the cached data to disk."""
        # Write to a sibling temp file in the same folder, then ``os.replace``
        # which is atomic on every modern OS.
        tmp_fd, tmp_path = tempfile.mkstemp(prefix=".tmp_", dir=self.path.parent)
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2)
            os.replace(tmp_path, self.path)
        except OSError:
            # If anything goes wrong, clean up the temp file but do not crash.
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

    # -------------------------------------------------------------- Accessors
    @property
    def users(self) -> list[dict]:
        return self._data["users"]

    @property
    def tasks(self) -> list[dict]:
        return self._data["tasks"]

    @property
    def session(self) -> dict | None:
        return self._data["session"]

    @session.setter
    def session(self, value: dict | None) -> None:
        self._data["session"] = value
        self.save()

    @property
    def settings(self) -> dict:
        return self._data["settings"]

    def update_settings(self, **kwargs) -> None:
        self._data["settings"].update(kwargs)
        self.save()
