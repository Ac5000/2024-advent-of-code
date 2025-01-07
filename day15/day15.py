"""Code for day 15"""

from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from enum import StrEnum
from itertools import repeat, pairwise


class Direction(StrEnum):
    """Directions the robot can go."""

    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


@dataclass
class MapObject:
    """Class representing something on the map.

    Attributes:
        x: X coordinate
        y: Y coordinate
    """

    x: int
    y: int
    moveable: bool = True

    def move(self, direction: Direction) -> None:
        """Move the object the given direction"""
        if not self.moveable:
            return
        match direction:
            case Direction.UP:
                self.y = self.y - 1
            case Direction.DOWN:
                self.y = self.y + 1
            case Direction.LEFT:
                self.x = self.x - 1
            case Direction.RIGHT:
                self.x = self.x + 1


@dataclass
class Wall(MapObject):
    """Class representing a wall."""

    moveable: bool = False

    def __repr__(self) -> str:
        return f"Wall: {self.x=},{self.y=}\n"

    def __str__(self) -> str:
        return "#"


@dataclass
class Box(MapObject):
    """Class representing a box."""

    def __repr__(self) -> str:
        return f"Box: {self.x=},{self.y=}\n"

    def __str__(self) -> str:
        return "O"


@dataclass
class Robot(MapObject):
    """Class representing the robot."""

    def __repr__(self) -> str:
        return f"Robot: {self.x=},{self.y=}\n"

    def __str__(self) -> str:
        return "@"


@dataclass
class EmptySpace(MapObject):
    """Class representing empty space."""

    def __repr__(self) -> str:
        return f"EmptySpace: {self.x=},{self.y=}\n"

    def __str__(self) -> str:
        return "."


