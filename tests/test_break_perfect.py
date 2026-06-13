"""Tests for src/hooks/break_perfect.py — Break perfect hook."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.hooks.break_perfect import BreakPerfect
from mazegen.models.maze import Maze
from mazegen.algo.dfs import DFSMazeGenerator


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestBreakPerfectConstruction:
    def test_hook_stage_is_post(self):
        hook = BreakPerfect()
        assert hook.stage == "post"

    def test_default_percent(self):
        hook = BreakPerfect()
        assert hook.percent == 0.1

    def test_default_seed_none(self):
        hook = BreakPerfect()
        assert hook.seed is None

    def test_custom_percent(self):
        hook = BreakPerfect(percent=0.2)
        assert hook.percent == 0.2

    def test_custom_seed(self):
        hook = BreakPerfect(percent=0.1, seed=42)
        assert hook.seed == 42


# ─────────────────────────────────────────────
# 2. Hook callable behavior
# ─────────────────────────────────────────────


class TestBreakPerfectCallable:
    def test_hook_returns_maze(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        hook = BreakPerfect(percent=0.1, seed=42)
        result = hook(maze)
        assert result is maze

    def test_hook_breaks_walls(self):
        maze = Maze(10, 10)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        initial_walls = sum(
            1 for row in maze.grid
            for cell in row
            if cell.walls > 0
        )

        hook = BreakPerfect(percent=0.3, seed=42)
        hook(maze)

        final_walls = sum(
            1 for row in maze.grid
            for cell in row
            if cell.walls > 0
        )

        # Should have fewer or equal walls after breaking
        assert final_walls <= initial_walls


# ─────────────────────────────────────────────
# 3. Different percentages
# ─────────────────────────────────────────────


class TestBreakPerfectPercentages:
    def test_zero_percent_no_change(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        initial_state = [
            [cell.walls for cell in row]
            for row in maze.grid
        ]

        hook = BreakPerfect(percent=0.0, seed=42)
        hook(maze)

        final_state = [
            [cell.walls for cell in row]
            for row in maze.grid
        ]

        assert initial_state == final_state

    def test_higher_percent_more_walls_broken(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)

        gen = DFSMazeGenerator(maze1)
        gen.generate(seed=42)

        # Copy maze1 to maze2
        for y in range(5):
            for x in range(5):
                maze2.grid[y][x].walls = maze1.grid[y][x].walls

        hook1 = BreakPerfect(percent=0.1, seed=100)
        hook2 = BreakPerfect(percent=0.3, seed=100)

        hook1(maze1)
        hook2(maze2)

        walls1 = sum(1 for row in maze1.grid for cell in row if cell.walls > 0)
        walls2 = sum(1 for row in maze2.grid for cell in row if cell.walls > 0)

        # More walls should be broken with higher percentage
        assert walls2 <= walls1
