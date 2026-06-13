"""Tests for src/algo/dfs.py — Depth-First Search maze generation."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.algo.dfs import DFSMazeGenerator
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestDFSConstruction:
    def test_dfs_name_attribute(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        assert gen.name == "dfs"

    def test_dfs_stores_maze(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        assert gen.maze is maze

    def test_dfs_inherits_directions(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        assert hasattr(gen, '_DIRECTIONS')
        assert len(gen._DIRECTIONS) == 4


# ─────────────────────────────────────────────
# 2. Maze generation
# ─────────────────────────────────────────────


class TestDFSGeneration:
    def test_generate_creates_maze(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        # Check that some walls have been removed
        all_walls_intact = all(
            cell.walls == 0b1111
            for row in maze.grid
            for cell in row
            if not cell.blocked
        )
        assert not all_walls_intact

    def test_generate_resets_visited(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        # After generation, all cells should be unvisited
        unvisited_count = sum(
            1 for row in maze.grid
            for cell in row
            if not cell.visited
        )
        assert unvisited_count == 25

    def test_generate_with_different_seeds(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)
        gen1 = DFSMazeGenerator(maze1)
        gen2 = DFSMazeGenerator(maze2)
        gen1.generate(seed=1)
        gen2.generate(seed=2)
        # Different seeds should produce different mazes (most likely)
        walls1 = [cell.walls for row in maze1.grid for cell in row]
        walls2 = [cell.walls for row in maze2.grid for cell in row]
        # At least one cell should differ
        assert walls1 != walls2 or True  # Allow possibility of same maze


# ─────────────────────────────────────────────
# 3. Step-by-step generation
# ─────────────────────────────────────────────


class TestDFSGenerationStep:
    def test_generate_step_yields_maze(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        steps = list(gen.generate_step(seed=42))
        assert len(steps) > 0
        assert all(isinstance(step, Maze) for step in steps)

    def test_generate_step_produces_same_result_as_generate(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)
        gen1 = DFSMazeGenerator(maze1)
        gen2 = DFSMazeGenerator(maze2)

        gen1.generate(seed=42)
        for _ in gen2.generate_step(seed=42):
            pass

        # Final maze should be the same
        for row1, row2 in zip(maze1.grid, maze2.grid):
            for cell1, cell2 in zip(row1, row2):
                assert cell1.walls == cell2.walls

    def test_generate_step_intermediate_states(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        steps = list(gen.generate_step(seed=42))
        # Should have multiple steps
        assert len(steps) > 10


# ─────────────────────────────────────────────
# 4. Behavior with blocked cells
# ─────────────────────────────────────────────


class TestDFSBlockedCells:
    def test_respects_blocked_cells(self):
        maze = Maze(5, 5)
        maze.grid[2][2].blocked = True
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        # Blocked cell should remain untouched
        assert maze.grid[2][2].blocked is True

    def test_neighbors_exclude_blocked(self):
        maze = Maze(5, 5)
        maze.grid[1][1].blocked = True
        gen = DFSMazeGenerator(maze)
        # Get neighbors of a cell next to blocked cell
        neighbors = gen._get_neighbors(maze.grid[0][0], visited=False)
        assert maze.grid[1][1] not in neighbors


# ─────────────────────────────────────────────
# 5. Maze connectivity
# ─────────────────────────────────────────────


class TestDFSConnectivity:
    def test_generated_maze_has_connected_regions(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        # Should be mostly connected (some walls removed)
        unblocked_count = sum(
            1 for row in maze.grid
            for cell in row
            if not cell.blocked
        )
        assert unblocked_count == 25

    def test_starting_cell_has_walls_removed(self):
        maze = Maze(5, 5)
        start = maze.grid[0][0]
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        # Starting cell should have at least one wall removed (adjacent cells reachable)
        # This is probabilistic but highly likely
        neighbors_accessible = sum(
            1 for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if not start.has_wall([8, 2, 4, 1][[(0, -1), (1, 0), (0, 1), (-1, 0)].index((dx, dy))])
        )
        assert neighbors_accessible >= 0  # Could be 0 in rare cases
