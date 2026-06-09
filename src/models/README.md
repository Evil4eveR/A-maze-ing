# Data Models — `src/models/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

This package contains the core data structures used to represent a maze.

## Overview

| File | Class | Description |
|---|---|---|
| [`cell.py`](#cell) | `Cell` | Represents a single cell in the maze grid |
| [`maze.py`](#maze) | `Maze` | Represents the complete maze (grid of cells) |

---

## Cell

**File:** [`cell.py`](cell.py)

A cell is a single unit in the maze grid. Each cell has coordinates `(x, y)`, a 4-bit wall bitmask, and status flags.

### Wall Encoding

Walls are encoded as a 4-bit integer where each bit represents a cardinal direction:

| Constant | Value (binary) | Value (decimal) | Direction |
|---|---|---|---|
| `Cell.NORTH` | `0b0001` | 1 | North |
| `Cell.EAST` | `0b0010` | 2 | East |
| `Cell.SOUTH` | `0b0100` | 4 | South |
| `Cell.WEST` | `0b1000` | 8 | West |

A new cell starts with all walls closed: `walls = 0b1111` (15).

### Constructor

```python
Cell(x: int, y: int, visited: bool = False, walls: int = 0b1111, blocked: bool = False)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `x` | `int` | — | Horizontal coordinate |
| `y` | `int` | — | Vertical coordinate |
| `visited` | `bool` | `False` | Whether the cell has been visited during generation |
| `walls` | `int` | `0b1111` | 4-bit wall bitmask (all walls closed by default) |
| `blocked` | `bool` | `False` | Whether the cell is blocked (e.g., part of the "42" pattern) |

### Methods

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `has_wall(direction)` | `direction: int` | `bool` | Check if the cell has a wall in the given direction |
| `remove_wall(direction)` | `direction: int` | `None` | Remove a wall in the given direction |
| `remove_walls_between(other, force)` | `other: Cell`, `force: bool = False` | `None` | Remove the shared wall between two adjacent cells |

### Examples

```python
from models.cell import Cell

cell = Cell(x=3, y=5)

# Check if north wall exists
cell.has_wall(Cell.NORTH)  # True (all walls start closed)

# Remove the east wall
cell.remove_wall(Cell.EAST)
cell.has_wall(Cell.EAST)   # False

# Remove walls between two adjacent cells
cell_a = Cell(x=3, y=5)
cell_b = Cell(x=4, y=5)
cell_a.remove_walls_between(cell_b)
```

### Equality & Hashing

Two cells are considered equal if they share the same `(x, y)` coordinates. Cells are hashable and can be used in sets and as dictionary keys.

### Exceptions

- Raises [`MazeWallError`](../README.md#exceptionspy) if the wall bitmask is outside `0–15`.
- Raises [`MazeWallError`](../README.md#exceptionspy) if `remove_walls_between` is called on non-adjacent cells.

---

## Maze

**File:** [`maze.py`](maze.py)

The `Maze` class represents the entire maze as a 2D grid of [`Cell`](#cell) objects.

### Constructor

```python
Maze(width: int, height: int, entry_point: tuple = (0, 0), exit_point: tuple | None = None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Number of cells horizontally |
| `height` | `int` | — | Number of cells vertically |
| `entry_point` | `tuple[int, int]` | `(0, 0)` | Entry cell coordinates |
| `exit_point` | `tuple[int, int] \| None` | `(width-1, height-1)` | Exit cell coordinates |

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `grid` | `list[list[Cell]]` | 2D array of cells (`grid[y][x]`) |
| `entry` | `Cell \| None` | Entry cell object |
| `exit` | `Cell \| None` | Exit cell object |
| `seed` | `int \| None` | Seed used for generation (set after creation) |
| `algorithm` | `str \| None` | Algorithm name used (set after creation) |

### Methods

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `get_cell(x, y)` | `x: int`, `y: int` | `Cell \| None` | Get cell at coordinates; returns `None` if out of bounds |
| `open_entry_exit()` | — | `None` | Open border walls at entry and exit cells |
| `get_unvisited()` | — | `list[Cell]` | Get all unvisited, non-blocked cells |
| `add_blocked_cells(cells, offset)` | `cells: list[tuple]`, `offset: tuple` | `None` | Mark cells as blocked with optional offset |

### Examples

```python
from models.maze import Maze

maze = Maze(width=10, height=10, entry_point=(0, 0), exit_point=(9, 9))

# Access a cell
cell = maze.get_cell(5, 5)  # Cell at (5, 5)

# Out-of-bounds returns None
maze.get_cell(-1, 0)  # None
maze.get_cell(10, 0)  # None

# Get all unvisited cells
unvisited = maze.get_unvisited()
```

---

## Related Modules

- **Algorithms** that operate on these models → [algo/](../algo)
- **Solver** that finds paths through the maze → [solver/](../solver)
- **Renderer** that visualises the maze → [renderer/](../renderer)
- **Hooks** that transform the maze → [hooks/](../hooks)
