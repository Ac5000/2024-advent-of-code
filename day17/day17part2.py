"""Code for day 17 part 2

This one kicked my butt...

I've never worked with octal before, and had 0 clue where to start and had to
look for help online pretty quickly.

Turns out many people have incorrect solutions that happen to work
for their input, but not with mine for some reason...

They would all generate a solution, but it was not the lowest solution.

I tried 3 different people's solutions and trying to understand what was
going wrong, but couldn't get it until I found:
https://github.com/LiquidFun/adventofcode/blob/main/2024/17/17.py

Their solution provided a different answer that was lower than the others
and enabled me to get the correct answer.
"""

# pylint: disable=logging-fstring-interpolation, too-many-instance-attributes

from collections.abc import Callable
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


@dataclass
class Computer:
    """Class representing the computer."""

    a_reg: int = 0
    b_reg: int = 0
    c_reg: int = 0
    program: list[int] = field(default_factory=list)
    output: list[int] = field(default_factory=list)
    pointer: int = 0
    pointer_jumped: bool = False

    def __post_init__(self):
        self.run_program()

    def reset(self, a: int):
        """Reset the computer to initial state with a register."""
        self.a_reg = a
        self.b_reg = 0
        self.c_reg = 0
        self.output = []
        self.pointer = 0
        self.pointer_jumped = False

    def reset_run(self, a: int) -> list[int]:
        """Reset the computer to initial state with a, run, and return output."""
        self.reset(a=a)
        self.run_program()
        return self.output

    def run_program(self):
        """Run the program"""
        # logging.info("Program Started")
        while True:
            opcode, operand = self.get_ops()
            if opcode is None or operand is None:
                break
            instruction = self.get_instruction(opcode)
            instruction(operand)
            self.mov_pointer()
            # logging.debug(f"Current output: {self.output}")
        # logging.info("Program Complete")

    def mov_pointer(self) -> None:
        """Move the pointer unless jumped is true."""
        if self.pointer_jumped:
            self.pointer_jumped = False
            return
        self.pointer += 2

    def get_ops(self) -> tuple[int | None, int | None]:
        """Get the opcode and operand"""
        try:
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
        except IndexError:
            return None, None
        return opcode, operand

    def combo_op(self, operand: int) -> int:
        """Return the value of the combo operand."""
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.a_reg
        if operand == 5:
            return self.b_reg
        if operand == 6:
            return self.c_reg
        raise ValueError(f"combo_op received a bad operand: {operand}")

    def get_instruction(self, opcode: int) -> Callable:
        """Returns a callable instruction based on the opcode."""
        match opcode:
            case 0:
                return self.adv
            case 1:
                return self.bxl
            case 2:
                return self.bst
            case 3:
                return self.jnz
            case 4:
                return self.bxc
            case 5:
                return self.out
            case 6:
                return self.bdv
            case 7:
                return self.cdv
            case _:
                raise RuntimeError("Bad instruction opcode")

    def adv(self, operand: int) -> None:
        """Division"""
        self.a_reg = int(self.a_reg / 2 ** self.combo_op(operand))

    def bxl(self, operand: int) -> None:
        """Bitwise XOR"""
        self.b_reg = self.b_reg ^ operand

    def bst(self, operand: int) -> None:
        """Modulo"""
        self.b_reg = self.combo_op(operand) % 8

    def jnz(self, operand: int) -> None:
        """Jump"""
        if self.a_reg == 0:
            return
        self.pointer = operand
        self.pointer_jumped = True

    def bxc(self, operand: int) -> None:
        """Bitwise XOR Registers"""
        _ = operand  # For legacy reasons...
        self.b_reg = self.b_reg ^ self.c_reg

    def out(self, operand: int) -> None:
        """Module out"""
        self.output.append(self.combo_op(operand) % 8)

    def bdv(self, operand: int) -> None:
        """Division to B register"""
        self.b_reg = int(self.a_reg / 2 ** self.combo_op(operand))

    def cdv(self, operand: int) -> None:
        """Division to C register"""
        self.c_reg = int(self.a_reg / 2 ** self.combo_op(operand))


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    computer = Computer(a_reg=8)
    computer.adv(2)
    assert computer.a_reg == 2

    # If register C contains 9, the program 2,6 would set register B to 1.
    computer = Computer(c_reg=9, program=[2, 6])
    assert computer.b_reg == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    computer = Computer(a_reg=10, program=[5, 0, 5, 1, 5, 4])
    assert computer.output == [0, 1, 2]

    # If register A contains 2024, the program 0,1,5,4,3,0 would output
    # 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    computer = Computer(a_reg=2024, program=[0, 1, 5, 4, 3, 0])
    assert computer.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert computer.a_reg == 0

    # If register B contains 29, the program 1,7 would set register B to 26.
    computer = Computer(b_reg=29, program=[1, 7])
    assert computer.b_reg == 26

    # If register B contains 2024 and register C contains 43690, the program
    # 4,0 would set register B to 44354.
    computer = Computer(b_reg=2024, c_reg=43690, program=[4, 0])
    assert computer.b_reg == 44354

    # Example program at end.
    computer = Computer(a_reg=729, program=[0, 1, 5, 4, 3, 0])
    assert computer.output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]


def copy_check(program: list[int], a_reg: int):
    """Check program copy worked."""
    computer = Computer(a_reg=a_reg, program=program)
    assert computer.output == program
    logging.info(("copy_check passed", computer.output))


class FoundSolution(Exception):
    """Custom Exception to catch solution from bottom of recursion stack..."""


def main() -> tuple[list[int], int]:
    """Get the answer for part2."""
    # 105875099939593 was too high
    # 105_875_099_939_593 was too high
    # 105875099912602
    # 105_875_099_912_602 Correct Solution.

    # Check my answer from part 1 still true and I haven't messed up...
    program = [2, 4, 1, 5, 7, 5, 0, 3, 1, 6, 4, 3, 5, 5, 3, 0]
    computer = Computer(a_reg=59_590_048, program=program)
    assert computer.output == [6, 5, 7, 4, 5, 7, 3, 1, 0]
    logging.info(("Part1 Solution=", computer.output))

    def find_a(a_input: int, indx: int = 15) -> None:
        """Recursively searches through solutions."""
        if indx == -1:
            raise FoundSolution(a_input)
        while True:
            if program[indx:] == computer.reset_run(a_input)[indx:]:
                find_a(a_input, indx - 1)
            a_input += 8**indx

    # Something with octal going on based on length of program...
    starting_index = len(computer.program) - 1
    solution = 0
    try:
        find_a(8**starting_index)
    except FoundSolution as e:
        solution = int(str(e))
        print(f"First solution found: {solution:,}")

    return program, solution


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    copy_check(*main())
