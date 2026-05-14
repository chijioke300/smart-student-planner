"""
Settings screen.

Hosts the small handful of preferences plus the sign-out action.
Settings are saved through the storage service so they survive between
sessions.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch

from utils.theme import THEME, FONT_BODY, FONT_TITLE, PADDING, SPACING
from views.common import RoundedButton, Card


class SettingsScreen(Screen):
    """User preferences and sign-out."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=PADDING, spacing=SPACING)

        # Header row
        header = BoxLayout(size_hint_y=None, height=44, spacing=8)
        back = RoundedButton(text="< Back", size_hint_x=None, width=92,
                             bg=THEME["border"], fg=THEME["text"])
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "dashboard"))
        heading = Label(text="Settings", font_size=FONT_TITLE, bold=True,
                        color=THEME["text"], halign="left", valign="middle")
        heading.bind(size=lambda *_: setattr(heading, "text_size", heading.size))
        header.add_widget(back)
        header.add_widget(heading)
        root.add_widget(header)

        # Preferences card
        prefs = Card(size_hint_y=None, height=120)
        row = BoxLayout(size_hint_y=None, height=44, spacing=8)
        row.add_widget(Label(text="High-contrast banner", color=THEME["text"],
                             font_size=FONT_BODY, halign="left", valign="middle"))
        self.contrast_switch = Switch(active=False, size_hint_x=None, width=80)
        self.contrast_switch.bind(active=self._on_contrast)
        row.add_widget(self.contrast_switch)
        prefs.add_widget(row)

        self.account_label = Label(
            text="", color=THEME["muted"], font_size=13,
            size_hint_y=None, height=22, halign="left", valign="middle",
        )
        self.account_label.bind(size=lambda *_:
                                setattr(self.account_label, "text_size", self.account_label.size))
        prefs.add_widget(self.account_label)
        root.add_widget(prefs)

        # Sign out button
        signout = RoundedButton(text="Sign out", bg=THEME["danger"],
                                size_hint_y=None, height=48)
        signout.bind(on_release=self._sign_out)
        root.add_widget(signout)

        root.add_widget(BoxLayout())  # spacer
        self.add_widget(root)

    # ------------------------------------------------------------- events
    def on_pre_enter(self, *_):
        app = App.get_running_app()
        self.contrast_switch.active = bool(app.storage.settings.get("dark_mode", False))
        if app.auth.current_user:
            self.account_label.text = f"Signed in as {app.auth.current_user.email}"

    def _on_contrast(self, _switch, value):
        App.get_running_app().storage.update_settings(dark_mode=value)

    def _sign_out(self, *_):
        app = App.get_running_app()
        app.auth.logout()
        self.manager.current = "login"
