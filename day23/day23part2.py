"""Code for day 23"""

# pylint: disable=logging-fstring-interpolation

from __future__ import annotations

import logging
from typing import Iterable, Iterator

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


def get_input(filename: str) -> Iterator[tuple[str, str]]:
    """Read the file and parse.

    Args:
        filename (str): Path to file to open.

    Yields:
        Connections as a tuple of two strings.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    for line in lines:
        computer_connection = tuple(line.split("-"))
        logging.debug(f"get_input: {computer_connection=}")
        yield computer_connection


def connections_to_dict(
    connections: Iterable[tuple[str, str]],
) -> dict[str, set[str]]:
    """Convert connections to a dictionary where each key is a computer name
    and the values for the key are a set of computer names it is connected to.
    """
    ret_dict: dict[str, set[str]] = {}
    for comp1, comp2 in connections:
        if comp1 not in ret_dict:
            ret_dict[comp1] = {comp2}
        else:
            ret_dict[comp1].add(comp2)
        if comp2 not in ret_dict:
            ret_dict[comp2] = {comp1}
        else:
            ret_dict[comp2].add(comp1)

    # logging.debug(f"connections_to_dict: {ret_dict=}")
    print(*ret_dict.items(), sep="\n")
    return ret_dict


def filter_triples(connections: dict[str, set[str]]) -> set[frozenset[str]]:
    """Filter the connections dictionary to a set of sets (frozensets) that
    represent three inter-connected computers."""

    triples: set = set()
    for key, computers in connections.items():
        for computer in computers:
            intersection = computers & connections[computer]
            if len(intersection) == 0:
                continue
            for inter in intersection:
                triples.add(frozenset((key, computer, inter)))
    logging.debug(f"filter_triples: {triples=}")
    return triples


def filter_sets_by_char(
    to_filter: set[frozenset[str]], char: str = "t"
) -> set[frozenset[str]]:
    """Filter the sets to only include those that start with the character."""
    ret_sets: set[frozenset[str]] = set()
    for subset in to_filter:
        for element in subset:
            if char == element[0]:
                ret_sets.add(subset)
                # break back to "to_filter" loop.
                break

    logging.debug(f"filter_sets_by_char: {ret_sets=}")
    return ret_sets


def find_max_intersection(connections: dict[str, set[str]]) -> set[str]:
    """Find the largest intersection amongst the connections."""
    # Also need to check each set has each of the elements in the intersection.
    ret_set: set = set()
    for key1, computers1 in connections.items():
        set_with_key1 = computers1
        set_with_key1.add(key1)
        for key2, computers2 in connections.items():
            # Skip same keys
            if key1 == key2:
                continue
            set_with_key2 = computers2
            set_with_key2.add(key2)
            logging.debug(f"{set_with_key1=} {set_with_key2=}")
            temp_intersection = set_with_key1 & set_with_key2
            if len(temp_intersection) < len(ret_set):
                continue
            # iterate each element in the connections using elements as keys
            # Check all the elements are in each value set of the dict.
            for element in temp_intersection:
                if not temp_intersection.issubset(connections[element]):
                    logging.debug(f"{element=} not in connections")
                    break
            else:
                logging.debug(f"FOUND NEW MAX{temp_intersection=}")
                ret_set = temp_intersection

    logging.debug(f"find_max_intersection: {ret_set=}")
    return ret_set


def decrypt_password(comp_names: set[str]) -> str:
    """The LAN party posters say that the password to get into the LAN party is
    the name of every computer at the LAN party, sorted alphabetically, then
    joined together with commas.
    """
    names = list(comp_names)
    names.sort()
    names = ",".join(names)
    logging.critical(f"FINAL PASSWORD: {names}")
    return names


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    connections = get_input("day23example1")
    connections_dict = connections_to_dict(connections)
    assert 12 == len((triples := filter_triples(connections_dict)))
    assert 7 == len(filter_sets_by_char(triples))
    assert (largest_set := find_max_intersection(connections_dict)) == {
        "co",
        "de",
        "ka",
        "ta",
    }
    assert decrypt_password(largest_set) == "co,de,ka,ta"


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    connections = get_input("day23input")
    connections_dict = connections_to_dict(connections)
    triples = filter_triples(connections_dict)
    final_set = filter_sets_by_char(triples)
    logging.critical(
        f"{len(final_set)} sets of 3 computers with one starting with t."
    )
    assert 1437 == len(final_set)
    decrypt_password(find_max_intersection(connections_dict))


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
