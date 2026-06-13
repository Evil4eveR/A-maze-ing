"""Tests for src/utils/file.py — File utilities."""

import sys
import os
import pytest
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.file import (
    create_simple_str,
    get_maze_str,
    get_path_str,
    get_walls_between,
    get_str_wall,
    save_maze_to_file
)
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.algo.dfs import DFSMazeGenerator


class TestGetStrWall:
    """Test get_str_wall function."""

    def test_north_wall_returns_n(self):
        """Test that north wall returns 'N'."""
        assert get_str_wall(Cell.NORTH) == "N"

    def test_south_wall_returns_s(self):
        """Test that south wall returns 'S'."""
        assert get_str_wall(Cell.SOUTH) == "S"

    def test_east_wall_returns_e(self):
        """Test that east wall returns 'E'."""
        assert get_str_wall(Cell.EAST) == "E"

    def test_west_wall_returns_w(self):
        """Test that west wall returns 'W'."""
        assert get_str_wall(Cell.WEST) == "W"

    def test_no_wall_returns_none(self):
        """Test that no wall returns 'None'."""
        assert get_str_wall(0) == "None"


class TestGetWallsBetween:
    """Test get_walls_between function."""

    def test_walls_between_x_cells_north_south(self):
        """Test walls between cells in same column (x-diff = 0)."""
        cell1 = Cell(0, 0)
        cell2 = Cell(0, 1)
        wall = get_walls_between(cell1, cell2)
        assert wall in [Cell.NORTH, Cell.SOUTH]

    def test_walls_between_y_cells_east_west(self):
        """Test walls between cells in same row (y-diff = 0)."""
        cell1 = Cell(0, 0)
        cell2 = Cell(1, 0)
        wall = get_walls_between(cell1, cell2)
        assert wall in [Cell.EAST, Cell.WEST]

    def test_non_adjacent_cells_raise_error(self):
        """Test that non-adjacent cells raise ValueError."""
        cell1 = Cell(0, 0)
        cell2 = Cell(2, 2)
        with pytest.raises(ValueError):
            get_walls_between(cell1, cell2)

    def test_same_cell_raises_error(self):
        """Test that same cell raises ValueError."""
        cell1 = Cell(0, 0)
        with pytest.raises(ValueError):
            get_walls_between(cell1, cell1)


class TestGetMazeStr:
    """Test get_maze_str function."""

    def test_get_maze_str_returns_string(self):
        """Test that get_maze_str returns a string."""
        maze = Maze(3, 3)
        maze_str = get_maze_str(maze)
        assert isinstance(maze_str, str)

    def test_get_maze_str_has_correct_lines(self):
        """Test that get_maze_str has one line per row."""
        maze = Maze(5, 5)
        maze_str = get_maze_str(maze)
        lines = maze_str.strip().split('\n')
        assert len(lines) == maze.height

    def test_get_maze_str_each_line_has_width_chars(self):
        """Test that each line has width characters."""
        maze = Maze(5, 3)
        maze_str = get_maze_str(maze)
        lines = maze_str.strip().split('\n')
        for line in lines:
            assert len(line) == maze.width

    def test_get_maze_str_uses_hex_format(self):
        """Test that maze uses hex format for walls."""
        maze = Maze(2, 2)
        maze_str = get_maze_str(maze)
        # Should contain hex characters
        assert any(c in maze_str for c in '0123456789ABCDEFabcdef')

    def test_get_maze_str_with_custom_walls(self):
        """Test get_maze_str with custom wall values."""
        maze = Maze(2, 2)
        maze.grid[0][0].walls = 0b1111  # All walls
        maze_str = get_maze_str(maze)
        assert 'F' in maze_str.upper()


class TestGetPathStr:
    """Test get_path_str function."""

    def test_get_path_str_returns_string(self):
        """Test that get_path_str returns a string."""
        path = [Cell(0, 0), Cell(1, 0)]
        path_str = get_path_str(path)
        assert isinstance(path_str, str)

    def test_get_path_str_single_cell(self):
        """Test path string with single cell."""
        path = [Cell(0, 0)]
        path_str = get_path_str(path)
        assert path_str == ""

    def test_get_path_str_two_adjacent_cells(self):
        """Test path string with two adjacent cells."""
        path = [Cell(0, 0), Cell(1, 0)]
        path_str = get_path_str(path)
        assert len(path_str) == 1
        assert path_str in ['N', 'S', 'E', 'W']

    def test_get_path_str_multiple_cells(self):
        """Test path string with multiple adjacent cells."""
        # Path going right then down
        path = [Cell(0, 0), Cell(1, 0), Cell(1, 1)]
        path_str = get_path_str(path)
        assert len(path_str) == 2


class TestCreateSimpleStr:
    """Test create_simple_str function."""

    def test_create_simple_str_format(self):
        """Test create_simple_str basic functionality with adjacent path."""
        maze = Maze(2, 2)
        # Create a simple adjacent path
        path = [maze.grid[0][0], maze.grid[1][0]]
        simple_str = create_simple_str(maze, path)
        assert isinstance(simple_str, str)
        assert len(simple_str) > 0

    def test_create_simple_str_has_newlines(self):
        """Test that simple_str has multiple lines."""
        maze = Maze(2, 2)
        path = [maze.grid[0][0]]
        simple_str = create_simple_str(maze, path)
        lines = simple_str.strip().split('\n')
        assert len(lines) > 1


class TestSaveMazeToFile:
    """Test save_maze_to_file function."""

    def test_save_maze_creates_file(self):
        """Test that save_maze_to_file creates a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_maze.txt"
            maze = Maze(2, 2)
            path = [maze.grid[0][0]]
            
            save_maze_to_file(maze, path, str(output_file))
            assert output_file.exists()

    def test_save_maze_writes_content(self):
        """Test that save_maze_to_file writes valid content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_maze.txt"
            maze = Maze(2, 2)
            path = [maze.grid[0][0]]
            
            save_maze_to_file(maze, path, str(output_file))
            content = output_file.read_text()
            assert len(content) > 0

    def test_save_maze_file_has_multiple_lines(self):
        """Test that saved maze file has multiple lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_maze.txt"
            maze = Maze(3, 3)
            path = [maze.grid[0][0]]
            
            save_maze_to_file(maze, path, str(output_file))
            content = output_file.read_text()
            lines = content.strip().split('\n')
            # Should have maze rows + entry + exit + path
            assert len(lines) >= 3

    def test_save_maze_overwrites_existing_file(self):
        """Test that save_maze_to_file overwrites existing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_maze.txt"
            output_file.write_text("old content")
            
            maze = Maze(2, 2)
            path = [maze.grid[0][0]]
            save_maze_to_file(maze, path, str(output_file))
            
            content = output_file.read_text()
            assert content != "old content"
            assert len(content) > 0
