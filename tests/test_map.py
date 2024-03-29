import pytest

from hashi_gen.map import Edge, Island


def test_bridge_count():
    i01 = Island(0, 1)
    i21 = Island(2, 1)
    edge = Edge(i01, i21)

    assert edge.bridge_count == 0

    edge.bridge_count += 1

    assert edge.bridge_count == 1

    edge.bridge_count = 2

    assert edge.bridge_count == 2

    with pytest.raises(ValueError):
        edge.bridge_count += 1
