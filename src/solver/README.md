# Maze Solver — `src/solver/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

This package contains the maze solving algorithm(s).

## Overview

| File | Class | Algorithm | Guarantee |
|---|---|---|---|
| [`bfs.py`](#bfsmmazesolver) | `BFSMazeSolver` | Breadth-First Search | Shortest path |

---

## BFSMazeSolver

**File:** [`bfs.py`](bfs.py) · **Class:** `BFSMazeSolver` · **Name:** `"BFS"`

Implements the [`MazeSolver`](../README.md#mazesolver-abc) abstract base class.

### How It Works

1. Start from `maze.entry`, initialise a queue and a `came_from` dictionary.
2. For each cell dequeued, check all four cardinal neighbours.
3. A neighbour is **passable** if there is no wall between the current cell and the neighbour (checked via `Cell.has_wall()`).
4. If the exit is reached, reconstruct the path by following the `came_from` chain backwards.

### Why BFS?

BFS explores cells level by level, guaranteeing the **shortest path** (fewest cells) from entry to exit. This is important for the output file format which requires the shortest valid path.

### API

```python
class BFSMazeSolver(MazeSolver):
    name = "BFS"

    def solve(self) -> list[Cell] | None:
        """Solve the maze and return the shortest path, or None if unsolvable."""
```

### Parameters

The solver takes a [`Maze`](../models#maze) object in its constructor:

```python
from solver.bfs import BFSMazeSolver
from models.maze import Maze

solver = BFSMazeSolver(maze)
```

### Return Value

- **`list[Cell]`** — Ordered list of cells from entry to exit (inclusive) representing the shortest path.
- **`None`** — If no path exists between entry and exit.

### Usage Example

```python
from maze_generator import MazeGenerator
from solver.bfs import BFSMazeSolver

maze = MazeGenerator.create(width=20, height=15, seed=42)
solver = BFSMazeSolver(maze)
path = solver.solve()

if path:
    print(f"Path found! Length: {len(path)} cells")
    for cell in path:
        print(f"  ({cell.x}, {cell.y})")
else:
    print("No path found.")
```

### Direction Mapping

The solver maps cell-to-cell movement to cardinal directions for the output file:

| Delta (dx, dy) | Wall Checked | Direction Letter |
|---|---|---|
| `(0, -1)` | `Cell.WEST` | `W` |
| `(1, 0)` | `Cell.SOUTH` | `S` |
| `(0, 1)` | `Cell.EAST` | `E` |
| `(-1, 0)` | `Cell.NORTH` | `N` |

### Internal Methods

| Method | Description |
|---|---|
| `_bfs()` | Core BFS traversal logic |
| `_reconstruct(came_from, end)` | Rebuild path from `came_from` dictionary |
| `_get_passable_neighbors(cell)` | Get neighbours reachable through open walls |

---

## Related Modules

- **Models** — [`Cell`](../models#cell), [`Maze`](../models#maze) data structures
- **Algorithms** that generate mazes → [algo/](../algo)
- **Renderer** that visualises the solution → [renderer/](../renderer)
