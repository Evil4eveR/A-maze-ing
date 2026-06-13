"""Tests for src/exceptions.py — Custom exception classes."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mazegen.exceptions import (
    MazeError,
    InvalidEntryExitError,
    MazeSizeError,
    MazeWallError,
)


class TestMazeError:
    def test_maze_error_is_exception(self):
        assert issubclass(MazeError, Exception)

    def test_maze_error_instantiation(self):
        error = MazeError("Test error")
        assert str(error) == "Test error"

    def test_maze_error_can_be_raised(self):
        with pytest.raises(MazeError):
            raise MazeError("Test")


class TestInvalidEntryExitError:
    def test_invalid_entry_exit_error_is_maze_error(self):
        assert issubclass(InvalidEntryExitError, MazeError)

    def test_invalid_entry_exit_error_instantiation(self):
        error = InvalidEntryExitError("Invalid entry/exit")
        assert str(error) == "Invalid entry/exit"

    def test_invalid_entry_exit_error_can_be_raised(self):
        with pytest.raises(InvalidEntryExitError):
            raise InvalidEntryExitError("Bad entry")

    def test_invalid_entry_exit_error_caught_as_maze_error(self):
        with pytest.raises(MazeError):
            raise InvalidEntryExitError("Test")


class TestMazeSizeError:
    def test_maze_size_error_is_maze_error(self):
        assert issubclass(MazeSizeError, MazeError)

    def test_maze_size_error_instantiation(self):
        error = MazeSizeError("Invalid size")
        assert str(error) == "Invalid size"

    def test_maze_size_error_can_be_raised(self):
        with pytest.raises(MazeSizeError):
            raise MazeSizeError("Size too small")

    def test_maze_size_error_caught_as_maze_error(self):
        with pytest.raises(MazeError):
            raise MazeSizeError("Test")


class TestMazeWallError:
    def test_maze_wall_error_is_maze_error(self):
        assert issubclass(MazeWallError, MazeError)

    def test_maze_wall_error_instantiation(self):
        error = MazeWallError("Invalid wall")
        assert str(error) == "Invalid wall"

    def test_maze_wall_error_can_be_raised(self):
        with pytest.raises(MazeWallError):
            raise MazeWallError("Wall conflict")

    def test_maze_wall_error_caught_as_maze_error(self):
        with pytest.raises(MazeError):
            raise MazeWallError("Test")


class TestExceptionHierarchy:
    def test_all_maze_errors_inherit_from_exception(self):
        errors = [MazeError, InvalidEntryExitError, MazeSizeError, MazeWallError]
        for error_class in errors:
            assert issubclass(error_class, Exception)

    def test_all_specific_errors_inherit_from_maze_error(self):
        specific_errors = [InvalidEntryExitError, MazeSizeError, MazeWallError]
        for error_class in specific_errors:
            assert issubclass(error_class, MazeError)
