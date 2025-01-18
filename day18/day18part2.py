"""Code for day 18 part 2."""

# pylint: disable=logging-fstring-interpolation, too-many-instance-attributes

import heapq
import logging
from collections import namedtuple
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)

Coord = namedtuple("Coord", ["x", "y"])
PosState = namedtuple("PosState", ["score", "coord", "path"])


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


@dataclass
class Grid:
    """Class representing the grid of the room"""

    max_x: int
    max_y: int
    input_data: dict[Coord, str] = field(default_factory=dict)
    map_positions: dict[Coord, str] = field(default_factory=dict)
    start: Coord = Coord(0, 0)
    finish: Coord = Coord(-1, -1)
    position_scores: dict[Coord, int] = field(default_factory=dict)
    shortest_path: list[Coord] = field(default_factory=list)
    priorityq: list = field(default_factory=list)
    visited: set[Coord] = field(default_factory=set)
    final_score: int | float = 0
    last_byte_index: int = 0
    last_byte_coord: Coord | None = None

    def __post_init__(self):
        # Increase maxes by 1 for 0 indexing
        self.max_x += 1
        self.max_y += 1
        # Establish finish based on maxes.
        self.finish = Coord(self.max_x - 1, self.max_y - 1)
        self.initialize_grid()

    def initialize_grid(self) -> None:
        """Initialize the grid with dots."""
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.map_positions[Coord(x, y)] = "."

    def byte_fall(self, num_bytes: int) -> bool | Coord:
        """Make num_bytes corrupt memory spaces on the map.

        Args:
            num_bytes: How many bytes should fall.

        Returns:
            Iterator[bool | Coord]: False if byte not on shortest_path,
                otherwise coordinate that was on shortest_path.
        """
        for byte_index, (coord, symbol) in zip(
            range(self.last_byte_index + num_bytes),
            self.input_data.items(),
        ):
            logging.debug(f"byte_fall {byte_index=} {coord=} {symbol=}")
            if coord not in self.map_positions:
                continue
            del self.map_positions[coord]
            self.last_byte_index = byte_index
            # Check and yield if coord in self.shortest_path
            if coord in self.shortest_path:
                logging.debug(f"Removed {coord} in self.shortest_path.")
                self.last_byte_coord = coord
                return coord
        return False

    def purge_deadends(self) -> None:
        """Deletes all deadends from the map."""
        logging.info(f"Number of positions before = {len(self.map_positions)}")
        while True:
            deadends: list[Coord] = []
            for k, v in self.map_positions.items():
                # Ignore start and finish.
                if k in [self.start, self.finish]:
                    continue
                # Ignore walls.
                if v == "#":
                    continue
                if len(list(self.get_neighbors(Coord(*k)))) == 1:
                    deadends.append(k)
            # Break the while loop once there are no deadends.
            if not deadends:
                break
            for deadend in deadends:
                del self.map_positions[deadend]
        logging.info(
            f"Number of positions after purge = {len(self.map_positions)}"
        )

    def get_neighbors(self, coord: Coord) -> Iterator[Coord]:
        """Return neighbor positions to the given"""
        for direction in Direction:
            new_coord = (
                direction.value[0] + coord.x,
                direction.value[1] + coord.y,
            )
            if new_coord in self.map_positions:
                if self.map_positions[new_coord] != "#":
                    yield Coord(*new_coord)

    def visit(self, pos: PosState) -> None:
        """Visit each position."""
        # logging.debug(f"visit: {pos.coord=} {pos.score=}")
        if self.finish == pos.coord:
            logging.debug(f"Updating final score: {pos.score}")
            self.shortest_path += pos.path
            self.final_score = pos.score
        if self.finish == pos.coord and pos.score <= self.final_score:
            logging.debug(f"Updating final score: {pos.score}")
            self.shortest_path += pos.path
            self.final_score = pos.score
        for poss_coord in self.get_neighbors(pos.coord):
            # logging.debug(f"Checking neighbor: {poss_coord}")
            temp_score = 1 + pos.score

            # Skip visited coordinates
            if poss_coord in self.visited:
                # logging.debug(f"\033[91m{poss_coord} in self.visited\033[0m")
                continue

            # Compare previous scores.
            if poss_coord in self.position_scores:
                if self.position_scores[poss_coord] <= temp_score:
                    # logging.debug(f"{poss_coord} <= {temp_score}")
                    continue

            # Otherwise, set new score and add to heap
            self.position_scores[poss_coord] = temp_score
            heapq.heappush(
                self.priorityq,
                PosState(temp_score, poss_coord, pos.path + [poss_coord]),
            )
        self.visited.add(pos.coord)

    def start_mapping2(self) -> int | float:
        """Start mapping until we reach the finish."""
        # Put start into visited
        self.visited.add(self.start)

        # Push start onto heap.
        heapq.heappush(
            self.priorityq,
            PosState(0, self.start, [self.start]),
        )

        # Keep looping until priority Q is empty.
        while self.priorityq and not self.final_score:
            self.visit(heapq.heappop(self.priorityq))
            # logging.debug(("VISITED: ", self.visited))
        logging.critical(f"Returning from start_mapping2: {self.final_score=}")
        return self.final_score

    def highlight_short_paths(self) -> None:
        """Colors the shortest_path with red O's"""
        for coord in self.shortest_path:
            self.map_positions[coord] = "\033[91mO\033[0m"
        print(repr(self))

    def find_blocking(self) -> Coord:
        """Start indexing bytes until we find the one that prevents a score."""
        while True:
            while not self.byte_fall(len(self.input_data)):
                continue
            logging.debug(
                "REMOVED SOMETHING ON PATH. RESOLVING MAZE"
                f" {self.last_byte_index=}"
            )
            self.reset_maze_solution()
            if self.start_mapping2() == 0:
                # Maze not solvable, return the coord.
                logging.info(
                    f"Maze no longer solvable because {self.last_byte_coord}"
                )
                if self.last_byte_coord is None:
                    raise RuntimeError("Idk how we got here...")
                return self.last_byte_coord

    def reset_maze_solution(self) -> None:
        """Reset the maze solution to be solved again."""
        self.priorityq.clear()
        self.visited.clear()
        self.final_score = 0
        self.shortest_path.clear()
        self.position_scores.clear()
        assert not self.priorityq
        assert self.visited == set()
        assert self.final_score == 0
        assert not self.shortest_path
        assert not self.position_scores

    def __repr__(self) -> str:
        """Prints the grid in a grid format with axis legends"""
        justification = 3
        head_foot: str = "".join([" " for _ in range(justification + 1)]) + (
            "".join([str(i).center(justification) for i in range(self.max_x)])
        )
        ret_str: str = ""

        for y in range(self.max_y + 1):
            # Add the header and footer numbers.
            if y == 0:
                ret_str += head_foot + "\n"
            if y == self.max_y:
                ret_str += head_foot + "\n"
                continue
            for x in range(self.max_x + 1):
                # Add left side legend
                if x == 0:
                    ret_str += f"{y}".rjust(justification)
                # Add right side legend
                if x == self.max_x:
                    ret_str += " " + f"{y}".ljust(justification) + "\n"
                    continue
                ret_str += "  " + self.map_positions.get(Coord(x, y), " ")
        return ret_str


