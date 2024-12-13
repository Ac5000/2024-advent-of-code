"""Code for day 6."""

from collections import namedtuple
from dataclasses import dataclass, field
from enum import StrEnum, auto

Coordinate = namedtuple("Coordinate", ["x", "y"])


class Direction(StrEnum):
    """Directions the guard can face."""

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


@dataclass
class Guard:
    """Represents the guard"""

    location: Coordinate
    direction: Direction
    positions: set = field(default_factory=set)
    left_area: bool = False

    def rotate(self):
        """Hit obstacle, rotate 90."""
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP


def get_input(filename: str) -> list[str]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def find_guard(the_map: list[str]) -> Guard:
    """Find starting location of the guard on the map"""
    for y, row in enumerate(the_map):
        for x, character in enumerate(row):
            if character == "^":
                guard = Guard(
                    location=Coordinate(x, y), direction=Direction.UP
                )
                guard.positions.add(Coordinate(x, y))
                return guard
    raise RuntimeError("Couldn't find the guard in the map")


def get_map_limits(the_map: list[str]) -> tuple[int, int]:
    """Find the max size of the map(x,y)"""
    x_limit = len(the_map) - 1
    y_limit = len(max(the_map, key=len)) - 1
    return x_limit, y_limit


def check_coordinate(coordinate: Coordinate, the_map: list[str]) -> bool:
    """Check if the coordinate is in bounds."""
    x_lim, y_lim = get_map_limits(the_map)
    if coordinate.x not in range(0, x_lim + 1) or coordinate.y not in range(
        0, y_lim + 1
    ):
        print(f"{coordinate} OUT OF BOUNDS")
        return False
    return True


def has_obstacle(coordinate: Coordinate, the_map: list[str]) -> bool:
    """Check if the coordinate has an obstacle"""
    return "#" == (the_map[coordinate.y][coordinate.x])


def get_next_coordinate(
    coordinate: Coordinate, direction: Direction
) -> Coordinate:
    """Get the next coordinate based on direction."""
    match direction:
        case Direction.UP:
            return Coordinate(coordinate.x, coordinate.y - 1)
        case Direction.DOWN:
            return Coordinate(coordinate.x, coordinate.y + 1)
        case Direction.LEFT:
            return Coordinate(coordinate.x - 1, coordinate.y)
        case Direction.RIGHT:
            return Coordinate(coordinate.x + 1, coordinate.y)


def get_turn_coordinate(
    start_coordinate: Coordinate,
    direction: Direction,
    the_map: list[str],
    guard: Guard,
) -> Coordinate:
    """Get the location just before an obstacle"""
    current_coordinate = start_coordinate
    found_obstacle = False
    while not found_obstacle:
        # Get the next coordinate
        next_coordinate = get_next_coordinate(current_coordinate, direction)
        # Check if next location in the map.
        if not check_coordinate(next_coordinate, the_map):
            guard.left_area = True
            print("Guard escaped")
            break
        # Check if next location has an obstacle.
        found_obstacle = has_obstacle(next_coordinate, the_map)
        # if it doesn't have obstacle, next coord becomes current.
        if not found_obstacle:
            current_coordinate = next_coordinate
            guard.positions.add(next_coordinate)
    return current_coordinate


def run_guard(guard: Guard, the_map: list[str]) -> int:
    """Map out the guard path."""
    while not guard.left_area:
        guard.location = get_turn_coordinate(
            guard.location, guard.direction, the_map, guard
        )
        if guard.left_area:
            break
        guard.rotate()
        print(f"Hit wall at {guard.location}, heading {guard.direction}")
    print(f"Guard traveled {len(guard.positions)}.")
    return len(guard.positions)


def debug_and_tests():
    """Test using the sample and examples first."""
    guard_map = get_input("day6example")
    [print(line) for line in guard_map]
    guard = find_guard(guard_map)
    print(guard)
    assert guard.direction == Direction.UP
    guard.rotate()
    assert guard.direction == Direction.RIGHT
    guard.rotate()
    guard.rotate()
    guard.rotate()
    assert guard.direction == Direction.UP
    assert (9, 9) == get_map_limits(guard_map)
    assert check_coordinate(Coordinate(2, 2), guard_map)
    assert check_coordinate(Coordinate(0, 0), guard_map)
    assert not check_coordinate(Coordinate(10, 0), guard_map)
    assert has_obstacle(Coordinate(4, 0), guard_map)
    assert not has_obstacle(Coordinate(3, 0), guard_map)
    assert Coordinate(1, 0) == get_next_coordinate(
        Coordinate(1, 1), Direction.UP
    )
    assert Coordinate(4, 1) == get_turn_coordinate(
        guard.location, guard.direction, guard_map, guard
    )
    print("Starting Run")
    assert 41 == run_guard(guard, guard_map)


def main():
    """Get the answer"""
    guard_map = get_input("day6input")
    guard = find_guard(guard_map)
    run_guard(guard, guard_map)


if __name__ == "__main__":
    debug_and_tests()
    print("\nStarting Real Run")
    main()
