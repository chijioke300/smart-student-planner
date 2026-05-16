"""
Settings screen.

Hosts the small handful of preferences plus the sign-out action.
Settings are saved through the storage service so they survive between
sessions.
"""

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    """User preferences and sign-out."""

    account_label_text = StringProperty("")

    def on_pre_enter(self, *_):
        app = App.get_running_app()
        self.ids.contrast_switch.active = bool(app.storage.settings.get("dark_mode", False))
        if app.auth.current_user:
            self.ids.account_label.text = f"Signed in as {app.auth.current_user.email}"

    def _on_contrast(self, _switch, value):
        App.get_running_app().storage.update_settings(dark_mode=value)

    def _sign_out(self, *_):
        app = App.get_running_app()
        app.auth.logout()
        self.manager.current = "login"
