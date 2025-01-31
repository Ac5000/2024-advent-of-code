"""Code for day 21 part 2

Same as part 1 code except just change the max_depth.

I struggled with this one a bit. My first attempts didn't work for all the
examples and I had to map things out. That's when I realized that I couldn't
just take shortest path on each keypad. Certain order chains could result in
fewer overall keypresses. I had to look online for how others did it."""

# pylint: disable=logging-fstring-interpolation

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cache
from itertools import chain, permutations, repeat

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


@dataclass()
class Coord:
    """Class representing a coordinate.

    Attributes:
        x: X part of the coordinate
        y: Y part of the coordinate
    """

    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: Coord) -> Coord:
        return Coord(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Coord) -> Coord:
        return Coord(x=other.x - self.x, y=other.y - self.y)


DIRECTIONS: dict[str, Coord] = {
    "^": Coord(0, -1),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
}

# Keys on the number keypad
NUM_KEYS: dict[str, Coord] = {
    "7": Coord(0, 0),
    "8": Coord(1, 0),
    "9": Coord(2, 0),
    "4": Coord(0, 1),
    "5": Coord(1, 1),
    "6": Coord(2, 1),
    "1": Coord(0, 2),
    "2": Coord(1, 2),
    "3": Coord(2, 2),
    " ": Coord(0, 3),
    "0": Coord(1, 3),
    "A": Coord(2, 3),
}

# Keys on the direction keypads
DIR_KEYS: dict[str, Coord] = {
    " ": Coord(0, 0),
    "^": Coord(1, 0),
    "a": Coord(2, 0),
    "<": Coord(0, 1),
    "v": Coord(1, 1),
    ">": Coord(2, 1),
}

movement_cache: dict[tuple[str, str], list[tuple[str]]] = {}


def moves_between_keys(start: Coord, end: Coord) -> list[tuple[str]]:
    """Returns a list of tuples of all possible moves between two keys."""
    diff = start - end
    moves = []
    for _ in repeat(0, abs(diff.x)):
        if diff.x < 0:
            moves.append("<")
        if diff.x > 0:
            moves.append(">")
    for _ in repeat(0, abs(diff.y)):
        if diff.y < 0:
            moves.append("^")
        if diff.y > 0:
            moves.append("v")
    moves = list(permutations(moves))
    logging.debug(f"moves_between_keys: {moves=}")
    return moves


def validate_moves(
    start: Coord, is_dir_pad: bool, moves: list[tuple[str]]
) -> list[tuple[str]]:
    """Returns list of moves that don't end up on blank space."""
    ret_list = []
    for move in moves:
        coord = start
        for direction in move:
            coord += DIRECTIONS[direction]
            if is_dir_pad and DIR_KEYS[" "] == coord:
                break
            if not is_dir_pad and NUM_KEYS[" "] == coord:
                break
        else:
            # Else only runs if loop finished. Add "a" to moveset.
            ret_list.append(move + ("a",))

    # Remove duplicates
    ret_list = list(set(ret_list))
    logging.debug(f"validate_moves: {ret_list=}")
    return ret_list


def build_cache():
    """Update the movement_cache with all possible movements."""
    for (key1, coord1), (key2, coord2) in permutations(NUM_KEYS.items(), 2):
        if coord1 == NUM_KEYS[" "] or coord2 == NUM_KEYS[" "]:
            continue
        movement_cache[(key1, key2)] = validate_moves(
            start=coord1,
            is_dir_pad=False,
            moves=moves_between_keys(coord1, coord2),
        )
    for (key1, coord1), (key2, coord2) in permutations(DIR_KEYS.items(), 2):
        if coord1 == DIR_KEYS[" "] or coord2 == DIR_KEYS[" "]:
            continue
        movement_cache[(key1, key2)] = validate_moves(
            start=coord1,
            is_dir_pad=True,
            moves=moves_between_keys(coord1, coord2),
        )
    # Add all "non-moves".
    for key in chain(NUM_KEYS.keys(), DIR_KEYS.keys()):
        if key == " ":
            continue
        movement_cache[(key, key)] = [("a",)]


@cache
def shortest_length(code: str, max_depth: int = 2, cur_depth: int = 0) -> int:
    """Recursively find min lengths until hitting max depth limit"""
    # Bots start on "a" keys.
    current_char = "A" if cur_depth == 0 else "a"
    total_length = 0

    for target_char in code:
        if cur_depth == max_depth:
            total_length += len(movement_cache[(current_char, target_char)][0])
        else:
            total_length += min(
                shortest_length(remaining_code, max_depth, cur_depth + 1)
                for remaining_code in movement_cache[
                    (current_char, target_char)
                ]
            )
        current_char = target_char

    logging.debug(f"{total_length=}")
    return total_length


def calc_score(code: str, length: int) -> int:
    """Calculate final score"""
    score = int(code[:3]) * length
    logging.critical(f"Code Score:{code} = {score}")
    return score


def get_input(filename: str) -> list[str]:
    """Read the file and parse.

    Returns:
        List of strings. Each string is a keycode.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    logging.debug(f"get_input: {lines}")
    return lines


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    assert moves_between_keys(Coord(0, 0), Coord(0, 1)) == [("v",)]
    assert moves_between_keys(Coord(2, 0), Coord(0, 0)) == [
        ("<", "<"),
        ("<", "<"),
    ]
    assert moves_between_keys(Coord(1, 1), Coord(0, 0)) == [
        ("<", "^"),
        ("^", "<"),
    ]
    build_cache()
    logging.debug("movement_cache")
    _ = [print(k, v) for k, v in movement_cache.items()]
    assert 1 == shortest_length("A", 0, 0)
    assert shortest_length("029A") == 68
    assert shortest_length("980A") == 60
    assert shortest_length("179A") == 68
    assert shortest_length("456A") == 64
    assert shortest_length("379A") == 64
    assert calc_score("029A", shortest_length("029A")) == 68 * 29
    assert calc_score("980A", shortest_length("980A")) == 60 * 980
    assert calc_score("179A", shortest_length("179A")) == 68 * 179
    assert calc_score("456A", shortest_length("456A")) == 64 * 456
    assert calc_score("379A", shortest_length("379A")) == 64 * 379
    final = 0
    for code in get_input("day21example1"):
        final += calc_score(code, shortest_length(code))
    assert final == 126384


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    final = 0
    for code in get_input("day21input"):
        final += calc_score(code, shortest_length(code, 25))
    logging.critical(f"{final=}")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
