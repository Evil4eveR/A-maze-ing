# Generation Algorithms — `src/algo/`

> [← Back to src/](../README.md) · [← Back to Project Root](../../README.md)

This package contains four maze generation algorithms, all implementing the [`MazeAlgorithm`](../README.md#mazealgorithm-abc) abstract base class.

## Overview

| File | Class | Algorithm | Time Complexity |
|---|---|---|---|
| [`dfs.py`](#depth-first-search-dfs) | `DFSMazeGenerator` | Recursive Backtracker (DFS) | O(n) |
| [`prim.py`](#prims-algorithm) | `PrimMazeGenerator` | Randomised Prim's | O(n log n) |
| [`kruskal.py`](#kruskals-algorithm) | `KruskalMazeGenerator` | Randomised Kruskal's | O(n log n) |
| [`wilson.py`](#wilsons-algorithm) | `WilsonMazeGenerator` | Wilson's (Loop-Erased Random Walk) | Variable |

All algorithms produce **perfect mazes** (spanning trees) — exactly one path between any two cells.

---

## Common Interface

Every algorithm inherits from [`MazeAlgorithm`](../README.md#mazealgorithm-abc) and provides:

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `generate(seed)` | `seed: int \| None` | `None` | Generate a complete maze in one call |
| `generate_step(seed)` | `seed: int \| None` | `Generator[Maze]` | Step-by-step generation (yields after each step) |

The `generate_step` method is useful for **animation** or **debugging** — it yields the maze state after each modification.

---

## Depth-First Search (DFS)

**File:** [`dfs.py`](dfs.py) · **Class:** `DFSMazeGenerator` · **Name:** `"dfs"`

### How It Works

1. Start at the entry cell, mark it visited, push onto stack.
2. While the stack is not empty:
   - Look at the top cell on the stack.
   - If it has unvisited neighbours, randomly pick one, remove the wall between them, mark it visited, push it.
   - Otherwise, pop the cell (backtrack).

### Characteristics

- **Bias:** Produces long, winding corridors with few branches
- **Memory:** O(n) stack space in worst case
- **Speed:** Very fast — linear in the number of cells
- **Visual style:** River-like passages, long dead ends

### Usage

```python
from algo.dfs import DFSMazeGenerator
from models.maze import Maze

maze = Maze(width=20, height=15)
algo = DFSMazeGenerator(maze)
algo.generate(seed=42)
```

---

## Prim's Algorithm

**File:** [`prim.py`](prim.py) · **Class:** `PrimMazeGenerator` · **Name:** `"prim"`

### How It Works

1. Start at the entry cell, mark it visited.
2. Add all unvisited neighbours of the start to a frontier list.
3. While the frontier is not empty:
   - Randomly pick a cell from the frontier and remove it.
   - Find its visited neighbours; randomly pick one and remove the wall between them.
   - Mark the cell visited and add its unvisited neighbours to the frontier.

### Characteristics

- **Bias:** Produces shorter corridors with more branching
- **Memory:** O(n) for the frontier list
- **Speed:** Efficient, slightly slower than DFS
- **Visual style:** Radial growth pattern from the start cell

### Usage

```python
from algo.prim import PrimMazeGenerator
from models.maze import Maze

maze = Maze(width=20, height=15)
algo = PrimMazeGenerator(maze)
algo.generate(seed=42)
```

---

## Kruskal's Algorithm

**File:** [`kruskal.py`](kruskal.py) · **Class:** `KruskalMazeGenerator` · **Name:** `"kruskal"`

### How It Works

1. Initialise a Union-Find structure with each non-blocked cell as its own set.
2. Collect all walls (pairs of adjacent cells) and shuffle them randomly.
3. For each wall, if the two cells belong to different sets:
   - Remove the wall between them.
   - Union the two sets.

### Characteristics

- **Bias:** Even distribution — no directional preference
- **Memory:** O(n) for the Union-Find structure
- **Speed:** Efficient with path compression
- **Visual style:** Balanced, no single dominant corridor direction

### Key Implementation Detail

Uses **path compression** in the `find` operation for near-constant-time lookups:

```python
def find(cell: Cell) -> Cell:
    if parent[cell] != cell:
        parent[cell] = find(parent[cell])
    return parent[cell]
```

### Usage

```python
from algo.kruskal import KruskalMazeGenerator
from models.maze import Maze

maze = Maze(width=20, height=15)
algo = KruskalMazeGenerator(maze)
algo.generate(seed=42)
```

---

## Wilson's Algorithm

**File:** [`wilson.py`](wilson.py) · **Class:** `WilsonMazeGenerator` · **Name:** `"wilson"`

### How It Works

1. Mark one random cell as part of the maze (visited).
2. For each unvisited cell:
   - Perform a **random walk** until hitting a visited cell, recording the path.
   - **Erase loops** from the path (only keep the last visit to each cell).
   - Add the loop-erased path to the maze by removing walls along it.

### Characteristics

- **Bias:** **Unbiased** — produces a uniform random spanning tree
- **Memory:** O(n) for the walk path
- **Speed:** Variable — can be slow for large mazes (random walks may take long)
- **Visual style:** Statistically uniform, no visual bias

### Usage

```python
from algo.wilson import WilsonMazeGenerator
from models.maze import Maze

maze = Maze(width=20, height=15)
algo = WilsonMazeGenerator(maze)
algo.generate(seed=42)
```

---

## Algorithm Comparison

| Feature | DFS | Prim | Kruskal | Wilson |
|---|---|---|---|---|
| Bias | Long corridors | Short, branching | Even | None (uniform) |
| Dead ends | Few, long | Many, short | Moderate | Moderate |
| Speed | ⭐⭐⭐ Fast | ⭐⭐ Good | ⭐⭐ Good | ⭐ Variable |
| Animation | Stack-based | Frontier growth | Wall-by-wall | Walk-by-walk |
| Uniformity | No | No | No | Yes |

---

## Related Modules

- **Models** used by algorithms → [models/](../models)
- **Interfaces** defining the contract → [interfaces.py](../README.md#interfacespy)
- **MazeGenerator** facade that selects algorithms → [maze_generator.py](../README.md#maze_generatorpy)
