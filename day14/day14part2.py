"""Code for day 14"""

from __future__ import annotations
from dataclasses import dataclass, field
import re
import time
import os


class Robot:
    """Class representing a robot.

    Attributes:
        init_x: X initial position
        init_y: Y initial position
        x_velocity: X velocity component
        y_velocity: Y velocity component
        current_x: X current position
        current_y: Y current position
    """

    def __init__(self, string: str) -> None:
        """Initialize the robot attributes."""
        m = re.search(
            r"p=(?P<init_x>\d+),(?P<init_y>\d+) v=(?P<x_velocity>-?\d+),(?P<y_velocity>-?\d+)",
            string,
        )
        if m is None:
            print(f"PROBLEM WITH: '{string}'")
            raise RuntimeError("Couldn't parse string in robot.")
        self.init_x = int(m.group("init_x"))
        self.init_y = int(m.group("init_y"))
        self.x_velocity = int(m.group("x_velocity"))
        self.y_velocity = int(m.group("y_velocity"))
        self.current_x = self.init_x
        self.current_y = self.init_y

    def move(self, grid: Grid) -> None:
        """Move the robot once"""
        self.current_x += self.x_velocity
        self.current_y += self.y_velocity
        # Wrap X
        if self.current_x >= grid.max_x:
            self.current_x = self.current_x - grid.max_x
        if self.current_x < 0:
            self.current_x = self.current_x + grid.max_x
        # Wrap Y
        if self.current_y >= grid.max_y:
            self.current_y = self.current_y - grid.max_y
        if self.current_y < 0:
            self.current_y = self.current_y + grid.max_y

    def __repr__(self) -> str:
        return (
            f"Robot: {self.current_x=},{self.current_y=}\n"
            f"{self.init_x=},{self.init_y=},{self.x_velocity=},{self.y_velocity=}"
        )


@dataclass
class Grid:
    """Class representing the grid of the room"""

    max_x: int
    max_y: int
    map_positions: list[list] = field(default_factory=list)
    robots: list[Robot] = field(default_factory=list)
    x_middle: int = -1
    y_middle: int = -1

    def __post_init__(self):
        self._make_or_clear_map()
        self._calc_middles()

    def _make_or_clear_map(self) -> None:
        """Reset the map grid back to dots."""
        temp_y = []
        for _ in range(0, self.max_y):
            temp_x = []
            for _ in range(0, self.max_x):
                temp_x.append(".")
            temp_y.append(temp_x)
        self.map_positions = temp_y

    def _calc_middles(self):
        self.x_middle = self.max_x // 2
        self.y_middle = self.max_y // 2

    def calc_safety_factor(self) -> int:
        """Calculate final safety factor/answer."""
        q1: int = 0
        q2: int = 0
        q3: int = 0
        q4: int = 0
        for robot in self.robots:
            # Q2/4
            if robot.current_x > self.x_middle:
                # Q2
                if robot.current_y < self.y_middle:
                    q2 += 1
                elif robot.current_y > self.y_middle:
                    q4 += 1
            # Q1/3
            elif robot.current_x < self.x_middle:
                # Q1
                if robot.current_y < self.y_middle:
                    q1 += 1
                elif robot.current_y > self.y_middle:
                    q3 += 1
        final_answer: int = q1 * q2 * q3 * q4
        print(f"FINAL SAFETY FACTOR: {final_answer}")
        return final_answer

    def update_map(self) -> None:
        """Update the map with robot positions."""
        self._make_or_clear_map()
        for robot in self.robots:
            self.map_positions[robot.current_y][robot.current_x] = "#"

    def move_robots(self, seconds: int = 1) -> None:
        """Move all robots"""
        for robot in self.robots:
            for _ in range(seconds):
                robot.move(grid=self)

    def __repr__(self) -> str:
        """Prints the grid in a grid format with axis legends"""
        self.update_map()
        justification = 1
        # head_foot: str = "".join([" " for _ in range(justification)]) + (
        #     "".join([str(i).center(3) for i in range(self.max_x)])
        # )
        ret_str: str = ""

        for i, y in enumerate(self.map_positions):
            # Add the header and footer numbers.
            # if i == 0:
            #     ret_str += head_foot + "\n"
            # line_start = f"{i}".rjust(justification) + " "
            line_end = "\n"
            line = "".join(y)
            ret_str += line + line_end
        return ret_str


def get_input(filename: str):
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def parse_input(input_data: list[str]) -> list[Robot]:
    """Parse the input data into objects.

    Args:
        input_data: List of strings from the input

    Returns:
        List of initialized robot objects.
    """
    robots: list[Robot] = []
    for string in input_data:
        robots.append(Robot(string=string))
    return robots


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    input_data = get_input("day14example")
    robots = parse_input(input_data)
    room_map = Grid(max_x=11, max_y=7, robots=robots)
    print(room_map)
    assert 12 == len(robots)
    assert robots[0].init_x == 0
    assert robots[0].init_y == 4
    assert robots[0].x_velocity == 3
    assert robots[0].y_velocity == -3
    # _ = [print(i) for i in robots]
    robots = parse_input(["p=2,4 v=2,-3"])
    room_map = Grid(max_x=11, max_y=7, robots=robots)
    print("Initial state:")
    print(room_map)
    room_map.move_robots()
    print("After 1 second:")
    print(room_map)
    room_map.move_robots()
    print("After 2 second:")
    print(room_map)
    room_map.move_robots()
    print("After 3 second:")
    print(room_map)
    room_map.move_robots()
    print("After 4 second:")
    print(room_map)
    room_map.move_robots()
    print("After 5 second:")
    print(room_map)
    robots = parse_input(input_data)
    room_map = Grid(max_x=11, max_y=7, robots=robots)
    print("Initial Example")
    print(room_map)
    room_map.move_robots(100)
    print("After 100s")
    print(room_map)
    assert room_map.calc_safety_factor() == 12


def main():
    """Get the answer"""
    # Higher than 1804
    # Lower than 8000
    # 7758 is too low, but shows the tree...
    input_data = get_input("day14input")
    robots = parse_input(input_data)
    room_map = Grid(max_x=101, max_y=103, robots=robots)
    cur_time = 7861
    # jump_time = 103
    room_map.move_robots(cur_time)
    print(f"CURRENT TIME: {cur_time}")
    print(room_map)
    # while cur_time < 8001:
    #     input()
    #     room_map.move_robots()
    #     print(f"CURRENT TIME: {cur_time}")
    #     print(room_map)
    #     # time.sleep(0.2)
    #     cur_time += 1


if __name__ == "__main__":
    # debug_and_tests()
    print("THE REAL DEAL")
    main()
