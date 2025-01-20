"""Code for day 19."""

# pylint: disable=logging-fstring-interpolation

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


def get_input(filename: str) -> tuple[list[str], list[str]]:
    """Read the file and yield rules.

    Returns:
        First list is the towels, second list is the designs.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    towels = lines[0]
    designs = lines[2:]
    towels = towels.split(", ")
    towels.sort(key=len)

    logging.debug(towels)
    return towels, designs


def index_map(towels: list[str], design: str) -> bool:
    """For each towel, make a set of indexes that are covered.

    Can use the design (return true) if all indexes are covered.
    """
    logging.debug(f"index_map: {design=}")
    covered: set[int] = set()
    for towel in towels:
        logging.debug(f"index_map: {towel=}")
        idx = 0
        for _ in range(design.count(towel)):
            found = design.find(towel, idx)
            logging.debug(f"index_map: {found=}, {towel=}, {idx=}")
            for i in range(found, found + len(towel)):
                covered.add(i)
            idx = found + len(towel)

    logging.debug(f"index_map: {covered=}")
    if covered == {i for i, _ in enumerate(design)}:
        return True
    return False


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    towels, designs = get_input("day19example1")
    final_count = 0
    for design in designs:
        if index_map(towels, design):
            final_count += 1

    assert final_count == 6
    logging.critical(f"{final_count} Designs are Possible.")


def main():
    """Get the answer"""
    # 289 was too high?
    #   Found out that disolving as I went was generating new options.
    # 230 was too low?
    #   This came down to missing some combinations.
    # 247 was correct.
    logging.getLogger().setLevel(logging.INFO)
    towels, designs = get_input("day19input")
    final_count = 0
    for design in designs:
        if index_map(towels, design):
            final_count += 1

    assert final_count < 289
    assert final_count > 230
    logging.critical(f"{final_count} Designs are Possible.")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
