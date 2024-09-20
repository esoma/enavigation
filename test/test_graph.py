# enavigation
from enavigation import Graph

# pytest
import pytest

# python
from copy import copy


def test_defaults() -> None:
    g = Graph()
    assert list(g.nodes) == []
    assert list(g.edges) == []


def test_add_unhashable_node() -> None:
    g = Graph()
    with pytest.raises(TypeError):
        g.add_node([1])


def test_node() -> None:
    g = Graph()

    assert not g.contains_node(None)

    g.add_node(None)
    assert list(g.nodes) == [None]
    assert list(g.edges) == []
    assert list(g.get_node_edges(None)) == []

    assert g.contains_node(None)

    g.add_node(None)
    assert list(g.nodes) == [None]
    assert list(g.edges) == []
    assert list(g.get_node_edges(None)) == []

    g.add_node(1)
    assert set(g.nodes) == {None, 1}
    assert list(g.edges) == []
    assert list(g.get_node_edges(None)) == []
    assert list(g.get_node_edges(1)) == []

    g.remove_node(None)
    assert set(g.nodes) == {1}
    assert list(g.edges) == []
    assert list(g.get_node_edges(None)) == []
    assert list(g.get_node_edges(1)) == []

    assert not g.contains_node(None)

    g.remove_node(None)
    assert set(g.nodes) == {1}
    assert list(g.edges) == []
    assert list(g.get_node_edges(None)) == []
    assert list(g.get_node_edges(1)) == []


def test_edge() -> None:
    g = Graph()

    assert not g.contains_edge(1, 2)

    g.add_edge(1, 2, 0.5)
    assert set(g.nodes) == {1, 2}
    assert set(g.edges) == {(1, 2, 0.5)}
    assert list(g.get_node_edges(1)) == [(2, 0.5)]
    assert list(g.get_node_edges(2)) == [(1, 0.5)]

    assert g.contains_edge(1, 2)
    assert g.contains_edge(2, 1)

    g.add_edge(1, 2, 0.8)
    assert set(g.nodes) == {1, 2}
    assert set(g.edges) == {(1, 2, 0.8)}
    assert list(g.get_node_edges(1)) == [(2, 0.8)]
    assert list(g.get_node_edges(2)) == [(1, 0.8)]

    g.add_edge(1, 3, 0.2)
    assert set(g.nodes) == {1, 2, 3}
    assert set(g.edges) == {(1, 2, 0.8), (1, 3, 0.2)}
    assert list(g.get_node_edges(1)) == [(2, 0.8), (3, 0.2)]
    assert list(g.get_node_edges(2)) == [(1, 0.8)]
    assert list(g.get_node_edges(3)) == [(1, 0.2)]

    g.remove_node(2)
    assert set(g.nodes) == {1, 3}
    assert set(g.edges) == {(1, 3, 0.2)}
    assert list(g.get_node_edges(1)) == [(3, 0.2)]
    assert list(g.get_node_edges(2)) == []
    assert list(g.get_node_edges(3)) == [(1, 0.2)]

    g.remove_edge(3, 1)
    assert set(g.nodes) == {1, 3}
    assert list(g.edges) == []
    assert list(g.get_node_edges(1)) == []
    assert list(g.get_node_edges(2)) == []
    assert list(g.get_node_edges(3)) == []

    assert not g.contains_edge(3, 1)

    g.remove_edge(3, 1)
    assert set(g.nodes) == {1, 3}
    assert list(g.edges) == []
    assert list(g.get_node_edges(1)) == []
    assert list(g.get_node_edges(2)) == []
    assert list(g.get_node_edges(3)) == []


def test_get_node_edges_does_not_exist() -> None:
    g = Graph()
    assert list(g.get_node_edges(0)) == []


def test_connected_components() -> None:
    g = Graph()

    g.add_edge(0, 1, 0)
    g.add_edge(1, 2, 0)
    g.add_edge(2, 3, 0)
    g.add_edge(3, 0, 0)

    g.add_edge(10, 11, 0)
    g.add_edge(11, 12, 0)
    g.add_edge(12, 13, 0)
    g.add_edge(13, 10, 0)

    g.add_edge(20, 21, 0)
    g.add_edge(21, 22, 0)
    g.add_edge(22, 0, 0)

    islands = [set(i) for i in g.get_connected_components()]
    assert len(islands) == 2
    assert {0, 1, 2, 3, 20, 21, 22} in islands
    assert {10, 11, 12, 13} in islands


def test_copy() -> None:
    g = Graph()

    empty_copy = copy(g)
    assert list(g.nodes) == []
    assert list(g.edges) == []

    g.add_node(1)
    assert set(g.nodes) == {1}
    assert list(g.edges) == []
    assert list(empty_copy.nodes) == []
    assert list(empty_copy.edges) == []

    g.add_edge(1, 2, 1)
    assert set(g.nodes) == {1, 2}
    assert set(g.edges) == {(1, 2, 1)}
    assert list(empty_copy.nodes) == []
    assert list(empty_copy.edges) == []

    non_empty_copy = copy(g)
    assert set(g.nodes) == {1, 2}
    assert set(g.edges) == {(1, 2, 1)}
    assert list(empty_copy.nodes) == []
    assert list(empty_copy.edges) == []
    assert set(non_empty_copy.nodes) == {1, 2}
    assert set(non_empty_copy.edges) == {(1, 2, 1)}

    g.remove_edge(1, 2)
    assert set(g.nodes) == {1, 2}
    assert list(g.edges) == []
    assert list(empty_copy.nodes) == []
    assert list(empty_copy.edges) == []
    assert set(non_empty_copy.nodes) == {1, 2}
    assert set(non_empty_copy.edges) == {(1, 2, 1)}

    g.remove_node(1)
    assert set(g.nodes) == {2}
    assert list(g.edges) == []
    assert list(empty_copy.nodes) == []
    assert list(empty_copy.edges) == []
    assert set(non_empty_copy.nodes) == {1, 2}
    assert set(non_empty_copy.edges) == {(1, 2, 1)}
