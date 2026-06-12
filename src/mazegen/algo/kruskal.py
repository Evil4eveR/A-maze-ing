from random import Random
from typing import Generator

from ..interfaces import MazeAlgorithm
from ..models.cell import Cell

from ..models.maze import Maze


class KruskalMazeGenerator(MazeAlgorithm):
    """Maze generator using Kruskal's algorithm."""

    name = 'kruskal'

    def generate(self, seed: int | None = None) -> None:
        """Generate a maze using Kruskal's algorithm."""
        for _ in self._generate_kruskal(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Yield maze states step-by-step using Kruskal's algorithm."""
        yield from self._generate_kruskal(seed)
        self._reset_visited()

    def _generate_kruskal(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Core Kruskal's generation logic; yields maze after each step."""
        rng = Random(seed)

        parent: dict[Cell, Cell] = {}
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if cell is None or cell.blocked:
                    continue
                parent[cell] = cell

        def find(cell: Cell) -> Cell:
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]

        def union(a: Cell, b: Cell) -> None:
            parent[find(a)] = find(b)

        def connected(a: Cell, b: Cell) -> bool:
            return find(a) == find(b)

        walls: list[tuple[Cell, Cell]] = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if cell is None or cell.blocked:
                    continue
                for dx, dy in self._DIRECTIONS:
                    neighbor = self.maze.get_cell(x + dx, y + dy)
                    if neighbor and not neighbor.blocked:
                        walls.append((cell, neighbor))

        rng.shuffle(walls)

        for cell, neighbor in walls:
            if not connected(cell, neighbor):
                cell.remove_walls_between(neighbor)
                union(cell, neighbor)
                cell.visited = True
                neighbor.visited = True
            yield self.maze
