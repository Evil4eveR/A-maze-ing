"""Tests for src/models/maze.py — Maze grid management."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.exceptions import InvalidEntryExitError


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestMazeConstruction:
    def test_basic_maze_creation(self):
        maze = Maze(5, 5)
        assert maze.width == 5
        assert maze.height == 5

    def test_grid_dimensions(self):
        maze = Maze(3, 4)
        assert len(maze.grid) == 4  # height
        assert len(maze.grid[0]) == 3  # width

    def test_default_entry_point(self):
        maze = Maze(5, 5)
        assert maze.entry.x == 0
        assert maze.entry.y == 0

    def test_custom_entry_point(self):
        maze = Maze(5, 5, entry_point=(2, 2))
        assert maze.entry.x == 2
        assert maze.entry.y == 2

    def test_default_exit_point(self):
        maze = Maze(5, 5)
        assert maze.exit.x == 4
        assert maze.exit.y == 4

    def test_custom_exit_point(self):
        maze = Maze(5, 5, exit_point=(1, 1))
        assert maze.exit.x == 1
        assert maze.exit.y == 1

    def test_seed_initially_none(self):
        maze = Maze(5, 5)
        assert maze.seed is None

    def test_algorithm_initially_none(self):
        maze = Maze(5, 5)
        assert maze.algo is None

    def test_all_cells_unique(self):
        maze = Maze(3, 3)
        cells = set()
        for row in maze.grid:
            for cell in row:
                cells.add(id(cell))
        assert len(cells) == 9

    def test_cells_have_correct_coordinates(self):
        maze = Maze(3, 3)
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                assert cell.x == x
                assert cell.y == y


# ─────────────────────────────────────────────
# 2. get_cell
# ─────────────────────────────────────────────


class TestGetCell:
    def test_get_valid_cell(self):
        maze = Maze(5, 5)
        cell = maze.get_cell(2, 3)
        assert cell is not None
        assert cell.x == 2
        assert cell.y == 3

    def test_get_corner_cells(self):
        maze = Maze(5, 5)
        assert maze.get_cell(0, 0) is not None
        assert maze.get_cell(4, 4) is not None
        assert maze.get_cell(0, 4) is not None
        assert maze.get_cell(4, 0) is not None

    def test_get_cell_negative_x(self):
        maze = Maze(5, 5)
        assert maze.get_cell(-1, 2) is None

    def test_get_cell_negative_y(self):
        maze = Maze(5, 5)
        assert maze.get_cell(2, -1) is None

    def test_get_cell_x_out_of_bounds(self):
        maze = Maze(5, 5)
        assert maze.get_cell(5, 2) is None

    def test_get_cell_y_out_of_bounds(self):
        maze = Maze(5, 5)
        assert maze.get_cell(2, 5) is None

    def test_get_cell_both_out_of_bounds(self):
        maze = Maze(5, 5)
        assert maze.get_cell(10, 10) is None


# ─────────────────────────────────────────────
# 3. get_unvisited
# ─────────────────────────────────────────────


class TestGetUnvisited:
    def test_all_unvisited_initially(self):
        maze = Maze(2, 2)
        unvisited = maze.get_unvisited()
        assert len(unvisited) == 4

    def test_unvisited_excludes_visited_cells(self):
        maze = Maze(2, 2)
        maze.grid[0][0].visited = True
        unvisited = maze.get_unvisited()
        assert len(unvisited) == 3

    def test_unvisited_excludes_blocked_cells(self):
        maze = Maze(2, 2)
        maze.grid[0][0].blocked = True
        unvisited = maze.get_unvisited()
        assert len(unvisited) == 3

    def test_unvisited_excludes_visited_and_blocked(self):
        maze = Maze(2, 2)
        maze.grid[0][0].visited = True
        maze.grid[0][1].blocked = True
        unvisited = maze.get_unvisited()
        assert len(unvisited) == 2

    def test_unvisited_empty_when_all_visited(self):
        maze = Maze(2, 2)
        for row in maze.grid:
            for cell in row:
                cell.visited = True
        unvisited = maze.get_unvisited()
        assert len(unvisited) == 0

    def test_unvisited_returns_correct_cells(self):
        maze = Maze(2, 2)
        target = maze.grid[1][1]
        maze.grid[0][0].visited = True
        maze.grid[0][1].blocked = True
        unvisited = maze.get_unvisited()
        assert target in unvisited


# ─────────────────────────────────────────────
# 4. add_blocked_cells
# ─────────────────────────────────────────────


class TestAddBlockedCells:
    def test_add_single_blocked_cell(self):
        maze = Maze(5, 5)
        maze.add_blocked_cells([(2, 2)])
        assert maze.grid[2][2].blocked is True

    def test_add_multiple_blocked_cells(self):
        maze = Maze(5, 5)
        cells = [(1, 1), (2, 2), (3, 3)]
        maze.add_blocked_cells(cells)
        for x, y in cells:
            assert maze.grid[y][x].blocked is True

    def test_add_blocked_cells_with_offset(self):
        maze = Maze(5, 5)
        maze.add_blocked_cells([(1, 1)], offset=(2, 2))
        assert maze.grid[3][3].blocked is True

    def test_add_blocked_cells_out_of_bounds_ignored(self):
        maze = Maze(3, 3)
        maze.add_blocked_cells([(10, 10)])
        # Should not crash, out of bounds cells ignored

    def test_add_blocked_cells_partial_overlap(self):
        maze = Maze(3, 3)
        cells = [(0, 0), (10, 10)]
        maze.add_blocked_cells(cells)
        assert maze.grid[0][0].blocked is True

    def test_unblocked_cells_remain_unblocked(self):
        maze = Maze(5, 5)
        maze.add_blocked_cells([(2, 2)])
        assert maze.grid[0][0].blocked is False
        assert maze.grid[1][1].blocked is False


# ─────────────────────────────────────────────
# 5. open_entry_exit
# ─────────────────────────────────────────────


class TestOpenEntryExit:
    def test_open_entry_exit_top_left(self):
        maze = Maze(5, 5, entry_point=(0, 0), exit_point=(4, 4))
        maze.open_entry_exit()
        # Entry at top-left should have west wall open
        assert maze.entry.has_wall(Cell.WEST) is False
        # Exit at bottom-right should have east wall open
        assert maze.exit.has_wall(Cell.EAST) is False

    def test_open_entry_exit_preserves_other_walls(self):
        maze = Maze(5, 5, entry_point=(0, 0))
        maze.open_entry_exit()
        assert maze.entry.has_wall(Cell.NORTH) is True
        assert maze.entry.has_wall(Cell.EAST) is True

    def test_entry_at_different_borders(self):
        # Entry at left border (y=0)
        maze1 = Maze(5, 5, entry_point=(0, 0), exit_point=(4, 4))
        maze1.open_entry_exit()
        assert maze1.entry.has_wall(Cell.WEST) is False

        # Entry at right border (y=height-1)
        maze2 = Maze(5, 5, entry_point=(0, 4), exit_point=(4, 0))
        maze2.open_entry_exit()
        assert maze2.entry.has_wall(Cell.EAST) is False


# ─────────────────────────────────────────────
# 6. State tracking
# ─────────────────────────────────────────────


class TestMazeStateTracking:
    def test_seed_can_be_set(self):
        maze = Maze(5, 5)
        maze.seed = 42
        assert maze.seed == 42

    def test_algorithm_can_be_set(self):
        maze = Maze(5, 5)
        maze.algo = "dfs"
        assert maze.algo == "dfs"

    def test_multiple_mazes_independent(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(10, 10)
        maze1.seed = 1
        maze2.seed = 2
        assert maze1.seed != maze2.seed
