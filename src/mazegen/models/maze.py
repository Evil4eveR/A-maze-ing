from .cell import Cell


class Maze:
    """2-D grid of cells representing a maze."""

    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple = (0, 0),
        exit_point: tuple | None = None,
    ):
        """Initialise maze grid with given dimensions and entry/exit points."""
        self.width = width
        self.height = height
        self.grid = [
            [
                Cell(x=x, y=y) for x in range(self.width)
            ] for y in range(self.height)
        ]
        _entry = self.get_cell(*entry_point)
        if _entry is None:
            raise ValueError(f"Invalid entry point: {entry_point}")
        self.entry: Cell = _entry
        _exit_pt = (
            exit_point if exit_point is not None else (width - 1, height - 1)
        )
        _exit = self.get_cell(*_exit_pt)
        if _exit is None:
            raise ValueError(f"Invalid exit point: {_exit_pt}")
        self.exit: Cell = _exit
        self.seed: int | None = None
        self.algo: str | None = None

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Return cell at (x, y), or None if out of bounds."""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return self.grid[y][x]

    def open_entry_exit(self) -> None:
        """Remove the border wall at the entry and exit cells."""
        self._open_border_wall(self.entry)
        self._open_border_wall(self.exit)

    def _open_border_wall(self, cell: Cell) -> None:
        """Remove the outer border wall for a border cell, raising ValueError if not on edge.""" # noqa
        if cell.y == 0:
            cell.remove_wall(Cell.WEST)
        elif cell.y == self.height - 1:
            cell.remove_wall(Cell.EAST)
        elif cell.x == 0:
            cell.remove_wall(Cell.NORTH)
        elif cell.x == self.width - 1:
            cell.remove_wall(Cell.SOUTH)
        else:
            raise ValueError(
                f"Cell ({cell.x}, {cell.y}) is not on the border."
            )

    def get_unvisited(self) -> list[Cell]:
        """Return all unvisited, non-blocked cells."""
        return [
            cell
            for row in self.grid
            for cell in row
            if not cell.visited and not cell.blocked
        ]

    def add_blocked_cells(
        self, cells: list[tuple[int, int]], offset: tuple[int, int] = (0, 0)
    ) -> None:
        """Mark cells at given relative coordinates as blocked."""
        ox, oy = offset
        for cx, cy in cells:
            cell = self.get_cell(cx + ox, cy + oy)
            if cell:
                cell.blocked = True
