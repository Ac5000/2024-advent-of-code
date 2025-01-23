"""Code for day 19 part 2."""

# pylint: disable=logging-fstring-interpolation

import logging
from functools import cache

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)

towels_global: list[str] = []


def get_input(filename: str) -> tuple[list[str], list[str]]:
    """Read the file and yield rules.

    Returns:
        First set is the towels, second set is the designs.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    towels = lines[0]
    designs = lines[2:]
    towels = towels.split(", ")

    logging.debug(towels)
    logging.debug(designs)
    return towels, designs


@cache
def recursive_match(design: str) -> int:
    """Find towels that match the start of the design.

    Recurse with the remainder of the design. If no design string remains, we
    were able to match towels all the way and need to return a count.
    """
    if not design:
        return 1

    final_count = 0
    for towel in towels_global:
        if design.find(towel) == 0:
            final_count += recursive_match(design=design[len(towel) :])

    return final_count


def debug_and_tests():
    """Test using the sample and examples first."""
    global towels_global
    logging.getLogger().setLevel(logging.DEBUG)
    towels_global, designs = get_input("day19example1")
    final_count = 0
    possible_arrangements = 0
    assert recursive_match("brwrr") == 2
    assert recursive_match("bggr") == 1
    assert recursive_match("gbbr") == 4
    assert recursive_match("rrbgbr") == 6
    assert recursive_match("bwurrg") == 1
    assert recursive_match("brgr") == 2
    assert recursive_match("ubwu") == 0
    assert recursive_match("bbrgwb") == 0

    for design in designs:
        temp = recursive_match(design)
        if temp:
            final_count += 1

        possible_arrangements += temp
    assert final_count == 6
    assert possible_arrangements == 16
    logging.critical(f"{final_count} Designs are Possible.")
    logging.critical(f"{possible_arrangements} Arrangements are Possible.")


def main():
    """Get the answer"""
    global towels_global
    logging.getLogger().setLevel(logging.INFO)
    towels_global, designs = get_input("day19input")
    final_count = 0
    possible_arrangements = 0
    for design in designs:
        temp = recursive_match(design)
        if temp:
            final_count += 1

        possible_arrangements += temp
    assert final_count == 247
    logging.critical(f"{final_count} Designs are Possible.")
    logging.critical(f"{possible_arrangements} Arrangements are Possible.")
    assert possible_arrangements == 692596560138745


if __name__ == "__main__":
    debug_and_tests()
    recursive_match.cache_clear()
    print("THE REAL DEAL")
    main()
