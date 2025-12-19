# backend/themes/templates/__init__.py
"""Theme templates for Storybook.ai"""

from .space_story import SPACE_TEMPLATE

THEMES = {
    "space": SPACE_TEMPLATE,
}

def get_theme(theme_id: str):
    """Get theme by ID, defaults to space."""
    return THEMES.get(theme_id, SPACE_TEMPLATE)
