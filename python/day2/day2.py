import re
import sys
from collections import Counter
from functools import reduce
from typing import Optional, Tuple

PASSWORD_LINE_RE = re.compile(
    r"(?P<first>\d+)\-(?P<second>\d+)\s+(?P<letter>\w):\s+(?P<password>\w+)"
)


def parse_line(line: str) -> Optional[Tuple[int, int, str, str]]:
    if match := PASSWORD_LINE_RE.match(line):
        return (
            int(match["first"]),
            int(match["second"]),
            match["letter"],
            match["password"],
        )
    return None


def is_line_valid_part1(line: str) -> bool:
    if match := parse_line(line):
        min, max, letter, password = match
        return min <= Counter(password).get(letter, 0) <= max
    return False


def is_line_valid_part2(line: str) -> bool:
    if match := parse_line(line):
        min, max, letter, password = match
        return (password[min - 1 : min] == letter) ^ (password[max - 1 : max] == letter)
    return False


def main() -> None:
    print(
        reduce(
            lambda x, y: (x[0] + y[0], x[1] + y[1]),
            (
                (is_line_valid_part1(line), is_line_valid_part2(line))
                for line in sys.stdin
            ),
            (0, 0),
        )
    )


if __name__ == "__main__":
    main()
