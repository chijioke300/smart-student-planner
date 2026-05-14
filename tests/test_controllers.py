"""
End-to-end controller tests using a temporary storage file.

These tests cover registration, login, the five task operations from
the brief, and the search filter.
"""

import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from services.storage_service import StorageService
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController


class ControllerIntegrationTests(unittest.TestCase):
    """Auth + task flows working together with a real JSON file."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.storage = StorageService(self.tmp / "store.json")
        self.auth = AuthController(self.storage)
        self.tasks = TaskController(self.storage)
        self.email = "test@yorksj.ac.uk"
        self.password = "secret123"

    def tearDown(self) -> None:
        for f in self.tmp.glob("*"):
            os.remove(f)
        os.rmdir(self.tmp)

    # ---------- auth ----------
    def test_register_then_login(self):
        ok, _ = self.auth.register(self.email, self.password, "Test User")
        self.assertTrue(ok)
        ok, _ = self.auth.login(self.email, self.password)
        self.assertTrue(ok)
        self.assertEqual(self.auth.current_user.email, self.email)

    def test_login_with_wrong_password_fails(self):
        self.auth.register(self.email, self.password)
        ok, _ = self.auth.login(self.email, "wrong-password")
        self.assertFalse(ok)

    # ---------- tasks ----------
    def _add_sample(self, **overrides):
        defaults = dict(
            owner_email=self.email,
            title="Revise Lecture 1",
            module="LDC6004M",
            due_date=(date.today() + timedelta(days=3)).isoformat(),
            priority="High",
            notes="Cross-platform frameworks",
        )
        defaults.update(overrides)
        return self.tasks.add_task(**defaults)

    def test_add_and_list_task(self):
        self.auth.register(self.email, self.password)
        ok, _, task = self._add_sample()
        self.assertTrue(ok)
        items = self.tasks.list_tasks(self.email)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].task_id, task.task_id)

    def test_edit_task(self):
        self.auth.register(self.email, self.password)
        _, _, task = self._add_sample()
        ok, _ = self.tasks.edit_task(task.task_id, title="Revise Lecture 2")
        self.assertTrue(ok)
        self.assertEqual(self.tasks.get_task(task.task_id).title, "Revise Lecture 2")

    def test_delete_task(self):
        self.auth.register(self.email, self.password)
        _, _, task = self._add_sample()
        self.tasks.delete_task(task.task_id)
        self.assertIsNone(self.tasks.get_task(task.task_id))

    def test_mark_complete_and_incomplete(self):
        self.auth.register(self.email, self.password)
        _, _, task = self._add_sample()
        self.tasks.mark_complete(task.task_id)
        self.assertTrue(self.tasks.get_task(task.task_id).completed)
        self.tasks.mark_incomplete(task.task_id)
        self.assertFalse(self.tasks.get_task(task.task_id).completed)

    def test_search_filters_results(self):
        self.auth.register(self.email, self.password)
        self._add_sample(title="Read Lecture 02")
        self._add_sample(title="Submit coursework")
        results = self.tasks.search_tasks(self.email, "lecture")
        self.assertEqual(len(results), 1)
        self.assertIn("Lecture", results[0].title)


if __name__ == "__main__":
    unittest.main()
