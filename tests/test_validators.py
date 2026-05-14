"""
Unit tests for the validation helpers.

Run with::

    python -m unittest discover -s tests
"""

import unittest
from datetime import date, timedelta

from utils.validators import (
    validate_email, validate_password,
    validate_task_title, validate_due_date, validate_priority,
)


class ValidatorTests(unittest.TestCase):
    """Validation rules should accept good input and reject bad input."""

    # ---------- e-mail
    def test_email_accepts_valid(self):
        ok, _ = validate_email("student@yorksj.ac.uk")
        self.assertTrue(ok)

    def test_email_rejects_missing_at(self):
        ok, msg = validate_email("studentyorksj.ac.uk")
        self.assertFalse(ok)
        self.assertIn("valid", msg.lower())

    def test_email_rejects_empty(self):
        ok, _ = validate_email("")
        self.assertFalse(ok)

    # ---------- password
    def test_password_minimum_length(self):
        self.assertFalse(validate_password("abc")[0])
        self.assertTrue(validate_password("abc123")[0])

    # ---------- title
    def test_title_must_not_be_blank(self):
        self.assertFalse(validate_task_title("   ")[0])

    def test_title_too_long(self):
        self.assertFalse(validate_task_title("a" * 81)[0])

    # ---------- due date
    def test_due_date_format(self):
        self.assertFalse(validate_due_date("12/06/2026")[0])

    def test_due_date_in_past_rejected(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        ok, _ = validate_due_date(yesterday)
        self.assertFalse(ok)

    def test_due_date_today_accepted(self):
        ok, _ = validate_due_date(date.today().isoformat())
        self.assertTrue(ok)

    # ---------- priority
    def test_priority_whitelist(self):
        self.assertTrue(validate_priority("High")[0])
        self.assertFalse(validate_priority("Urgent")[0])


if __name__ == "__main__":
    unittest.main()
