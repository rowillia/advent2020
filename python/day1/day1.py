import math
import sys
from typing import Iterable
from typing import Iterator
from typing import Tuple


def two_sum(values: Iterable[int], target: int) -> Iterator[Tuple[int, int]]:
    values_as_set = set()
    for value in values:
        if target - value in values_as_set:
            yield value, target - value
        else:
            values_as_set.add(value)


def three_sum(values: Iterable[int], target: int) -> Iterator[Tuple[int, int, int]]:
    for i, value in enumerate(values):
        yield from (
            x + (value,)
            for x in two_sum(
                ((y for j, y in enumerate(values) if j != i)), target - value
            )
        )


def main() -> None:
    stdin_as_ints = [int(line.strip()) for line in sys.stdin]
    print(math.prod(next(three_sum(stdin_as_ints, 2020))))


if __name__ == "__main__":
    main()
