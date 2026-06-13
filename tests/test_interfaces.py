"""Tests for src/interfaces.py — Abstract base classes and protocols."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.interfaces import MazeAlgorithm, BaseMazeSolver, MazeRenderer, MazeHook
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell


class TestMazeAlgorithmInterface:
    """Test MazeAlgorithm interface."""

    def test_has_name_attribute(self):
        """Test that algorithms have a name attribute."""
        from mazegen.algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, 'name')
        assert algo.name == "dfs"

    def test_has_directions(self):
        """Test that algorithms have directions."""
        from mazegen.algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, '_DIRECTIONS')
        assert len(algo._DIRECTIONS) == 4


class TestBaseMazeSolverInterface:
    """Test BaseMazeSolver interface."""

    def test_solver_has_solve_method(self):
        """Test that solvers have a solve method."""
        from mazegen.solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, 'solve')
        assert callable(solver.solve)
    
    def test_solver_has_solve_step_method(self):
        """Test that solvers have a solve_step method."""
        from mazegen.solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, 'solve_step')
        assert callable(solver.solve_step)


class TestMazeRendererInterface:
    """Test MazeRenderer interface."""

    def test_renderer_has_name(self):
        """Test that renderers have a name attribute."""
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert hasattr(renderer, 'name')
        assert renderer.name == "ascii"

    def test_renderer_has_render_method(self):
        """Test that renderers have a render method."""
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert hasattr(renderer, 'render')
        assert callable(renderer.render)


class TestMazeHookInterface:
    """Test MazeHook interface."""

    def test_hook_has_stage(self):
        """Test that hooks have a stage attribute."""
        from mazegen.hooks.break_perfect import BreakPerfect
        hook = BreakPerfect()
        assert hasattr(hook, 'stage')

    def test_hook_is_callable(self):
        """Test that hooks are callable."""
        from mazegen.hooks.break_perfect import BreakPerfect
        hook = BreakPerfect()
        assert callable(hook)
