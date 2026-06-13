"""Tests for src/algo/prim.py — Prim maze generation."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.algo.prim import PrimMazeGenerator
from mazegen.models.maze import Maze


class TestPrimConstruction:
    def test_prim_name_attribute(self):
        maze = Maze(5, 5)
        gen = PrimMazeGenerator(maze)
        assert gen.name == "prim"

    def test_prim_stores_maze(self):
        maze = Maze(5, 5)
        gen = PrimMazeGenerator(maze)
        assert gen.maze is maze


class TestPrimGeneration:
    def test_generate_creates_maze(self):
        maze = Maze(5, 5)
        gen = PrimMazeGenerator(maze)
        gen.generate(seed=42)
        all_walls_intact = all(
            cell.walls == 0b1111
            for row in maze.grid
            for cell in row
            if not cell.blocked
        )
        assert not all_walls_intact

    def test_generate_resets_visited(self):
        maze = Maze(5, 5)
        gen = PrimMazeGenerator(maze)
        gen.generate(seed=42)
        unvisited_count = sum(
            1 for row in maze.grid
            for cell in row
            if not cell.visited
        )
        assert unvisited_count == 25

    def test_generate_step_yields_maze(self):
        maze = Maze(5, 5)
        gen = PrimMazeGenerator(maze)
        steps = list(gen.generate_step(seed=42))
        assert len(steps) > 0

    def test_respects_blocked_cells(self):
        maze = Maze(5, 5)
        maze.grid[2][2].blocked = True
        gen = PrimMazeGenerator(maze)
        gen.generate(seed=42)
        assert maze.grid[2][2].blocked is True
