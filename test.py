from typing import ClassVar

from src.exceptions import MazeWallError


class Cell:
    NORTH: ClassVar[int] = 0b0001
    EAST:  ClassVar[int] = 0b0010
    SOUTH: ClassVar[int] = 0b0100
    WEST:  ClassVar[int] = 0b1000

    def __init__(
        self,
        x: int,
        y: int,
        visited: bool = False,
        walls: int = 0b1111,
        blocked: bool = False
    ):
        self.x = x
        self.y = y
        self.visited = visited
        self.walls = walls
        self.blocked = blocked

    def remove_wall(
        self,
        direction: int
    ) -> None:
        if not self.has_wall(direction):
            return
        self.walls &= ~direction

    def has_wall(self, direction: int) -> bool:
        """Check if the cell has a wall in the specified direction."""
        self._validate_direction(value=direction)
        return (self.walls & direction) != 0

    def remove_walls_between(
        self,
        other: 'Cell',
        force: bool = False
    ) -> None:
        """Remove walls between this cell and another cell."""
        if not force and (self.blocked or other.blocked):
            return

        (dx, dy) = self._validate_cell_between(other)
        # dx = other.x - self.x
        # dy = other.y - self.y

        if dx == 1:
            self.remove_wall(Cell.SOUTH)
            other.remove_wall(Cell.NORTH)
        elif dx == -1:
            self.remove_wall(Cell.NORTH)
            other.remove_wall(Cell.SOUTH)
        elif dy == 1:
            self.remove_wall(Cell.EAST)
            other.remove_wall(Cell.WEST)
        elif dy == -1:
            self.remove_wall(Cell.WEST)
            other.remove_wall(Cell.EAST)

    def _validate_direction(
        self,
        value: int
    ) -> None:
        if value is not None and not value in range(16):
            raise MazeWallError(
                "Walls must be a 4-bit integer (0-15)."
            )

    def _validate_cell_between(self, other: 'Cell') -> tuple[int, int]:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            return (other.x - self.x, other.y - self.y)
        raise MazeWallError(
            "Cells must be adjacent to remove walls between them."
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            raise TypeError("Can only compare Cell with another Cell.")
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

