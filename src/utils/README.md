# Utilities — `src/utils/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

This package contains utility functions used by other modules.

## Overview

| File | Function | Description |
|---|---|---|
| [`algo.py`](#break_perfect) | `break_perfect()` | Remove random walls to break maze perfection |

---

## `break_perfect()`

**File:** [`algo.py`](algo.py)

Removes a random percentage of internal walls from a generated maze, converting it from a perfect maze (single path) to an imperfect maze (multiple paths).

### Signature

```python
def break_perfect(
    maze: Maze,
    percent: float,
    seed: int | None = None
) -> None:
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `maze` | [`Maze`](../models#maze) | — | The maze to modify (mutated in place) |
| `percent` | `float` | — | Fraction of remaining walls to remove (0.0–1.0) |
| `seed` | `int \| None` | `None` | Random seed for reproducibility |

### How It Works

1. **Collect walls**: Iterates through all cells and collects pairs of adjacent non-blocked cells that still have a wall between them. Only checks **south** (`Cell.SOUTH`) and **east** (`Cell.EAST`) walls to avoid duplicates.
2. **Shuffle**: Randomly shuffles the collected walls using the provided seed.
3. **Remove**: Removes the first `int(len(walls) * percent)` walls by calling `cell.remove_walls_between(neighbor)`.

### Usage

```python
from utils.algo import break_perfect
from models.maze import Maze

# Assuming 'maze' is already generated
break_perfect(maze, percent=0.15, seed=42)  # Remove 15% of walls
```

### Notes

- This function **mutates** the maze in place — it does not return a new maze.
- It is typically used via the [`BreakPerfect`](../hooks#breakperfect) hook rather than called directly.
- Blocked cells are skipped — walls adjacent to blocked cells are never removed.

---

## Related Modules

- **Hooks** — [`BreakPerfect`](../hooks#breakperfect) wraps this function
- **Models** — [`Cell`](../models#cell), [`Maze`](../models#maze) used by this function
