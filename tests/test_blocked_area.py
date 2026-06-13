"""Tests for src/hooks/blocked_area.py — Blocked area hook."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.hooks.blocked_area import AddBlockedArea
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.exceptions import MazeSizeError


class TestAddBlockedAreaConstruction:
    """Test AddBlockedArea construction."""

    def test_hook_stage_is_pre(self):
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        assert hook.stage == "pre"

    def test_hook_stores_parameters(self):
        hook = AddBlockedArea(start=(1, 1), width=3, height=4, maze_resize=False)
        assert hook.start == (1, 1)
        assert hook.width == 3
        assert hook.height == 4
        assert hook.maze_resize is False

    def test_hook_default_maze_resize(self):
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        assert hook.maze_resize is False


class TestAddBlockedAreaDirectMethod:
    """Test AddBlockedArea using direct method call."""

    def test_add_blocked_area_with_tuple_start(self):
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        hook.add_blocked_area(maze)
        assert maze.grid[1][1].blocked is True
        assert maze.grid[1][2].blocked is True
        assert maze.grid[2][1].blocked is True
        assert maze.grid[2][2].blocked is True

    def test_blocked_area_preserves_unblocked(self):
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        hook.add_blocked_area(maze)
        assert maze.grid[0][0].blocked is False
        assert maze.grid[4][4].blocked is False


class TestGetCoordinates:
    """Test coordinate resolution."""

    def test_get_coordinates_returns_tuple(self):
        maze = Maze(10, 10)
        hook = AddBlockedArea(start=(2, 3), width=2, height=2)
        start, end = hook._get_coordinates(maze)
        assert isinstance(start, tuple)
        assert isinstance(end, tuple)
        assert start == (2, 3)
        assert end == (4, 5)

    def test_get_coordinates_string_center(self):
        maze = Maze(10, 10)
        hook = AddBlockedArea(start="center:center", width=2, height=2)
        start, end = hook._get_coordinates(maze)
        assert isinstance(start, tuple)
        assert len(start) == 2

    def test_get_coordinates_string_top_left(self):
        maze = Maze(10, 10)
        hook = AddBlockedArea(start="left:top", width=2, height=2)
        start, end = hook._get_coordinates(maze)
        assert start == (0, 0)

    def test_get_coordinates_string_bottom_right(self):
        maze = Maze(10, 10)
        hook = AddBlockedArea(start="right:bottom", width=2, height=2)
        start, end = hook._get_coordinates(maze)
        assert start == (8, 8)


class TestBlockedAreaBoundaryChecking:
    """Test boundary checking for blocked areas."""

    def test_area_within_bounds_succeeds(self):
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        # Should not raise
        hook.add_blocked_area(maze)

    def test_area_at_edge_succeeds(self):
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(3, 3), width=2, height=2)
        # Should not raise (boundaries are 0-4)
        hook.add_blocked_area(maze)

    def test_area_exceeds_bounds_raises(self):
        """Test that area exceeding bounds raises MazeSizeError."""
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(4, 4), width=3, height=3)
        with pytest.raises(MazeSizeError):
            hook.add_blocked_area(maze)


class TestMazeResize:
    """Test maze resizing with blocked area."""

    def test_maze_resize_true(self):
        """Test that maze_resize=True resizes the maze grid."""
        maze = Maze(5, 5)
        original_width = maze.width
        original_height = maze.height
        
        hook = AddBlockedArea(start=(0, 0), width=3, height=3, maze_resize=True)
        hook.add_blocked_area(maze)
        
        # Maze should be resized to include the blocked area
        assert maze.width == original_width + 3
        assert maze.height == original_height + 3

    def test_maze_resize_false(self):
        """Test that maze_resize=False doesn't resize the maze."""
        maze = Maze(5, 5)
        original_width = maze.width
        original_height = maze.height
        
        hook = AddBlockedArea(start=(0, 0), width=2, height=2, maze_resize=False)
        hook.add_blocked_area(maze)
        
        # Maze should not be resized
        assert maze.width == original_width
        assert maze.height == original_height


class TestCallable:
    """Test AddBlockedArea as a callable hook."""

    def test_hook_is_callable(self):
        """Test that AddBlockedArea is callable."""
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        assert callable(hook)

    def test_call_returns_maze(self):
        """Test that __call__ returns a Maze instance."""
        maze = Maze(5, 5)
        hook = AddBlockedArea(start=(1, 1), width=2, height=2)
        result = hook(maze)
        assert isinstance(result, Maze)
        assert result is maze  # Should return the same maze instance
