# Step-by-Step Guide: How a Maze Is Generated 🧩

> This guide explains the entire maze generation process from start to finish.
> Written for those who are just getting started with programming.

---

## Table of Contents

1. [The Big Picture](#1-the-big-picture)
2. [Step 1 — Reading the Configuration](#2-step-1--reading-the-configuration)
3. [Step 2 — Creating an Empty Grid](#3-step-2--creating-an-empty-grid)
4. [Step 3 — What Is a Cell?](#4-step-3--what-is-a-cell)
5. [Step 4 — Generating the Maze (DFS Algorithm)](#5-step-4--generating-the-maze-dfs-algorithm)
6. [Step 5 — Other Algorithms (Overview)](#6-step-5--other-algorithms-overview)
7. [Step 6 — Hooks (Pre- and Post-Processing)](#7-step-6--hooks-pre--and-post-processing)
8. [Step 7 — Solving the Maze (BFS)](#8-step-7--solving-the-maze-bfs)
9. [Step 8 — Rendering in the Terminal](#9-step-8--rendering-in-the-terminal)
10. [Step 9 — Saving to a File](#10-step-9--saving-to-a-file)
11. [Full Data Flow Diagram](#11-full-data-flow-diagram)
12. [Glossary](#12-glossary)

---

## 1. The Big Picture

The program performs the following steps:

```
Configuration ➜ Empty Grid ➜ Hooks (pre) ➜ Generation Algorithm ➜ Hooks (post) ➜ Solving ➜ Rendering / File
```

Everything starts with the `config.txt` file and ends with a beautiful maze in the terminal and an output file with the result.

---

## 2. Step 1 — Reading the Configuration

**File:** `src/config.py`

The program reads the `config.txt` file, which defines the maze parameters:

```ini
WIDTH=20          # width (number of cells horizontally)
HEIGHT=15         # height (number of cells vertically)
ENTRY=0,0         # entry coordinates
EXIT=19,14        # exit coordinates
OUTPUT_FILE=maze.txt
PERFECT=true      # "perfect" maze (exactly one path between any two cells)
# SEED=42         # optional — for reproducibility
```

**What happens under the hood:**
- The `pydantic-settings` library loads the values and **automatically validates their types** (for example, ensuring that `WIDTH` is an integer).
- If any parameter is invalid, the program raises a clear error before generation even begins.

---

## 3. Step 2 — Creating an Empty Grid

**File:** `src/models/maze.py` → class `Maze`

After reading the configuration, a `Maze` object is created — a two-dimensional array of cells (grid).

```
Maze(width=5, height=4) creates a 5×4 grid:

  ┌───┬───┬───┬───┬───┐
  │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
  │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
  │   │   │   │   │   │
  ├───┼───┼───┼───┼───┤
  │   │   │   │   │   │
  └───┴───┴───┴───┴───┘
```

At this stage, **all walls are closed** — every cell is completely isolated from its neighbours.

**How it looks in code:**

```python
self.grid = [
    [Cell(x=x, y=y) for x in range(self.width)]
    for y in range(self.height)
]
```

This creates a list of lists, where each position is a `Cell` object.

---

## 4. Step 3 — What Is a Cell?

**File:** `src/models/cell.py` → class `Cell`

Each cell stores:

| Field | Type | Default Value | Meaning |
|-------|------|---------------|---------|
| `x` | int | — | Horizontal position (column) |
| `y` | int | — | Vertical position (row) |
| `walls` | int | `0b1111` (15) | Wall bitmask |
| `visited` | bool | `False` | Whether the cell has been visited by the algorithm |
| `blocked` | bool | `False` | Whether the cell is blocked |

### How the Wall Bitmask Works

Walls are encoded using 4 bits — one bit for each direction:

```
Bit 3   Bit 2   Bit 1   Bit 0
WEST    SOUTH   EAST    NORTH
 8       4       2       1
```

**Examples:**

| Value | Binary | Walls |
|-------|--------|-------|
| `15` | `1111` | All walls closed |
| `0`  | `0000` | All walls open |
| `5`  | `0101` | South and North closed |
| `10` | `1010` | West and East closed |

### How a Wall Is Removed

When the algorithm decides to connect two adjacent cells, the `remove_walls_between` method is called:

```
Before:                        After:
┌───┬───┐                    ┌───┬───┐
│ A │ B │   ── remove ──►    │ A   B │
└───┴───┘   wall between    └───┴───┘
```

In the code, this is done using bitwise operations:

```python
# Remove a wall: clear the corresponding bit
self.walls &= ~direction
```

For example, if `A` and `B` are horizontal neighbours (B is to the right of A):
- Cell `A` has its **EAST** wall removed
- Cell `B` has its **WEST** wall removed

---

## 5. Step 4 — Generating the Maze (DFS Algorithm)

**File:** `src/algo/dfs.py` → class `DFSMazeGenerator`

DFS (Depth-First Search) is the most intuitive algorithm. It works like a person walking through a maze and carving a path as they go.

### Algorithm Step by Step

**Initial state:** all walls are closed, no cell has been visited.

```
Step 0: Start at the entry cell. Push it onto the stack.

        ┌───┬───┬───┐
        │ S │   │   │    S = start (current cell)
        ├───┼───┼───┤    Stack: [S]
        │   │   │   │
        ├───┼───┼───┤
        │   │   │   │
        └───┴───┴───┘
```

```
Step 1: Look at S's neighbours. Pick a random unvisited neighbour.
        Remove the wall between S and the neighbour. Move to it.

        ┌───┬───┬───┐
        │ ✓   ● │   │    ● = current cell
        ├───┼───┼───┤    ✓ = visited
        │   │   │   │    Stack: [S, ●]
        ├───┼───┼───┤
        │   │   │   │
        └───┴───┴───┘
```

```
Step 2: Repeat — pick a random unvisited neighbour.

        ┌───┬───┬───┐
        │ ✓   ✓ │   │
        ├───┼───┼───┤
        │   │ ● │   │    Stack: [S, ✓, ●]
        ├───┼───┼───┤
        │   │   │   │
        └───┴───┴───┘
```

```
Step N: If the current cell has no unvisited neighbours —
        BACKTRACK: pop the cell from the stack,
        return to the previous one and try another neighbour.
```

```
End: When the stack is empty — all cells have been visited and the maze is ready!
```

### The Same Algorithm in Code

```python
def _generate_dfs(self, seed=None):
    rng = Random(seed)                          # random number generator
    stack = [self.maze.entry]                    # stack starts with the entry
    self.maze.entry.visited = True               # mark entry as visited

    while stack:                                 # while the stack is not empty
        current_cell = stack[-1]                 # peek at the top of the stack

        # Find unvisited neighbours
        neighbors = self._get_neighbors(current_cell, visited=False)

        if neighbors:
            # There is somewhere to go — pick a random neighbour
            next_cell = rng.choice(neighbors)
            current_cell.remove_walls_between(next_cell)  # remove the wall
            stack.append(next_cell)                        # push onto the stack
            next_cell.visited = True                       # mark as visited
        else:
            # Dead end — backtrack
            stack.pop()
```

### Why Does This Work?

DFS guarantees that:
1. Every cell will be visited **exactly once**
2. There will be **exactly one path** between any two cells (= a "perfect" maze)
3. The result is a **spanning tree** of the grid graph

---

## 6. Step 5 — Other Algorithms (Overview)

All algorithms solve the same problem: build a spanning tree of the grid. But they do it differently.

### Prim's Algorithm (`src/algo/prim.py`)

Principle: **"grow outward"**

```
1. Start with one cell — mark it as visited.
2. Add all its unvisited neighbours to a "frontier" list.
3. Randomly pick a cell from the frontier.
4. Connect it to any visited neighbour (remove the wall).
5. Add the new cell's neighbours to the frontier.
6. Repeat until the frontier is empty.
```

**Result:** a maze with short corridors and many branches.

### Kruskal's Algorithm (`src/algo/kruskal.py`)

Principle: **"remove random walls"**

```
1. Each cell is its own set (Union-Find).
2. Collect ALL walls and shuffle them randomly.
3. For each wall:
   - If the cells on both sides belong to different sets → remove the wall, merge the sets.
   - If they belong to the same set → skip (otherwise a cycle would be created).
4. Repeat until all cells are in one set.
```

**Result:** an evenly distributed maze.

### Wilson's Algorithm (`src/algo/wilson.py`)

Principle: **"random walks with loop erasure"**

```
1. Mark one random cell as part of the maze.
2. Pick any unvisited cell.
3. Start a random walk until you hit an already-visited cell.
4. Erase all loops (loop-erased random walk): if a cell was visited twice,
   only keep the last path.
5. Carve the path — remove walls along it.
6. Repeat from step 2 until all cells have been visited.
```

**Result:** a uniformly random, unbiased maze.

### Comparison Table

| | DFS | Prim | Kruskal | Wilson |
|---|---|---|---|---|
| Corridor style | Long, winding | Short, branching | Balanced | Uniform |
| Complexity | Simple | Medium | Medium | Complex |
| File | `dfs.py` | `prim.py` | `kruskal.py` | `wilson.py` |

---

## 7. Step 6 — Hooks (Pre- and Post-Processing)

**Files:** `src/hooks/`

Hooks are functions that are applied **before** (`pre`) or **after** (`post`) maze generation. They allow you to modify the maze without changing the algorithm code.

### How Hooks Work

```
      Pre-hooks            Generation           Post-hooks
         │                    │                     │
         ▼                    ▼                     ▼
  ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
  │  Add "42"   │    │  Algorithm  │    │  Break a     │
  │  pattern    │ ➜  │  (DFS and   │ ➜  │  percentage  │
  │  Block      │    │   others)   │    │  of walls    │
  │  areas      │    │             │    │  (break      │
  └─────────────┘    └─────────────┘    │  perfect)    │
                                        └──────────────┘
```

### "42" Pattern (`pattern_42.py`)

A mandatory part of the assignment: draws the digits **42** using blocked cells in the centre of the maze.

### Blocked Areas (`blocked_area.py`)

Allows you to make certain cells "impassable" — the algorithm will route around them.

### Breaking Perfection (`break_perfect.py`)

Removes a random percentage of walls **after** generation to create alternative paths.

---

## 8. Step 7 — Solving the Maze (BFS)

**File:** `src/solver/bfs.py` → class `BFSMazeSolver`

After generating the maze, the program finds the shortest path from entry to exit using BFS (Breadth-First Search).

### How BFS Works

```
1. Start at the entry cell. Add it to the queue.
2. Take a cell from the front of the queue.
3. For each neighbour that can be reached (no wall between them):
   - If the neighbour has not been visited yet → add it to the queue, record "where we came from".
4. Repeat until the exit is reached.
5. Reconstruct the path by tracing back from the exit to the entry using the recorded cells.
```

### Example

```
┌───────────┐
│ S ─ ─ ─   │       S = entry
│   ┌───┐ │ │       E = exit
│   │   │ │ │       ─ = solution path
│   │   ─ ─ │
│   │     E │
└───────────┘
```

### Key Point — Wall Checking

BFS only passes through **open passages** (where the wall has been removed):

```python
def _get_passable_neighbors(self, cell):
    passable = []
    for (dx, dy), wall in [
        ((0, -1), Cell.WEST),
        ((1, 0),  Cell.SOUTH),
        ((0, 1),  Cell.EAST),
        ((-1, 0), Cell.NORTH)
    ]:
        neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
        if neighbor and not cell.has_wall(wall):   # is the wall open?
            passable.append(neighbor)
    return passable
```

---

## 9. Step 8 — Rendering in the Terminal

**File:** `src/renderer/ascii.py` → class `AsciiMazeRenderer`

The renderer transforms the maze data into colourful text for the terminal.

### How the Grid Becomes Text

Each maze cell is turned into a 3×3 block in the render array:

```
Cell (1,1) without an EAST wall:

  wall    wall    wall         ██ ██ ██
  wall    empty   passage  ➜   ██      
  wall    wall    wall         ██ ██ ██
```

The render array is twice the size of the original grid plus a border:

```
Maze 3×3 → Render array 7×7
```

### Colour Scheme

The renderer uses the **Rich** library for coloured output with RGB colours:

| Element | Default Colour |
|---------|---------------|
| Empty cell | Light grey |
| Wall | Purple |
| Blocked cell | Grey |
| Solution path | Yellow |
| Entry | Pink |
| Exit | Red |

---

## 10. Step 9 — Saving to a File

The result is written to a file (e.g., `maze.txt`) in hexadecimal format.

### File Format

Each cell is written as **one hexadecimal digit** (0–F), encoding the wall state:

```
Example cell with wall value 0b1010 (= 10 = A):
- Bit 0 (NORTH) = 0 → open
- Bit 1 (EAST)  = 1 → closed
- Bit 2 (SOUTH) = 0 → open
- Bit 3 (WEST)  = 1 → closed
```

**Example file:**

```
E8A6C
D159B
...

0,0
19,14
S E E S S E S S ...
```

The last lines contain: entry coordinates, exit coordinates, and the shortest path (directions N/E/S/W).

---

## 11. Full Data Flow Diagram

```
┌─────────────┐
│ config.txt  │  ← User defines parameters
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Config     │  ← pydantic-settings parses and validates
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Maze(w, h)  │  ← Empty grid with all walls closed is created
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Pre-hooks   │  ← "42" pattern, blocked areas
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validation  │  ← Check: entry/exit are valid, graph is connected
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Algorithm      │  ← DFS / Prim / Kruskal / Wilson
│  (removes walls)│     builds a spanning tree
└──────┬──────────┘
       │
       ▼
┌─────────────┐
│ Post-hooks  │  ← Breaking perfection
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ BFS Solver  │  ← Finds the shortest path
└──────┬──────┘
       │
       ├──────────────┐
       ▼              ▼
┌────────────┐  ┌────────────┐
│  Renderer  │  │  Output    │
│  (Rich)    │  │  (hex file)│
└────────────┘  └────────────┘
```

---

## 12. Glossary

| Term | Explanation |
|------|-------------|
| **Cell** | A single "square" of the maze with 4 walls |
| **Grid** | A two-dimensional array of cells |
| **Wall** | A boundary between two adjacent cells |
| **Bitmask** | A number where each bit represents one wall (0 = open, 1 = closed) |
| **Stack** | A "last in, first out" (LIFO) data structure |
| **Queue** | A "first in, first out" (FIFO) data structure |
| **DFS** | Depth-First Search |
| **BFS** | Breadth-First Search |
| **Spanning tree** | A graph that connects all vertices without cycles |
| **Perfect maze** | A maze in which there is exactly one path between any two cells |
| **Union-Find** | A data structure for tracking sets (used in Kruskal's algorithm) |
| **Hook** | A transformer function applied before or after generation |
| **Frontier** | A list of cells on the boundary of the already-built portion of the maze (in Prim's algorithm) |
| **Seed** | An initial value for the random number generator — the same seed produces the same maze |

---

> 💡 **Tip:** To better understand how the algorithm works, try running the program with a small maze (e.g., `WIDTH=5 HEIGHT=5`) and a fixed `SEED`. This way the result is reproducible and easy to trace manually.
