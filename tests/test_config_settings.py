"""Tests for src/config.py — Settings configuration."""

import sys
import os
import pytest
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestSettingsConstantsAndClass:
    """Test Settings class constants and attributes."""
    
    def test_settings_wall_character_defined(self):
        """Test wall character is defined."""
        from config import Settings
        assert hasattr(Settings, 'wall')
        assert Settings.wall == "\u2588\u2588"
    
    def test_settings_cell_character_defined(self):
        """Test cell character is defined."""
        from config import Settings
        assert hasattr(Settings, 'cell')
    
    def test_settings_path_character_defined(self):
        """Test path character is defined."""
        from config import Settings
        assert hasattr(Settings, 'path')
        assert Settings.path == "\u2591\u2591"


class TestSettingsInitialization:
    """Test Settings initialization with valid config."""
    
    def test_settings_can_be_created_with_config(self):
        """Test that Settings can be instantiated with a valid config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "test_config.txt"
            config_file.write_text(
                "width=10\nheight=10\nentry=0,0\nexit=9,9\noutput_file=maze.txt\nperfect=true"
            )
            
            # Temporarily change sys.argv for Settings to load the config
            old_argv = sys.argv.copy()
            try:
                sys.argv = ['test', str(config_file)]
                # Reload config module to pick up new sys.argv
                import importlib
                import config
                importlib.reload(config)
                
                settings = config.settings
                assert settings.width == 10
                assert settings.height == 10
            finally:
                sys.argv = old_argv
    
    def test_settings_entry_parsing(self):
        """Test that entry string is parsed correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "test_config.txt"
            config_file.write_text(
                "width=10\nheight=10\nentry=2,3\nexit=9,9\noutput_file=maze.txt\nperfect=true"
            )
            
            old_argv = sys.argv.copy()
            try:
                sys.argv = ['test', str(config_file)]
                import importlib
                import config
                importlib.reload(config)
                
                settings = config.settings
                assert settings.entry == (2, 3)
            finally:
                sys.argv = old_argv
    
    def test_settings_exit_parsing(self):
        """Test that exit string is parsed correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "test_config.txt"
            config_file.write_text(
                "width=10\nheight=10\nentry=0,0\nexit=5,7\noutput_file=maze.txt\nperfect=true"
            )
            
            old_argv = sys.argv.copy()
            try:
                sys.argv = ['test', str(config_file)]
                import importlib
                import config
                importlib.reload(config)
                
                settings = config.settings
                assert settings.exit == (5, 7)
            finally:
                sys.argv = old_argv


class TestSettingsValidation:
    """Test Settings field validation."""
    
    def test_settings_fields_are_required(self):
        """Test that required fields must be provided."""
        from pydantic_core import ValidationError
        from config import Settings
        
        with pytest.raises(ValidationError):
            Settings()
    
    def test_settings_accepts_all_required_fields(self):
        """Test Settings initialization with all required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "test_config.txt"
            config_file.write_text(
                "width=5\nheight=5\nentry=0,0\nexit=4,4\noutput_file=test.txt\nperfect=false"
            )
            
            old_argv = sys.argv.copy()
            try:
                sys.argv = ['test', str(config_file)]
                import importlib
                import config
                importlib.reload(config)
                
                settings = config.settings
                assert settings.width == 5
                assert settings.height == 5
                assert settings.entry == (0, 0)
                assert settings.exit == (4, 4)
                assert settings.output_file == "test.txt"
                assert settings.perfect is False
            finally:
                sys.argv = old_argv
