# Source Code — `src/`

> [← Back to Project Root](../README.md)

This directory contains all the source code for the **A-Maze-ing** maze generator.

## Directory Overview

| File / Directory | Description | Documentation |
|---|---|---|
| [`a_maze_ing.py`](#a_maze_ingpy) | Main entry point | Below |
| [`config.py`](#configpy) | Configuration loader (Pydantic) | Below |
| [`exceptions.py`](#exceptionspy) | Custom exception hierarchy | Below |
| [`interfaces.py`](#interfacespy) | Abstract base classes & protocols | Below |
| [`maze_generator.py`](#maze_generatorpy) | `MazeGenerator` facade (reusable module) | Below |
| [`test.py`](#testpy) | Manual test / demo script | Below |
| [`models/`](models) | `Cell` and `Maze` data models | [models/README.md](models) |
| [`algo/`](algo) | Generation algorithms (DFS, Prim, Kruskal, Wilson) | [algo/README.md](algo) |
| [`solver/`](solver) | BFS maze solver | [solver/README.md](solver) |
| [`renderer/`](renderer) | ASCII terminal renderer | [renderer/README.md](renderer) |
| [`hooks/`](hooks) | Pre/post-generation hooks | [hooks/README.md](hooks) |
| [`utils/`](utils) | Utility functions | [utils/README.md](utils) |

---

## `a_maze_ing.py`

The main entry point of the application. Launched via:

```bash
python3 a_maze_ing.py config.txt
```

Reads the configuration file passed as an argument and orchestrates the maze generation, solving, and rendering pipeline.

---

## `config.py`

Configuration management using [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

### `Settings` (class)

Inherits from `BaseSettings`. Automatically loads values from `config.txt`.

| Field | Type | Description |
|---|---|---|
| `width` | `int` | Maze width in cells |
| `height` | `int` | Maze height in cells |
| `entry_raw` | `str` (alias: `entry`) | Raw entry coordinates string (e.g. `"0,0"`) |
| `exit_raw` | `str` (alias: `exit`) | Raw exit coordinates string (e.g. `"19,14"`) |
| `output_file` | `str` | Output filename |
| `perfect` | `bool` | Whether to generate a perfect maze |
| `seed` | `int \| None` | Optional random seed |

**Computed fields:**

| Property | Type | Description |
|---|---|---|
| `entry` | `tuple[int, int]` | Parsed entry coordinates |
| `exit` | `tuple[int, int]` | Parsed exit coordinates |

**Class variables (rendering):**

| Variable | Value | Description |
|---|---|---|
| `pattern_42` | `list[tuple[int, int]]` | Coordinates for the "42" blocked-cell pattern |
| `wall` | `"██"` | Wall display characters |
| `cell` | `"  "` | Empty cell display characters |
| `path` | `"░░"` | Path display characters |

---

## `exceptions.py`

Custom exception hierarchy for maze-related errors.

```
Exception
└── MazeError                    # Base class for all maze errors
    ├── InvalidEntryExitError    # Invalid entry/exit points
    ├── MazeSizeError            # Invalid maze dimensions
    └── MazeWallError            # Invalid wall configuration
```

| Exception | Raised When |
|---|---|
| `MazeError` | General maze error (base class) |
| `InvalidEntryExitError` | Entry/exit are the same, out of bounds, or blocked |
| `MazeSizeError` | Maze too small, or blocked areas disconnect the maze |
| `MazeWallError` | Invalid wall bitmask or non-adjacent cell wall removal |

---

## `interfaces.py`

Abstract base classes and protocols that define the contracts for all pluggable components.

### `MazeAlgorithm` (ABC)

Base class for maze generation algorithms. See → [algo/](algo)

| Method | Description |
|---|---|
| `generate(seed)` | Generate a complete maze |
| `_get_neighbors(cell, visited)` | Get valid neighbouring cells |
| `_reset_visited()` | Reset all cells' visited flags |

### `MazeSolver` (ABC)

Base class for maze solving algorithms. See → [solver/](solver)

| Method | Description |
|---|---|
| `solve()` | Solve the maze; returns `list[Cell] \| None` |

### `MazeRenderer` (ABC, Generic[T])

Base class for maze renderers. See → [renderer/](renderer)

| Method | Description |
|---|---|
| `render()` | Render the maze; returns result of type `T` |
| `display()` | Print the rendered result |

### `MazeHook` (Protocol)

Protocol for pre/post-generation hooks. See → [hooks/](hooks)

| Attribute | Type | Description |
|---|---|---|
| `stage` | `Literal["pre", "post"]` | When the hook runs |
| `__call__` | `(Maze) → Maze` | Transform the maze |

---

## `maze_generator.py`

The central facade class. See full documentation in the [main README](../README.md#reusable-module--mazegenerator).

### `MazeGenerator` (class)

| Method | Description |
|---|---|
| `create(...)` | Class method — create and return a fully generated `Maze` |
| `_validate(maze)` | Validate entry/exit and connectivity |
| `_valid_entry_exit(maze)` | Validate that entry and exit are valid |
| `_is_connected(maze)` | BFS check that all free cells are reachable |

**Algorithm map:**

| Key | Class |
|---|---|
| `"dfs"` | [`DFSMazeGenerator`](algo#depth-first-search-dfs) |
| `"prim"` | [`PrimMazeGenerator`](algo#prims-algorithm) |
| `"kruskal"` | [`KruskalMazeGenerator`](algo#kruskals-algorithm) |
| `"wilson"` | [`WilsonMazeGenerator`](algo#wilsons-algorithm) |

---

## `test.py`

A manual demo script that demonstrates the full pipeline:

1. Creates a 20×10 maze using Wilson's algorithm with seed `420`
2. Applies `BreakPerfect` (20% wall removal) and `Add42Pattern` hooks
3. Solves the maze using BFS
4. Renders and displays the result with custom colours
