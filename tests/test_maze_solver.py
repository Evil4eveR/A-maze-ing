"""Tests for src/maze_solver.py — MazeSolver facade."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.maze_solver import MazeSolver
from mazegen.models.maze_config import MazeConfig
from mazegen.models.maze import Maze
from mazegen.maze_generator import MazeGenerator
from mazegen.exceptions import MazeError


class TestMazeSolverMapping:
    """Test solver mapping."""

    def test_solver_map_has_bfs(self):
        assert "bfs" in MazeSolver.SOLVER_MAP


class TestMazeSolverSolve:
    """Test MazeSolver.solve method."""

    def test_solve_simple_maze(self):
        """Test solving a simple generated maze."""
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        path = MazeSolver.solve(maze, algo="bfs")
        
        # Path should exist (not None)
        assert path is not None
        # Path should start at entry
        assert path[0] == maze.entry
        # Path should end at exit
        assert path[-1] == maze.exit

    def test_solve_with_default_algo(self):
        """Test solving with default BFS algorithm."""
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        path = MazeSolver.solve(maze)
        
        assert path is not None
        assert len(path) > 0

    def test_solve_with_invalid_algo_raises(self):
        """Test that invalid algorithm raises error."""
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        
        with pytest.raises(MazeError):
            MazeSolver.solve(maze, algo="invalid")

    def test_solve_respects_entry_exit(self):
        """Test that solution respects entry and exit points."""
        config = MazeConfig(
            width=10,
            height=10,
            algo="dfs",
            seed=42,
            entry_point=(0, 0),
            exit_point=(9, 9)
        )
        maze = MazeGenerator.create(config)
        path = MazeSolver.solve(maze)
        
        if path:  # Maze is solvable
            assert path[0] == maze.entry
            assert path[-1] == maze.exit
