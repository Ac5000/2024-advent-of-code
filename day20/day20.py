"""Code for day 20."""

# pylint: disable=logging-fstring-interpolation

import logging
from collections import namedtuple
from enum import Enum

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)

Coord = namedtuple("Coord", ["x", "y"])


class Direction(tuple, Enum):
    """Directions that can be faced."""

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def get_input(filename: str) -> tuple[Coord, Coord, set[Coord]]:
    """Read the file and parse.

    Returns:
        Tuple of Start Coordinate, End Coordinate, and a set of the other
        coordinates.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    start = None
    end = None
    coords: set[Coord] = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case ".":
                    coords.add(Coord(x, y))
                case "S":
                    start = Coord(x, y)
                case "E":
                    end = Coord(x, y)
                case _:
                    pass
    # Check we got stuff.
    assert start
    assert end
    assert coords
    return start, end, coords


def get_next_coord(
    coord: Coord, coord_set: set[Coord], coord_dict: dict[Coord, int]
) -> Coord:
    """Return next position to the given coordinate."""
    for direction in Direction:
        new_coord = Coord(
            direction.value[0] + coord.x,
            direction.value[1] + coord.y,
        )
        if new_coord in coord_set and new_coord not in coord_dict:
            return new_coord
    raise RuntimeError("Didn't find next coordinate")


def coords_to_dict(
    start: Coord, end: Coord, coords: set[Coord]
) -> dict[Coord, int]:
    """Turn the coordinates into a dictionary with values representing
    picoseconds from start."""
    coords.add(end)
    picosecond = 0
    ret_dict: dict[Coord, int] = {start: picosecond}
    coord = start
    while end not in ret_dict:
        assert picosecond <= len(coords)
        picosecond += 1
        coord = get_next_coord(coord, coords, ret_dict)
        ret_dict[coord] = picosecond
    return ret_dict


def check_cheats(
    coord: Coord, value: int, positions: dict[Coord, int]
) -> dict[tuple[Coord, Coord], int]:
    """Check all 4 directions around the coordinate for cheats.

    Returns a dictionary of possible start/end cheats with time savings.

    Don't return cheats that lose time. (New value<current value)
    """
    ret_dict: dict[tuple[Coord, Coord], int] = {}
    for direction in Direction:
        cheat_end = Coord(
            (direction.value[0] * 2) + coord.x,
            (direction.value[1] * 2) + coord.y,
        )
        # Eliminate positions not on the path.
        if cheat_end not in positions:
            continue
        # Eliminate positions that lose/waste time.
        if positions[cheat_end] <= value + 2:
            continue
        ret_dict[(coord, cheat_end)] = positions[cheat_end] - value - 2
    return ret_dict


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    # Initial tests of logic
    start, end, coords = get_input("day20example1")
    assert start == Coord(1, 3)
    assert end == Coord(5, 7)
    coords_dict = coords_to_dict(start, end, coords)
    assert coords_dict[start] == 0
    assert coords_dict[end] == 84
    test = check_cheats(Coord(7, 1), coords_dict[Coord(7, 1)], coords_dict)
    assert test == {(Coord(7, 1), Coord(9, 1)): 12}
    all_cheats = {}
    for coord, value in coords_dict.items():
        all_cheats.update(check_cheats(coord, value, coords_dict))
    logging.debug(all_cheats)
    all_cheat_times = list(all_cheats.values())
    logging.debug(all_cheat_times)
    assert all_cheat_times.count(2) == 14
    assert all_cheat_times.count(4) == 14
    assert all_cheat_times.count(6) == 2
    assert all_cheat_times.count(8) == 4
    assert all_cheat_times.count(10) == 2
    assert all_cheat_times.count(12) == 3
    assert all_cheat_times.count(20) == 1
    assert all_cheat_times.count(36) == 1
    assert all_cheat_times.count(38) == 1
    assert all_cheat_times.count(40) == 1
    assert all_cheat_times.count(64) == 1
    total = sum(1 for x in all_cheats.values() if x >= 40)
    assert total == 2


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    start, end, coords = get_input("day20input")
    coords_dict = coords_to_dict(start, end, coords)
    all_cheats = {}
    for coord, value in coords_dict.items():
        all_cheats.update(check_cheats(coord, value, coords_dict))
    total = sum(1 for x in all_cheats.values() if x >= 100)
    logging.critical(f"CHEATS OVER 100 picoseconds: {total}")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
