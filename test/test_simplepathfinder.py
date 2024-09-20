# enavigation
from enavigation import Graph
from enavigation import SimplePathFinder

# pytest
import pytest


def test_empty_graph_to_self() -> None:
    g = Graph()
    f = SimplePathFinder(g, None, None)
    assert list(f) == []


def test_path_to_self() -> None:
    g = Graph()
    g.add_node(None)
    f = SimplePathFinder(g, None, None)
    assert list(f) == [(None,)]


def test_no_path_exists() -> None:
    g = Graph()
    g.add_node(1)
    g.add_node(2)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_start_does_not_exist() -> None:
    g = Graph()
    g.add_node(2)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_end_does_not_exist() -> None:
    g = Graph()
    g.add_node(1)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_one_path() -> None:
    g = Graph()
    g.add_edge(-1, 0, 1)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 1)
    f = SimplePathFinder(g, 0, 2)
    assert list(f) == [(0, 1, 2)]


def test_two_paths() -> None:
    g = Graph()

    g.add_edge(0, -1, 0.5)
    g.add_edge(0, 1, 1)

    g.add_edge(-1, -2, 1)
    g.add_edge(1, 2, 1)

    g.add_edge(-2, None, 1)
    g.add_edge(2, None, 1)

    f = SimplePathFinder(g, 0, None)
    assert list(f) == [(0, -1, -2, None), (0, 1, 2, None)]


def test_ignore_node() -> None:
    g = Graph()

    g.add_edge(0, 1, 1)
    g.add_edge(1, "a", 1)
    g.add_edge(1, "b", 1)
    g.add_edge("a", None, 0.5)
    g.add_edge("b", None, 1)

    f = SimplePathFinder(g, 0, None)
    assert next(f) == (0, 1, "a", None)
    f.ignore_node(1)
    with pytest.raises(StopIteration):
        next(f)
