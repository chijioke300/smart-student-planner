"""
Task form screen.

A single screen reused for both Add and Edit modes. ``load(None)`` puts
it in create mode, ``load(task)`` pre-fills it for editing. Validation
errors are surfaced inline so the user always knows what to fix.
"""

from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from utils.theme import THEME, FONT_BODY, FONT_TITLE, PADDING, SPACING
from views.common import RoundedButton, Card, Snackbar


class TaskFormScreen(Screen):
    """Reusable Add / Edit task form."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._editing_id: str | None = None

        root = BoxLayout(orientation="vertical", padding=PADDING, spacing=SPACING)

        # Header
        header = BoxLayout(size_hint_y=None, height=44, spacing=8)
        back = RoundedButton(text="< Back", size_hint_x=None, width=92, bg=THEME["border"], fg=THEME["text"])
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "dashboard"))
        self.heading = Label(
            text="Add task", font_size=FONT_TITLE, bold=True, color=THEME["text"],
            halign="left", valign="middle",
        )
        self.heading.bind(size=lambda *_: setattr(self.heading, "text_size", self.heading.size))
        header.add_widget(back)
        header.add_widget(self.heading)
        root.add_widget(header)

        # Form fields
        card = Card(size_hint_y=None, height=440)

        self.title_input = TextInput(
            hint_text="Title (required)", multiline=False,
            size_hint_y=None, height=44, padding=[10, 12],
        )
        self.module_input = TextInput(
            hint_text="Module (e.g. LDC6004M)", multiline=False,
            size_hint_y=None, height=44, padding=[10, 12],
        )
        self.due_input = TextInput(
            hint_text="Due date (YYYY-MM-DD)", multiline=False,
            text=(date.today() + timedelta(days=7)).isoformat(),
            size_hint_y=None, height=44, padding=[10, 12],
        )
        self.priority_input = Spinner(
            text="Medium", values=("High", "Medium", "Low"),
            size_hint_y=None, height=44,
            background_normal="", background_color=THEME["primary"],
            color=(1, 1, 1, 1),
        )
        self.notes_input = TextInput(
            hint_text="Notes (optional)",
            size_hint_y=None, height=140, padding=[10, 12],
        )
        self.error_label = Label(
            text="", color=THEME["danger"], font_size=13,
            size_hint_y=None, height=20,
        )

        card.add_widget(self.title_input)
        card.add_widget(self.module_input)
        card.add_widget(self.due_input)
        card.add_widget(self.priority_input)
        card.add_widget(self.notes_input)
        card.add_widget(self.error_label)
        root.add_widget(card)

        # Action button
        self.save_button = RoundedButton(text="Save task", size_hint_y=None, height=52)
        self.save_button.bind(on_release=self._save)
        root.add_widget(self.save_button)
        root.add_widget(BoxLayout())  # spacer

        self.add_widget(root)

    # ----------------------------------------------------------------- API
    def load(self, task) -> None:
        """Switch between create and edit modes."""
        if task is None:
            self._editing_id = None
            self.heading.text = "Add task"
            self.title_input.text = ""
            self.module_input.text = ""
            self.due_input.text = (date.today() + timedelta(days=7)).isoformat()
            self.priority_input.text = "Medium"
            self.notes_input.text = ""
            self.save_button.text = "Save task"
        else:
            self._editing_id = task.task_id
            self.heading.text = "Edit task"
            self.title_input.text = task.title
            self.module_input.text = task.module
            self.due_input.text = task.due_date
            self.priority_input.text = task.priority
            self.notes_input.text = task.notes
            self.save_button.text = "Update task"
        self.error_label.text = ""

    # ----------------------------------------------------------------- save
    def _save(self, *_):
        app = App.get_running_app()
        if not app.auth.current_user:
            return  # safety net, should never happen

        title = self.title_input.text
        module = self.module_input.text
        due = self.due_input.text
        priority = self.priority_input.text
        notes = self.notes_input.text

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
            Snackbar(msg, success=True).show()
            self.manager.current = "dashboard"
        else:
            self.error_label.text = msg
