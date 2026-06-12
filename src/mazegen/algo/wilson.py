from random import Random
from typing import Generator

from ..interfaces import MazeAlgorithm
from ..models.cell import Cell

from ..models.maze import Maze


class WilsonMazeGenerator(MazeAlgorithm):
    """Maze generator using Wilson's algorithm (loop-erased random walks)."""

    name = 'wilson'

    def generate(self, seed: int | None = None) -> None:
        """Generate a maze using Wilson's algorithm."""
        for _ in self._generate_wilson(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Yield maze states step-by-step using Wilson's algorithm."""
        yield from self._generate_wilson(seed)
        self._reset_visited()

    def _generate_wilson(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Core Wilson's generation logic; yields maze after each step."""
        rng = Random(seed)

        all_cells = self.maze.get_unvisited()
        rng.choice(all_cells).visited = True

        for start in all_cells:
            if start.visited:
                continue

            next_step: dict[Cell, Cell] = {}
            cell = start

            while not cell.visited:
                neighbor = rng.choice(self._get_neighbors(cell))
                next_step[cell] = neighbor
                cell = neighbor

            cell = start
            while not cell.visited:
                nxt = next_step[cell]
                cell.remove_walls_between(nxt)
                cell.visited = True
                cell = nxt
            yield self.maze
