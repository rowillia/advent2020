from day2.day2 import is_line_valid_part1, is_line_valid_part2


def test_is_line_valid_part1() -> None:
    assert is_line_valid_part1("1-3 a: abcde")
    assert not is_line_valid_part1("1-3 b: cdefg")
    assert is_line_valid_part1("2-42 c: ccccccccc")


def test_is_line_valid_part2() -> None:
    assert is_line_valid_part2("1-3 a: abcde")
    assert not is_line_valid_part2("1-3 b: cdefg")
    assert not is_line_valid_part2("2-9 c: ccccccccc")
