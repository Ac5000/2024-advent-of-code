"""Code for day 5."""

from collections.abc import Iterator
from graphlib import TopologicalSorter


def get_rules(filename: str) -> Iterator[tuple[int, int]]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    for line in lines:
        if "|" in line:
            x, y = line.split(sep="|")
            yield int(x), int(y)


def get_updates(filename: str) -> Iterator[list[int]]:
    """Read the file and yield updates."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    for line in lines:
        if "," in line:
            yield [int(i) for i in line.split(sep=",")]


def middle_page(update: list[int]) -> int:
    """Get the middle page number from the updates."""
    return update[len(update) // 2]


def topo_sorter(rules_pairs: list[tuple[int, int]]) -> list[int]:
    """Make a graph of the rules and put the sort into a deck.

    Can't just do all the rules though, they included a cycle error...
    """
    ts = TopologicalSorter()
    order_list: list[int] = []
    for rule in rules_pairs:
        # Node, Predecessor(s)
        ts.add(rule[1], rule[0])
    # Mark as finished and check for cycles.
    ts.prepare()

    # Put the nodes into a deck.
    while ts.is_active():
        for node in ts.get_ready():
            order_list.append(node)
            ts.done(node)

    return order_list


def get_applicable_rules(
    rules_pairs: list[tuple[int, int]], update: list[int]
) -> list[tuple[int, int]]:
    """Get rules that apply to the update."""
    applicable_rules: list[tuple[int, int]] = []
    for rule in rules_pairs:
        if rule[0] not in update or rule[1] not in update:
            continue
        applicable_rules.append(rule)
    return applicable_rules


if __name__ == "__main__":
    # Test using the sample and examples first.
    rules = get_rules("day5example")
    updates = get_updates("day5example")
    assert middle_page([75, 47, 61, 53, 29]) == 61
    assert middle_page([97, 61, 53, 29, 13]) == 53
    assert middle_page([75, 29, 13]) == 29
    rules = list(rules)
    final_result: int = 0
    for update_ in updates:
        app_rules = get_applicable_rules(rules, update_)
        order = topo_sorter(app_rules)
        if order == update_:
            final_result += middle_page(update_)
    assert final_result == 143

    # Actual Input

    rules = get_rules("day5input")
    updates = get_updates("day5input")
    rules = list(rules)
    final_result: int = 0
    for update_ in updates:
        app_rules = get_applicable_rules(rules, update_)
        order = topo_sorter(app_rules)
        if order == update_:
            final_result += middle_page(update_)
    print(final_result)
