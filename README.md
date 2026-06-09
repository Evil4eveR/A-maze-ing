This project has been created as part of the 42 curriculum by dbobrov[, <login2>]

*This project has been created as part of the 42 curriculum by dbobrov.*

# A-Maze-ing 🏗️

> Create your own maze generator and display its result!

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running](#running)
  - [Debugging](#debugging)
  - [Linting](#linting)
  - [Cleaning](#cleaning)
- [Configuration File Format](#configuration-file-format)
- [Output File Format](#output-file-format)
- [Maze Generation Algorithms](#maze-generation-algorithms)
  - [Depth-First Search (DFS)](#depth-first-search-dfs)
  - [Prim's Algorithm](#prims-algorithm)
  - [Kruskal's Algorithm](#kruskals-algorithm)
  - [Wilson's Algorithm](#wilsons-algorithm)
  - [Why These Algorithms?](#why-these-algorithms)
- [Reusable Module — MazeGenerator](#reusable-module--mazegenerator)
  - [Instantiation & Basic Usage](#instantiation--basic-usage)
  - [Custom Parameters](#custom-parameters)
  - [Accessing the Generated Structure](#accessing-the-generated-structure)
  - [Accessing a Solution](#accessing-a-solution)
- [Visual Representation](#visual-representation)
- [The "42" Pattern](#the-42-pattern)
- [Hooks System](#hooks-system)
- [Source Code Documentation](#source-code-documentation)
- [Team & Project Management](#team--project-management)
- [Resources](#resources)

---

## Description

**A-Maze-ing** is a maze generator and solver written in Python. The program reads a configuration file, generates a random maze (optionally *perfect* — with exactly one path between any two cells), and writes the result to a file using hexadecimal wall encoding. It also provides an interactive ASCII visual representation in the terminal via the [Rich](https://github.com/Textualize/rich) library.

The project is built with a modular, object-oriented architecture. The maze generation logic is fully reusable and can be imported as a standalone module in other projects.

## Features

- **Multiple generation algorithms**: [DFS](src/algo#depth-first-search-dfs), [Prim](src/algo#prims-algorithm), [Kruskal](src/algo#kruskals-algorithm), [Wilson](src/algo#wilsons-algorithm)
- **Perfect maze generation** with a single unique path between entry and exit
- **BFS shortest-path solver** — see [Solver](src/solver)
- **ASCII terminal rendering** with customisable RGB colours — see [Renderer](src/renderer)
- **Configurable** via a simple `KEY=VALUE` text file
- **Reproducible** mazes through optional seed support
- **Hook system** for pre/post-generation transformations (blocked areas, "42" pattern, break perfect) — see [Hooks](src/hooks)
- **Hexadecimal output** file format with encoded wall data
- **Type-checked** with `mypy` and linted with `flake8`

## Project Structure

```
A-maze-ing/
├── Makefile                 # Build automation
├── README.md                # This file
├── Task.pdf                 # Project assignment
├── config.txt               # Default configuration file
├── pyproject.toml            # Python project metadata
├── uv.lock                  # Dependency lock file
└── src/                     # Source code — see src/README.md
    ├── a_maze_ing.py         # Main entry point
    ├── config.py             # Settings / configuration loader
    ├── exceptions.py         # Custom exception classes
    ├── interfaces.py         # Abstract base classes & protocols
    ├── maze_generator.py     # MazeGenerator facade (reusable module)
    ├── test.py               # Manual test / demo script
    ├── algo/                 # Generation algorithms — see src/algo/README.md
    │   ├── dfs.py
    │   ├── kruskal.py
    │   ├── prim.py
    │   └── wilson.py
    ├── models/               # Data models — see src/models/README.md
    │   ├── cell.py
    │   └── maze.py
    ├── renderer/             # Rendering engines — see src/renderer/README.md
    │   └── ascii.py
    ├── solver/               # Solving algorithms — see src/solver/README.md
    │   └── bfs.py
    ├── hooks/                # Pre/post-generation hooks — see src/hooks/README.md
    │   ├── blocked_area.py
    │   ├── break_perfect.py
    │   └── pattern_42.py
    └── utils/                # Utility functions — see src/utils/README.md
        └── algo.py
```

## Instructions

### Requirements

- Python **3.14+** (as specified in `pyproject.toml`)
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
make install
```

This runs `uv sync` to install all project dependencies defined in `pyproject.toml`:

| Dependency | Purpose |
|---|---|
| `pydantic` / `pydantic-settings` | Configuration validation and loading |
| `rich` | Coloured terminal output |
| `flake8` | Code style linting |
| `mypy` | Static type checking |
| `python-dotenv` | `.env` / config file support |

### Running

```bash
make run
```

Equivalent to:

```bash
uv run python src/a_maze_ing.py config.txt
```

### Debugging

```bash
make debug
```

Launches the program with Python's built-in debugger (`pdb`).

### Linting

```bash
make lint          # Standard lint (flake8 + mypy)
make lint-strict   # Strict mode (mypy --strict)
```

### Cleaning

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, `.ruff_cache`, and compiled Python files.

---

## Configuration File Format

The configuration file is a plain text file with one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

| Key | Type | Required | Description | Example |
|---|---|---|---|---|
| `WIDTH` | int | ✅ | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | int | ✅ | Maze height (number of cells) | `HEIGHT=15` |
| `ENTRY` | x,y | ✅ | Entry coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | ✅ | Exit coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | string | ✅ | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | ✅ | Whether the maze is perfect | `PERFECT=true` |
| `SEED` | int | ❌ | Random seed for reproducibility | `SEED=42` |

**Default configuration** (`config.txt`):

```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=true
# SEED=42  Optional
```

## Output File Format

The maze is written to the output file using **one hexadecimal digit per cell**, encoding which walls are closed:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

- A closed wall sets the corresponding bit to `1`; an open wall sets it to `0`.
- Example: `3` (binary `0011`) → North and East walls closed, South and West open.
- Example: `A` (binary `1010`) → East and West walls closed.
- Cells are stored **row by row**, one row per line.
- After an empty line, three additional lines are written:
  1. Entry coordinates
  2. Exit coordinates
  3. Shortest valid path from entry to exit (`N`, `E`, `S`, `W`)

---

## Maze Generation Algorithms

The project supports **four** maze generation algorithms. Each produces a spanning tree of the grid graph, guaranteeing a perfect maze. See full documentation → [src/algo/README.md](src/algo).

### Depth-First Search (DFS)

Recursive backtracker using a stack. Produces mazes with long, winding corridors and relatively few dead ends. → [Details](src/algo#depth-first-search-dfs)

### Prim's Algorithm

Grows the maze outward from a starting cell by randomly selecting frontier cells. Creates mazes with shorter corridors and more branching. → [Details](src/algo#prims-algorithm)

### Kruskal's Algorithm

Randomly shuffles all walls and removes them if they connect two disjoint sets (Union-Find). Produces evenly distributed mazes. → [Details](src/algo#kruskals-algorithm)

### Wilson's Algorithm

Uses loop-erased random walks to create an unbiased spanning tree. Produces uniform random mazes. → [Details](src/algo#wilsons-algorithm)

### Why These Algorithms?

| Algorithm | Bias | Corridor Style | Performance | Best For |
|---|---|---|---|---|
| DFS | Long passages | Winding | O(n) | Quick, visually interesting mazes |
| Prim | Short passages | Branching | O(n log n) | Mazes with many branches |
| Kruskal | Even distribution | Balanced | O(n log n) | Uniform-looking mazes |
| Wilson | Unbiased | Uniform random | Variable | Statistically perfect mazes |

All four algorithms were chosen to demonstrate different approaches to spanning-tree generation and to allow users to compare the visual and structural characteristics of each.

---

## Reusable Module — MazeGenerator

The [`MazeGenerator`](src/maze_generator.py) class is the main public API for generating mazes. It is designed to be imported and used in external projects.

### Instantiation & Basic Usage

```python
from maze_generator import MazeGenerator

maze = MazeGenerator.create(
    width=20,
    height=15,
    algo="dfs",
    entry_point=(0, 0),
    exit_point=(19, 14),
    seed=42
)
```

### Custom Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Maze width in cells |
| `height` | `int` | — | Maze height in cells |
| `algo` | `str` or `Type[MazeAlgorithm]` | `"dfs"` | Algorithm: `"dfs"`, `"prim"`, `"kruskal"`, `"wilson"` |
| `entry_point` | `tuple[int, int]` | `(0, 0)` | Entry cell coordinates |
| `exit_point` | `tuple[int, int]` | `(width-1, height-1)` | Exit cell coordinates |
| `seed` | `int \| None` | `None` | Random seed for reproducibility |
| `hooks` | `list[MazeHook] \| None` | `None` | Pre/post-generation hooks |

### Accessing the Generated Structure

The `create()` method returns a [`Maze`](src/models) object:

```python
maze = MazeGenerator.create(width=10, height=10)

# Access the grid (2D list of Cell objects)
for row in maze.grid:
    for cell in row:
        print(f"Cell ({cell.x}, {cell.y}) walls={cell.walls:#06b}")

# Access entry and exit
print(f"Entry: ({maze.entry.x}, {maze.entry.y})")
print(f"Exit: ({maze.exit.x}, {maze.exit.y})")

# Check specific walls
cell = maze.get_cell(5, 5)
if cell and cell.has_wall(Cell.NORTH):
    print("Cell has a north wall")
```

### Accessing a Solution

Use the [`BFSMazeSolver`](src/solver) to find the shortest path:

```python
from solver.bfs import BFSMazeSolver

solver = BFSMazeSolver(maze)
path = solver.solve()  # Returns list[Cell] | None

if path:
    directions = []
    for i in range(len(path) - 1):
        dx = path[i + 1].x - path[i].x
        dy = path[i + 1].y - path[i].y
        if dx == 1:   directions.append("S")
        elif dx == -1: directions.append("N")
        elif dy == 1:  directions.append("E")
        elif dy == -1: directions.append("W")
    print("Path:", " → ".join(directions))
```

---

## Visual Representation

The project provides **ASCII terminal rendering** via the [`AsciiMazeRenderer`](src/renderer). The renderer uses the [Rich](https://github.com/Textualize/rich) library for RGB-coloured output.

```python
from renderer.ascii import AsciiMazeRenderer

colors = [
    (200, 200, 200),  # cell colour
    (37, 150, 190),   # wall colour
    (200, 200, 200),  # blocked wall colour
    (255, 255, 0),    # path colour
]

renderer = AsciiMazeRenderer(maze, path=path, colors=colors)
renderer.render()
renderer.display()
```

The visual representation clearly shows walls, entry point, exit point, and the solution path.

---

## The "42" Pattern

As required by the assignment, each generated maze contains a visible **"42"** drawn by fully closed (blocked) cells. The pattern is automatically centred in the maze using the [`Add42Pattern`](src/hooks) hook.

If the maze is too small (less than 8×7), a `MazeSizeError` is raised.

---

## Hooks System

Hooks allow transformations to be applied before or after maze generation. See → [src/hooks/README.md](src/hooks).

| Hook | Stage | Description |
|---|---|---|
| [`Add42Pattern`](src/hooks#add42pattern) | `pre` | Adds the "42" blocked-cell pattern |
| [`AddBlockedArea`](src/hooks#addblockedarea) | `pre` | Adds arbitrary blocked areas |
| [`BreakPerfect`](src/hooks#breakperfect) | `post` | Removes a percentage of walls to break perfection |

---

## Source Code Documentation

Each directory in `src/` has its own `README.md` with detailed documentation:

| Directory | Description | Link |
|---|---|---|
| `src/` | Source overview, entry points, configuration | [src/README.md](src) |
| `src/models/` | `Cell` and `Maze` data models | [src/models/README.md](src/models) |
| `src/algo/` | Generation algorithms (DFS, Prim, Kruskal, Wilson) | [src/algo/README.md](src/algo) |
| `src/solver/` | BFS maze solver | [src/solver/README.md](src/solver) |
| `src/renderer/` | ASCII terminal renderer | [src/renderer/README.md](src/renderer) |
| `src/hooks/` | Pre/post-generation hooks | [src/hooks/README.md](src/hooks) |
| `src/utils/` | Utility functions | [src/utils/README.md](src/utils) |

---

## Team & Project Management

### Roles

| Member | Role |
|---|---|
| **dbobrov** | Full-stack developer — architecture, algorithms, rendering, documentation |

### Planning & Evolution

The project was planned in the following phases:

1. **Phase 1 — Core models**: Implemented `Cell` and `Maze` data structures with wall encoding.
2. **Phase 2 — Generation**: Implemented DFS as the primary algorithm, then added Prim, Kruskal, and Wilson for comparison and bonus points.
3. **Phase 3 — Solver & Output**: Implemented BFS solver and hexadecimal output file format.
4. **Phase 4 — Rendering**: Built the ASCII renderer with Rich for coloured terminal output.
5. **Phase 5 — Hooks & Patterns**: Added the hook system for the "42" pattern, blocked areas, and break-perfect functionality.
6. **Phase 6 — Documentation & Polish**: Wrote comprehensive README files, linting, and testing.

### What Worked Well

- Modular architecture with clear separation of concerns (interfaces, models, algorithms)
- The hook system made it easy to add features without modifying core generation logic
- Multiple algorithm support provides variety and educational value

### What Could Be Improved

- Adding graphical rendering (MLX) alongside ASCII
- More comprehensive automated test suite
- Animation during maze generation

### Tools Used

- **Python 3.14** — main language
- **uv** — fast package manager
- **Pydantic** — configuration validation
- **Rich** — terminal rendering
- **flake8** / **mypy** — code quality
- **Git** — version control

---

## Resources

- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Prim's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Kruskal's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Wilson's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Loop-erased_random_walk)
- [Depth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Think Labyrinth — Maze Algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### AI Usage

AI tools were used to assist with the following tasks:
- Generating boilerplate documentation structure
- Reviewing code for type-hint completeness
- Exploring algorithm trade-offs and comparisons

All AI-generated content was reviewed, understood, and validated by the team before inclusion.