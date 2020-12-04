from typing import List, Tuple
import pytest

from day3.day3 import parse_tree_line, parse_tree_map, count_trees_hit


def test_parse_tree_line() -> None:
    assert parse_tree_line(".##..") == [False, True, True, False, False]


def test_parse_tree_map() -> None:
    assert parse_tree_map([".#", "#."]) == [[False, True], [True, False]]


@pytest.mark.parametrize(
    "tree_map,slope,expected_output",
    [([".#", "#."], (1, 1), 0), ([".#", "#.", "##", "##"], (1, 1), 2)],
)
def test_count_trees_hit(
    tree_map: List[str], slope: Tuple[int, int], expected_output: int
) -> None:
    assert count_trees_hit(parse_tree_map(tree_map), slope) == expected_output
