"""Tests for src/models/cell.py — Cell class."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models.cell import Cell
from exceptions import MazeWallError

# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestCellConstruction:
    def test_default_walls_are_all_closed(self):
        cell = Cell(0, 0)
        assert cell.walls == 0b1111

    def test_coordinates_stored(self):
        cell = Cell(3, 7)
        assert cell.x == 3
        assert cell.y == 7

    def test_default_not_visited(self):
        assert Cell(0, 0).visited is False

    def test_default_not_blocked(self):
        assert Cell(0, 0).blocked is False

    def test_custom_walls(self):
        cell = Cell(0, 0, walls=0b0101)
        assert cell.walls == 0b0101

    def test_custom_visited_and_blocked(self):
        cell = Cell(1, 2, visited=True, blocked=True)
        assert cell.visited is True
        assert cell.blocked is True


# ─────────────────────────────────────────────
# 2. has_wall
# ─────────────────────────────────────────────


class TestHasWall:
    def test_all_walls_present_by_default(self):
        cell = Cell(0, 0)
        assert cell.has_wall(Cell.NORTH) is True
        assert cell.has_wall(Cell.EAST) is True
        assert cell.has_wall(Cell.SOUTH) is True
        assert cell.has_wall(Cell.WEST) is True

    def test_no_walls_when_zero(self):
        cell = Cell(0, 0, walls=0)
        assert cell.has_wall(Cell.NORTH) is False
        assert cell.has_wall(Cell.EAST) is False
        assert cell.has_wall(Cell.SOUTH) is False
        assert cell.has_wall(Cell.WEST) is False

    def test_only_north_wall(self):
        cell = Cell(0, 0, walls=Cell.NORTH)
        assert cell.has_wall(Cell.NORTH) is True
        assert cell.has_wall(Cell.EAST) is False
        assert cell.has_wall(Cell.SOUTH) is False
        assert cell.has_wall(Cell.WEST) is False

    def test_invalid_direction_raises(self):
        cell = Cell(0, 0)
        with pytest.raises(MazeWallError):
            cell.has_wall(16)  # 0b10000 — 5 bits, out of range

    def test_combined_bits(self):
        # walls = NORTH | WEST = 0b1001 = 9
        cell = Cell(0, 0, walls=Cell.NORTH | Cell.WEST)
        assert cell.has_wall(Cell.NORTH) is True
        assert cell.has_wall(Cell.WEST) is True
        assert cell.has_wall(Cell.EAST) is False
        assert cell.has_wall(Cell.SOUTH) is False


# ─────────────────────────────────────────────
# 3. remove_wall
# ─────────────────────────────────────────────


class TestRemoveWall:
    def test_remove_existing_wall(self):
        cell = Cell(0, 0)
        cell.remove_wall(Cell.NORTH)
        assert cell.has_wall(Cell.NORTH) is False

    def test_remove_wall_leaves_others_intact(self):
        cell = Cell(0, 0)
        cell.remove_wall(Cell.EAST)
        assert cell.has_wall(Cell.NORTH) is True
        assert cell.has_wall(Cell.SOUTH) is True
        assert cell.has_wall(Cell.WEST) is True

    def test_remove_already_open_wall_is_noop(self):
        cell = Cell(0, 0, walls=0b0000)
        cell.remove_wall(Cell.NORTH)  # should not crash
        assert cell.walls == 0

    def test_remove_all_walls_one_by_one(self):
        cell = Cell(0, 0)
        for direction in [Cell.NORTH, Cell.EAST, Cell.SOUTH, Cell.WEST]:
            cell.remove_wall(direction)
        assert cell.walls == 0


# ─────────────────────────────────────────────
# 4. remove_walls_between
# ─────────────────────────────────────────────


class TestRemoveWallsBetween:
    """
    IMPORTANT — coordinate system:
      x = row (vertical).  dx == 1 means 'one row below' → SOUTH/NORTH pair.
      y = col (horizontal). dy == 1 means 'one col right'  → EAST/WEST pair.
    """

    def test_south_north_pair_when_dx_is_1(self):
        # cell_a is one row ABOVE cell_b  (cell_b.x = cell_a.x + 1)
        cell_a = Cell(0, 0)
        cell_b = Cell(1, 0)
        cell_a.remove_walls_between(cell_b)
        assert cell_a.has_wall(Cell.SOUTH) is False
        assert cell_b.has_wall(Cell.NORTH) is False
        # other walls untouched
        assert cell_a.has_wall(Cell.NORTH) is True
        assert cell_b.has_wall(Cell.SOUTH) is True

    def test_north_south_pair_when_dx_is_minus1(self):
        cell_a = Cell(1, 0)
        cell_b = Cell(0, 0)
        cell_a.remove_walls_between(cell_b)
        assert cell_a.has_wall(Cell.NORTH) is False
        assert cell_b.has_wall(Cell.SOUTH) is False

    def test_east_west_pair_when_dy_is_1(self):
        # cell_a is one col to the LEFT of cell_b
        cell_a = Cell(0, 0)
        cell_b = Cell(0, 1)
        cell_a.remove_walls_between(cell_b)
        assert cell_a.has_wall(Cell.EAST) is False
        assert cell_b.has_wall(Cell.WEST) is False

    def test_west_east_pair_when_dy_is_minus1(self):
        cell_a = Cell(0, 1)
        cell_b = Cell(0, 0)
        cell_a.remove_walls_between(cell_b)
        assert cell_a.has_wall(Cell.WEST) is False
        assert cell_b.has_wall(Cell.EAST) is False

    def test_blocked_cell_prevents_wall_removal(self):
        cell_a = Cell(0, 0, blocked=True)
        cell_b = Cell(1, 0)
        cell_a.remove_walls_between(cell_b)
        # no walls should have been removed
        assert cell_a.walls == 0b1111
        assert cell_b.walls == 0b1111

    def test_blocked_other_prevents_wall_removal(self):
        cell_a = Cell(0, 0)
        cell_b = Cell(1, 0, blocked=True)
        cell_a.remove_walls_between(cell_b)
        assert cell_a.walls == 0b1111
        assert cell_b.walls == 0b1111

    def test_force_bypasses_blocked(self):
        cell_a = Cell(0, 0, blocked=True)
        cell_b = Cell(1, 0)
        cell_a.remove_walls_between(cell_b, force=True)
        assert cell_a.has_wall(Cell.SOUTH) is False
        assert cell_b.has_wall(Cell.NORTH) is False

    def test_non_adjacent_raises(self):
        cell_a = Cell(0, 0)
        cell_b = Cell(2, 0)  # two rows away — not adjacent
        with pytest.raises(MazeWallError):
            cell_a.remove_walls_between(cell_b)

    def test_diagonal_raises(self):
        cell_a = Cell(0, 0)
        cell_b = Cell(1, 1)  # diagonal — both dx and dy are 1
        with pytest.raises(MazeWallError):
            cell_a.remove_walls_between(cell_b)

    def test_same_cell_raises(self):
        cell_a = Cell(0, 0)
        cell_b = Cell(0, 0)
        with pytest.raises(MazeWallError):
            cell_a.remove_walls_between(cell_b)

    def test_symmetry_is_maintained(self):
        """After removing walls, neighbor consistency holds."""
        cell_a = Cell(0, 0)
        cell_b = Cell(0, 1)
        cell_a.remove_walls_between(cell_b)
        # cell_a lost EAST, cell_b lost WEST — they agree on the shared wall
        assert cell_a.has_wall(Cell.EAST) == cell_b.has_wall(Cell.WEST)


# ─────────────────────────────────────────────
# 5. Equality and hashing
# ─────────────────────────────────────────────


class TestEqualityAndHash:
    def test_equal_cells_same_coordinates(self):
        assert Cell(2, 3) == Cell(2, 3)

    def test_unequal_cells_different_x(self):
        assert Cell(1, 3) != Cell(2, 3)

    def test_unequal_cells_different_y(self):
        assert Cell(2, 3) != Cell(2, 4)

    def test_walls_do_not_affect_equality(self):
        # Two cells at the same position are equal regardless of wall state
        assert Cell(1, 1, walls=0) == Cell(1, 1, walls=0b1111)

    def test_comparing_non_cell_raises_type_error(self):
        with pytest.raises(TypeError):
            Cell(0, 0) == "not a cell"

    def test_cells_usable_as_dict_keys(self):
        d = {Cell(0, 0): "start", Cell(1, 1): "mid"}
        assert d[Cell(0, 0)] == "start"

    def test_cells_usable_in_sets(self):
        s = {Cell(0, 0), Cell(1, 1), Cell(0, 0)}
        assert len(s) == 2

    def test_hash_consistency(self):
        c = Cell(3, 4)
        assert hash(c) == hash(Cell(3, 4))


# ─────────────────────────────────────────────
# 6. Class constants sanity
# ─────────────────────────────────────────────


class TestConstants:
    def test_all_four_directions_are_distinct_bits(self):
        directions = [Cell.NORTH, Cell.EAST, Cell.SOUTH, Cell.WEST]
        # Each must be a unique power of 2
        assert len(set(directions)) == 4
        for d in directions:
            assert d & (d - 1) == 0, f"{d} is not a power of 2"

    def test_all_walls_combined_equals_15(self):
        assert Cell.NORTH | Cell.EAST | Cell.SOUTH | Cell.WEST == 0b1111

    def test_bit_positions(self):
        assert Cell.NORTH == 0b0001  # bit 0
        assert Cell.EAST == 0b0010  # bit 1
        assert Cell.SOUTH == 0b0100  # bit 2
        assert Cell.WEST == 0b1000  # bit 3
