from day1.day1 import two_sum
from day1.day1 import three_sum


def test_two_sum() -> None:
    assert next(two_sum([1, 2, 3], 4)) == (3, 1)
    assert next(two_sum(range(int(1e12)), 4)) == (3, 1)


def test_three_sum() -> None:
    assert next(three_sum([1, 2, 3], 4), None) == None
    assert next(three_sum([0, 3], 6), None) == None
    assert next(three_sum([1, 2, 3], 6), None) == (3, 2, 1)
