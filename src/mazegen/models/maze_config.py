from dataclasses import dataclass
from typing import Type

from ..interfaces import MazeAlgorithm, MazeHook


@dataclass
class MazeConfig:
    """Configuration parameters for maze generation."""

    width: int
    height: int
    algo: str | Type[MazeAlgorithm] = "dfs"
    entry_point: tuple[int, int] = (0, 0)
    exit_point: tuple[int, int] | None = None
    seed: int | None = None
    hooks: list[MazeHook] | None = None
