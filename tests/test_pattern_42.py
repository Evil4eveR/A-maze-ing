"""Tests for src/hooks/pattern_42.py — 42 pattern hook."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.hooks.pattern_42 import Add42Pattern
from mazegen.models.maze import Maze
from mazegen.exceptions import MazeSizeError


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestAdd42PatternConstruction:
    def test_hook_stage_is_pre(self):
        hook = Add42Pattern()
        assert hook.stage == "pre"

    def test_min_width_constant(self):
        assert Add42Pattern.MIN_WIDTH == 8

    def test_min_height_constant(self):
        assert Add42Pattern.MIN_HEIGHT == 7


# ─────────────────────────────────────────────
# 2. Size validation
# ─────────────────────────────────────────────


class TestAdd42PatternSizeValidation:
    def test_maze_too_small_width_raises(self):
        maze = Maze(5, 10)
        hook = Add42Pattern()
        with pytest.raises(MazeSizeError):
            hook(maze)

    def test_maze_too_small_height_raises(self):
        maze = Maze(10, 5)
        hook = Add42Pattern()
        with pytest.raises(MazeSizeError):
            hook(maze)

    def test_maze_too_small_both_raises(self):
        maze = Maze(5, 5)
        hook = Add42Pattern()
        with pytest.raises(MazeSizeError):
            hook(maze)

    def test_minimum_size_maze(self):
        maze = Maze(8, 7)
        hook = Add42Pattern()
        result = hook(maze)
        assert result is maze

    def test_larger_maze_accepted(self):
        maze = Maze(20, 20)
        hook = Add42Pattern()
        result = hook(maze)
        assert result is maze


# ─────────────────────────────────────────────
# 3. Pattern application
# ─────────────────────────────────────────────


class TestAdd42PatternApplication:
    def test_pattern_creates_blocked_cells(self):
        maze = Maze(20, 20)
        hook = Add42Pattern()
        hook(maze)

        # Should have some blocked cells
        blocked_count = sum(
            1 for row in maze.grid
            for cell in row
            if cell.blocked
        )
        assert blocked_count > 0

    def test_pattern_centered(self):
        maze = Maze(20, 20)
        hook = Add42Pattern()
        hook(maze)

        # Pattern should be roughly centered
        # Some cells around the center should be blocked
        center_x, center_y = maze.width // 2, maze.height // 2
        blocked_in_center = 0
        for y in range(max(0, center_y - 5), min(maze.height, center_y + 5)):
            for x in range(max(0, center_x - 5), min(maze.width, center_x + 5)):
                if maze.grid[y][x].blocked:
                    blocked_in_center += 1

        assert blocked_in_center > 0


# ─────────────────────────────────────────────
# 4. Hook callable behavior
# ─────────────────────────────────────────────


class TestAdd42PatternCallable:
    def test_hook_returns_maze(self):
        maze = Maze(20, 20)
        hook = Add42Pattern()
        result = hook(maze)
        assert result is maze

    def test_hook_is_callable(self):
        hook = Add42Pattern()
        assert callable(hook)

    def test_multiple_calls_consistent(self):
        maze1 = Maze(20, 20)
        maze2 = Maze(20, 20)

        hook = Add42Pattern()
        hook(maze1)
        hook(maze2)

        # Both should have the same pattern
        for y in range(20):
            for x in range(20):
                assert maze1.grid[y][x].blocked == maze2.grid[y][x].blocked
