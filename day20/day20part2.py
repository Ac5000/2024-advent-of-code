"""Code for day 20 part 2."""

# pylint: disable=logging-fstring-interpolation

import logging
from collections import namedtuple
from enum import Enum
from operator import countOf

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


def make_possible_offsets(max_dist: int = 2) -> dict[Coord, int]:
    """Calculate offsets for all positions that can be reached.

    Returns:
        Dictionary where keys are offsets and values are the distances to them.
    """
    ret_dict: dict[Coord, int] = {}
    positives = range(0, max_dist + 1)
    negatives = range(0, (max_dist + 1) * -1, -1)
    # Right
    for i, x in enumerate(positives):
        # and Up
        for j, y in enumerate(range(0, max_dist + 1 - x)):
            ret_dict[Coord(x, y)] = i + j
        # and Down
        for j, y in enumerate(range(0, -1 * (max_dist + 1 - x), -1)):
            ret_dict[Coord(x, y)] = i + j
    # Left
    for i, x in enumerate(negatives):
        # and Up
        for j, y in enumerate(range(0, max_dist + 1 + x)):
            ret_dict[Coord(x, y)] = i + j
        # and Down
        for j, y in enumerate(range(0, -1 * (max_dist + 1 + x), -1)):
            ret_dict[Coord(x, y)] = i + j

    return ret_dict


def get_offset_coords(
    coord: Coord, value: int, offsets: dict[Coord, int]
) -> dict[tuple[Coord, Coord], int]:
    """Using the coord/value as origin, generate all possible cheat options.

    Returns:
        Dictionary of (start,end) with values equal to distance+starting.
    """
    ret_dict: dict[tuple[Coord, Coord], int] = {}
    for offset, offset_val in offsets.items():
        ret_dict[(coord, Coord(coord.x + offset.x, coord.y + offset.y))] = (
            offset_val + value
        )
    logging.debug(f"get_offset_coords: {ret_dict=}")
    return ret_dict


def get_valid_cheats(
    cheats: dict[tuple[Coord, Coord], int], path_coords: dict[Coord, int]
) -> dict[tuple[Coord, Coord], int]:
    """Filter out invalid, or wasteful cheats."""
    ret_dict: dict[tuple[Coord, Coord], int] = {}
    for (cheat_start, cheat_end), value in cheats.items():
        # Eliminate positions not on the path.
        if cheat_end not in path_coords:
            continue
        # Eliminate positions that lose/waste time.
        logging.debug(
            f"get_valid_cheats: {cheat_end=}, {value=}, {path_coords[cheat_end]=}"
        )
        if path_coords[cheat_end] <= value:
            continue
        ret_dict[(cheat_start, cheat_end)] = path_coords[cheat_end] - value

    return ret_dict


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.INFO)
    # Initial tests of logic
    start, end, coords = get_input("day20example1")
    assert start == Coord(1, 3)
    assert end == Coord(5, 7)
    coords_dict = coords_to_dict(start, end, coords)
    assert coords_dict[start] == 0
    assert coords_dict[end] == 84

    # Part 1 Remade
    offsets = make_possible_offsets()
    all_cheats = {}
    for coord, value in coords_dict.items():
        cheats = get_offset_coords(coord, value, offsets)
        all_cheats.update(get_valid_cheats(cheats, coords_dict))

    assert countOf(all_cheats.values(), 2) == 14
    assert countOf(all_cheats.values(), 4) == 14
    assert countOf(all_cheats.values(), 6) == 2
    assert countOf(all_cheats.values(), 8) == 4
    assert countOf(all_cheats.values(), 10) == 2
    assert countOf(all_cheats.values(), 12) == 3
    assert countOf(all_cheats.values(), 20) == 1
    assert countOf(all_cheats.values(), 36) == 1
    assert countOf(all_cheats.values(), 38) == 1
    assert countOf(all_cheats.values(), 40) == 1
    assert countOf(all_cheats.values(), 64) == 1

    total = sum(1 for x in all_cheats.values() if x >= 40)
    assert total == 2

    # Part 2
    offsets = make_possible_offsets(20)
    all_cheats = {}
    for coord, value in coords_dict.items():
        cheats = get_offset_coords(coord, value, offsets)
        all_cheats.update(get_valid_cheats(cheats, coords_dict))

    assert countOf(all_cheats.values(), 50) == 32
    assert countOf(all_cheats.values(), 52) == 31
    assert countOf(all_cheats.values(), 54) == 29
    assert countOf(all_cheats.values(), 56) == 39
    assert countOf(all_cheats.values(), 58) == 25
    assert countOf(all_cheats.values(), 60) == 23
    assert countOf(all_cheats.values(), 62) == 20
    assert countOf(all_cheats.values(), 64) == 19
    assert countOf(all_cheats.values(), 66) == 12
    assert countOf(all_cheats.values(), 68) == 14
    assert countOf(all_cheats.values(), 70) == 12
    assert countOf(all_cheats.values(), 72) == 22
    assert countOf(all_cheats.values(), 74) == 4
    assert countOf(all_cheats.values(), 76) == 3

    total = sum(1 for x in all_cheats.values() if x >= 74)
    assert total == 7


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    start, end, coords = get_input("day20input")
    coords_dict = coords_to_dict(start, end, coords)
    offsets = make_possible_offsets(20)
    all_cheats = {}
    for coord, value in coords_dict.items():
        cheats = get_offset_coords(coord, value, offsets)
        all_cheats.update(get_valid_cheats(cheats, coords_dict))
    total = sum(1 for x in all_cheats.values() if x >= 100)
    logging.critical(f"CHEATS OVER 100 picoseconds: {total}")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
