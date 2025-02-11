"""Code for day 24 part 2

I let myself struggle on this one for a while. Thought there might be some way
to use boolean algebra to simplify and identify the issue. But while I could
see a bit of a pattern forming, I couldn't tell why. I could also identify
where the addition started going wrong by bit index, but not by gates.

Thanks to https://github.com/D3STNY27/advent-of-code-2024/blob/main/day-24/part-2.py
I was able to see there is a way to logically parse the ripple adder logic.
"""

# pylint: disable=logging-fstring-interpolation


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
        self.processed = True


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
    return ret_gates


def produce_num(
    wires: dict[str, bool | None], wire_label: str = "z", as_bin: bool = False
) -> int | list[int]:
    """Return number from the binary conversion for the given wire_label."""
    label_dict: dict[str, bool] = {}
    for key, val in wires.items():
        if wire_label in key:
            if val is None:
                continue
                # raise RuntimeError(f"Got None on a {wire_label} wire somehow.")
            label_dict[key] = val
    label_keys = list(label_dict.keys())
    label_keys.sort(reverse=True)
    binary = "0b"
    binary_list = []
    for label_key in label_keys:
        binary += str(int(label_dict[label_key]))
        binary_list.append(int(label_dict[label_key]))
    logging.debug(
        f"produce_num: {wire_label=}, {binary=}, {int(binary,base=2)}"
    )
    if as_bin:
        return binary_list
    return int(binary, base=2)


def find_gate(
    gates: list[Gate],
    in1: str | None = None,
    in2: str | None = None,
    out: str | None = None,
    instruction: str | None = None,
) -> Gate:
    """Find and return the gate matching the provided args."""
    logging.debug(f"find_gate: {in1=}, {in2=}, {out=}, {instruction=}")

    for gate in gates:
        if in1 and in1 not in [gate.in1, gate.in2]:
            continue
        if in2 and in2 not in [gate.in1, gate.in2]:
            continue
        if out and gate.out != out:
            continue
        if instruction and gate.instruction != instruction:
            continue
        # Break if we get past all the filters to return the gate.
        break
    else:
        raise RuntimeError("find_gate didn't find gate.")

    logging.debug(f"find_gate: {gate=}")
    return gate


def swap_output_wires(
    wire_a: str, wire_b: str, gates: list[Gate]
) -> list[Gate]:
    """Swaps the outputs for the gates with matching wires."""
    new_configurations: list[Gate] = []

    for gate in gates:

        if gate.out == wire_a:
            gate.out = wire_b
            new_configurations.append(gate)

        elif gate.out == wire_b:
            gate.out = wire_a
            new_configurations.append(gate)

        else:
            new_configurations.append(gate)

    return new_configurations


def check_adders(gates: list[Gate]):
    """Check for consistent adder logic and note swaps."""
    max_bit = max(
        gates, key=lambda x: int(x.out[1:]) if x.out[0] == "z" else 0
    )
    max_bit = int(max_bit.out[1:])
    logging.debug(f"{max_bit=}")
    current_carry_wire = None
    swaps = []
    bit = 0

    while True:
        x_wire = f"x{bit:02d}"
        y_wire = f"y{bit:02d}"
        z_wire = f"z{bit:02d}"

        if bit == 0:
            current_carry_wire = find_gate(
                gates=gates, in1=x_wire, in2=y_wire, instruction="AND"
            ).out
        else:
            ab_xor_gate = find_gate(
                gates=gates, in1=x_wire, in2=y_wire, instruction="XOR"
            ).out
            ab_and_gate = find_gate(
                gates=gates, in1=x_wire, in2=y_wire, instruction="AND"
            ).out

            try:
                cin_ab_xor_gate = find_gate(
                    gates=gates,
                    in1=ab_xor_gate,
                    in2=current_carry_wire,
                    instruction="XOR",
                ).out
            except RuntimeError:
                cin_ab_xor_gate = None
            if cin_ab_xor_gate is None:
                swaps.append(ab_xor_gate)
                swaps.append(ab_and_gate)
                gates = swap_output_wires(ab_xor_gate, ab_and_gate, gates)
                bit = 0
                continue

            if cin_ab_xor_gate != z_wire:
                swaps.append(cin_ab_xor_gate)
                swaps.append(z_wire)
                gates = swap_output_wires(cin_ab_xor_gate, z_wire, gates)
                bit = 0
                continue

            cin_ab_and_gate = find_gate(
                gates=gates,
                in1=ab_xor_gate,
                in2=current_carry_wire,
                instruction="AND",
            ).out

            carry_wire = find_gate(
                gates=gates,
                in1=ab_and_gate,
                in2=cin_ab_and_gate,
                instruction="OR",
            ).out
            current_carry_wire = carry_wire

        bit += 1
        if bit >= max_bit:
            break

    return swaps


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.DEBUG)
    wires, gates = get_input("day24input")
    wires = parse_wire_declarations(wires)
    gates = parse_gates(gates, wires)
    swaps = check_adders(gates=gates)
    swaps = ",".join(sorted(swaps))
    logging.critical(f"{swaps=}")


if __name__ == "__main__":
    main()
