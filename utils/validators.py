"""
Input validation helpers.

Centralising validation here keeps the controllers thin and lets us
unit-test the rules without spinning up the Kivy event loop.
"""

from __future__ import annotations
from datetime import datetime
import re


# A pragmatic e-mail pattern. Strict RFC 5322 validation is overkill
# for a student planner and tends to reject perfectly normal addresses.
_EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

ALLOWED_PRIORITIES = ("High", "Medium", "Low")


def validate_email(email: str) -> tuple[bool, str]:
    """Return ``(is_valid, message)`` for the given e-mail address."""
    if not email or not email.strip():
        return False, "E-mail address is required."
    if not _EMAIL_PATTERN.match(email.strip()):
        return False, "Please enter a valid e-mail address."
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Enforce a minimum strength rule for a student-grade application."""
    if not password:
        return False, "Password is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""


def validate_task_title(title: str) -> tuple[bool, str]:
    """Tasks must have a non-empty title up to 80 characters."""
    if not title or not title.strip():
        return False, "Title cannot be empty."
    if len(title.strip()) > 80:
        return False, "Title must be 80 characters or fewer."
    return True, ""


def validate_due_date(value: str) -> tuple[bool, str]:
    """Accept ISO dates (YYYY-MM-DD) only and prevent dates in the past."""
    if not value or not value.strip():
        return False, "Due date is required."
    try:
        due = datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return False, "Use the format YYYY-MM-DD."
    if due < datetime.today().date():
        return False, "Due date cannot be in the past."
    return True, ""


def validate_priority(value: str) -> tuple[bool, str]:
    """Restrict priority to a predefined list."""
    if value not in ALLOWED_PRIORITIES:
        return False, "Priority must be High, Medium or Low."
    return True, ""
