import pytest

from hashi_gen.logic import (
    do_bridges_intersect,
    get_intersecting_bridges,
    is_legal_bridge,
    is_legal_island,
)
from hashi_gen.map import Edge, Grid, Island

grid = Grid(5, 5)
i00 = Island(0, 0)
i10 = Island(1, 0)
i01 = Island(0, 1)
i11 = Island(1, 1)
i12 = Island(1, 2)
i21 = Island(2, 1)

grid.add_island(i00)
grid.add_island(i12)
grid.add_island(i21)

b0001 = Edge(i00, i01)
b1011 = Edge(i10, i11)
b0010 = Edge(i00, i10)
b0121 = Edge(i01, i21)
b1012 = Edge(i10, i12)

grid.add_bridge(b0001)
grid.add_bridge(b0010)
grid.add_bridge(b1011)
grid.add_bridge(b0121)
grid.add_bridge(b1012)


@pytest.mark.parametrize(
    ["grid", "i1", "expected_result"],
    [
        (grid, i01, False),
        (grid, i11, False),
        (grid, i21, True),
    ],
)
def test_is_legal_island(grid, i1, expected_result):
    assert is_legal_island(grid, i1) == expected_result


@pytest.mark.parametrize(
    ["b1", "b2", "expected_result"],
    [(b0001, b1011, False), (b0001, b0010, False), (b0121, b1012, True)],
)
def test_do_bridges_intersect(b1, b2, expected_result):
    assert do_bridges_intersect(b1, b2) == expected_result


@pytest.mark.parametrize(
    ["grid", "b1", "expected_bridges"],
    [
        (grid, b0001, []),
        (grid, b0121, [b1012]),
        (grid, b1012, [b0121]),
    ],
)
def test_get_intersecting_bridges(grid, b1, expected_bridges):
    assert (
        get_intersecting_bridges(
            grid,
            b1,
        )
        == expected_bridges
    )


@pytest.mark.parametrize(
    ["grid", "b1", "expected_result"],
    [
        (grid, b0001, True),
        (grid, b1012, False),
    ],
)
def test_is_legal_bridge(grid, b1, expected_result):
    assert is_legal_bridge(grid, b1) == expected_result
