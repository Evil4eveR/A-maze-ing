"""Pytest configuration and fixtures for maze tests."""

import sys
import os
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import patch


@pytest.fixture
def mock_settings():
    """Mock settings with default values to prevent initialization errors."""
    mock_config = {
        'width': 10,
        'height': 10,
        'entry_raw': '0,0',
        'exit_raw': '9,9',
        'output_file': 'maze.txt',
        'perfect': True,
        'seed': None,
        'entry': (0, 0),
        'exit': (9, 9),
    }
    
    with patch('config.settings', **mock_config):
        yield mock_config


@pytest.fixture
def sample_maze():
    """Create a basic 5x5 maze for testing."""
    from mazegen.models.maze import Maze
    return Maze(5, 5)


@pytest.fixture
def sample_maze_10x10():
    """Create a 10x10 maze for testing."""
    from mazegen.models.maze import Maze
    return Maze(10, 10)


@pytest.fixture
def autouse_mock_config(monkeypatch):
    """Automatically mock settings for all tests."""
    # Create a minimal config file for testing
    test_config = """width=10
height=10
entry=0,0
exit=9,9
output_file=test_maze.txt
perfect=true"""
    
    config_path = Path(__file__).parent / "test_config.txt"
    config_path.write_text(test_config)
    
    # Mock sys.argv to point to test config
    monkeypatch.setattr(sys, 'argv', ['test', str(config_path)])
    
    yield
    
    # Cleanup
    if config_path.exists():
        config_path.unlink()
