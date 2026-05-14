"""
Login screen.

Combines login and quick registration in a single, tabbed view. The
screen delegates every business decision to ``AuthController`` so it
stays a thin presentation layer.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from utils.theme import THEME, FONT_BODY, FONT_LARGE, FONT_TITLE, PADDING, SPACING
from views.common import RoundedButton, Card, Snackbar


class LoginScreen(Screen):
    """Sign-in / register entry point."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        wrapper = BoxLayout(
            orientation="vertical",
            padding=[PADDING, PADDING * 3, PADDING, PADDING],
            spacing=SPACING,
        )

        # ------------------- Header -------------------
        wrapper.add_widget(
            Label(
                text="Smart Student Planner",
                font_size=FONT_TITLE, bold=True,
                color=THEME["text"], size_hint_y=None, height=40,
            )
        )
        wrapper.add_widget(
            Label(
                text="Plan modules, deadlines and revision in one place.",
                font_size=FONT_BODY, color=THEME["muted"],
                size_hint_y=None, height=24,
            )
        )

        # ------------------- Mode toggle -------------------
        toggle_row = BoxLayout(size_hint_y=None, height=44, spacing=8)
        self.tab_signin = ToggleButton(
            text="Sign in", state="down", group="auth_mode",
            background_normal="", background_down="",
            background_color=THEME["primary"], color=(1, 1, 1, 1),
        )
        self.tab_signup = ToggleButton(
            text="Create account", group="auth_mode",
            background_normal="", background_down="",
            background_color=THEME["border"], color=THEME["text"],
        )
        self.tab_signin.bind(on_release=lambda *_: self._switch_mode("signin"))
        self.tab_signup.bind(on_release=lambda *_: self._switch_mode("signup"))
        toggle_row.add_widget(self.tab_signin)
        toggle_row.add_widget(self.tab_signup)
        wrapper.add_widget(toggle_row)

        # ------------------- Card with inputs -------------------
        card = Card(size_hint_y=None, height=320)

        self.name_field = TextInput(
            hint_text="Display name (optional)",
            multiline=False, size_hint_y=None, height=44,
            padding=[10, 12], background_color=(1, 1, 1, 1),
            foreground_color=THEME["text"],
        )
        self.email_field = TextInput(
            hint_text="E-mail address",
            multiline=False, size_hint_y=None, height=44,
            padding=[10, 12],
        )
        self.password_field = TextInput(
            hint_text="Password (min 6 characters)",
            password=True, multiline=False,
            size_hint_y=None, height=44, padding=[10, 12],
        )
        self.action_button = RoundedButton(
            text="Sign in", size_hint_y=None, height=48,
        )
        self.action_button.bind(on_release=self._submit)

        self.status_label = Label(
            text="", color=THEME["muted"], font_size=13,
            size_hint_y=None, height=20,
        )

        card.add_widget(self.name_field)
        card.add_widget(self.email_field)
        card.add_widget(self.password_field)
        card.add_widget(self.action_button)
        card.add_widget(self.status_label)
        wrapper.add_widget(card)

        wrapper.add_widget(BoxLayout())  # spacer
        self.add_widget(wrapper)

        # Start in sign-in mode
        self._switch_mode("signin")

    # --------------------------------------------------- handlers
    def _switch_mode(self, mode: str) -> None:
        self._mode = mode
        self.name_field.opacity = 1 if mode == "signup" else 0
        self.name_field.disabled = mode != "signup"
        self.action_button.text = "Create account" if mode == "signup" else "Sign in"
        self.status_label.text = ""

    def _submit(self, *_):
        app = App.get_running_app()
        email = self.email_field.text
        password = self.password_field.text

        if self._mode == "signup":
            ok, msg = app.auth.register(email, password, self.name_field.text)
        else:
            ok, msg = app.auth.login(email, password)

        if ok:
            Snackbar(msg, success=True).show()
            if self._mode == "signup":
                # After registering, switch to sign-in for clarity
                self._switch_mode("signin")
                self.tab_signin.state = "down"
                self.tab_signup.state = "normal"
            else:
                # Reset fields then navigate to dashboard
                self.password_field.text = ""
                self.manager.current = "dashboard"
        else:
            self.status_label.color = THEME["danger"]
            self.status_label.text = msg
