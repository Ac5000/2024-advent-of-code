"""Code for day 8"""

from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import combinations, filterfalse


@dataclass(order=True)
class Antinode:
    """Class representing an antinode"""

    signal: str
    x: int
    y: int

    def __repr__(self) -> str:
        return f"Antinode: {self.signal} @ ({self.x},{self.y})"


@dataclass(order=True)
class Antenna:
    """Class representing an antenna"""

    signal: str
    x: int
    y: int

    def __repr__(self) -> str:
        return f"Antenna: {self.signal} @ ({self.x},{self.y})"


@dataclass
class Grid:
    """Class representing the grid of the city/antenna"""

    initial_map: list[list[str]] = field(default_factory=list)
    max_x: int = 0
    max_y: int = 0
    antennas: list[Antenna] = field(default_factory=list)
    signal_group: dict[str, list[Antenna]] = field(default_factory=dict)

    def __post_init__(self):
        self._get_limits()
        self._find_antennas()
        self._group_signals()

    def coord(self, x: int, y: int) -> str:
        """Returns the value at the coordinate"""
        return self.initial_map[y][x]

    def mark_antinode(self, antinode: Antinode):
        """Update the grid with #'s for the antinode"""
        self.initial_map[antinode.y][antinode.x] = "#"

    def _get_limits(self) -> tuple[int, int]:
        """Set the max limits for the grid"""
        self.max_x = len(max(self.initial_map, key=len)) - 1
        self.max_y = len(self.initial_map) - 1
        return self.max_x, self.max_y

    def _find_antennas(self) -> list[Antenna]:
        """Make a list of the various antennas"""
        for i, y in enumerate(self.initial_map):
            for j, x in enumerate(y):
                if x != ".":
                    self.antennas.append(Antenna(signal=x, x=j, y=i))
        self.antennas.sort(key=lambda x: x.signal)
        return self.antennas

    def _group_signals(self):
        """Group antennas by signal/frequency"""
        for antenna in self.antennas:
            if antenna.signal in self.signal_group:
                self.signal_group[antenna.signal].append(antenna)
            else:
                self.signal_group[antenna.signal] = [antenna]

    def signal_combos(self, signal: str) -> Iterable[tuple[Antenna, Antenna]]:
        """Get all combinations of antenna pairs for the signal"""
        return combinations(self.signal_group[signal], 2)

    def __repr__(self) -> str:
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


def get_antinodes(antenna1: Antenna, antenna2: Antenna) -> list[Antinode]:
    """Get antinodes for two antenna"""
    # 1>2
    # a2 to a1 equal a1 to x1
    x1 = antenna1.x - (antenna2.x - antenna1.x)
    y1 = antenna1.y - (antenna2.y - antenna1.y)
    antinode1 = Antinode(signal=antenna1.signal, x=x1, y=y1)

    # 2>1
    # a1 to a2 equal a2 to x2
    x2 = antenna2.x - (antenna1.x - antenna2.x)
    y2 = antenna2.y - (antenna1.y - antenna2.y)
    antinode2 = Antinode(signal=antenna2.signal, x=x2, y=y2)
    return [antinode1, antinode2]


def get_antinodes2(
    antenna1: Antenna, antenna2: Antenna, max_x: int, max_y: int
) -> list[Antinode]:
    """Get antinodes for two antenna"""
    antinodes = []
    antinodes.append(
        Antinode(signal=antenna1.signal, x=antenna1.x, y=antenna1.y)
    )
    antinodes.append(
        Antinode(signal=antenna2.signal, x=antenna2.x, y=antenna2.y)
    )
    # 1>2
    # a2 to a1 equal a1 to x1
    antinodes1 = []
    x = antenna1.x - (antenna2.x - antenna1.x)
    y = antenna1.y - (antenna2.y - antenna1.y)
    while (x <= max_x) and (x >= 0) and (y <= max_y) and (y >= 0):
        antinodes1.append((x, y))
        x = x - (antenna2.x - antenna1.x)
        y = y - (antenna2.y - antenna1.y)

    # 2>1
    # a1 to a2 equal a2 to x2
    antinodes2 = []
    x = antenna2.x - (antenna1.x - antenna2.x)
    y = antenna2.y - (antenna1.y - antenna2.y)
    while (x <= max_x) and (x >= 0) and (y <= max_y) and (y >= 0):
        antinodes2.append((x, y))
        x = x - (antenna1.x - antenna2.x)
        y = y - (antenna1.y - antenna2.y)

    for antinode in antinodes1 + antinodes2:
        antinodes.append(
            Antinode(signal=antenna1.signal, x=antinode[0], y=antinode[1])
        )

    return antinodes


def get_all_antinodes(grid: Grid) -> list[Antinode]:
    """Use the grid to find all antinodes within the grid"""
    antinodes = []
    for key in grid.signal_group.keys():
        for pair in grid.signal_combos(key):
            antinodes.extend(
                get_antinodes2(
                    antenna1=pair[0],
                    antenna2=pair[1],
                    max_x=grid.max_x,
                    max_y=grid.max_y,
                )
            )
    return list(
        filterfalse(
            lambda x: (x.x > grid.max_x)
            or (x.x < 0)
            or (x.y > grid.max_y)
            or (x.y < 0),
            antinodes,
        )
    )


def unique_antinodes(antinodes: list[Antinode]) -> int:
    """Return the count of unique antinode coordinates"""
    anti_set = set()
    for antinode in antinodes:
        anti_set.add((antinode.x, antinode.y))
    print(f"There are {len(anti_set)} unique locations with an antinode.")
    return len(anti_set)


def debug_and_tests():
    """Test using the sample and examples first."""
    city_map = get_input("day8example")
    grid = Grid(initial_map=city_map)
    print(grid)
    # _ = [print(i) for i in grid.antennas]
    a1 = Antenna(signal="a", x=4, y=3)
    a2 = Antenna(signal="a", x=5, y=5)
    x1 = Antinode(signal="a", x=3, y=1)
    x2 = Antinode(signal="a", x=6, y=7)
    assert [x1, x2] == get_antinodes(a1, a2)
    # _ = [print(i) for i in grid.signal_combos("a")]
    antinodes = get_all_antinodes(grid)

    # _ = [print(i) for i in antinodes]
    print(f"Length before unique={len(antinodes)}")
    unique_location_count = unique_antinodes(antinodes)
    for antinode in antinodes:
        grid.mark_antinode(antinode)
    print(grid)
    assert 34 == unique_location_count


def main():
    """Get the answer"""
    city_map = get_input("day8input")
    grid = Grid(initial_map=city_map)
    antinodes = get_all_antinodes(grid)
    unique_antinodes(antinodes)


if __name__ == "__main__":
    # debug_and_tests()
    print("THE REAL DEAL")
    main()
