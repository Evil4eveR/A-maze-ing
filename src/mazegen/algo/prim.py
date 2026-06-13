from typing import Generator
from random import Random

from ..interfaces import MazeAlgorithm
from ..models.maze import Maze


class PrimMazeGenerator(MazeAlgorithm):
    """Maze generator using Prim's algorithm."""

    name = 'prim'

    def generate(self, seed: int | None = None) -> None:
        """Generate a maze using Prim's algorithm."""
        for _ in self._generate_prim(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Yield maze states step-by-step using Prim's algorithm."""
        yield from self._generate_prim(seed)
        self._reset_visited()

    def _generate_prim(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Core Prim's generation logic; yields maze after each step."""
        rng = Random(seed)

        start = self.maze.get_cell(0, 0)
        assert start is not None
        start.visited = True

        frontier = self._get_neighbors(start, visited=False)

        while frontier:
            cell = rng.choice(frontier)
            frontier.remove(cell)

            neighbors = self._get_neighbors(cell, visited=True)
            if neighbors:
                neighbor = rng.choice(neighbors)
                cell.remove_walls_between(neighbor)
                cell.visited = True
                frontier.extend(
                    c for c in self._get_neighbors(cell, visited=False)
                    if c not in frontier
                )
            yield self.maze
