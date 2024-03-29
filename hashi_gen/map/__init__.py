"""Contains classes and utilities for dealing with the game board."""

from typing import List, Optional


class Island:
    """Represents an island in the game."""

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        """Public getter for `x`."""
        return self._x

    @property
    def y(self):
        """Public getter for `y`."""
        return self._y


class Edge:
    """Represents a bridge in the game.

    Args:
        i1 (Island): First island
        i2 (Island): Second island
    """

    def __init__(self, i1: Island, i2: Island):
        self._i1 = i1
        self._i2 = i2
        self._bridge_count = 0

    @property
    def islands(self):
        """Gets a list of the islands."""
        return [self._i1, self._i2]

    @property
    def bridge_count(self):
        """Gets the current count of bridges."""
        return self._bridge_count

    @bridge_count.setter
    def bridge_count(self, val):
        """Increment bridge count."""
        if val > 2:  # TODO: This should be configurable
            raise ValueError("Bridge count cannot exceed 2")

        self._bridge_count = val


class Grid:
    """Represents a grid of all potential island locations.

    Args:
        width (int): the width of the grid
        height (int): the height of the grid
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        self._grid: List[List[Optional[Island]]] = [
            [None for _ in range(0, height)] for _ in range(0, width)
        ]
        self._bridges = set()

    def get_island(self, x: int, y: int) -> Optional[Island]:
        """Public getter for a grid location."""
        return self._grid[y][x]

    def add_island(self, i: Island):
        """Add an island to the grid."""
        self._grid[i.y][i.x] = i

    def add_bridge(self, b: Edge):
        """Add a bridge to the grid."""
        self._bridges.add(b)

    def get_bridges(self):
        """Get all bridges in the grid."""
        return self._bridges
