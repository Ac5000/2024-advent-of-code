"""Code for day 12 part 2"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum, auto


class Direction(StrEnum):
    """Directions the trail can go."""

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


@dataclass
class Plot:
    """Class representing a single plot.

    Attributes:
        x: X position of the plot
        y: Y position of the plot
        plant: String representing the plant type.
    """

    x: int
    y: int
    plant: str
    _up: Plot | None = field(default=None)
    _down: Plot | None = field(default=None)
    _left: Plot | None = field(default=None)
    _right: Plot | None = field(default=None)
    perimeter: int = 0
    region: Region | None = field(default=None)
    up_fence: bool = False
    down_fence: bool = False
    left_fence: bool = False
    right_fence: bool = False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.plant))

    @property
    def up(self) -> Plot | None:
        """Return plot up from this plot.

        Returns:
            Plot above.
        """
        return self._up

    @up.setter
    def up(self, plot):
        self._up = plot
        self.up_fence = self.check_perimeter(plot)

    @property
    def down(self) -> Plot | None:
        """Return plot down from this plot.

        Returns:
            Plot below.
        """
        return self._down

    @down.setter
    def down(self, plot):
        self._down = plot
        self.down_fence = self.check_perimeter(plot)

    @property
    def left(self) -> Plot | None:
        """Return plot left from this plot.

        Returns:
            Plot left.
        """
        return self._left

    @left.setter
    def left(self, plot):
        self._left = plot
        self.left_fence = self.check_perimeter(plot)

    @property
    def right(self) -> Plot | None:
        """Return plot right from this plot.

        Returns:
            Plot right.
        """
        return self._right

    @right.setter
    def right(self, plot):
        self._right = plot
        self.right_fence = self.check_perimeter(plot)

    def adjacent_plots(self) -> list[Plot | None]:
        """Helper function to return adjacent plots.

        Returns:
            List of all adjacent plots.
        """
        return [self.up, self.down, self.left, self.right]

    def adjacent_matching_plots(self) -> list[Plot]:
        """Helper function to return adjacent plots of same plant.

        Returns:
            List of all adjacent plots.
        """
        ret_list: list[Plot] = []
        for plot in self.adjacent_plots():
            if plot is None:
                continue
            if self.plant == plot.plant:
                ret_list.append(plot)
        return ret_list

    def check_perimeter(self, plot: Plot | None) -> bool:
        """Returns true if there should be a fence."""
        if plot is None:
            return True
        if plot.plant != self.plant:
            return True
        return False

    def set_perimeter(self):
        """Set perimeter based on fences"""
        self.perimeter = 0
        for fence in [
            self.up_fence,
            self.down_fence,
            self.left_fence,
            self.right_fence,
        ]:
            if fence:
                self.perimeter += 1

    def __repr__(self) -> str:
        return f"Plot: {self.plant} @ ({self.x},{self.y}, {self.perimeter=})"


@dataclass
class Region:
    """Class representing a region

    Attributes:
        plots: A list of plots that make up the region.
    """

    first_plot: Plot
    plots: set[Plot] = field(default_factory=set)
    area: int = 0
    perimeter: int = 0
    cost: int = 0
    cost2: int = 0
    plant_type: str = ""
    top_sides: int = 0
    bottom_sides: int = 0
    left_sides: int = 0
    right_sides: int = 0

    def __post_init__(self):
        # Crawl the region based on the initial plot.
        self.plots.add(self.first_plot)
        self._crawl_plots(self.first_plot)
        self._set_plot_regions()
        self.get_top_sides()
        self.get_bottom_sides()
        self.get_left_sides()
        self.get_right_sides()
        self.run_calcs()

    def _crawl_plots(self, plot):
        for p in plot.adjacent_matching_plots():
            if p in self.plots:
                continue
            self.plots.add(p)
            self._crawl_plots(p)

    def _set_plot_regions(self):
        for plot in self.plots:
            plot.region = self

    @property
    def top(self) -> int:
        """Get the top most Y coordinate"""
        return min(self.plots, key=lambda x: x.y).y

    @property
    def bottom(self) -> int:
        """Get the bottom most Y coordinate"""
        return max(self.plots, key=lambda x: x.y).y

    @property
    def left(self) -> int:
        """Get the left most X coordinate"""
        return min(self.plots, key=lambda x: x.x).x

    @property
    def right(self) -> int:
        """Get the right most X coordinate"""
        return max(self.plots, key=lambda x: x.x).x

    def get_top_sides(self) -> int:
        """Get the number of sides.

        Returns:
            Integer of how many of this side.
        """
        self.top_sides = 0
        for y in range(self.top, self.bottom + 1):
            for x in range(self.left, self.right + 1):
                for plot in [p for p in self.plots if (p.y == y and p.x == x)]:
                    if not plot.up_fence:
                        continue
                    if (
                        plot.right is not None
                        and plot.right.plant == plot.plant
                    ):
                        if plot.right.up_fence:
                            continue
                    self.top_sides += 1
        return self.top_sides

    def get_bottom_sides(self) -> int:
        """Get the number of sides.

        Returns:
            Integer of how many of this side.
        """
        self.bottom_sides = 0
        for y in range(self.top, self.bottom + 1):
            for x in range(self.left, self.right + 1):
                for plot in [p for p in self.plots if (p.y == y and p.x == x)]:
                    if not plot.down_fence:
                        continue
                    if (
                        plot.right is not None
                        and plot.right.plant == plot.plant
                    ):
                        if plot.right.down_fence:
                            continue
                    self.bottom_sides += 1
        return self.bottom_sides

    def get_left_sides(self) -> int:
        """Get the number of sides.

        Returns:
            Integer of how many of this side.
        """
        self.left_sides = 0
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                for plot in [p for p in self.plots if (p.y == y and p.x == x)]:
                    if not plot.left_fence:
                        continue
                    if plot.down is not None and plot.down.plant == plot.plant:
                        if plot.down.left_fence:
                            continue
                    self.left_sides += 1
        return self.left_sides

    def get_right_sides(self) -> int:
        """Get the number of sides.

        Returns:
            Integer of how many of this side.
        """
        self.right_sides = 0
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                for plot in [p for p in self.plots if (p.y == y and p.x == x)]:
                    if not plot.right_fence:
                        continue
                    if plot.down is not None and plot.down.plant == plot.plant:
                        if plot.down.right_fence:
                            continue
                    self.right_sides += 1
        return self.right_sides

    def calc_area(self) -> int:
        """Calc area based on the plots.

        Returns:
            Area calculated from the plots.
        """
        self.area = len(self.plots)
        return self.area

    def calc_perimeter(self) -> int:
        """Calc perimeter based on the plots.

        Returns:
            Sum of perimeters of the plots.
        """
        self.perimeter = 0
        for plot in self.plots:
            self.perimeter += plot.perimeter
        return self.perimeter

    def calc_cost(self) -> int:
        """Calc cost based on attributes.

        Returns:
            Int cost based on perimeter and area.
        """
        self.cost = self.area * self.perimeter
        return self.cost

    def calc_cost2(self) -> int:
        """Calc cost based on attributes.

        Returns:
            Int cost based on # of sides and area.
        """
        self.cost2 = self.area * (
            self.top_sides
            + self.bottom_sides
            + self.left_sides
            + self.right_sides
        )
        return self.cost

    def run_calcs(self):
        """Run all calcs"""
        self.calc_area()
        self.calc_perimeter()
        self.calc_cost()
        self.calc_cost2()


@dataclass
class Grid:
    """Class representing the grid of the map"""

    initial_map: list[list[str]] = field(default_factory=list)
    max_x: int = 0
    max_y: int = 0
    plots: set[Plot] = field(default_factory=set)
    regions: list[Region] = field(default_factory=list)

    def __post_init__(self):
        self._get_limits()
        self._init_plots()
        self._init_regions()

    def get_plot(self, x: int, y: int) -> Plot | None:
        """Get the plot at the location.

        Args:
            x: X location of the plot/grid.
            y: Y location of the plot/grid.

        Returns:
            Returns the Plot object at the location if on the grid, otherwise
            returns None.
        """
        if x not in range(0, self.max_x + 1) or y not in range(
            0, self.max_y + 1
        ):
            return None
        for plot in self.plots:
            if plot.x == x and plot.y == y:
                return plot
        return None

    def plots_around_plot(self, plot: Plot):
        """Sets Plots from around the given Plot"""
        for direction in Direction:
            match direction:
                case Direction.UP:
                    plot.up = self.get_plot(plot.x, plot.y - 1)
                case Direction.DOWN:
                    plot.down = self.get_plot(plot.x, plot.y + 1)
                case Direction.LEFT:
                    plot.left = self.get_plot(plot.x - 1, plot.y)
                case Direction.RIGHT:
                    plot.right = self.get_plot(plot.x + 1, plot.y)

    def _get_limits(self) -> tuple[int, int]:
        """Set the max limits for the grid"""
        self.max_x = len(max(self.initial_map, key=len)) - 1
        self.max_y = len(self.initial_map) - 1
        return self.max_x, self.max_y

    def _init_plots(self):
        """Initialize the plots for the grid."""
        for i, y in enumerate(self.initial_map):
            for j, x in enumerate(y):
                self.plots.add(Plot(x=j, y=i, plant=x))
        for plot in self.plots:
            self.plots_around_plot(plot)
            plot.set_perimeter()

    def _init_regions(self):
        for plot in self.plots:
            if not plot.region:
                self.regions.append(
                    Region(first_plot=plot, plant_type=plot.plant)
                )

    def get_final_cost(self) -> int:
        """Get the final total cost for the fencing."""
        final_cost: int = 0
        for region in self.regions:
            final_cost += region.cost
        print(f"FINAL COST = {final_cost}")
        return final_cost

    def get_final_cost2(self) -> int:
        """Get the final total cost for the fencing with the discount."""
        final_cost: int = 0
        for region in self.regions:
            final_cost += region.cost2
        print(f"FINAL COST2 = {final_cost}")
        return final_cost

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


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    input_data = get_input("day12example1")
    grid = Grid(initial_map=input_data)
    print(grid)
    # _ = [print(i) for i in grid.plots]
    assert 5 == len(grid.regions)
    for region in grid.regions:
        if region.plant_type == "A":
            assert 4 == region.area
            assert 10 == region.perimeter
            assert 40 == region.cost
            assert 1 == region.get_top_sides()
            assert 1 == region.get_bottom_sides()
            assert 1 == region.get_left_sides()
            assert 1 == region.get_right_sides()
            assert 16 == region.cost2
        if region.plant_type == "B":
            assert 4 == region.area
            assert 8 == region.perimeter
            assert 32 == region.cost
            assert 1 == region.get_top_sides()
            assert 1 == region.get_bottom_sides()
            assert 1 == region.get_left_sides()
            assert 1 == region.get_right_sides()
            assert 16 == region.cost2
        if region.plant_type == "C":
            assert 4 == region.area
            assert 10 == region.perimeter
            assert 40 == region.cost
            assert 2 == region.get_top_sides()
            assert 2 == region.get_bottom_sides()
            assert 2 == region.get_left_sides()
            assert 2 == region.get_right_sides()
            assert 32 == region.cost2
        if region.plant_type == "D":
            assert 1 == region.area
            assert 4 == region.perimeter
            assert 4 == region.cost
            assert 1 == region.get_top_sides()
            assert 1 == region.get_bottom_sides()
            assert 1 == region.get_left_sides()
            assert 1 == region.get_right_sides()
            assert 4 == region.cost2
        if region.plant_type == "E":
            assert 3 == region.area
            assert 8 == region.perimeter
            assert 24 == region.cost
            assert 1 == region.get_top_sides()
            assert 1 == region.get_bottom_sides()
            assert 1 == region.get_left_sides()
            assert 1 == region.get_right_sides()
            assert 12 == region.cost2
    assert 140 == grid.get_final_cost()
    assert 80 == grid.get_final_cost2()

    # Larger example
    input_data = get_input("day12example2")
    grid = Grid(initial_map=input_data)
    print(grid)
    assert 11 == len(grid.regions)
    for region in grid.regions:
        if region.plant_type == "R":
            assert 12 == region.area
            assert 18 == region.perimeter
            assert 216 == region.cost
            assert 2 == region.get_top_sides()
            assert 3 == region.get_bottom_sides()
        if region.plant_type == "F":
            assert 10 == region.area
            assert 18 == region.perimeter
            assert 180 == region.cost
            assert 2 == region.get_top_sides()
            assert 4 == region.get_bottom_sides()
            assert 4 == region.get_left_sides()
        if region.plant_type == "V":
            assert 13 == region.area
            assert 20 == region.perimeter
            assert 260 == region.cost
        if region.plant_type == "J":
            assert 11 == region.area
            assert 20 == region.perimeter
            assert 220 == region.cost
        if region.plant_type == "E":
            assert 13 == region.area
            assert 18 == region.perimeter
            assert 234 == region.cost
    assert 1930 == grid.get_final_cost()
    assert 1206 == grid.get_final_cost2()


def main():
    """Get the answer"""
    input_data = get_input("day12input")
    grid = Grid(initial_map=input_data)
    print(grid)
    grid.get_final_cost()
    grid.get_final_cost2()


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