def get_input(filename: str) -> dict[Coord, str]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    ret_dict: dict[Coord, str] = {}
    for line in lines:
        x, y = line.split(",")
        ret_dict[Coord(int(x), int(y))] = "#"

    return ret_dict


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.INFO)
    # Initial tests of logic
    input_data = get_input("day18example1")
    mem_map = Grid(max_x=6, max_y=6, input_data=input_data)
    assert mem_map.start == Coord(0, 0)
    assert mem_map.finish == Coord(6, 6)
    logging.debug(mem_map.input_data)
    _ = [logging.debug(pos) for pos in mem_map.map_positions.items()]
    mem_map.byte_fall(12)
    mem_map.purge_deadends()
    logging.debug(mem_map.input_data)
    _ = [logging.debug(pos) for pos in mem_map.map_positions.items()]
    print(mem_map)
    score = mem_map.start_mapping2()
    logging.info(("SCORE: ", score))
    assert score == 22
    mem_map.highlight_short_paths()


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.DEBUG)
    input_data = get_input("day18input")
    mem_map = Grid(max_x=70, max_y=70, input_data=input_data)
    assert mem_map.start == Coord(0, 0)
    assert mem_map.finish == Coord(70, 70)
    mem_map.byte_fall(1024)
    mem_map.purge_deadends()
    score = mem_map.start_mapping2()
    assert score == 276
    assert mem_map.last_byte_index == 1023

    # From here on is new compared to part1.
    logging.info("Starting part 2 stuff.")
    part2_answer = mem_map.find_blocking()
    assert part2_answer == Coord(60, 37)


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
