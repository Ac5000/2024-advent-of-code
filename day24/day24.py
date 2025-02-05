"""Code for day 24"""

# pylint: disable=logging-fstring-interpolation

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


@dataclass
class Gate:
    """Dataclass representing a gate.

    Attributes:
        in1: Input 1 string
        in2: Input 2 string
        out: Output string
        instruction: Instruction type
        processed: False if the gate hasn't activated.
    """

    in1: str
    in2: str
    out: str
    instruction: str
    processed: bool = False

    def can_process(self, wires: dict[str, bool | None]) -> bool:
        """Look through the wires and check if inputs are not None.
        Also, don't process if already processed."""
        if (
            wires[self.in1] is not None
            and wires[self.in2] is not None
            and not self.processed
        ):
            return True
        return False

    def process(self, wires: dict[str, bool | None]) -> None:
        """Process/operate the gate."""
        if wires[self.in1] is None or wires[self.in2] is None:
            raise RuntimeError("Gate not ready to process.")
        if self.instruction == "AND":
            wires[self.out] = wires[self.in1] and wires[self.in2]
        elif self.instruction == "OR":
            wires[self.out] = wires[self.in1] or wires[self.in2]
        elif self.instruction == "XOR":
            wires[self.out] = wires[self.in1] ^ wires[self.in2]
        else:
            raise RuntimeError("Gate instruction is messed up.")


def get_input(filename: str) -> tuple[list[str], list[str]]:
    """Read the file and parse.

    Args:
        filename (str): Path to file to open.

    Returns:
        Two lists of strings. First is wires, second is gates.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    for i, line in enumerate(lines):
        if line == "":
            return lines[:i], lines[i + 1 :]
    raise RuntimeError("Didn't find the empty line")


def parse_wire_declarations(wires: list[str]) -> dict[str, bool | None]:
    """Convert the input text to a dictionary"""
    ret_dict: dict[str, bool | None] = {}
    for wire in wires:
        key, val = wire.split(": ", maxsplit=2)
        # Convert string to bool
        val = val == "1"
        ret_dict[key] = val
    logging.debug(f"parse_wire_declarations: {ret_dict=}")
    return ret_dict


def parse_gates(gates: list[str], wires: dict[str, bool | None]) -> list[Gate]:
    """Convert gate strings into gate objects and add wires to wire dictionary."""
    ret_gates: list[Gate] = []
    for gate in gates:
        keys = [in1, in2, out] = re.split(
            r" AND | OR | XOR | -> ", gate, maxsplit=3
        )
        logging.debug(f"{in1=}, {in2=}, {out=}")
        for key in keys:
            if key not in wires:
                wires[key] = None
        # Note the order of the instructions is important since OR in XOR...
        for instruction in ["AND", "XOR", "OR"]:
            if instruction in gate:
                break
        else:
            raise RuntimeError("Didn't find instruction in gate text.")
        ret_gates.append(
            Gate(in1=in1, in2=in2, out=out, instruction=instruction)
        )

    logging.debug(f"parse_gates: {ret_gates=}")
    return ret_gates


def produce_num(wires: dict[str, bool | None]) -> int:
    """Ultimately, the system is trying to produce a number by combining the
    bits on all wires starting with z. z00 is the least significant bit, then
    z01, then z02, and so on."""
    # Find key:vals with z
    z_dict: dict[str, bool] = {}
    for key, val in wires.items():
        if "z" in key:
            if val is None:
                raise RuntimeError("Got None on a z wire somehow.")
            z_dict[key] = val
    logging.debug(f"{z_dict=}")
    z_keys = list(z_dict.keys())
    z_keys.sort(reverse=True)
    binary = "0b"
    for z_key in z_keys:
        binary += str(int(z_dict[z_key]))
    logging.debug(f"{binary=}")
    logging.critical(f"FINAL NUMBER: {int(binary,base=2)}")
    return int(binary, base=2)


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    # Example 1
    wires, gates = get_input("day24example1")
    wires = parse_wire_declarations(wires)
    gates = parse_gates(gates, wires)
    while None in wires.values():
        for gate in gates:
            if gate.can_process(wires):
                gate.process(wires)
    assert produce_num(wires) == 4

    # Example 2
    wires, gates = get_input("day24example2")
    wires = parse_wire_declarations(wires)
    gates = parse_gates(gates, wires)
    while None in wires.values():
        for gate in gates:
            if gate.can_process(wires):
                gate.process(wires)
    assert produce_num(wires) == 2024


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    wires, gates = get_input("day24input")
    wires = parse_wire_declarations(wires)
    gates = parse_gates(gates, wires)
    while None in wires.values():
        for gate in gates:
            if gate.can_process(wires):
                gate.process(wires)
    produce_num(wires)


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
