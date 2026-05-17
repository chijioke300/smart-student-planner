"""
Smart Student Planner - Mobile Application Entry Point.

Module: LDC6004M Mobile Application Development
Framework: Kivy (Python cross-platform framework)
Architecture: Model-View-Controller (MVC)

This file bootstraps the Kivy application, registers every screen with
the ScreenManager, wires the controllers, and starts the main event loop.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Local imports: controllers, services and screens
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController
from services.storage_service import StorageService

from views.login_screen import LoginScreen
from views.dashboard_screen import DashboardScreen
from views.task_form_screen import TaskFormScreen
from views.settings_screen import SettingsScreen

from utils.theme import THEME


# Set a realistic phone aspect ratio for desktop testing.
# On Android/iOS the operating system controls the window size.
Window.size = (380, 760)
Window.clearcolor = THEME["background"]


class SmartStudentPlannerApp(App):
    """Root Kivy application class.

    Holds references to the shared services and controllers so every
    screen can access the same state through ``App.get_running_app()``.
    """

    title = "Smart Student Planner"

    def build(self):
        """Create services, controllers, load KV rules, and build the UI."""
        self.storage = StorageService()
        self.auth = AuthController(self.storage)
        self.tasks = TaskController(self.storage)
        
        # Load the KV file to register screen class rules
        Builder.load_file("Ui/smartstudentplanner.kv")
        
        # Create the ScreenManager
        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        
        # Add each screen to the manager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TaskFormScreen(name="task_form"))
        sm.add_widget(SettingsScreen(name="settings"))
        
        return sm

    def on_start(self):
        if self.auth.current_user:
            self.root.current = "dashboard"
        else:
            self.root.current = "login"


if __name__ == "__main__":
    SmartStudentPlannerApp().run()
