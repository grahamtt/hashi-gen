"""Contains logic for building Hashi puzzles."""

from typing import List

from hashi_gen.map import Edge, Grid, Island


def is_legal_island(grid: Grid, i: Island) -> bool:
    """Check whether the given island can be added to the grid.

    Args:
        grid(Grid): The grid.
        i(Island): The island.

    Returns:
        bool: Whether the given island is legal.
    """
    return (
        grid.get_island(i.x - 1, i.y) is None
        and grid.get_island(i.x + 1, i.y) is None
        and grid.get_island(i.x, i.y - 1) is None
        and grid.get_island(i.x, i.y + 1) is None
    )


def is_legal_bridge(grid: Grid, b: Edge) -> bool:
    """Check whether the given bridge can be added to the grid.

    Args:
        grid(Grid): The grid.
        b(Edge): The bridge.

    Returns:
        bool: Whether the given bridge is legal.
    """
    return not get_intersecting_bridges(grid, b)


def get_intersecting_bridges(grid: Grid, b1: Edge) -> List[Edge]:
    """Get all bridges in the grid that intersect with the given bridge.

    Args:
        grid(Grid): The grid.
        b1(Edge): The island.

    Returns:
        List[Edge]: All the intersecting bridges.
    """
    return [b2 for b2 in grid.get_bridges() if do_bridges_intersect(b1, b2)]


def do_bridges_intersect(b1: Edge, b2: Edge) -> bool:
    """Check whether any two given bridges intersect.

    Args:
        b1(Edge): The first bridge.
        b2(Edge): The second bridge.

    Returns:
        bool: Whether the two bridges intersect.
    """
    b1i1 = b1.islands[0]
    b1i2 = b1.islands[1]
    b2i1 = b2.islands[0]
    b2i2 = b2.islands[1]

    # Check whether bridges are parallel
    if b1i1.x == b1i2.x and b2i1.x == b2i2.x or b1i1.y == b1i2.y and b2i1.y == b2i2.y:
        return False

    if b1i1.x == b1i2.x:
        mx = b1i1.x
        my = b2i1.y
        y1 = min(b1i1.y, b1i2.y)
        y2 = max(b1i1.y, b1i2.y)
        x1 = min(b2i1.x, b2i2.x)
        x2 = max(b2i1.x, b2i2.x)
    else:
        my = b1i1.y
        mx = b2i1.x
        x1 = min(b1i1.x, b1i2.x)
        x2 = max(b1i1.x, b1i2.x)
        y1 = min(b2i1.y, b2i2.y)
        y2 = max(b2i1.y, b2i2.y)

    return x1 < mx < x2 and y1 < my < y2
