import sys
import re
from functools import reduce

from typing import Dict, Iterable, Iterator


def is_valid_height(height_str: str) -> bool:
    if match := re.match(r"(?P<height>\d+)(?P<units>cm|in)", height_str):
        height = int(match["height"])
        if match["units"] == "in":
            return 59 <= height <= 76
        else:
            return 150 <= height <= 193
        return True
    return False


REQUIRED_FIELD = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": is_valid_height,
    "hcl": lambda x: bool(re.match(r"^#[\da-f]{6}$", x)),
    "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda x: bool(re.match(r"^\d{9}$", x)),
}


def passports_from_input(input_lines: Iterable[str]) -> Iterator[Dict[str, str]]:
    current_passport: Dict[str, str] = {}
    for line in input_lines:
        line = line.strip()
        if not line:
            yield current_passport
            current_passport = {}
        current_passport.update(
            {y[0]: y[1] for y in (x.split(":", 1) for x in line.split())}
        )
    if current_passport:
        yield current_passport


def is_passport_valid_part1(passport: Dict[str, str]) -> bool:
    return not bool(REQUIRED_FIELD.keys() - passport.keys())


def is_passport_valid_part2(passport: Dict[str, str]) -> bool:
    for key, validator in REQUIRED_FIELD.items():
        try:
            if not validator(passport[key]):
                return False
        except Exception:
            return False
    return True


if __name__ == "__main__":
    result = reduce(
        lambda x, y: (x[0] + y[0], x[1] + y[1]),
        (
            (is_passport_valid_part1(p), is_passport_valid_part2(p))
            for p in passports_from_input(sys.stdin)
        ),
        (0, 0),
    )
    print(f"part1: {result[0]}, part2: {result[1]}")
