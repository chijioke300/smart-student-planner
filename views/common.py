"""
Reusable Kivy widget helpers used across multiple screens.

Keeping these in one file avoids duplicating boilerplate (rounded
buttons, status bars, padded labels, snackbar-style notifications) and
helps the codebase feel consistent.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.modalview import ModalView

from utils.theme import THEME, FONT_BODY, FONT_SMALL, PADDING


class RoundedButton(Button):
    """A flat, rounded button that respects the THEME palette."""

    def __init__(self, bg=None, fg=None, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = fg or THEME["surface"]
        self._bg = bg or THEME["primary"]
        with self.canvas.before:
            self._color_instr = Color(*self._bg)
            self._rect = RoundedRectangle(radius=[12], pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)
        self.font_size = FONT_BODY

    def _sync(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_bg(self, rgba):
        self._bg = rgba
        self._color_instr.rgba = rgba


class Card(BoxLayout):
    """A white surface with a soft border and rounded corners."""

    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("padding", PADDING)
        kwargs.setdefault("spacing", 8)
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*THEME["surface"])
            self._bg = RoundedRectangle(radius=[14], pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size


class Snackbar(ModalView):
    """Lightweight bottom notification for user feedback messages."""

    def __init__(self, message: str, success: bool = True, **kwargs):
        super().__init__(
            size_hint=(0.86, None), height=64,
            background="", background_color=(0, 0, 0, 0),
            auto_dismiss=False, **kwargs,
        )
        bar = BoxLayout(padding=PADDING)
        with bar.canvas.before:
            Color(*(THEME["success"] if success else THEME["danger"]))
            self._bg = RoundedRectangle(radius=[10], pos=bar.pos, size=bar.size)
        bar.bind(pos=self._sync, size=self._sync)
        bar.add_widget(Label(text=message, color=(1, 1, 1, 1), font_size=FONT_SMALL))
        self.add_widget(bar)

    def _sync(self, instance, *_):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def show(self):
        self.open()
        Clock.schedule_once(lambda *_: self.dismiss(), 1.8)
