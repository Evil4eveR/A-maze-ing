from typing import Generator

from collections import deque
from random import randint

from mazegen.interfaces import MazeAlgorithm

from .algo.dfs import DFSMazeGenerator
from .algo.kruskal import KruskalMazeGenerator

from .algo.prim import PrimMazeGenerator
from .algo.wilson import WilsonMazeGenerator

from .exceptions import (
    InvalidEntryExitError,
    MazeError,
    MazeSizeError
)

from .models.maze import Maze
from .models.maze_config import MazeConfig


class MazeGenerator:
    ALGO_MAP = {
        'dfs': DFSMazeGenerator,
        'prim': PrimMazeGenerator,
        'kruskal': KruskalMazeGenerator,
        'wilson': WilsonMazeGenerator,
    }

    @classmethod
    def create(cls, config: MazeConfig) -> Maze:
        for maze in cls._build(config):
            pass
        return maze

    @classmethod
    def create_animated(
        cls,
        config: MazeConfig
    ) -> Generator[Maze, None, None]:
        yield from cls._build(config, animated=True)

    @classmethod
    def _build(
        cls,
        cfg: MazeConfig,
        animated: bool = False
    ) -> Generator[Maze, None, None]:
        maze = Maze(
            width=cfg.width,
            height=cfg.height,
            entry_point=cfg.entry_point,
            exit_point=cfg.exit_point or (cfg.width - 1, cfg.height - 1)
        )

        if cfg.seed is None:
            cfg.seed = randint(1, 100000000000000)

        pre_hooks = [hook for hook in cfg.hooks or [] if hook.stage == "pre"]
        post_hooks = [hook for hook in cfg.hooks or [] if hook.stage == "post"]

        algo_class: type[MazeAlgorithm] | None = None
        if isinstance(cfg.algo, str):
            algo_class = cls.ALGO_MAP.get(cfg.algo)
        else:
            algo_class = cfg.algo

        if algo_class is None:
            raise MazeError(f"Unsupported algorithm: {cfg.algo}")

        for hook in pre_hooks or []:
            maze = hook(maze)

        cls._validate(maze)

        algorithm = algo_class(maze=maze)
        if animated:
            yield from algorithm.generate_step(seed=cfg.seed)
        else:
            algorithm.generate(seed=cfg.seed)
            yield maze

        maze.seed = cfg.seed
        maze.algo = algo_class.name

        for hook in post_hooks or []:
            maze = hook(maze)

        cls._valid_entry_exit(maze)

        return maze

    @staticmethod
    def _valid_entry_exit(maze: Maze) -> None:
        if not (maze.entry and maze.exit):
            raise InvalidEntryExitError(
                "Entry and exit points must be defined."
            )
        if maze.entry.blocked or maze.exit.blocked:
            raise InvalidEntryExitError(
                "Entry and exit points cannot be blocked."
            )
        if maze.entry == maze.exit:
            raise InvalidEntryExitError(
                "Entry and exit points cannot be the same."
            )

    @staticmethod
    def _is_connected(maze: Maze) -> bool:
        start = maze.entry
        if start.blocked:
            return False

        visited = set()
        queue = deque([start])
        visited.add((start.x, start.y))

        while queue:
            cell = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = maze.get_cell(cell.x + dx, cell.y + dy)
                if neighbor and not neighbor.blocked:
                    pos = (neighbor.x, neighbor.y)
                    if pos not in visited:
                        visited.add(pos)
                        queue.append(neighbor)

        total_free = sum(
            1 for row in maze.grid
            for cell in row
            if not cell.blocked
        )
        return len(visited) == total_free

    @classmethod
    def _validate(cls, maze: Maze) -> None:
        cls._valid_entry_exit(maze)
        if not cls._is_connected(maze):
            raise MazeSizeError("Blocked areas disconnect the maze.")
