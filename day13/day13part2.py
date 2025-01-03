"""Code for day 13"""

from dataclasses import dataclass
import re
from fractions import Fraction

BUTTON_A_COST = 3
BUTTON_B_COST = 1
MAX_BUTTON_PRESS = 100


class Button:
    """Class representing a button.

    Attributes:
        x: X movement
        y: Y movement
        cost: Cost to press
    """

    def __init__(self, string: str, cost: int) -> None:
        m = re.search(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", string)
        if m is None:
            print(f"PROBLEM WITH: '{string}'")
            raise RuntimeError("Couldn't parse string in button.")
        self.x = int(m.group("x"))
        self.y = int(m.group("y"))
        self.cost = cost

    def __repr__(self) -> str:
        return f"Button: {self.x=},{self.y=},{self.cost=}"


@dataclass
class Prize:
    """Class representing a prize location.

    Attributes:
        x: X position
        y: Y position
    """

    def __init__(self, string: str) -> None:
        m = re.search(r"X=(?P<x>\d+), Y=(?P<y>\d+)", string)
        if m is None:
            print(f"PROBLEM WITH: {string}")
            raise RuntimeError("Couldn't parse string in prize.")
        self.x = int(m.group("x")) + 10000000000000
        self.y = int(m.group("y")) + 10000000000000

    def __repr__(self) -> str:
        return f"Prize: {self.x=},{self.y=}"


@dataclass
class Machine:
    """Class representing a single machine

    Attributes:
        button_a: Button A attributes
        button_b: Button B attributes
        prize: Prize attributes
        id_number: Machine ID number
        solvable: Is the machine solvable/winnable?
        a_presses: Presses of button A to win.
        b_presses: Presses of button B to win.
    """

    button_a: Button
    button_b: Button
    prize: Prize
    id_number: int

    @property
    def cost_to_win(self) -> Fraction:
        """Calculate and return the cost to win with this machine.

        Returns:
            Cost to win as a Fraction/Int.
        """
        return (self.button_a.cost * self.a_presses) + (
            self.button_b.cost * self.b_presses
        )

    # Slope check = -(A/B)==-(D/F)
    #   -(buttonax/buttonbx)==-(buttonay/buttonby)
    # Solve for x = (b1c2-b2c1)/(a1b2-a2b1)
    #   (buttonbx*prizex-buttonby*prizex)/(buttonax*buttonby-buttonay*buttonbx)
    # Solve for y = (c1a2-c2a1)/(a1b2-a2b1)
    #   (prizex*buttonay-prizey*buttonax)/(buttonax*buttonby-buttonay*buttonbx)
    @property
    def solvable(self) -> bool:
        """Is this machine solvable/winnable?

        Returns:
            Boolean of True if solvable/winnable, false if not.
        """
        # Check slopes for parallel lines.
        if Fraction(-self.button_a.x, self.button_b.x) == Fraction(
            -self.button_a.y, self.button_b.y
        ):
            return False
        # Check for non-rational button presses.
        if not self.a_presses.is_integer() or not self.b_presses.is_integer():
            return False
        return True

    @property
    def a_presses(self) -> Fraction:
        """Number of presses on button A to win.

        Returns:
            Number of button A presses to win.
        """
        return Fraction(
            (
                self.button_b.x * -self.prize.y
                - self.button_b.y * -self.prize.x
            ),
            (
                self.button_a.x * self.button_b.y
                - self.button_a.y * self.button_b.x
            ),
        )

    @property
    def b_presses(self) -> Fraction:
        """Number of presses on button B to win.

        Returns:
            Number of button B presses to win.
        """
        return Fraction(
            (-self.prize.x * self.button_a.y + self.prize.y * self.button_a.x),
            (
                self.button_a.x * self.button_b.y
                - self.button_a.y * self.button_b.x
            ),
        )


def get_input(filename: str):
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def parse_input(input_data: list[str]) -> list[Machine]:
    """Parse the input into objects.

    Args:
        input_data: List of strings from the input

    Returns:
        List of initialized machine objects.
    """
    id_number = 0
    machines: list[Machine] = []
    button_a = None
    button_b = None
    prize = None
    for string in input_data:
        if "Button A" in string:
            button_a = Button(string=string, cost=BUTTON_A_COST)
        if "Button B" in string:
            button_b = Button(string=string, cost=BUTTON_B_COST)
        if "Prize" in string:
            prize = Prize(string=string)
        if string == "" and button_a and button_b and prize:
            machines.append(
                Machine(
                    button_a=button_a,
                    button_b=button_b,
                    prize=prize,
                    id_number=id_number,
                )
            )
            id_number += 1
    return machines


def get_total_cost(machines: list[Machine]) -> int | Fraction:
    """Calculate the final answer

    Args:
        machines: List of the machine objects

    Returns:
        Total cost to win.
    """
    total = 0
    for machine in machines:
        if not machine.solvable:
            continue
        total += machine.cost_to_win
    print(f"TOTAL COST TO WIN: {total}")
    return total


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    input_data = get_input("day13example")
    machines = parse_input(input_data)
    assert machines[0].id_number == 0
    assert machines[0].button_a.x == 94
    assert machines[0].button_a.y == 34
    assert machines[0].button_b.x == 22
    assert machines[0].button_b.y == 67
    assert machines[0].button_a.cost == 3
    assert machines[0].button_b.cost == 1
    assert machines[0].prize.x == 10000000008400
    assert machines[0].prize.y == 10000000005400
    assert machines[0].solvable is False
    assert machines[1].solvable is True
    assert machines[2].solvable is False
    assert machines[3].solvable is True
    get_total_cost(machines=machines)


def main():
    """Get the answer"""
    input_data = get_input("day13input")
    machines = parse_input(input_data)
    get_total_cost(machines=machines)


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
