from typing import Generator
from random import Random

from ..interfaces import MazeAlgorithm
from ..models.maze import Maze


class DFSMazeGenerator(MazeAlgorithm):
    """Maze generator using depth-first search (recursive backtracker)."""
    name = 'dfs'

    def generate(self, seed: int) -> None:
        """Generate a maze using DFS."""
        for _ in self._generate_dfs(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int
    ) -> Generator[Maze, None, None]:
        """Yield maze states step-by-step using DFS.""" # noqa
        yield from self._generate_dfs(seed)
        self._reset_visited()

    def _generate_dfs(
        self,
        seed: int
    ) -> Generator[Maze, None, None]:
        """Core DFS generation logic; yields maze after each step."""
        rng = Random(seed)
        first_cell = self.maze.get_cell(0, 0)
        assert first_cell is not None
        stack = [first_cell]
        first_cell.visited = True

        while stack:
            current_cell = stack[-1]

            neighbors = self._get_neighbors(current_cell, visited=False)
            if neighbors:
                next_cell = rng.choice(neighbors)
                current_cell.remove_walls_between(next_cell)
                stack.append(next_cell)
                next_cell.visited = True
            else:
                stack.pop()
            yield self.maze
