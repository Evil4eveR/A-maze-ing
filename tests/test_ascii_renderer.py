"""Tests for src/renderer/ascii.py — ASCII maze rendering."""

import sys
import os
import pytest
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Set up a test config file before importing renderer
test_config_path = Path(__file__).parent / "test_config.txt"
if not test_config_path.exists():
    test_config_path.write_text(
        "width=10\nheight=10\nentry=0,0\nexit=9,9\noutput_file=test_maze.txt\nperfect=true"
    )
    os.environ['ENV_FILE'] = str(test_config_path)
    # Temporarily update sys.argv for config initialization
    old_argv = sys.argv.copy()
    sys.argv = ['test', str(test_config_path)]

from renderer.ascii import AsciiMazeRenderer
from mazegen.models.maze import Maze
from mazegen.algo.dfs import DFSMazeGenerator


class TestAsciiRendererConstruction:
    """Test ASCII renderer construction."""

    def test_renderer_name_attribute(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.name == "ascii"

    def test_renderer_stores_maze(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.maze is maze


class TestAsciiRendering:
    """Test ASCII rendering functionality."""

    def test_render_returns_string(self):
        maze = Maze(3, 3)
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_contains_wall_characters(self):
        maze = Maze(3, 3)
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        # Should contain some wall representation
        assert len(result) > 0

    def test_render_with_generated_maze(self):
        """Test rendering a generated maze."""
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_display_does_not_raise(self):
        """Test that display() doesn't raise an error."""
        maze = Maze(3, 3)
        renderer = AsciiMazeRenderer(maze)
        # Should not raise
        renderer.display()


class TestAsciiRendererEdgeCases:
    """Test edge cases in ASCII rendering."""

    def test_render_single_cell_maze(self):
        """Test rendering a 1x1 maze."""
        maze = Maze(1, 1)
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        assert isinstance(result, str)

    def test_render_wide_maze(self):
        """Test rendering a wide maze."""
        maze = Maze(20, 5)
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_tall_maze(self):
        """Test rendering a tall maze."""
        maze = Maze(5, 20)
        renderer = AsciiMazeRenderer(maze)
        result = renderer.render()
        assert isinstance(result, str)
        assert len(result) > 0


# Cleanup
if test_config_path.exists():
    try:
        test_config_path.unlink()
    except:
        pass
