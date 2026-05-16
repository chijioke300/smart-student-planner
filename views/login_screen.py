"""
Login screen.

Combines login and quick registration in a single, tabbed view. The
screen delegates every business decision to ``AuthController`` so it
stays a thin presentation layer.
"""

from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen

from views.common import Snackbar


class LoginScreen(Screen):
    """Sign-in / register entry point."""

    mode = StringProperty("signin")
    status_text = StringProperty("")
    status_error = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Track when the screen is displayed so we can initialize fields
        self.bind(on_enter=self._on_enter)

    def _on_enter(self, *args):
        """Initialize field references when screen is shown."""
        # These will be created by KV before on_enter is called
        pass

    def _submit(self, *_):
        app = App.get_running_app()
        email = self.ids.email_field.text
        password = self.ids.password_field.text

        if self.mode == "signup":
            ok, msg = app.auth.register(email, password, self.ids.name_field.text)
        else:
            ok, msg = app.auth.login(email, password)

        if ok:
            Snackbar(msg, success=True).show()
            if self.mode == "signup":
                self.mode = "signin"
                self.ids.tab_signin.state = "down"
                self.ids.tab_signup.state = "normal"
            else:
                self.ids.password_field.text = ""
                self.manager.current = "dashboard"
        else:
            self.status_error = True
            self.status_text = msg
