"""Tests for src/models/theme.py — Theme management."""

import sys
import os
import pytest
from dataclasses import is_dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.theme import Theme


class TestThemeConstruction:
    """Test Theme class construction."""

    def test_theme_is_dataclass(self):
        """Test that Theme is a dataclass."""
        assert is_dataclass(Theme)

    def test_theme_creation_with_defaults(self):
        """Test creating a Theme with default values."""
        theme = Theme()
        assert theme.name == "Default"
        assert theme.cell == "#000000"
        assert theme.wall == "#2596BE"

    def test_theme_creation_with_custom_values(self):
        """Test creating a Theme with custom values."""
        theme = Theme(
            name="custom",
            cell="#111111",
            wall="#222222",
            path="#333333"
        )
        assert theme.name == "custom"
        assert theme.cell == "#111111"
        assert theme.wall == "#222222"

    def test_theme_has_all_required_fields(self):
        """Test that Theme has all required color fields."""
        theme = Theme()
        required_fields = ['name', 'cell', 'wall', 'blocked_cell', 'path', 'entry', 'exit']
        for field in required_fields:
            assert hasattr(theme, field)

    def test_theme_default_colors(self):
        """Test Theme default color values."""
        theme = Theme()
        assert theme.cell == "#000000"
        assert theme.wall == "#2596BE"
        assert theme.blocked_cell == "#757575"
        assert theme.path == "#FFFF00"
        assert theme.entry == "#FF00FF"
        assert theme.exit == "#FF0000"

    def test_theme_creation_partial_override(self):
        """Test creating Theme with partial field overrides."""
        theme = Theme(name="MyTheme", wall="#FFFFFF")
        assert theme.name == "MyTheme"
        assert theme.wall == "#FFFFFF"
        assert theme.cell == "#000000"  # Still default


class TestThemeUsage:
    """Test using themes."""

    def test_multiple_themes_independent(self):
        """Test that multiple themes are independent."""
        theme1 = Theme(name="Theme1", wall="#111111")
        theme2 = Theme(name="Theme2", wall="#222222")
        
        assert theme1.name != theme2.name
        assert theme1.wall != theme2.wall

    def test_theme_colors_are_strings(self):
        """Test that all theme colors are strings."""
        theme = Theme()
        color_fields = ['cell', 'wall', 'blocked_cell', 'path', 'entry', 'exit']
        for field in color_fields:
            color_value = getattr(theme, field)
            assert isinstance(color_value, str)
            assert color_value.startswith('#')


class TestThemeModification:
    """Test modifying theme attributes."""

    def test_theme_fields_are_mutable(self):
        """Test that theme fields can be modified."""
        theme = Theme()
        original_wall = theme.wall
        theme.wall = "#AABBCC"
        assert theme.wall != original_wall
        assert theme.wall == "#AABBCC"

    def test_theme_preserves_color_format(self):
        """Test that themes maintain hex color format."""
        theme = Theme()
        new_color = "#ABCDEF"
        theme.cell = new_color
        assert theme.cell == new_color
        assert theme.cell.startswith('#')
