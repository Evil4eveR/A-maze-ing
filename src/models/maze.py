from models.cell import Cell
from exceptions import InvalidEntryExitError


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple = (0, 0),
        exit_point: tuple | None = None,
    ):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x=x, y=y) for x in range(self.width)] for y in range(self.height)
        ]
        self.entry = self.get_cell(*entry_point)
        self.exit = (
            self.get_cell(*exit_point)
            if exit_point is not None
            else self.get_cell(width - 1, height - 1)
        )
        self.seed: int | None = None
        self.algorithm: str | None = None

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            raise InvalidEntryExitError(f"Cell ({x}, {y}) is out of bounds.")
        return self.grid[y][x]

    def open_entry_exit(self) -> None:
        self._open_border_wall(self.entry)
        self._open_border_wall(self.exit)

    def _open_border_wall(self, cell: Cell) -> None:
        if cell.y == 0:
            cell.remove_wall(Cell.WEST)
        elif cell.y == self.height - 1:
            cell.remove_wall(Cell.EAST)
        elif cell.x == 0:
            cell.remove_wall(Cell.NORTH)
        elif cell.x == self.width - 1:
            cell.remove_wall(Cell.SOUTH)
        else:
            raise ValueError(f"Cell ({cell.x}, {cell.y}) is not on the border.")

    def get_unvisited(self) -> list[Cell]:
        return [
            cell
            for row in self.grid
            for cell in row
            if not cell.visited and not cell.blocked
        ]

    def add_blocked_cells(
        self, cells: list[tuple[int, int]], offset: tuple[int, int] = (0, 0)
    ) -> None:
        ox, oy = offset
        for cx, cy in cells:
            cell = self.get_cell(cx + ox, cy + oy)
            if cell:
                cell.blocked = True
