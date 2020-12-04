import math
import sys
from typing import Iterable, List, Tuple


def parse_tree_line(tree_line: str) -> List[bool]:
    return [x == "#" for x in tree_line]


def parse_tree_map(tree_map_input: Iterable[str]) -> List[List[bool]]:
    return [parse_tree_line(x.strip()) for x in tree_map_input]


def count_trees_hit(tree_map: List[List[bool]], slope: Tuple[int, int]) -> int:
    current_location = (0, 0)
    trees_hit = 0
    height = len(tree_map)
    width = len(tree_map[0])
    while current_location[0] < height:
        if tree_map[current_location[0]][current_location[1]]:
            trees_hit += 1
        current_location = (
            (current_location[0] + slope[0]),
            (current_location[1] + slope[1]) % width,
        )
    return trees_hit


def main() -> None:
    tree_map = parse_tree_map(sys.stdin)
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    part1_answer = count_trees_hit(tree_map, (3, 1))
    part2_answer = math.prod(count_trees_hit(tree_map, slope) for slope in slopes)
    print(f"Part 1: {part1_answer}, Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
