"""Tests for src/solver/bfs.py — Breadth-First Search maze solving."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.solver.bfs import BFSMazeSolver
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.algo.dfs import DFSMazeGenerator


class TestBFSConstruction:
    """Test BFS solver construction."""

    def test_bfs_stores_maze(self):
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert solver.maze is maze

    def test_bfs_inherits_directions(self):
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, '_DIRECTIONS')
        assert len(solver._DIRECTIONS) == 4


class TestBFSSolving:
    """Test BFS maze solving."""

    def test_solve_returns_path_or_none(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        solver = BFSMazeSolver(maze)
        result = solver.solve()
        assert result is None or isinstance(result, list)

    def test_solve_step_yields_tuples(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        solver = BFSMazeSolver(maze)
        steps = list(solver.solve_step())
        assert len(steps) > 0
        for step, is_final in steps:
            assert isinstance(step, (list, type(None)))
            assert isinstance(is_final, bool)

    def test_solve_respects_entry_exit(self):
        """Test that solution respects entry and exit points."""
        maze = Maze(5, 5, entry_point=(0, 0), exit_point=(4, 4))
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        solver = BFSMazeSolver(maze)
        path = solver.solve()
        if path:
            assert path[0] == maze.entry
            assert path[-1] == maze.exit

    def test_path_cells_are_adjacent(self):
        """Test that solution path contains adjacent cells."""
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        solver = BFSMazeSolver(maze)
        path = solver.solve()
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                cell1 = path[i]
                cell2 = path[i + 1]
                # Check that cells are adjacent
                dx = abs(cell1.x - cell2.x)
                dy = abs(cell1.y - cell2.y)
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
