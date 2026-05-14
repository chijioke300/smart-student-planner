"""
User model.

Stores the credentials needed for the login feature. Passwords are
hashed using SHA-256 before persistence so the JSON file never holds
clear-text secrets. This is a teaching-grade safeguard; a production
system would use a salted, slow hash such as bcrypt or Argon2 (OWASP,
2023).
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib


def hash_password(plain: str) -> str:
    """Return the SHA-256 hash of a plain text password."""
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


@dataclass
class User:
    """A registered application user."""

    email: str
    password_hash: str
    display_name: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            email=data["email"],
            password_hash=data["password_hash"],
            display_name=data.get("display_name", ""),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def check_password(self, plain: str) -> bool:
        """Compare ``plain`` against the stored hash."""
        return hash_password(plain) == self.password_hash
