# Hooks — `src/hooks/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

Hooks are pluggable transformations applied **before** or **after** maze generation. They implement the [`MazeHook`](../README.md#mazehook-protocol) protocol.

## Overview

| File | Class | Stage | Description |
|---|---|---|---|
| [`pattern_42.py`](#add42pattern) | `Add42Pattern` | `pre` | Adds the "42" blocked-cell pattern |
| [`blocked_area.py`](#addblockedarea) | `AddBlockedArea` | `pre` | Adds arbitrary rectangular blocked areas |
| [`break_perfect.py`](#breakperfect) | `BreakPerfect` | `post` | Removes random walls to break maze perfection |

### Hook Stages

| Stage | When | Purpose |
|---|---|---|
| `"pre"` | Before generation algorithm runs | Modify the grid structure (block cells, resize) |
| `"post"` | After generation algorithm runs | Modify the generated maze (remove walls, add features) |

Hooks are passed to [`MazeGenerator.create()`](../README.md#maze_generatorpy) via the `hooks` parameter:

```python
from maze_generator import MazeGenerator
from hooks import Add42Pattern, BreakPerfect

maze = MazeGenerator.create(
    width=20,
    height=15,
    hooks=[
        Add42Pattern(),            # pre-hook
        BreakPerfect(percent=0.2), # post-hook
    ]
)
```

---

## Add42Pattern

**File:** [`pattern_42.py`](pattern_42.py) · **Stage:** `pre`

Adds the "42" pattern as blocked cells in the centre of the maze. This is a requirement of the project assignment — the maze must contain a visible "42" drawn by fully closed cells.

### Requirements

- Maze must be at least **8 cells wide** and **7 cells tall**.
- Raises [`MazeSizeError`](../README.md#exceptionspy) if the maze is too small.

### Pattern Layout

The "42" pattern is defined as a set of `(x, y)` offsets in [`Settings.pattern_42`](../README.md#configpy) and is automatically centred:

```
Offset: ox = width // 2 - 4, oy = height // 2 - 2
```

### Usage

```python
from hooks import Add42Pattern

hook = Add42Pattern()
# Pass to MazeGenerator.create(..., hooks=[hook])
```

---

## AddBlockedArea

**File:** [`blocked_area.py`](blocked_area.py) · **Stage:** `pre`

Adds a rectangular area of blocked cells to the maze. Useful for creating obstacles or custom patterns.

### Constructor

```python
AddBlockedArea(
    start: str | tuple[int, int],
    width: int,
    height: int,
    maze_resize: bool = False
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `start` | `str \| tuple[int, int]` | — | Top-left corner position |
| `width` | `int` | — | Width of the blocked area |
| `height` | `int` | — | Height of the blocked area |
| `maze_resize` | `bool` | `False` | Whether to resize the maze to fit the area |

### Position Strings

When `start` is a string, it uses the format `"x_position:y_position"`:

| X Position | Meaning |
|---|---|
| `"left"` | Left edge (x = 0) |
| `"center"` | Horizontally centred |
| `"right"` | Right edge |
| `<number>` | Exact x coordinate |

| Y Position | Meaning |
|---|---|
| `"top"` | Top edge (y = 0) |
| `"center"` | Vertically centred |
| `"bottom"` | Bottom edge |
| `<number>` | Exact y coordinate |

### Usage

```python
from hooks import AddBlockedArea

# Block a 3x3 area at the center
hook = AddBlockedArea(start="center:center", width=3, height=3)

# Block a 2x2 area at specific coordinates
hook = AddBlockedArea(start=(5, 5), width=2, height=2)

# Block an area and resize the maze to accommodate it
hook = AddBlockedArea(start="right:bottom", width=4, height=4, maze_resize=True)
```

### Exceptions

- Raises [`MazeSizeError`](../README.md#exceptionspy) if the blocked area exceeds maze boundaries.
- Raises `ValueError` if the position string is invalid.

---

## BreakPerfect

**File:** [`break_perfect.py`](break_perfect.py) · **Stage:** `post`

Removes a random percentage of remaining walls to break the maze's perfection, creating multiple paths between cells. Uses the [`break_perfect()`](../utils) utility function.

### Constructor

```python
BreakPerfect(percent: float = 0.1, seed: int | None = None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `percent` | `float` | `0.1` | Fraction of remaining walls to remove (0.0–1.0) |
| `seed` | `int \| None` | `None` | Random seed for reproducibility |

### Usage

```python
from hooks import BreakPerfect

# Remove 20% of walls
hook = BreakPerfect(percent=0.2, seed=42)

# Remove 10% of walls (default)
hook = BreakPerfect()
```

### How It Works

1. Collects all remaining internal walls (pairs of adjacent non-blocked cells with a wall between them).
2. Shuffles the walls randomly (using the seed if provided).
3. Removes the first `percent × total_walls` walls.

---

## Creating Custom Hooks

Any callable that implements the [`MazeHook`](../README.md#mazehook-protocol) protocol can be used as a hook:

```python
from models.maze import Maze

class MyCustomHook:
    stage = "post"  # or "pre"

    def __call__(self, maze: Maze) -> Maze:
        # Transform the maze
        return maze
```

---

## Related Modules

- **Models** — [`Cell`](../models#cell), [`Maze`](../models#maze) data structures
- **Utils** — [`break_perfect()`](../utils) utility function
- **MazeGenerator** — orchestrates hooks → [maze_generator.py](../README.md#maze_generatorpy)
