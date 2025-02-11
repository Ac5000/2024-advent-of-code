"""Code for day 25"""

# pylint: disable=logging-fstring-interpolation

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)

max_overlap: int = 0


def get_input(filename: str) -> list[list[str]]:
    """Read the file and return lines

    Args:
        filename (str): Path to file to open.

    Returns:
        List of lists of strings from the file. Each primary list is a key/lock.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    ret_lists = []
    temp_list = []
    for line in lines:
        logging.debug(f"{line=}")
        if line == "":
            ret_lists.append(temp_list)
            temp_list = []
            continue
        temp_list.append(line)
    ret_lists.append(temp_list)

    logging.debug(f"get_input: {ret_lists=}")
    return ret_lists


def parse_input(lines: list[str]) -> tuple[bool, tuple]:
    """Parse the strings to determine if lock or key.

    Args:
        lines (list[str]): List of strings that make up a lock/key.

    Returns:
        Tuple of bool, tuple. Bool is true if the 2nd tuple is a lock."""
    lock = False

    # Create a list to store index values based on the size of the strings.
    values = []
    max_len = len(max(lines, key=len))
    for _ in range(max_len):
        values.append(0)

    if lines[-1] == "." * max_len:
        lock = True
    for line in lines[1:-1]:
        for i, char in enumerate(line):
            if char == "#":
                values[i] += 1

    values = tuple(values)
    logging.debug(f"parse_input: {lock=},{values=}")
    return lock, values


def parse_inputs(inputs: list[list[str]]) -> tuple[set[tuple], set[tuple]]:
    """Parse the inputs into locks and keys.

    Args:
        inputs (list[list[str]]): List of lists of strings from the input file.

    Returns:
        Tuple of sets of tuples. First set is locks, second is keys.
    """
    # pylint: disable=global-statement
    global max_overlap
    max_overlap = len(max(inputs, key=len)) - 2
    locks: set[tuple] = set()
    keys: set[tuple] = set()

    for input_ in inputs:
        is_lock, values = parse_input(input_)
        if is_lock:
            locks.add(values)
        else:
            keys.add(values)
    logging.debug(f"{keys=}\n{locks=}")
    return locks, keys


def find_fitting_keys(keys: set[tuple], lock: tuple) -> int:
    """Find the number of keys that fit the lock"""
    temp_keys = set()
    for i, tumbler in enumerate(lock):
        for key in keys:
            if tumbler + key[i] <= max_overlap:
                logging.debug(f"{lock=}, {tumbler=}, {key=}, {i=}")
                temp_keys.add(key)
        keys = temp_keys
        temp_keys = set()
    ret_val = len(keys)

    logging.debug(f"find_fitting_keys: {lock=}, {ret_val=}")
    return ret_val


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    inputs = get_input("day25example1")
    assert parse_input(inputs[0]) == (True, (0, 5, 3, 4, 3))
    locks, keys = parse_inputs(inputs=inputs)
    total = 0
    for lock in locks:
        total += find_fitting_keys(keys=keys, lock=lock)
    assert total == 3


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    inputs = get_input("day25input")
    locks, keys = parse_inputs(inputs=inputs)
    total = 0
    for lock in locks:
        total += find_fitting_keys(keys=keys, lock=lock)
    logging.critical(f"FINAL TOTAL = {total}")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
