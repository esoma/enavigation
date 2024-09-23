# enavigation
from enavigation import Graph
from enavigation import SimplePathFinder
from enavigation import find_path

# pytest
import pytest

# python
from unittest.mock import MagicMock
from unittest.mock import patch


def test_empty_graph_to_self():
    g = Graph()
    f = SimplePathFinder(g, None, None)
    assert list(f) == []


def test_path_to_self():
    g = Graph()
    g.add_node(None)
    f = SimplePathFinder(g, None, None)
    assert list(f) == [(None,)]


def test_no_path_exists():
    g = Graph()
    g.add_node(1)
    g.add_node(2)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_start_does_not_exist():
    g = Graph()
    g.add_node(2)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_end_does_not_exist():
    g = Graph()
    g.add_node(1)
    f = SimplePathFinder(g, 1, 2)
    assert list(f) == []


def test_one_path():
    g = Graph()
    g.add_edge(-1, 0, 1)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 1)
    f = SimplePathFinder(g, 0, 2)
    assert list(f) == [(0, 1, 2)]


def test_two_paths():
    g = Graph()

    g.add_edge(0, -1, 0.5)
    g.add_edge(0, 1, 1)

    g.add_edge(-1, -2, 1)
    g.add_edge(1, 2, 1)

    g.add_edge(-2, None, 1)
    g.add_edge(2, None, 1)

    f = SimplePathFinder(g, 0, None)
    assert list(f) == [(0, -1, -2, None), (0, 1, 2, None)]


def test_ignore_node():
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


def test_find_path_found():
    path = MagicMock()
    g = MagicMock()
    start = MagicMock()
    end = MagicMock()

    finder = MagicMock()
    finder.__next__.return_value = path

    with patch(
        "enavigation._simplepathfinder.SimplePathFinder", return_value=finder
    ) as SimplePathFinderMock:
        assert find_path(g, start, end) == path
    SimplePathFinderMock.assert_called_once_with(g, start, end)


def test_find_path_not_found():
    g = MagicMock()
    start = MagicMock()
    end = MagicMock()

    finder = MagicMock()
    finder.__next__.side_effect = StopIteration

    with patch(
        "enavigation._simplepathfinder.SimplePathFinder", return_value=finder
    ) as SimplePathFinderMock:
        assert find_path(g, start, end) is None
    SimplePathFinderMock.assert_called_once_with(g, start, end)
