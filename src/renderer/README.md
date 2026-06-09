# Renderer — `src/renderer/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

This package contains the maze rendering engine(s).

## Overview

| File | Class | Output Type | Description |
|---|---|---|---|
| [`ascii.py`](#ascimazerenderer) | `AsciiMazeRenderer` | `str` | Coloured ASCII terminal rendering via Rich |

---

## AsciiMazeRenderer

**File:** [`ascii.py`](ascii.py) · **Class:** `AsciiMazeRenderer` · **Name:** `"ascii"`

Implements the [`MazeRenderer[str]`](../README.md#mazerenderer-abc-generict) abstract base class.

### How It Works

1. Creates a 2D integer grid of size `(height * 2 + 1) × (width * 2 + 1)` — each cell occupies one position with walls between them.
2. For each maze cell, sets the cell position to `0` (empty) and checks which walls are open.
3. Blocked cells are rendered as a different wall style (value `2`).
4. If a solution path is provided, marks path cells with value `3`.
5. Entry and exit cells are marked with values `4` and `5` respectively.
6. Converts the integer grid to a coloured string using Rich markup (`[rgb(r,g,b)]...[/rgb(r,g,b)]`).

### Constructor

```python
AsciiMazeRenderer(
    maze: Maze,
    path: list[Cell] | None = None,
    colors: list[tuple[int, int, int]] | None = None
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `maze` | [`Maze`](../models#maze) | — | The maze to render |
| `path` | `list[Cell] \| None` | `None` | Solution path to highlight |
| `colors` | `list[tuple[int, int, int]] \| None` | `None` | Custom RGB colour palette (4 colours) |

### Colour Palette

If custom colours are provided, they must be a list of exactly **4** RGB tuples:

| Index | Purpose | Default |
|---|---|---|
| 0 | Cell (empty space) | `(200, 200, 200)` |
| 1 | Wall | `(120, 50, 150)` |
| 2 | Blocked wall ("42" pattern) | `(100, 100, 100)` |
| 3 | Solution path | `(255, 255, 0)` |

Two additional colours are automatically appended:

| Index | Purpose | Value |
|---|---|---|
| 4 | Entry point | `(255, 0, 255)` |
| 5 | Exit point | `(255, 0, 0)` |

### Methods

| Method | Returns | Description |
|---|---|---|
| `render()` | `str` | Render the maze to a Rich-formatted string |
| `display()` | `None` | Print the rendered maze to the terminal |
| `set_colors(colors)` | `list[tuple]` | Set or reset the colour palette |

### Usage Example

```python
from models.maze import Maze
from maze_generator import MazeGenerator
from solver.bfs import BFSMazeSolver
from renderer.ascii import AsciiMazeRenderer

# Generate and solve
maze = MazeGenerator.create(width=20, height=15, seed=42)
path = BFSMazeSolver(maze).solve()

# Render with default colours
renderer = AsciiMazeRenderer(maze, path=path)
renderer.render()
renderer.display()

# Render with custom colours
custom_colors = [
    (200, 200, 200),  # cell
    (37, 150, 190),   # wall
    (200, 200, 200),  # blocked wall
    (255, 255, 0),    # path
]
renderer = AsciiMazeRenderer(maze, path=path, colors=custom_colors)
renderer.display()
```

### Rendering Grid Values

The internal `renderer` grid uses integer values to represent cell types:

| Value | Meaning | Display |
|---|---|---|
| `0` | Empty cell | `"  "` (two spaces) |
| `1` | Wall | `"██"` (full block) |
| `2` | Blocked wall | `"██"` (different colour) |
| `3` | Solution path | `"░░"` (light shade) |
| `4` | Entry point | `"░░"` (entry colour) |
| `5` | Exit point | `"░░"` (exit colour) |

---

## Related Modules

- **Models** — [`Cell`](../models#cell), [`Maze`](../models#maze) data structures
- **Solver** that provides the path → [solver/](../solver)
- **Config** for display characters → [config.py](../README.md#configpy)
