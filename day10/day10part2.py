"""Code for day 10"""

from dataclasses import dataclass, field
from enum import StrEnum, auto


class Direction(StrEnum):
    """Directions the trail can go."""

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


@dataclass
class Trailhead:
    """Class representing a trailhead"""

    x: int
    y: int
    score: int = 0
    trailends: list = field(default_factory=list)

    def add_trailend(self, coordinate):
        """Increase score"""
        self.score += 1
        # if coordinate not in self.trailends:
        #     self.trailends.append(coordinate)
        #     self.score += 1

    def __repr__(self) -> str:
        return f"Trailhead: {self.score} @ ({self.x},{self.y}) ends:{self.trailends}"


@dataclass
class Coordinate:
    """Class representing a coordinate on the map"""

    x: int
    y: int
    height: int = -1
    trailheads: list[Trailhead] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Coordinate: {self.height} @ ({self.x},{self.y})"


@dataclass
class Grid:
    """Class representing the grid of the map"""

    initial_map: list[list[str]] = field(default_factory=list)
    max_x: int = 0
    max_y: int = 0
    trailheads: list[Trailhead] = field(default_factory=list)

    def __post_init__(self):
        self._get_limits()
        self._find_trailheads()

    def coord_height(self, x: int, y: int) -> Coordinate | None:
        """Returns a Coordinate object at the location. Return None if OOB"""
        if x not in range(0, self.max_x + 1) or y not in range(
            0, self.max_y + 1
        ):
            return None
        # Catch example dots.
        if self.initial_map[y][x] == ".":
            return None
        return Coordinate(x=x, y=y, height=int(self.initial_map[y][x]))

    def coords_around_coord(
        self, coordinate: Coordinate
    ) -> list[Coordinate | None]:
        """Returns coordinates from around the given coordinate"""
        ret_list: list[Coordinate | None] = []
        for direction in Direction:
            match direction:
                case Direction.UP:
                    ret_list.append(
                        self.coord_height(coordinate.x, coordinate.y - 1)
                    )
                case Direction.DOWN:
                    ret_list.append(
                        self.coord_height(coordinate.x, coordinate.y + 1)
                    )
                case Direction.LEFT:
                    ret_list.append(
                        self.coord_height(coordinate.x - 1, coordinate.y)
                    )
                case Direction.RIGHT:
                    ret_list.append(
                        self.coord_height(coordinate.x + 1, coordinate.y)
                    )
        return ret_list

    def _get_limits(self) -> tuple[int, int]:
        """Set the max limits for the grid"""
        self.max_x = len(max(self.initial_map, key=len)) - 1
        self.max_y = len(self.initial_map) - 1
        return self.max_x, self.max_y

    def _find_trailheads(self) -> list[Trailhead]:
        """Make a list of the various trailheads"""
        for i, y in enumerate(self.initial_map):
            for j, x in enumerate(y):
                if x == "0":
                    self.trailheads.append(Trailhead(x=j, y=i))
        return self.trailheads

    def sum_trailheads(self) -> int:
        """Return the sum of the trailhead scores. Final Answer"""
        score_sum: int = 0
        for trailhead in self.trailheads:
            score_sum += trailhead.score
        print(f"Sum of trailhead scores is {score_sum}")
        return score_sum

    def __repr__(self) -> str:
        """Prints the grid in a grid format with axis legends"""
        justification = 3
        head_foot: str = "".join([" " for _ in range(justification)]) + (
            "".join([str(i).center(3) for i in range(self.max_x + 1)])
        )
        ret_str: str = ""

        for i, y in enumerate(self.initial_map):
            # Add the header and footer numbers.
            if i == 0:
                ret_str += head_foot + "\n"
            line_start = f"{i}".rjust(justification) + " "
            line_end = " " + f"{i}".ljust(justification) + "\n"
            line = "  ".join(y)
            ret_str += line_start + line + line_end
            if i == self.max_y:
                ret_str += head_foot
        return ret_str


def get_input(filename: str) -> list[list[str]]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    ret_val: list[list[str]] = []
    for line in lines:
        temp_axis = []
        for c in line:
            temp_axis.append(c)
        ret_val.append(temp_axis)
    return ret_val


def find_next_path(
    coordinate: Coordinate, topo_map: Grid, trailhead: Trailhead
) -> list[Coordinate]:
    """Find the next possible path(s) from the given coordinate"""
    # Return early if this coordinate is the max height.
    if coordinate.height == 9:
        trailhead.add_trailend(coordinate)
        return []
    paths = topo_map.coords_around_coord(coordinate)
    ret_paths: list[Coordinate] = []
    for path in paths:
        if path is None:
            continue
        if path.height == (coordinate.height + 1):
            path.trailheads.append(trailhead)
            ret_paths.append(path)
    return ret_paths


def chart_path(trailhead: Trailhead, topo_map: Grid):
    """Start charting paths from the trailhead"""
    init_coord = Coordinate(
        x=trailhead.x, y=trailhead.y, height=0, trailheads=[trailhead]
    )
    paths = [init_coord]
    while paths:
        path = paths.pop()
        paths.extend(find_next_path(path, topo_map, trailhead))


def debug_and_tests():
    """Test using the sample and examples first."""
    # 1 trailhead, 3 score.
    topo_map = get_input("day10example4")
    grid = Grid(initial_map=topo_map)
    assert 1 == len(grid.trailheads)
    for i, trailhead in enumerate(grid.trailheads):
        print(f"Trailblazing {i+1}/{len(grid.trailheads)}")
        chart_path(trailhead, grid)
    assert 3 == grid.sum_trailheads()

    # 1 trailhead, 13 score.
    topo_map = get_input("day10example5")
    grid = Grid(initial_map=topo_map)
    assert 1 == len(grid.trailheads)
    for i, trailhead in enumerate(grid.trailheads):
        print(f"Trailblazing {i+1}/{len(grid.trailheads)}")
        chart_path(trailhead, grid)
    assert 13 == grid.sum_trailheads()

    # 1 trailhead, 227 score.
    topo_map = get_input("day10example6")
    grid = Grid(initial_map=topo_map)
    assert 1 == len(grid.trailheads)
    for i, trailhead in enumerate(grid.trailheads):
        print(f"Trailblazing {i+1}/{len(grid.trailheads)}")
        chart_path(trailhead, grid)
    assert 227 == grid.sum_trailheads()

    # 9 trailheads, 81 score primary example.
    topo_map = get_input("day10example")
    grid = Grid(initial_map=topo_map)
    assert 9 == len(grid.trailheads)
    for i, trailhead in enumerate(grid.trailheads):
        print(f"Trailblazing {i+1}/{len(grid.trailheads)}")
        chart_path(trailhead, grid)
    assert 81 == grid.sum_trailheads()


def main():
    """Get the answer"""
    topo_map = get_input("day10input")
    grid = Grid(initial_map=topo_map)
    print(f"Found {len(grid.trailheads)} trailheads.")
    for i, trailhead in enumerate(grid.trailheads):
        print(f"Trailblazing {i+1}/{len(grid.trailheads)}")
        chart_path(trailhead, grid)
    grid.sum_trailheads()


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
