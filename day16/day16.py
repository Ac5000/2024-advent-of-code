"""Code for day 16"""

from dataclasses import dataclass, field
from enum import Enum
import os
import heapq
from collections import namedtuple
from collections.abc import Iterator

Coord = namedtuple("Coord", ["x", "y"])
PosState = namedtuple("PosState", ["score", "coord", "direction", "visited"])


class Direction(tuple, Enum):
    """Directions that can be faced."""

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def opposite(self):
        """Return the opposite direction"""
        if self.name == "UP":
            return Direction.DOWN
        if self.name == "DOWN":
            return Direction.UP
        if self.name == "RIGHT":
            return Direction.LEFT
        if self.name == "LEFT":
            return Direction.RIGHT
        raise ValueError("Something went wrong here.")

    def string(self) -> str:
        """Return the arrow direction as a string."""
        if self.name == "UP":
            return "^"
        if self.name == "DOWN":
            return "v"
        if self.name == "RIGHT":
            return ">"
        if self.name == "LEFT":
            return "<"
        raise ValueError("Something went wrong here.")


def get_surrounding(x: int, y: int) -> list[tuple[Direction, tuple[int, int]]]:
    """Get surrounding coordinates for the given x,y.

    Args:
        x: X coord
        y: Y coord

    Yields:
        Iterable of coordinates with direction as keys.
    """
    surroundings = []
    surroundings.append((Direction.UP, (x, y - 1)))
    surroundings.append((Direction.DOWN, (x, y + 1)))
    surroundings.append((Direction.LEFT, (x - 1, y)))
    surroundings.append((Direction.RIGHT, (x + 1, y)))
    return surroundings


