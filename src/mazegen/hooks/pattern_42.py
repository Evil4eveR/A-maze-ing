from typing import ClassVar
from ..exceptions import MazeSizeError

from ..interfaces import MazeHook
from ..models.maze import Maze


class Add42Pattern(MazeHook):
    """Pre-generation hook that stamps a '42' pattern of blocked cells."""

    stage = "pre"

    MIN_WIDTH = 8
    MIN_HEIGHT = 7
    pattern_42: ClassVar[list[tuple[int, int]]] = [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4),  # noqa: E501
    ]

    def __call__(self, maze: Maze) -> Maze:
        """Stamp the 42 pattern onto the maze, raising MazeSizeError if too small.""" # noqa
        if maze.width < self.MIN_WIDTH or maze.height < self.MIN_HEIGHT:
            raise MazeSizeError(
                f"Maze must be at least {self.MIN_WIDTH}x{self.MIN_HEIGHT} "
                "to fit the 42 pattern."
            )
        ox = maze.width // 2 - 4
        oy = maze.height // 2 - 2
        maze.add_blocked_cells(self.pattern_42, offset=(ox, oy))
        return maze
