from mazegen.interfaces import MazeRenderer
from mazegen.models.cell import Cell

from config import settings
from models.theme import Theme

from mazegen.models.maze import Maze
from rich import print as rich_print


class AsciiMazeRenderer(MazeRenderer[str]):
    """Renders a maze as a Rich-coloured ASCII string."""

    name = 'ascii'

    def __init__(
        self,
        maze: Maze,
        themes: Theme | None = None,
        path: list[Cell] | None = None,
    ):
        """Initialise renderer with maze, optional theme and path.""" # noqa
        super().__init__(maze)
        self.path = path
        self.renderer = [
            [1] * (maze.width * 2 + 1) for _ in range(maze.height * 2 + 1)
        ]
        self.output_str = ""
        self.themes = themes or Theme()
        self.connect = True

    def render(self) -> str:
        """Render the maze and return it as a coloured ASCII string."""
        self._render_all()
        self.output_str = self._render_ascii()
        return self.output_str

    def display(self) -> None:
        """Print the rendered maze to the terminal."""
        rich_print(self.render())

    def _render_all(self) -> None:
        """Populate the internal renderer grid with cell, wall, and path values.""" # noqa
        for y in range(1, self.maze.height * 2, 2):
            for x in range(1, self.maze.width * 2, 2):
                cell = self.maze.get_cell(x // 2, y // 2)
                if cell is None:
                    continue
                if cell.blocked:
                    self._render_blocked_cells(x, y)
                    continue
                self.renderer[y][x] = 0
                self._render_cell_walls(cell, x, y)

        if self.path and self.connect:
            self._render_path()
        elif self.path:
            self._render_explored()

        self._render_entry_exit()

    def _render_entry_exit(self) -> None:
        """Mark entry and exit cells in the renderer grid."""
        en_x, en_y = self.maze.entry.x * 2 + 1, self.maze.entry.y * 2 + 1
        ex_x, ex_y = self.maze.exit.x * 2 + 1, self.maze.exit.y * 2 + 1
        self.renderer[en_y][en_x] = 4
        self.renderer[ex_y][ex_x] = 5

    def _get_exit_wall(self, cell: Cell) -> int:
        """Return the wall direction that faces outward for a border cell."""
        if cell.y == 0:
            return Cell.WEST
        elif cell.y == self.maze.height - 1:
            return Cell.EAST
        elif cell.x == 0:
            return Cell.NORTH
        elif cell.x == self.maze.width - 1:
            return Cell.SOUTH
        raise ValueError(f"Cell ({cell.x}, {cell.y}) is not on the border.")

    def _get_wall_coords(self, cell: Cell, wall: int) -> tuple[int, int]:
        """Return renderer grid (col, row) for the wall segment of a cell."""
        x, y = cell.x * 2 + 1, cell.y * 2 + 1
        if wall == Cell.NORTH:
            return (x - 1, y)
        elif wall == Cell.SOUTH:
            return (x + 1, y)
        elif wall == Cell.WEST:
            return (x, y - 1)
        elif wall == Cell.EAST:
            return (x, y + 1)
        raise ValueError(f"Unknown wall: {wall}")

    def _render_ascii(self) -> str:
        """Convert the renderer grid to a Rich-formatted string."""
        s = ""
        for row in self.renderer:
            for cell in row:
                if cell == 0:
                    s += self._get_colored_str(settings.cell, self.themes.cell)
                elif cell == 1:
                    s += self._get_colored_str(settings.wall, self.themes.wall)
                elif cell == 2:
                    s += self._get_colored_str(settings.wall, self.themes.blocked_cell) # noqa
                elif cell == 3:
                    s += self._get_colored_str(settings.path, self.themes.path)
                elif cell == 4:
                    s += self._get_colored_str(settings.path, self.themes.entry) # noqa
                elif cell == 5:
                    s += self._get_colored_str(settings.path, self.themes.exit)
            s += "\n"
        return s

    def _get_colored_str(
        self,
        chrs: str,
        color: str
    ) -> str:
        """Wrap `chrs` in Rich color markup."""
        return f"[{color}]{chrs}[/{color}]"

    def _render_blocked_cells(
        self,
        x: int,
        y: int,
    ) -> None:
        """Mark a blocked cell and its right/below neighbours in the grid."""
        self.renderer[y][x] = 2
        if x + 2 < self.maze.width * 2 + 1:
            right = self.maze.get_cell((x + 2) // 2, y // 2)
            if right and right.blocked:
                self.renderer[y][x + 1] = 2

        if y + 2 < self.maze.height * 2 + 1:
            below = self.maze.get_cell(x // 2, (y + 2) // 2)
            if below and below.blocked:
                self.renderer[y + 1][x] = 2

    def _render_cell_walls(
        self,
        cell: Cell,
        x: int,
        y: int,
    ) -> None:
        """Clear renderer grid slots for each open wall of a cell."""
        for wall in [cell.WEST, cell.SOUTH, cell.EAST, cell.NORTH]:
            if not cell.has_wall(wall):
                if wall == cell.WEST:
                    self.renderer[y - 1][x] = 0
                elif wall == cell.SOUTH:
                    self.renderer[y][x + 1] = 0
                elif wall == cell.EAST:
                    self.renderer[y + 1][x] = 0
                elif wall == cell.NORTH:
                    self.renderer[y][x - 1] = 0

    def _render_path(self) -> None:
        """Mark solution path cells in the renderer grid."""
        if self.path is None:
            return
        for i, cell in enumerate(self.path):
            x, y = cell.x * 2 + 1, cell.y * 2 + 1
            self.renderer[y][x] = 3

            if i + 1 < len(self.path):
                next_cell = self.path[i + 1]
                nx, ny = next_cell.x * 2 + 1, next_cell.y * 2 + 1
                self.renderer[(y + ny) // 2][(x + nx) // 2] = 3

    def _render_explored(self) -> None:
        """Mark explored (non-final path) cells in the renderer grid."""
        if self.path is None:
            return
        for cell in self.path:
            x, y = cell.x * 2 + 1, cell.y * 2 + 1
            self.renderer[y][x] = 3
