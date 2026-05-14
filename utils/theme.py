"""
Centralised theme constants for the Smart Student Planner.

Keeping colours, sizes and fonts in one module means any future
redesign only needs to change a single file. This is a simple
implementation of the Single Source of Truth principle.
"""

# Colour palette (RGBA tuples in the 0-1 range that Kivy expects).
# Inspired by Material Design 3 colour-token guidance (Google, 2024).
THEME = {
    "primary": (0.30, 0.46, 0.92, 1),       # Calm indigo
    "primary_dark": (0.20, 0.34, 0.75, 1),
    "accent": (0.99, 0.66, 0.18, 1),        # Warm amber
    "success": (0.18, 0.69, 0.38, 1),
    "danger": (0.86, 0.21, 0.27, 1),
    "background": (0.96, 0.97, 0.99, 1),
    "surface": (1.00, 1.00, 1.00, 1),
    "text": (0.10, 0.13, 0.20, 1),
    "muted": (0.45, 0.49, 0.58, 1),
    "border": (0.85, 0.88, 0.93, 1),
}

# Priority chip colours
PRIORITY_COLOURS = {
    "High": (0.86, 0.21, 0.27, 1),
    "Medium": (0.99, 0.66, 0.18, 1),
    "Low": (0.18, 0.69, 0.38, 1),
}

# Standard padding, spacing and font sizes
PADDING = 16
SPACING = 12
FONT_SMALL = 13
FONT_BODY = 15
FONT_LARGE = 18
FONT_TITLE = 22
