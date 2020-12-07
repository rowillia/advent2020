import sys
from typing import Iterable, Iterator, List, Set


def declarations(input_lines: Iterable[str]) -> Iterator[List[Set[str]]]:
    current_declarations: List[Set[str]] = []
    for line in input_lines:
        line = line.strip()
        if not line:
            yield current_declarations
            current_declarations = []
        else:
            current_declarations.append(set(line))
    if current_declarations:
        yield current_declarations


def main() -> None:
    all_declarations = list(declarations(sys.stdin))
    part1_answer = sum(len(set.union(*x)) for x in all_declarations)
    part2_answer = sum(len(set.intersection(*x)) for x in all_declarations)
    print(f"Part 1: {part1_answer}, Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