@dataclass
class Grid:
    """Class representing the grid of the room"""

    input_data: list[str] = field(default_factory=list)
    max_x: int = 0
    max_y: int = 0
    map_positions: dict[tuple[int, int], str] = field(default_factory=dict)
    start: tuple[int, int] = (-1, -1)
    finish: tuple[int, int] = (-1, -1)
    position_scores: dict[
        tuple[int, int], tuple[int | float, bool, Direction | None]
    ] = field(default_factory=dict)
    predecessors: dict[tuple[int, int], tuple[int, int]] = field(
        default_factory=dict
    )
    shortest_path: list = field(default_factory=list)
    priorityq: list = field(default_factory=list)
    visited: dict[tuple[Coord, Direction], int] = field(default_factory=dict)

    def __post_init__(self):
        self.parse_input()
        self._get_limits()
        self.purge_deadends()

    def parse_input(self) -> None:
        """Parses the input data into objects."""
        for y, line in enumerate(self.input_data):
            for x, char in enumerate(line):
                match char:
                    case ".":
                        self.map_positions[(x, y)] = "."
                    case "E":
                        self.map_positions[(x, y)] = "E"
                        self.finish = (x, y)
                    case "S":
                        self.map_positions[(x, y)] = "S"
                        self.start = (x, y)
                    case _:
                        pass

    def _get_limits(self) -> tuple[int, int]:
        """Set the max limits for the grid"""
        self.max_x = max(obj[0] for obj in self.map_positions)
        self.max_y = max(obj[1] for obj in self.map_positions)
        return self.max_x, self.max_y

    def get_coord(self, x: int, y: int) -> str:
        """Return the object at the coordinate or the object in the direction.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Dictionary at the coordinates
        """
        try:
            return self.map_positions[(x, y)]
        except KeyError:
            return " "

    def get_connected(
        self, x: int, y: int
    ) -> list[tuple[Direction, tuple[int, int]]]:
        """Get a list of connected coordinates that exist on map.

        Args:
            x: X coord
            y: Y coord

        Returns:
            List of direction,(x,y) coordinate/keys that exist.
        """
        connected = []
        for direction, coordinate in get_surrounding(x, y):
            try:
                _ = self.map_positions[coordinate]
                connected.append((direction, coordinate))
            except KeyError:
                continue
        return connected

    def purge_deadends(self) -> None:
        """Deletes all deadends from the map."""
        print(f"Number of positions before = {len(self.map_positions)}")
        while True:
            deadends: list[tuple[int, int]] = []
            for k, v in self.map_positions.items():
                if v in ["E", "S"]:
                    continue
                if len(self.get_connected(*k)) == 1:
                    deadends.append(k)
            # Break the while loop.
            if not deadends:
                break
            for deadend in deadends:
                del self.map_positions[deadend]
        print(f"Number of positions after purge = {len(self.map_positions)}")

    def get_neighbors(self, coord: Coord) -> Iterator[tuple[Coord, Direction]]:
        """Return neighbor positions to the given"""
        for direction in Direction:
            new_coord = (
                direction.value[0] + coord.x,
                direction.value[1] + coord.y,
            )
            if new_coord in self.map_positions:
                yield Coord(*new_coord), direction

    def visit(self, pos: PosState) -> None:
        """Visit each position."""
        for poss_coord, poss_dir in self.get_neighbors(pos.coord):
            # Score is 1 if no turn, otherwise its turn+1
            temp_score = (
                1001 + pos.score
                if poss_dir != pos.direction
                else 1 + pos.score
            )

            # Skip visited coordinates
            if ((poss_coord, poss_dir) in self.visited) and self.visited[
                (poss_coord, poss_dir)
            ] < temp_score:
                continue

            # Otherwise, set new score and add to heap
            self.visited[(poss_coord, poss_dir)] = temp_score
            heapq.heappush(
                self.priorityq,
                PosState(temp_score, poss_coord, poss_dir, False),
            )
            # Mark it off the map
            self.map_positions[poss_coord] = poss_dir.string()

    def start_mapping2(self) -> int:
        """Start mapping until we reach the finish."""
        # Put start into visited
        self.visited[(Coord(*self.start), Direction.RIGHT)] = 0
        # Push start onto heap.
        heapq.heappush(
            self.priorityq,
            PosState(0, Coord(*self.start), Direction.RIGHT, False),
        )
        # Keep looping until priority Q is empty.
        while self.priorityq:
            self.visit(heapq.heappop(self.priorityq))
        final_scores: list[int] = []
        for direction in Direction:
            try:
                final_scores.append(
                    self.visited[(Coord(*self.finish), direction)]
                )
            except KeyError:
                continue
        print(f"FINAL SCORE = {min(final_scores)}")
        return min(final_scores)

    def highlight_shortest(self) -> None:
        if not self.position_scores[self.finish][1]:
            raise RuntimeError("Haven't found finish yet.")
        pos = self.finish
        prev_dir = self.position_scores[pos][2]
        self.shortest_path.insert(0, prev_dir)
        while True:
            self.shortest_path.insert(0, pos)
            if prev_dir != self.position_scores[pos][2]:
                # Spot check for more than 90 degree turns.
                match prev_dir:
                    case Direction.UP:
                        assert self.position_scores[pos][2] != Direction.DOWN
                    case Direction.DOWN:
                        assert self.position_scores[pos][2] != Direction.UP
                    case Direction.LEFT:
                        assert self.position_scores[pos][2] != Direction.RIGHT
                    case Direction.RIGHT:
                        assert self.position_scores[pos][2] != Direction.LEFT

                prev_dir = self.position_scores[pos][2]
                self.shortest_path.insert(0, prev_dir)
            self.map_positions[pos] = "\033[91m#\033[0m"
            prep = repr(self)
            os.system("clear")
            print(prep)
            try:
                pos = self.predecessors[pos]
            except KeyError:
                break

    def __repr__(self) -> str:
        """Prints the grid in a grid format with axis legends"""
        justification = 3
        head_foot: str = (
            " "
            + "".join([" " for _ in range(justification + 1)])
            + (
                "".join(
                    [
                        str(i).center(justification)
                        for i in range(self.max_x + 1)
                    ]
                )
            )
        )
        ret_str: str = ""

        for y in range(self.max_y + 2):
            # Add the header and footer numbers.
            if y == 0:
                ret_str += head_foot + "\n"
            if y == self.max_y + 1:
                ret_str += head_foot + "\n"
                continue
            for x in range(self.max_x + 2):
                # Add left side legend
                if x == 0:
                    ret_str += f"{y}".rjust(justification) + " "
                # Add right side legend
                if x == self.max_x + 1:
                    ret_str += " " + f"{y}".ljust(justification) + "\n"
                    continue
                ret_str += "  " + str(self.get_coord(x, y))
        return ret_str


def get_input(filename: str) -> list[str]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    input_data = get_input("day16example1")
    maze_map = Grid(input_data=input_data)
    assert maze_map.start == (1, 13)
    assert maze_map.finish == (13, 1)
    assert get_surrounding(1, 1) == [
        (Direction.UP, (1, 0)),
        (Direction.DOWN, (1, 2)),
        (Direction.LEFT, (0, 1)),
        (Direction.RIGHT, (2, 1)),
    ]
    # assert maze_map.get_connected(1, 13) == [(Direction.UP, (1, 12))]
    assert maze_map.get_connected(9, 6) == [
        (Direction.UP, (9, 5)),
        (Direction.DOWN, (9, 7)),
    ]
    print(maze_map)
    assert Direction.DOWN == (0, 1)
    assert Direction.DOWN.opposite() == Direction.UP
    assert maze_map.get_neighbors(Coord(1, 13)).__next__() == (
        (1, 12),
        Direction.UP,
    )
    assert maze_map.start_mapping2() == 7036
    print(maze_map)
    # _ = [print(k, v) for k, v in maze_map.visited.items()]

    # # Second example
    input_data = get_input("day16example2")
    maze_map = Grid(input_data=input_data)
    print(maze_map)
    assert maze_map.start_mapping2() == 11048
    print(maze_map)


def main():
    """Get the answer"""
    # 105512 was too high.
    # 104512 was too low.
    # Off by 1?
    # 105511 was too high.
    # 105508 is the answer from someone else's code.
    input_data = get_input("day16input")
    maze_map = Grid(input_data=input_data)
    maze_map.start_mapping2()


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
