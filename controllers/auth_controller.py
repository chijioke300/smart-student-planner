"""
Authentication controller.

Handles registration, login and logout. Validation rules live in
``utils.validators`` and the storage layer is opaque to this class,
which keeps the controller easy to unit-test.
"""

from __future__ import annotations
from typing import Optional

from models.user import User, hash_password
from services.storage_service import StorageService
from utils.validators import validate_email, validate_password


class AuthController:
    """Authentication business logic."""

    def __init__(self, storage: StorageService) -> None:
        self.storage = storage
        self.current_user: Optional[User] = None
        self._restore_session()

    # ------------------------------------------------------------ public API
    def register(self, email: str, password: str, display_name: str = "") -> tuple[bool, str]:
        """Create a new user account. Returns ``(success, message)``."""
        valid_email, msg = validate_email(email)
        if not valid_email:
            return False, msg
        valid_pwd, msg = validate_password(password)
        if not valid_pwd:
            return False, msg
        if self._find_user(email):
            return False, "An account already exists for that e-mail."

        user = User(
            email=email.strip().lower(),
            password_hash=hash_password(password),
            display_name=display_name.strip() or email.split("@")[0],
        )
        self.storage.users.append(user.to_dict())
        self.storage.save()
        return True, "Account created. You can now sign in."

    def login(self, email: str, password: str) -> tuple[bool, str]:
        """Verify credentials and remember the session on success."""
        valid_email, msg = validate_email(email)
        if not valid_email:
            return False, msg
        valid_pwd, msg = validate_password(password)
        if not valid_pwd:
            return False, msg

        record = self._find_user(email)
        if not record:
            return False, "No account found for that e-mail."

        user = User.from_dict(record)
        if not user.check_password(password):
            return False, "Incorrect password. Please try again."

        self.current_user = user
        self.storage.session = {"email": user.email}
        return True, f"Welcome back, {user.display_name}."

    def logout(self) -> None:
        """Forget the active user and clear the persisted session."""
        self.current_user = None
        self.storage.session = None

    # ------------------------------------------------------------ helpers
    def _find_user(self, email: str) -> dict | None:
        target = email.strip().lower()
        for record in self.storage.users:
            if record["email"] == target:
                return record
        return None

    def _restore_session(self) -> None:
        """Reload the previously logged-in user, if any."""
        session = self.storage.session
        if not session:
            return
        record = self._find_user(session.get("email", ""))
        if record:
            self.current_user = User.from_dict(record)
