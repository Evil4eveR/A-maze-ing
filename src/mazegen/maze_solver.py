from typing import Generator, Type
from .models.cell import Cell

from .models.maze import Maze
from .interfaces import BaseMazeSolver as MazeSolverBase

from .exceptions import MazeError
from .solver.bfs import BFSMazeSolver


class MazeSolver:
    """Facade for solving a Maze using pluggable solver algorithms."""

    SOLVER_MAP: dict[str, Type[MazeSolverBase]] = {
        'bfs': BFSMazeSolver,
    }

    @classmethod
    def solve(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs'
    ) -> list[Cell] | None:
        """Return the shortest path through the maze, or None if unsolvable."""
        solver_class: type[MazeSolverBase] | None = None
        if isinstance(algo, str):
            solver_class = cls.SOLVER_MAP.get(algo)
        else:
            solver_class = algo
        if solver_class is None:
            raise MazeError(f"Unsupported solver: {algo}")
        return solver_class(maze).solve()

    @classmethod
    def solve_animated(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs'
    ) -> Generator[tuple[list[Cell] | None, bool], None, None]:
        """Yield (partial_path, is_final) tuples as the solver progresses."""
        yield from cls._build(maze, algo)

    @classmethod
    def _build(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs',
    ) -> Generator[tuple[list[Cell] | None, bool], None, None]:
        """Internal generator that runs the solver and yields progress states.""" # noqa
        solver_class: type[MazeSolverBase] | None = None
        if isinstance(algo, str):
            solver_class = cls.SOLVER_MAP.get(algo)
        else:
            solver_class = algo
        if solver_class is None:
            raise MazeError(f"Unsupported solver: {algo}")
        solver = solver_class(maze)
        yield from solver.solve_step()
