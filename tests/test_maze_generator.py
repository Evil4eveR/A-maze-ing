"""Tests for src/maze_generator.py — MazeGenerator facade."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.maze_generator import MazeGenerator
from mazegen.models.maze_config import MazeConfig
from mazegen.models.maze import Maze
from mazegen.exceptions import MazeError, InvalidEntryExitError, MazeSizeError


class TestAlgorithmMapping:
    """Test algorithm mapping."""

    def test_algo_map_has_dfs(self):
        assert "dfs" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_prim(self):
        assert "prim" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_kruskal(self):
        assert "kruskal" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_wilson(self):
        assert "wilson" in MazeGenerator.ALGO_MAP


class TestMazeGeneratorCreation:
    """Test MazeGenerator.create method."""

    def test_create_with_dfs(self):
        """Test creating a maze with DFS algorithm."""
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)
        assert maze.width == 5
        assert maze.height == 5

    def test_create_with_prim(self):
        """Test creating a maze with Prim algorithm."""
        config = MazeConfig(width=5, height=5, algo="prim", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_with_kruskal(self):
        """Test creating a maze with Kruskal algorithm."""
        config = MazeConfig(width=5, height=5, algo="kruskal", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_with_wilson(self):
        """Test creating a maze with Wilson algorithm."""
        config = MazeConfig(width=5, height=5, algo="wilson", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_with_invalid_algo_raises(self):
        """Test that invalid algorithm raises error."""
        config = MazeConfig(width=5, height=5, algo="invalid", seed=42)
        with pytest.raises(MazeError):
            MazeGenerator.create(config)

    def test_create_respects_seed(self):
        """Test that same seed produces same maze."""
        config1 = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        config2 = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze1 = MazeGenerator.create(config1)
        maze2 = MazeGenerator.create(config2)
        
        for row1, row2 in zip(maze1.grid, maze2.grid):
            for cell1, cell2 in zip(row1, row2):
                assert cell1.walls == cell2.walls
