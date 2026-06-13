from abc import ABC, abstractmethod
from typing import ClassVar, Literal, Protocol, Generic, TypeVar, Generator # noqa

from .models.cell import Cell
from .models.maze import Maze


T = TypeVar('T')


class MazeAlgorithm(ABC):
    """Abstract base class for maze generation algorithms."""

    name: str

    _DIRECTIONS: ClassVar[list[tuple[int, int]]] = [
        (0, -1),  # NORTH
        (1, 0),   # EAST
        (0, 1),   # SOUTH
        (-1, 0)   # WEST
    ]

    def __init__(
        self,
        maze: Maze
    ):
        """Initialise with the maze to generate."""
        self.maze = maze

    @abstractmethod
    def generate(
        self,
        seed: int
    ) -> None:
        """Generate a maze with the specified parameters."""
        raise NotImplementedError()

    def generate_step(
        self,
        seed: int
    ) -> Generator[Maze, None, None]:
        """Yield maze states step-by-step (for animation)."""
        self.generate(seed)
        yield self.maze

    def _get_neighbors(
        self,
        cell: Cell,
        visited: bool | None = None
    ) -> list[Cell]:
        """Return neighbouring cells, optionally filtered by visited state."""
        neighbors = []
        for dx, dy in self._DIRECTIONS:
            neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not neighbor.blocked:
                if visited is None or neighbor.visited == visited:
                    neighbors.append(neighbor)
        return neighbors

    def _reset_visited(self) -> None:
        """Mark all cells in the maze as unvisited."""
        for row in self.maze.grid:
            for cell in row:
                cell.visited = False


class BaseMazeSolver(ABC):
    """Abstract base class for maze solving algorithms."""

    name: str

    _DIRECTIONS: ClassVar[list[tuple[int, int]]] = [
        (0, -1),  # NORTH
        (1, 0),   # EAST
        (0, 1),   # SOUTH
        (-1, 0)   # WEST
    ]

    def __init__(
        self,
        maze: Maze
    ):
        """Initialise with the maze to solve."""
        self.maze = maze

    @abstractmethod
    def solve(self) -> list[Cell] | None:
        """Solve the maze and return the path from entry to exit."""
        raise NotImplementedError()

    def solve_step(
        self
    ) -> Generator[tuple[list[Cell] | None, bool], None, None]:
        """Solve the maze step-by-step and yield the current path."""
        path = self.solve()
        yield path, True


class MazeRenderer(ABC, Generic[T]):
    """Abstract base class for maze renderers."""

    name: str

    def __init__(
        self,
        maze: Maze
    ):
        """Initialise with the maze to render."""
        self.maze = maze

    @abstractmethod
    def render(self) -> T:
        """Render the maze and return the result."""
        raise NotImplementedError()

    def display(self) -> None:
        """Display the rendered maze."""
        print(self.render())


class MazeHook(Protocol):
    stage: Literal["pre", "post"]

    def __call__(self, maze: Maze) -> Maze: ...
