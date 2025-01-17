"""Code for day 6."""

import copy
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
    positions: set[tuple[Coordinate, Direction, int]] = field(
        default_factory=set
    )
    left_area: bool = False
    turn_positions: list[Coordinate] = field(default_factory=list)
    turn_directions: list[Direction] = field(default_factory=list)
    obstacle_options: set[Coordinate] = field(default_factory=set)
    loops_found: int = 0

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


def get_input(filename: str) -> list[list[str]]:
    """Read the file and yield rules."""
    ret_value: list[list[str]] = []

    with open(filename, "r", encoding="utf-8") as input_data:
        for line in input_data:
            ret_value.append(list(line.strip()))

    return ret_value


def find_guard(the_map: list[list[str]]) -> Guard:
    """Find starting location of the guard on the map"""
    for y, row in enumerate(the_map):
        for x, character in enumerate(row):
            if character == "^":
                guard = Guard(
                    location=Coordinate(x, y), direction=Direction.UP
                )
                guard.positions.add((Coordinate(x, y), Direction.UP, 1))
                return guard
    raise RuntimeError("Couldn't find the guard in the map")


def find_obstacles(the_map: list[list[str]]) -> set[Coordinate]:
    """Find all the obstacles on the map."""
    obstacles: set[Coordinate] = set()
    for y, row in enumerate(the_map):
        for x, character in enumerate(row):
            if character == "#":
                obstacles.add(Coordinate(x, y))
    return obstacles


def get_map_limits(the_map: list[list[str]]) -> tuple[int, int]:
    """Find the max size of the map(x,y)"""
    x_limit = len(the_map) - 1
    y_limit = len(max(the_map, key=len)) - 1
    return x_limit, y_limit


def check_coordinate(coordinate: Coordinate, the_map: list[list[str]]) -> bool:
    """Check if the coordinate is in bounds."""
    x_lim, y_lim = get_map_limits(the_map)
    if coordinate.x not in range(0, x_lim + 1) or coordinate.y not in range(
        0, y_lim + 1
    ):
        return False
    return True


def has_obstacle(coordinate: Coordinate, the_map: list[list[str]]) -> bool:
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


def rotate(direction: Direction) -> Direction:
    """Rotate 90 degrees"""
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP


