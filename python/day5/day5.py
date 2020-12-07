import sys
from math import ceil
from dataclasses import dataclass
from typing import Tuple


def partition_left(value_range: Tuple[int, int]) -> Tuple[int, int]:
    return value_range[0], ((value_range[1] - value_range[0]) // 2) + value_range[0]


def partition_right(value_range: Tuple[int, int]) -> Tuple[int, int]:
    return ceil((value_range[1] - value_range[0]) / 2) + value_range[0], value_range[1]


@dataclass
class SeatRange:
    col_range: Tuple[int, int]
    row_range: Tuple[int, int]

    def process_partition(self, partition: str) -> None:
        if partition == "F":
            self.col_range = partition_left(self.col_range)
        elif partition == "B":
            self.col_range = partition_right(self.col_range)
        elif partition == "L":
            self.row_range = partition_left(self.row_range)
        elif partition == "R":
            self.row_range = partition_right(self.row_range)

    def process_assignment(self, assignment: str) -> None:
        for partition in assignment:
            self.process_partition(partition)

    @property
    def seat_id(self) -> int:
        return self.col_range[0] * 8 + self.row_range[0]


def seat_id_from_assignment(assignment: str) -> int:
    seat_range = SeatRange((0, 127), (0, 7))
    seat_range.process_assignment(assignment)
    return seat_range.seat_id


def main() -> None:
    seat_assignments = sorted(seat_id_from_assignment(x.strip()) for x in sys.stdin)
    part1_answer = seat_assignments[-1]
    last_value = seat_assignments[0]
    part2_answer = -1
    for value in seat_assignments[1:]:
        if (value - last_value) > 1:
            part2_answer = value - 1
            break
        last_value = value
    print(f"Part 1: {part1_answer}, Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
