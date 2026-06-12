from mazegen.models.maze import Maze
from mazegen.models.cell import Cell


def create_simple_str(maze: Maze, path: list[Cell]) -> str:
    """Return the full maze output string (grid + entry/exit + path)."""
    maze_str = get_maze_str(maze)
    entry_str = f"{maze.entry.x},{maze.entry.y}"
    exit_str = f"{maze.exit.x},{maze.exit.y}"
    path_str = get_path_str(path)
    simple_str = (
        maze_str + "\n" + entry_str + "\n" + exit_str + "\n" + path_str
    )
    return simple_str


def get_walls_between(cell1: Cell, cell2: Cell) -> int:
    """Return the wall bitmask that separates two adjacent cells."""
    if cell1.x == cell2.x:
        if cell1.y == cell2.y + 1:
            return Cell.NORTH
        elif cell1.y == cell2.y - 1:
            return Cell.SOUTH
    elif cell1.y == cell2.y:
        if cell1.x == cell2.x + 1:
            return Cell.WEST
        elif cell1.x == cell2.x - 1:
            return Cell.EAST
    raise ValueError("Cells are not adjacent.")


def get_str_wall(wall: int) -> str:
    """Return the cardinal letter (N/S/E/W) for a wall bitmask."""
    if wall & Cell.NORTH:
        return "N"
    if wall & Cell.SOUTH:
        return "S"
    if wall & Cell.EAST:
        return "E"
    if wall & Cell.WEST:
        return "W"
    return "None"


def get_path_str(path: list[Cell]) -> str:
    """Convert a cell path to a string of directional letters (e.g. 'SSEN')."""
    path_str = ""
    for i in range(len(path) - 1):
        path_str += get_str_wall(get_walls_between(path[i], path[i + 1]))
    return path_str


def get_maze_str(maze: Maze) -> str:
    """Encode maze walls row-by-row as hex digits (one char per cell)."""
    maze_str = ""
    for row in maze.grid:
        line = ""
        for cell in row:
            line += "{:X}".format(cell.walls)
        maze_str += line + "\n"
    return maze_str


def save_maze_to_file(maze: Maze, path: list[Cell], filename: str) -> None:
    """Write the maze output string to a file."""
    with open(filename, "w") as f:
        maze_str = create_simple_str(maze, path)
        f.write(maze_str)