@dataclass
class Grid:
    """Class representing the grid of the room"""

    input_data: list[str] = field(default_factory=list)
    max_x: int = 0
    max_y: int = 0
    map_positions: list = field(default_factory=list)
    movements: deque = field(default_factory=deque)
    robot: Robot | None = None

    def __post_init__(self):
        self.parse_input()
        self._get_limits()

    def parse_input(self) -> None:
        """Parses the input data into objects."""
        for y, line in enumerate(self.input_data):
            for x, char in enumerate(line):
                match char:
                    case "#":
                        self.map_positions.append(Wall(x, y))
                    case "@":
                        self.robot = Robot(x, y)
                        self.map_positions.append(self.robot)
                    case "O":
                        self.map_positions.append(Box(x, y))
                    case ".":
                        self.map_positions.append(EmptySpace(x, y))
                    case "":
                        continue
                    case _:
                        self.movements.append(Direction(char))

    def _get_limits(self) -> tuple[int, int]:
        """Set the max limits for the grid"""
        self.max_x = max(obj.x for obj in self.map_positions)
        self.max_y = max(obj.y for obj in self.map_positions)
        return self.max_x, self.max_y

    def get_coord(
        self, x: int, y: int, direction: Direction | None = None
    ) -> MapObject:
        """Return the object at the coordinate or the object in the direction.

        Args:
            x: X coordinate
            y: Y coordinate
            direction: Direction enum to look, defaults to None

        Returns:
            MapObject at the coordinates

        Raises:
            LookupError: If the coordinates don't return something.
        """
        match direction:
            case Direction.UP:
                y = y - 1
            case Direction.DOWN:
                y = y + 1
            case Direction.LEFT:
                x = x - 1
            case Direction.RIGHT:
                x = x + 1
            case None:
                pass
        for i in self.map_positions:
            if i.x == x and i.y == y:
                return i
        raise LookupError(f"Could not find {x},{y}")

    def move_robot(self, direction: Direction) -> None:
        """Move the robot in the direction.

        Args:
            direction: Direction Enum to move

        Raises:
            RuntimeError: If there's not a robot object yet.
        """
        if self.robot is None:
            raise RuntimeError("No robot")
        next_obj = self.get_coord(self.robot.x, self.robot.y, direction)
        if isinstance(next_obj, Wall):
            # Hit a wall, can't move.
            return
        # EmptySpaces get swapped
        if isinstance(next_obj, EmptySpace):
            next_obj.x = self.robot.x
            next_obj.y = self.robot.y
            self.robot.move(direction)
            return
        if not isinstance(next_obj, Box):
            raise RuntimeError(
                "Not sure what we found. But clears linter complaint."
            )
        # Should only be boxes at this point.
        moveable, objs = self.determine_moveable(next_obj, direction)
        if not moveable:
            return
        objs.insert(0, self.robot)
        last = None
        # Last object should be the EmptySpace.
        for obj1, obj2 in pairwise(reversed(objs)):
            if last is not None:
                obj1 = last
            tempx = obj1.x
            tempy = obj1.y
            obj1.x = obj2.x
            obj1.y = obj2.y
            obj2.x = tempx
            obj2.y = tempy
            last = obj1

    def determine_moveable(
        self, box: Box, direction: Direction
    ) -> tuple[bool, list[MapObject]]:
        """Determine if the provided box is moveable or not.

        Args:
            box: Box object as starting point.
            direction: Direction we are trying to move.

        Returns:
            True if we can move the box. Basically EmptySpace before Wall.
            Plus a list of all the boxes that need to move with the empty space.

        Raises:
            RuntimeError: If we don't find a wall, box, or EmptySpace.
        """
        ret_objs: list[MapObject] = [box]
        x_coords = repeat(box.x)
        y_coords = repeat(box.y)
        match direction:
            case Direction.UP:
                y_coords = list(range(box.y - 1, -1, -1))
            case Direction.DOWN:
                y_coords = list(range(box.y + 1, self.max_y + 1))
            case Direction.LEFT:
                x_coords = list(range(box.x - 1, -1, -1))
            case Direction.RIGHT:
                x_coords = list(range(box.x + 1, self.max_x + 1))
        for x, y in zip(x_coords, y_coords):
            obj = self.get_coord(x, y)
            if isinstance(obj, Wall):
                return False, ret_objs
            if isinstance(obj, EmptySpace):
                ret_objs.append(obj)
                return True, ret_objs
            if isinstance(obj, Box):
                ret_objs.append(obj)
                continue
        raise RuntimeError(f"Didn't find object in {direction.name}.")

    def do_moves(self) -> None:
        """Do all the movements."""
        for move in self.movements:
            self.move_robot(move)

    def gps(self) -> int:
        """Calculate the GPS sum for final answer.

        Returns:
            Sum of box GPS values.
        """
        total = 0
        for box in [i for i in self.map_positions if isinstance(i, Box)]:
            total += (box.y * 100) + box.x
        print(f"TOTAL GPS: {total}")
        return total

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
                if x == 0:
                    ret_str += f"{y}".rjust(justification) + " "
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
    input_data = get_input("day15smallexample")
    # print(input_data)
    room_map = Grid(input_data=input_data)
    assert isinstance(room_map.get_coord(0, 0), Wall)
    assert isinstance(room_map.get_coord(0, 0, Direction.RIGHT), Wall)
    assert isinstance(room_map.get_coord(1, 0, Direction.DOWN), EmptySpace)
    room_map.move_robot(Direction.UP)
    assert room_map.robot.x == 2
    assert room_map.robot.y == 1
    room_map.move_robot(Direction.DOWN)
    assert room_map.robot.x == 2
    assert room_map.robot.y == 2
    room_map.move_robot(Direction.LEFT)
    assert room_map.robot.x == 2
    assert room_map.robot.y == 2
    assert not room_map.determine_moveable(Box(3, 1), Direction.UP)[0]
    assert room_map.determine_moveable(Box(3, 1), Direction.LEFT)[0]
    assert room_map.determine_moveable(Box(3, 1), Direction.RIGHT)[0]
    assert room_map.determine_moveable(Box(3, 1), Direction.DOWN)[0]
    room_map.move_robot(Direction.UP)
    room_map.move_robot(Direction.RIGHT)
    room_map.move_robot(Direction.RIGHT)
    room_map.move_robot(Direction.RIGHT)
    room_map.move_robot(Direction.DOWN)

    # Run the whole small example
    input_data = get_input("day15smallexample")
    room_map = Grid(input_data=input_data)
    room_map.do_moves()
    assert room_map.robot.x == 4 and room_map.robot.y == 4
    print(room_map)
    assert room_map.gps() == 2028

    # Run the whole large example
    input_data = get_input("day15largeexample")
    room_map = Grid(input_data=input_data)
    room_map.do_moves()
    assert room_map.robot.x == 3 and room_map.robot.y == 4
    print(room_map)
    assert room_map.gps() == 10092


def main():
    """Get the answer"""
    input_data = get_input("day15input")
    room_map = Grid(input_data=input_data)
    room_map.do_moves()
    print(room_map)
    room_map.gps()


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
