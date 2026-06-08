from rich import print
from maze_generator import MazeGenerator

from config import settings

from algo.hooks import Add42Pattern, BreakPerfect
from models.cell import Cell
from models.maze import Maze
from renderer.ascii import AsciiMazeRenderer
from utils.renderer import get_walls_between

from solver.bfs import BFSMazeSolver



width, height = 20, 10

maze = MazeGenerator.create(
    width=width,
    height=height,
    hooks=[
        BreakPerfect(percent=0.2, seed=42),
        Add42Pattern(),
    ],
    seed=420
)

colors = [
    (200, 200, 200),  # cell
    (120, 50, 150),   # wall
    (100, 100, 100),  # blocked wall
    (255, 255, 0),    # path
]

# maze.open_entry_exit()

path = BFSMazeSolver(maze).solve()
# path = None

renderer = AsciiMazeRenderer(maze, path=path, colors=colors)

renderer.render()
renderer.display()


# m = [[1] * (width * 2 + 1) for _ in range(height * 2 + 1)]


# def get_blocked_neighbors(cell: Cell, maze: Maze):
#     neighbors = []
#     if cell.y > 0 and maze.get_cell(cell.x, cell.y - 1).blocked:
#         neighbors.append(maze.get_cell(cell.x, cell.y - 1))

#     if cell.x < maze.width - 1 and maze.get_cell(cell.x + 1, cell.y).blocked:
#         neighbors.append(maze.get_cell(cell.x + 1, cell.y))

#     if cell.y < maze.height - 1 and maze.get_cell(cell.x, cell.y + 1).blocked:
#         neighbors.append(maze.get_cell(cell.x, cell.y + 1))

#     if cell.x > 0 and maze.get_cell(cell.x - 1, cell.y).blocked:
#         neighbors.append(maze.get_cell(cell.x - 1, cell.y))

#     return neighbors


# for y in range(1, height * 2, 2):
#     for i in range(1, len(m[y]) - 1, 2):
#         cell = maze.get_cell(i // 2, y // 2)

#         if cell.blocked:
#             m[y][i] = 2
#             if i + 2 < width * 2 + 1:
#                 right = maze.get_cell((i + 2) // 2, y // 2)
#                 if right and right.blocked:
#                     m[y][i + 1] = 2
#             if y + 2 < height * 2 + 1:
#                 below = maze.get_cell(i // 2, (y + 2) // 2)
#                 if below and below.blocked:
#                     m[y + 1][i] = 2
#             continue
#         m[y][i] = 0

#         for wall in [cell.WEST, cell.SOUTH, cell.EAST, cell.NORTH]:
#             if not cell.has_wall(wall):
#                 if wall == cell.WEST:
#                     m[y - 1][i] = 0
#                 elif wall == cell.SOUTH:
#                     m[y][i + 1] = 0
#                 elif wall == cell.EAST:
#                     m[y + 1][i] = 0
#                 elif wall == cell.NORTH:
#                     m[y][i - 1] = 0

# RED   = "[rgb(120,50,150)]{}[/rgb(120,50,150)]"
# GRAY  = "[rgb(100,100,100)]{}[/rgb(100,100,100)]"

# s = ""
# for row in m:
#     for cell in row:
#         if cell == 1:
#             s += RED.format(settings.wall)
#         elif cell == 0:
#             s += settings.cell
#         elif cell == 2:
#             s += GRAY.format(settings.wall)
#     s += "\n"

# blocked = [(c.x, c.y) for row in maze.grid for c in row if c.blocked]
# print(f"Blocked: {len(blocked)}", blocked)
# print(s)

# print(f"[green]Hi[/green]")