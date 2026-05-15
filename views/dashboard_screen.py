"""
Dashboard (home) screen.

Lists the active user's tasks with a quick search box, completion toggles,
edit and delete actions, plus a floating-style button for adding a new
task.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView

from utils.theme import (
    THEME, PRIORITY_COLOURS, FONT_BODY, FONT_LARGE, FONT_SMALL,
    FONT_TITLE, PADDING, SPACING,
)
from views.common import RoundedButton, Card, Snackbar


class DashboardScreen(Screen):
    """Lists tasks for the current user."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=PADDING, spacing=SPACING)

        # ---------------- Header bar ----------------
        header = BoxLayout(size_hint_y=None, height=46, spacing=8)
        self.title_label = Label(
            text="My Tasks", font_size=FONT_TITLE, bold=True,
            color=THEME["text"], halign="left", valign="middle",
        )
        self.title_label.bind(size=lambda *_:
                              setattr(self.title_label, "text_size", self.title_label.size))

        settings_button = RoundedButton(text="Settings", size_hint_x=None, width=110)
        settings_button.bind(on_release=lambda *_: setattr(self.manager, "current", "settings"))
        logout_button = RoundedButton(
            text="Logout", size_hint_x=None, width=110, bg=THEME["danger"]
        )
        logout_button.bind(on_release=self._logout)
        header.add_widget(self.title_label)
        header.add_widget(settings_button)
        header.add_widget(logout_button)
        root.add_widget(header)

        # ---------------- Search bar ----------------
        search_card = Card(size_hint_y=None, height=64, padding=8)
        self.search_input = TextInput(
            hint_text="Search by title, module or notes...",
            multiline=False, size_hint_y=None, height=44, padding=[10, 12],
        )
        self.search_input.bind(text=lambda *_: self.refresh())
        search_card.add_widget(self.search_input)
        root.add_widget(search_card)

        # ---------------- Task list ----------------
        self.scroll = ScrollView(do_scroll_x=False)
        self.task_list = GridLayout(cols=1, spacing=SPACING, size_hint_y=None, padding=[0, 4])
        self.task_list.bind(minimum_height=self.task_list.setter("height"))
        self.scroll.add_widget(self.task_list)
        root.add_widget(self.scroll)

        # ---------------- Add button ----------------
        add_button = RoundedButton(
            text="+  Add new task",
            size_hint_y=None, height=52,
            bg=THEME["accent"], fg=(1, 1, 1, 1),
        )
        add_button.bind(on_release=self._add_task)
        root.add_widget(add_button)

        self.add_widget(root)

    # ------------------------------------------------------------------ events
    def on_pre_enter(self, *_):
        app = App.get_running_app()
        if app.auth.current_user:
            name = app.auth.current_user.display_name or "Student"
            self.title_label.text = f"Hello, {name}"
        self.refresh()

    # ------------------------------------------------------------------ list
    def refresh(self) -> None:
        app = App.get_running_app()
        self.task_list.clear_widgets()
        if not app.auth.current_user:
            return

        tasks = app.tasks.list_tasks(
            app.auth.current_user.email, self.search_input.text
        )

        if not tasks:
            empty = Label(
                text=("No tasks match your search." if self.search_input.text
                      else "No tasks yet. Tap '+ Add new task' to get started."),
                color=THEME["muted"], font_size=FONT_BODY,
                size_hint_y=None, height=80,
            )
            self.task_list.add_widget(empty)
            return

        for task in tasks:
            self.task_list.add_widget(self._build_task_row(task))

    def _build_task_row(self, task) -> Card:
        """Construct a single task card with toggle, edit and delete actions."""
        row = Card(size_hint_y=None, height=118)

        # Top: completion toggle + title + priority chip
        top = BoxLayout(size_hint_y=None, height=30, spacing=8)
        cb = CheckBox(active=task.completed, size_hint_x=None, width=30)
        cb.bind(active=lambda _w, value, t=task: self._toggle(t, value))

        title_lbl = Label(
            text=("[s]" + task.title + "[/s]") if task.completed else task.title,
            markup=True, color=THEME["text"], font_size=FONT_LARGE, bold=True,
            halign="left", valign="middle",
        )
        title_lbl.bind(size=lambda *_:
                       setattr(title_lbl, "text_size", title_lbl.size))

        chip = Label(
            text=task.priority, color=(1, 1, 1, 1), font_size=FONT_SMALL, bold=True,
            size_hint_x=None, width=72,
        )
        # Cheap rounded background using canvas instructions
        from kivy.graphics import Color, RoundedRectangle
        with chip.canvas.before:
            Color(*PRIORITY_COLOURS.get(task.priority, THEME["muted"]))
            chip._rect = RoundedRectangle(radius=[10], pos=chip.pos, size=chip.size)
        chip.bind(pos=lambda *_: setattr(chip._rect, "pos", chip.pos),
                  size=lambda *_: setattr(chip._rect, "size", chip.size))

        top.add_widget(cb)
        top.add_widget(title_lbl)
        top.add_widget(chip)

        meta = Label(
            text=f"Module: {task.module or '-'}    Due: {task.due_date}",
            color=THEME["muted"], font_size=FONT_SMALL,
            size_hint_y=None, height=22, halign="left", valign="middle",
        )
        meta.bind(size=lambda *_: setattr(meta, "text_size", meta.size))

        # Buttons
        actions = BoxLayout(size_hint_y=None, height=36, spacing=8)
        edit_btn = RoundedButton(text="Edit", bg=THEME["primary"])
        edit_btn.bind(on_release=lambda *_, t=task: self._edit_task(t))
        del_btn = RoundedButton(text="Delete", bg=THEME["danger"])
        del_btn.bind(on_release=lambda *_, t=task: self._delete_task(t))
        actions.add_widget(edit_btn)
        actions.add_widget(del_btn)

        row.add_widget(top)
        row.add_widget(meta)
        row.add_widget(actions)
        return row

    # ------------------------------------------------------------------ actions
    def _toggle(self, task, value):
        app = App.get_running_app()
        if value:
            app.tasks.mark_complete(task.task_id)
        else:
            app.tasks.mark_incomplete(task.task_id)
        self.refresh()

    def _add_task(self, *_):
        # Reset the form into "create" mode and navigate
        form = self.manager.get_screen("task_form")
        form.load(None)
        self.manager.current = "task_form"

    def _logout(self, *_):
        self._show_logout_confirmation()

    def _show_logout_confirmation(self) -> None:
        confirm = ModalView(size_hint=(0.8, None), height=180, auto_dismiss=False)
        body = BoxLayout(orientation="vertical", padding=16, spacing=16)

        body.add_widget(
            Label(
                text="Are you sure you want to log out?",
                color=THEME["text"], font_size=18,
                halign="center", valign="middle",
                size_hint_y=None, height=60,
            )
        )

        button_row = BoxLayout(size_hint_y=None, height=48, spacing=12)
        cancel_btn = RoundedButton(text="Cancel", bg=THEME["muted"])
        confirm_btn = RoundedButton(text="Log out", bg=THEME["danger"])
        button_row.add_widget(cancel_btn)
        button_row.add_widget(confirm_btn)

        body.add_widget(button_row)
        confirm.add_widget(body)

        cancel_btn.bind(on_release=lambda *_: confirm.dismiss())
        confirm_btn.bind(on_release=lambda *_: self._perform_logout(confirm))
        confirm.open()

    def _perform_logout(self, dialog: ModalView) -> None:
        dialog.dismiss()
        app = App.get_running_app()
        app.auth.logout()
        self.manager.current = "login"

    def _edit_task(self, task):
        form = self.manager.get_screen("task_form")
        form.load(task)
        self.manager.current = "task_form"

    def _delete_task(self, task):
        app = App.get_running_app()
        ok, msg = app.tasks.delete_task(task.task_id)
        Snackbar(msg, success=ok).show()
        self.refresh()
