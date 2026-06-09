import time

from rich import print
from maze_generator import MazeGenerator

from config import settings

from models.cell import Cell

from models.maze import Maze
from renderer.ascii import AsciiMazeRenderer

from solver.bfs import BFSMazeSolver
from hooks import BreakPerfect, Add42Pattern

from models.maze_config import MazeConfig

from rich.live import Live


cfg = MazeConfig(
    width=20,
    height=10,
    entry_point=(19, 9),
    exit_point=(1, 1),
    hooks=[
        Add42Pattern(),
        # BreakPerfect(percent=0.1, seed=420)
    ],
    algo="prim",
)

maze = MazeGenerator.create(config=cfg)

colors = [
    (200, 200, 200),  # cell
    (37, 150, 190),   # wall
    (200, 200, 200),  # blocked wall
    (255, 255, 0),    # path
]

# path = BFSMazeSolver(maze).solve()

renderer = AsciiMazeRenderer(maze, path=None, colors=colors)

with Live(refresh_per_second=5) as live:
    for maze in MazeGenerator.create_animated(config=cfg):
        renderer = AsciiMazeRenderer(maze, path=None, colors=colors)
        live.update(renderer.render())
        time.sleep(0.05)

# renderer.render()
# renderer.display()
