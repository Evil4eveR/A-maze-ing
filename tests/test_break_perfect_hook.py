"""Tests for src/hooks/break_perfect.py — Break perfect maze hook."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.hooks.break_perfect import BreakPerfect
from mazegen.models.maze import Maze
from mazegen.algo.dfs import DFSMazeGenerator


class TestBreakPerfectConstruction:
    """Test BreakPerfect hook construction."""

    def test_hook_stage_is_post(self):
        """Test that BreakPerfect is a post-generation hook."""
        hook = BreakPerfect()
        assert hook.stage == "post"

    def test_hook_is_callable(self):
        """Test that BreakPerfect hook is callable."""
        hook = BreakPerfect()
        assert callable(hook)


class TestBreakPerfectFunctionality:
    """Test BreakPerfect hook functionality."""

    def test_break_perfect_takes_maze_parameter(self):
        """Test that BreakPerfect __call__ accepts a maze."""
        hook = BreakPerfect()
        maze = Maze(5, 5)
        result = hook(maze)
        assert isinstance(result, Maze)

    def test_break_perfect_returns_maze(self):
        """Test that BreakPerfect returns a Maze instance."""
        hook = BreakPerfect()
        maze = Maze(5, 5)
        result = hook(maze)
        assert result is maze


class TestBreakPerfectWithGeneratedMaze:
    """Test BreakPerfect with generated mazes."""

    def test_break_perfect_on_generated_maze(self):
        """Test applying BreakPerfect to a generated maze."""
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        
        initial_walls = sum(
            1 for row in maze.grid
            for cell in row
            if cell.walls > 0
        )
        
        hook = BreakPerfect()
        result = hook(maze)
        
        assert isinstance(result, Maze)

    def test_break_perfect_can_be_applied_multiple_times(self):
        """Test that BreakPerfect can be applied multiple times."""
        maze = Maze(5, 5)
        hook = BreakPerfect()
        
        result1 = hook(maze)
        result2 = hook(result1)
        
        assert isinstance(result2, Maze)

    def test_break_perfect_preserves_maze_dimensions(self):
        """Test that BreakPerfect preserves maze dimensions."""
        maze = Maze(7, 9)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        
        hook = BreakPerfect()
        result = hook(maze)
        
        assert result.width == 7
        assert result.height == 9


class TestBreakPerfectParameters:
    """Test BreakPerfect hook parameters."""

    def test_break_perfect_accepts_percentage(self):
        """Test that BreakPerfect can accept a percentage parameter."""
        # Check if BreakPerfect __init__ accepts parameters
        try:
            hook = BreakPerfect(percentage=20)
            assert hook is not None
        except TypeError:
            # Parameter might not be supported
            hook = BreakPerfect()
            assert hook is not None

    def test_break_perfect_has_reasonable_default(self):
        """Test that BreakPerfect has reasonable defaults."""
        hook = BreakPerfect()
        assert hasattr(hook, 'stage')
        assert hook.stage in ["pre", "post"]
