from __future__ import annotations
from collections import defaultdict

import re
import sys
from dataclasses import dataclass
from typing import DefaultDict, Dict, Iterable, Iterator, List, Optional, Set, Tuple

CONTAINER_RE = re.compile(r"(?P<bag_type>.*)\s+bags contain\s+(?P<contained_bags>.*).")
BAGS_RE = re.compile(r"(?P<bag_count>\d+)\s+(?P<bag_type>[^,]*)\s+bags?")


@dataclass
class Bag:
    bag_type: str
    contains: Dict[str, int]

    @staticmethod
    def from_input(line: str) -> Optional[Bag]:
        if match := CONTAINER_RE.match(line):
            return Bag(
                bag_type=match["bag_type"],
                contains={
                    x["bag_type"]: int(x["bag_count"])
                    for x in re.finditer(BAGS_RE, match["contained_bags"])
                },
            )
        return None

    @staticmethod
    def parse_input(lines: Iterable[str]) -> Iterator[Bag]:
        yield from (x for line in lines if (x := Bag.from_input(line)) is not None)


def build_reverse_index(definitions: Iterable[Bag]) -> Dict[str, List[Tuple[int, Bag]]]:
    result: DefaultDict[str, List[Tuple[int, Bag]]] = defaultdict(list)
    for bag in definitions:
        for contained_type, contained_count in bag.contains.items():
            result[contained_type].append((contained_count, bag))
    return result


def part1(definitions: Iterable[Bag], target_type: str) -> int:
    reverse_index = build_reverse_index(definitions)
    done: Set[str] = set()
    to_process = {target_type}
    while to_process:
        next_item = to_process.pop()
        for _, container in reverse_index.get(next_item, set()):
            if container.bag_type not in done:
                to_process.add(container.bag_type)
        done.add(next_item)
    return len(done) - 1


def part2(definitions: Iterable[Bag], target_type: str) -> int:
    done: Dict[str, int] = dict()
    to_process = {target_type}
    bag_index = {x.bag_type: x for x in definitions}
    while to_process:
        next_item = to_process.pop()
        if next_item in done:
            continue
        result_for_item = 0
        deps_met = True
        for bag_type, bag_count in bag_index[next_item].contains.items():
            if bag_type not in done:
                deps_met = False
                to_process.add(bag_type)
            else:
                result_for_item += (1 + done[bag_type]) * bag_count
        if deps_met:
            done[next_item] = result_for_item
        else:
            to_process.add(next_item)
    return done[target_type]


def main() -> None:
    bags = list(Bag.parse_input(sys.stdin))
    print(f'Part 1: {part1(bags, "shiny gold")}')
    print(f'Part 2: {part2(bags, "shiny gold")}')


if __name__ == "__main__":
    main()