def get_turn_coordinate(
    start_coordinate: Coordinate,
    direction: Direction,
    the_map: list[list[str]],
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
            # print("Guard escaped")
            break
        # Check if next location has an obstacle.
        found_obstacle = has_obstacle(next_coordinate, the_map)
        # if it doesn't have obstacle, next coord becomes current.
        if not found_obstacle:
            current_coordinate = next_coordinate
            guard.positions.add(
                (next_coordinate, direction, len(guard.positions) + 1)
            )
    return current_coordinate


def look_for_past_move(
    pos_dir: tuple[Coordinate, Direction, int],
    obstacles: set[Coordinate],
    turns: list[Coordinate],
    positions: set[tuple[Coordinate, Direction, int]],
):
    """At this position and direction, can we see a previous position or turn
    without an obstacle in the way?

    Basically, if we turn now, can we end up on a path already traveled in the
    same direction.
    """
    # Previous positions will be ones with a smaller index number.
    prev_positions = [pos for pos in positions if pos_dir[2] > pos[2]]

    match pos_dir[1]:
        case Direction.UP:
            # Check all values right / larger x's.
            obstacles_in_direction = [
                abs(i.x - pos_dir[0].x)
                for i in obstacles
                if (i.x > pos_dir[0].x) and (i.y == pos_dir[0].y)
            ]
            turns_in_direction = [
                abs(i.x - pos_dir[0].x)
                for i in turns
                if (i.x > pos_dir[0].x) and (i.y == pos_dir[0].y)
            ]
            prev_pos_in_direction = [
                abs(i[0].x - pos_dir[0].x)
                for i in prev_positions
                if (i[0].x > pos_dir[0].x) and (i[0].y == pos_dir[0].y)
            ]
        case Direction.DOWN:
            # Check all values left / smaller x's.
            obstacles_in_direction = [
                abs(i.x - pos_dir[0].x)
                for i in obstacles
                if (i.x < pos_dir[0].x) and (i.y == pos_dir[0].y)
            ]
            turns_in_direction = [
                abs(i.x - pos_dir[0].x)
                for i in turns
                if (i.x < pos_dir[0].x) and (i.y == pos_dir[0].y)
            ]
            prev_pos_in_direction = [
                abs(i[0].x - pos_dir[0].x)
                for i in prev_positions
                if (i[0].x < pos_dir[0].x) and (i[0].y == pos_dir[0].y)
            ]
        case Direction.LEFT:
            # Check all values above / smaller y's.
            obstacles_in_direction = [
                abs(i.y - pos_dir[0].y)
                for i in obstacles
                if (i.y < pos_dir[0].y) and (i.x == pos_dir[0].x)
            ]
            turns_in_direction = [
                abs(i.y - pos_dir[0].y)
                for i in turns
                if (i.y < pos_dir[0].y) and (i.x == pos_dir[0].x)
            ]
            prev_pos_in_direction = [
                abs(i[0].y - pos_dir[0].y)
                for i in prev_positions
                if (i[0].y < pos_dir[0].y) and (i[0].x == pos_dir[0].x)
            ]
        case Direction.RIGHT:
            # Check all values below / larger y's.
            # Turn all coordinates into a distance from pos_dir.
            obstacles_in_direction = [
                abs(i.y - pos_dir[0].y)
                for i in obstacles
                if (i.y > pos_dir[0].y) and (i.x == pos_dir[0].x)
            ]
            turns_in_direction = [
                abs(i.y - pos_dir[0].y)
                for i in turns
                if (i.y > pos_dir[0].y) and (i.x == pos_dir[0].x)
            ]
            prev_pos_in_direction = [
                abs(i[0].y - pos_dir[0].y)
                for i in prev_positions
                if (i[0].y > pos_dir[0].y) and (i[0].x == pos_dir[0].x)
            ]
    # print("Obstacles in direction:")
    # _ = [print(i) for i in obstacles_in_direction]
    # print("Turns in direction:")
    # _ = [print(i) for i in turns_in_direction]
    # print("Previous positions in direction:")
    # _ = [print(i) for i in prev_pos_in_direction]

    # If there's no obstacles or turns, this shouldn't be a path.
    if (
        not obstacles_in_direction
        or not turns_in_direction
        or not prev_pos_in_direction
    ):
        return False

    # If the smallest turn or prev_pos is smaller than an obstacle, this
    # should be a new path.
    if min(obstacles_in_direction) > min(turns_in_direction) or min(
        obstacles_in_direction
    ) > min(prev_pos_in_direction):
        return True
    return False


def brute_force(
    guard: Guard,
    the_map: list[list[str]],
):
    """Brute forcing every location..."""
    # At each position the guard visits:
    #   Add an obstacle at the next pos:
    #   Run the guard:
    #   Check for loop.
    #       if true, add to total.
    loops_found = 0
    init_guard = find_guard(the_map)
    tested_coords = []
    for position in guard.positions:
        next_coordinate = position[0]
        # Get one position ahead to place an obstacle.
        # next_coordinate = get_next_coordinate(position[0], position[1])

        # If the next cordinate is the guard's original location, continue.
        if next_coordinate == init_guard.location:
            continue

        # If the next cordinate is directly in front of guard's original
        # location, continue.
        if next_coordinate == get_next_coordinate(
            init_guard.location, init_guard.direction
        ):
            continue

        # Check if next location in the map.
        if not check_coordinate(next_coordinate, the_map):
            continue

        # Check we haven't already tried this position.
        if next_coordinate in tested_coords:
            continue

        # If next location doesn't already have obstacle, update/create the map.
        if not has_obstacle(next_coordinate, the_map):
            new_map = copy.deepcopy(the_map)
            new_map[next_coordinate.y][next_coordinate.x] = "#"
            new_guard = find_guard(new_map)
            run_guard(new_guard, new_map)
            tested_coords.append(next_coordinate)
            if new_guard.loops_found:
                loops_found += new_guard.loops_found
                print(f"{loops_found=}")
    print(f"Finished with {loops_found=}")


def run_guard(guard: Guard, the_map: list[list[str]]) -> int:
    """Map out the guard path."""
    while not guard.left_area:
        guard.location = get_turn_coordinate(
            guard.location, guard.direction, the_map, guard
        )
        if guard.location not in guard.turn_positions:
            guard.turn_positions.append(guard.location)
            guard.turn_directions.append(guard.direction)
        # Check we aren't in a corner by referencing directions.
        elif any(
            pos == guard.location and turn == guard.direction
            for pos, turn in zip(guard.turn_positions, guard.turn_directions)
        ):
            # print("Loop found")
            guard.loops_found += 1
            break
        else:
            # We in a corner, append.
            guard.turn_positions.append(guard.location)
            guard.turn_directions.append(guard.direction)

        # Break if the guard got out.
        if guard.left_area:
            break
        guard.rotate()
        assert len(guard.turn_directions) == len(guard.turn_positions)
    # print(f"Guard traveled {len(guard.positions)}.")
    return len(guard.positions)


def debug_and_tests():
    """Test using the sample and examples first."""
    guard_map = get_input("day6example")
    _ = [print(line) for line in guard_map]
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
    assert 8 == len(find_obstacles(guard_map))

    print("Starting Run")
    guard = find_guard(guard_map)
    run_guard(guard, guard_map)
    print("BRUTE FORCE BEGIN")
    brute_force(guard, guard_map)
    # KNOWN_OBSTACLES = [
    #     Coordinate(3, 6),
    #     Coordinate(6, 7),
    #     Coordinate(7, 7),
    #     Coordinate(1, 8),
    #     Coordinate(3, 8),
    #     Coordinate(7, 9),
    # ]
    #
    # obstacle_positions = find_obstacles(guard_map)
    # future_obstacle_positions = []
    # for pos in guard.positions:
    #     if look_for_past_move(
    #         pos, obstacle_positions, guard.turn_positions, guard.positions
    #     ):
    #         if Coordinate(pos[0].x, pos[0].y) not in guard.turn_positions:
    #             future_obstacle_positions.append(
    #                 get_next_coordinate(pos[0], pos[1])
    #             )
    # _ = [print(i) for i in future_obstacle_positions]
    #
    # def compare(x, y):
    #     """Compare two lists that might not be in same order."""
    #     return Counter(x) == Counter(y)
    #
    # assert compare(KNOWN_OBSTACLES, KNOWN_OBSTACLES)
    # # Check results against expected.
    # assert compare(KNOWN_OBSTACLES, future_obstacle_positions)


def main():
    """Get the answer"""
    guard_map = get_input("day6input")
    guard = find_guard(guard_map)
    run_guard(guard, guard_map)
    # 488 was too low...

    # # Find the obstacles
    # obstacle_positions = find_obstacles(guard_map)
    # future_obstacle_positions = []
    # # Loop through the positions the guard moved.
    # for pos in guard.positions:
    #     # For each position, check if you can see a previous move from that
    #     # location.
    #     if look_for_past_move(
    #         pos, obstacle_positions, guard.turn_positions, guard.positions
    #     ):
    #         if Coordinate(pos[0].x, pos[0].y) not in guard.turn_positions:
    #             future_obstacle_positions.append(
    #                 get_next_coordinate(pos[0], pos[1])
    #             )
    # print(
    #     f"Final amount of possible places to put an obstacle = {len(future_obstacle_positions)}"
    # )
    # 1895 was also too low...
    print("BRUTE FORCE BEGIN")
    brute_force(guard, guard_map)


if __name__ == "__main__":
    debug_and_tests()
    print("\nStarting Real Run")
    main()
