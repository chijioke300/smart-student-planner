"""
Task form screen.

A single screen reused for both Add and Edit modes. ``load(None)`` puts
it in create mode, ``load(task)`` pre-fills it for editing. Validation
errors are surfaced inline so the user always knows what to fix.
"""

from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import Screen


class TaskFormScreen(Screen):
    """Reusable Add / Edit task form."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._editing_id = None

    def load(self, task) -> None:
        if task is None:
            self._editing_id = None
            self.ids.heading.text = "Add task"
            self.ids.title_input.text = ""
            self.ids.module_input.text = ""
            self.ids.due_input.text = (date.today() + timedelta(days=7)).isoformat()
            self.ids.priority_input.text = "Medium"
            self.ids.notes_input.text = ""
            self.ids.save_button.text = "Save task"
        else:
            self._editing_id = task.task_id
            self.ids.heading.text = "Edit task"
            self.ids.title_input.text = task.title
            self.ids.module_input.text = task.module
            self.ids.due_input.text = task.due_date
            self.ids.priority_input.text = task.priority
            self.ids.notes_input.text = task.notes
            self.ids.save_button.text = "Update task"
        self.ids.error_label.text = ""

    def _save(self, *_):
        app = App.get_running_app()
        if not app.auth.current_user:
            return

        title = self.ids.title_input.text
        module = self.ids.module_input.text
        due = self.ids.due_input.text
        priority = self.ids.priority_input.text
        notes = self.ids.notes_input.text

        if self._editing_id:
            ok, msg = app.tasks.edit_task(
                self._editing_id,
                title=title, module=module, due_date=due,
                priority=priority, notes=notes,
            )
        else:
            ok, msg, _ = app.tasks.add_task(
                owner_email=app.auth.current_user.email,
                title=title, module=module, due_date=due,
                priority=priority, notes=notes,
            )

        if ok:
            from views.common import Snackbar
            Snackbar(msg, success=True).show()
            self.manager.current = "dashboard"
        else:
            self.ids.error_label.text = msg
