"""Tests for src/models/maze_config.py — MazeConfig dataclass."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.models.maze_config import MazeConfig
from mazegen.interfaces import MazeAlgorithm


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestMazeConfigConstruction:
    def test_basic_construction(self):
        config = MazeConfig(width=10, height=10)
        assert config.width == 10
        assert config.height == 10

    def test_default_algo_is_dfs(self):
        config = MazeConfig(width=10, height=10)
        assert config.algo == "dfs"

    def test_custom_algo_string(self):
        config = MazeConfig(width=10, height=10, algo="prim")
        assert config.algo == "prim"

    def test_default_entry_point(self):
        config = MazeConfig(width=10, height=10)
        assert config.entry_point == (0, 0)

    def test_custom_entry_point(self):
        config = MazeConfig(width=10, height=10, entry_point=(2, 3))
        assert config.entry_point == (2, 3)

    def test_default_exit_point_none(self):
        config = MazeConfig(width=10, height=10)
        assert config.exit_point is None

    def test_custom_exit_point(self):
        config = MazeConfig(width=10, height=10, exit_point=(5, 5))
        assert config.exit_point == (5, 5)

    def test_default_seed_none(self):
        config = MazeConfig(width=10, height=10)
        assert config.seed is None

    def test_custom_seed(self):
        config = MazeConfig(width=10, height=10, seed=42)
        assert config.seed == 42

    def test_default_hooks_none(self):
        config = MazeConfig(width=10, height=10)
        assert config.hooks is None


# ─────────────────────────────────────────────
# 2. Field validation
# ─────────────────────────────────────────────


class TestMazeConfigFields:
    def test_width_required(self):
        with pytest.raises(TypeError):
            MazeConfig(height=10)

    def test_height_required(self):
        with pytest.raises(TypeError):
            MazeConfig(width=10)

    def test_all_required_fields(self):
        config = MazeConfig(
            width=5,
            height=5,
            algo="kruskal",
            entry_point=(0, 0),
            exit_point=(4, 4),
            seed=100,
            hooks=None
        )
        assert config.width == 5
        assert config.height == 5
        assert config.algo == "kruskal"
        assert config.seed == 100


# ─────────────────────────────────────────────
# 3. Supported algorithms
# ─────────────────────────────────────────────


class TestMazeConfigAlgorithms:
    def test_dfs_algorithm(self):
        config = MazeConfig(width=10, height=10, algo="dfs")
        assert config.algo == "dfs"

    def test_prim_algorithm(self):
        config = MazeConfig(width=10, height=10, algo="prim")
        assert config.algo == "prim"

    def test_kruskal_algorithm(self):
        config = MazeConfig(width=10, height=10, algo="kruskal")
        assert config.algo == "kruskal"

    def test_wilson_algorithm(self):
        config = MazeConfig(width=10, height=10, algo="wilson")
        assert config.algo == "wilson"

    def test_custom_algorithm_class(self):
        from mazegen.algo.dfs import DFSMazeGenerator
        config = MazeConfig(width=10, height=10, algo=DFSMazeGenerator)
        assert config.algo == DFSMazeGenerator


# ─────────────────────────────────────────────
# 4. Multiple configurations
# ─────────────────────────────────────────────


class TestMazeConfigMultiple:
    def test_different_sizes(self):
        config1 = MazeConfig(width=5, height=5)
        config2 = MazeConfig(width=10, height=10)
        assert config1.width != config2.width

    def test_different_seeds(self):
        config1 = MazeConfig(width=10, height=10, seed=1)
        config2 = MazeConfig(width=10, height=10, seed=2)
        assert config1.seed != config2.seed

    def test_independent_configs(self):
        config1 = MazeConfig(width=5, height=5, algo="dfs", seed=10)
        config2 = MazeConfig(width=10, height=10, algo="prim", seed=20)
        config1.seed = 99
        assert config2.seed == 20
