from day1.day1 import two_sum


def test_two_sum():
    assert next(two_sum([1, 2, 3], 4)) == (3, 1)
    assert next(two_sum(range(int(1e12)), 4)) == (3, 1)
