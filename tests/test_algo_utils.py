"""Tests for algorithm utilities and hooks."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.hooks.break_perfect import BreakPerfect
from mazegen.models.maze import Maze
from mazegen.models.maze_config import MazeConfig
from mazegen.maze_generator import MazeGenerator


class TestAlgoUtils:
    """Tests for algorithm utility functions."""

    def test_break_perfect_can_be_instantiated(self):
        """Test that BreakPerfect hook can be created."""
        hook = BreakPerfect()
        assert hook is not None

    def test_break_perfect_is_callable(self):
        """Test that BreakPerfect hook is callable."""
        hook = BreakPerfect()
        assert callable(hook)
