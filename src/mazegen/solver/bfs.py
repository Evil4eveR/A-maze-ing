from typing import Generator

from ..interfaces import BaseMazeSolver
from ..models.cell import Cell

from collections import deque


class BFSMazeSolver(BaseMazeSolver):
    """Maze solver using breadth-first search."""

    def solve(self) -> list[Cell] | None:
        """Return the shortest path from entry to exit, or None if unsolvable.""" # noqa
        path: list[Cell] | None = None
        for path, _ in self._bfs():
            pass
        return path

    def solve_step(self) -> Generator[tuple[list[Cell] | None, bool], None, None]: # noqa
        """Yield (partial_path, is_final) tuples as BFS explores the maze."""
        yield from self._bfs()

    def _bfs(self) -> Generator[tuple[list[Cell] | None, bool], None, None]:
        """Core BFS loop; yields explored cells and final path."""
        start = self.maze.entry
        end = self.maze.exit

        queue = deque([start])
        came_from: dict[Cell, Cell | None] = {start: None}

        while queue:
            cell = queue.popleft()

            if cell == end:
                path = self._reconstruct(came_from, end)
                for i in range(1, len(path) + 1):
                    yield path[:i], True
                return

            for neighbor in self._get_passable_neighbors(cell):
                if neighbor in came_from:
                    continue
                came_from[neighbor] = cell
                queue.append(neighbor)
                yield list(came_from.keys()), False

        yield [], False

    def _reconstruct(
        self,
        came_from: dict[Cell, Cell | None],
        end: Cell
    ) -> list[Cell]:
        """Reconstruct the path from entry to `end` using the came_from map."""
        path = []

        cell: Cell | None = end
        while cell:
            path.append(cell)
            cell = came_from[cell]
        return path[::-1]

    def _get_passable_neighbors(self, cell: Cell) -> list[Cell]:
        """Return neighbouring cells reachable through open walls."""
        passable = []

        for (dx, dy), wall in [
            ((0, -1), Cell.WEST),
            ((1, 0), Cell.SOUTH),
            ((0, 1), Cell.EAST),
            ((-1, 0), Cell.NORTH)
        ]:
            neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not cell.has_wall(wall):
                passable.append(neighbor)
        return passable
