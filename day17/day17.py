"""Code for day 17"""

# pylint: disable=logging-fstring-interpolation, too-many-instance-attributes

import logging
from collections.abc import Callable
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


@dataclass
class Computer:
    init_a: int = 0
    init_b: int = 0
    init_c: int = 0
    init_program: list[int] = field(default_factory=list)
    a_reg: int = 0
    b_reg: int = 0
    c_reg: int = 0
    program: list[int] = field(default_factory=list)
    output: list[int] = field(default_factory=list)
    pointer: int = 0
    pointer_jumped: bool = False

    def __post_init__(self):
        self.a_reg = self.init_a
        self.b_reg = self.init_b
        self.c_reg = self.init_c
        self.program = self.init_program
        self.run_program()

    def run_program(self):
        """Run the program"""
        logging.info("Program Started")
        while True:
            opcode, operand = self.get_ops()
            logging.debug(f"{opcode=},{operand=}")
            if opcode is None:
                logging.info("Program Halting")
                break
            instruction = self.get_instruction(opcode)
            output = instruction(operand)
            if output is not None:
                self.output.append(output)
            self.mov_pointer()
            logging.debug(f"Current output: {self.output}")
        logging.info("Program Complete")
        logging.info(f"{self}")

    def mov_pointer(self) -> None:
        """Move the pointer unless jumped is true."""
        logging.debug(f"mov_pointer: {self.pointer_jumped=}")
        if self.pointer_jumped:
            self.pointer_jumped = (
                False  # Assume they meant only 1 instruction?
            )
            return
        self.pointer += 2
        logging.debug(f"mov_pointer: {self.pointer=}")

    def get_ops(self) -> tuple[int | None, int | None]:
        """Get the opcode and operand"""
        try:
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
        except IndexError:
            logging.warning("Pointer IndexError, Halting.")
            return None, None
        return opcode, operand

    def literal_op(self, operand: int) -> int:
        """Return the value of the literal operand."""
        return operand

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
        logging.debug(f"adv called with {operand=}")
        numerator = self.a_reg
        denominator = pow(2, self.combo_op(operand))
        self.a_reg = int(numerator / denominator)
        logging.debug(f"adv return: {numerator=},{denominator=},{self.a_reg=}")

    def bxl(self, operand: int) -> None:
        """Bitwise XOR"""
        self.b_reg = self.b_reg ^ self.literal_op(operand)

    def bst(self, operand: int) -> None:
        """Modulo"""
        self.b_reg = self.combo_op(operand) % 8

    def jnz(self, operand: int) -> None:
        """Jump"""
        if self.a_reg == 0:
            return
        self.pointer = self.literal_op(operand)
        self.pointer_jumped = True

    def bxc(self, operand: int) -> None:
        """Bitwise XOR Registers"""
        _ = operand  # For legacy reasons...
        logging.debug(f"bxc: {self.b_reg=},{self.c_reg=}")
        self.b_reg = self.b_reg ^ self.c_reg
        logging.debug(f"bxc returning: {self.b_reg=}")

    def out(self, operand: int) -> int:
        """Module out"""
        ret_val = self.combo_op(operand) % 8
        logging.debug(f"out: {ret_val=}")
        return ret_val

    def bdv(self, operand: int) -> None:
        """Division to B register"""
        numerator = self.a_reg
        denominator = pow(2, self.combo_op(operand))
        self.b_reg = int(numerator / denominator)

    def cdv(self, operand: int) -> None:
        """Division to C register"""
        numerator = self.a_reg
        denominator = pow(2, self.combo_op(operand))
        self.c_reg = int(numerator / denominator)

    def __str__(self) -> str:
        return (
            f"Computer: {self.a_reg=}\n{self.b_reg=}\n{self.c_reg=}\n"
            f"{self.output=}"
        )


def debug_and_tests():
    """Test using the sample and examples first."""
    # Initial tests of logic
    computer = Computer(init_a=8)
    computer.adv(2)
    assert computer.a_reg == 2

    # If register C contains 9, the program 2,6 would set register B to 1.
    computer = Computer(init_c=9, init_program=[2, 6])
    assert computer.b_reg == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    computer = Computer(init_a=10, init_program=[5, 0, 5, 1, 5, 4])
    assert computer.output == [0, 1, 2]

    # If register A contains 2024, the program 0,1,5,4,3,0 would output
    # 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    computer = Computer(init_a=2024, init_program=[0, 1, 5, 4, 3, 0])
    assert computer.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert computer.a_reg == 0

    # If register B contains 29, the program 1,7 would set register B to 26.
    computer = Computer(init_b=29, init_program=[1, 7])
    assert computer.b_reg == 26

    # If register B contains 2024 and register C contains 43690, the program
    # 4,0 would set register B to 44354.
    computer = Computer(init_b=2024, init_c=43690, init_program=[4, 0])
    assert computer.b_reg == 44354

    # Example program at end.
    computer = Computer(init_a=729, init_program=[0, 1, 5, 4, 3, 0])
    assert computer.output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]


def main():
    """Get the answer"""
    computer = Computer(
        init_a=59590048,
        init_b=0,
        init_c=0,
        init_program=[2, 4, 1, 5, 7, 5, 0, 3, 1, 6, 4, 3, 5, 5, 3, 0],
    )


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
