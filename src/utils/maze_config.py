from typing import Type
from mazegen.interfaces import MazeAlgorithm, MazeHook

from mazegen.hooks.break_perfect import BreakPerfect
from mazegen.hooks.pattern_42 import Add42Pattern

from mazegen.models.maze_config import MazeConfig
from config import settings


def make_maze_config(
    algo: str | Type[MazeAlgorithm] = "prim",
) -> MazeConfig:
    """Build a MazeConfig from application settings with default hooks."""
    hooks: list[MazeHook] = [Add42Pattern()]
    if not settings.perfect:
        hooks.append(BreakPerfect(percent=0.1, seed=settings.seed))
    return MazeConfig(
        width=settings.width,
        height=settings.height,
        entry_point=(0, 0),
        exit_point=(settings.width - 1, settings.height - 1),
        hooks=hooks,
        algo=algo,
        seed=settings.seed
    )
