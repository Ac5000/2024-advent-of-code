"""Code for day 22 part 2"""

# pylint: disable=logging-fstring-interpolation

from __future__ import annotations

import logging
from collections import deque
from functools import cache
from itertools import islice
from typing import Any, Iterable, Iterator

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s ", level=logging.DEBUG)


def get_input(filename: str) -> Iterator[int]:
    """Read the file and parse.

    Args:
        filename (str): Path to file to open.

    Yields:
        Secret numbers as ints.
    """
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    for line in lines:
        logging.debug(f"get_input: {line=}")
        yield int(line)


@cache
def mix(secret_num: int, mixin: int) -> int:
    """To mix a value into the secret number, calculate the bitwise XOR of the
    given value and the secret number. Then, the secret number becomes the
    result of that operation."""
    ret_val = secret_num ^ mixin
    logging.debug(f"mix: {ret_val=}")
    return ret_val


@cache
def prune(secret_num: int) -> int:
    """To prune the secret number, calculate the value of the secret number
    modulo 16777216. Then, the secret number becomes the result of that
    operation."""
    ret_val = secret_num % 16777216
    logging.debug(f"prune: {ret_val=}")
    return ret_val


@cache
def step1(secret_num: int) -> int:
    """Calculate the result of multiplying the secret number by 64.
    Then, mix this result into the secret number.
    Finally, prune the secret number."""
    ret_val = secret_num * 64
    ret_val = mix(secret_num, ret_val)
    ret_val = prune(ret_val)
    logging.debug(f"step1: {ret_val=}")
    return ret_val


@cache
def step2(secret_num: int) -> int:
    """Calculate the result of dividing the secret number by 32.
    Round the result down to the nearest integer.
    Then, mix this result into the secret number.
    Finally, prune the secret number."""
    ret_val = secret_num // 32
    ret_val = mix(secret_num, ret_val)
    ret_val = prune(ret_val)
    logging.debug(f"step2: {ret_val=}")
    return ret_val


@cache
def step3(secret_num: int) -> int:
    """Calculate the result of multiplying the secret number by 2048.
    Then, mix this result into the secret number.
    Finally, prune the secret number."""
    ret_val = secret_num * 2048
    ret_val = mix(secret_num, ret_val)
    ret_val = prune(ret_val)
    logging.debug(f"step2: {ret_val=}")
    return ret_val


@cache
def evolve(secret_num: int) -> int:
    """Run the 3 steps to evolve the secret number into the next.

    Args:
        secret_num (int): Secret number to evolve

    Returns:
        New secret number as an integer.
    """
    new_secret_num = step3(step2(step1(secret_num)))
    logging.debug(f"evolve: {new_secret_num=}")
    return new_secret_num


def ones(init_num: int, secret_nums: list[int]) -> list[int]:
    """Read the secret numbers and return the ones places."""
    ret_vals: list[int] = []
    nums: list[int] = [init_num] + secret_nums
    for num in nums:
        ret_vals.append(num % 10)
    logging.debug(f"ones: {ret_vals=}")
    return ret_vals


def sliding_window(iterable: Iterable[Any], n: int) -> Iterator[tuple]:
    """Collect data into overlapping fixed-length chunks or blocks."""
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def get_changes(ones_digits: Iterable[int]) -> Iterator[tuple[int, int]]:
    """Return tuples of price and change."""
    for x, y in sliding_window(ones_digits, 2):
        yield y, (y - x)


def make_dict(
    changes: Iterable[tuple[int, int]],
    in_dict: dict[tuple[int, int, int, int], int],
) -> dict[tuple[int, int, int, int], int]:
    """For each 4 number changes, make element. Values are added.

    Track 4-number sequences to only add the first instance.
    """
    sequences: set[tuple[int, int, int, int]] = set()
    for change_series in sliding_window(changes, 4):
        key = ()
        for _, diff in change_series:
            key += (diff,)
        # after the hiding spot is sold, the monkey will move on to the next...
        if key in sequences:
            continue
        if key in in_dict:
            in_dict[key] += change_series[3][0]
        else:
            in_dict[key] = change_series[3][0]
        sequences.add(key)
    logging.debug(f"make_dict: {in_dict=}")
    return in_dict


def calc_final_score(buyer_numbers: dict[int, list[int]]) -> int:
    """Calculate the final score for answer"""
    final_score = 0
    for secret_numbers in buyer_numbers.values():
        final_score += secret_numbers[-1]
    logging.critical(f"The final total score is {final_score}")
    return final_score


def debug_and_tests():
    """Test using the sample and examples first."""
    logging.getLogger().setLevel(logging.DEBUG)
    _ = [print(i) for i in get_input("day22example1")]

    # If the secret number is 42 and you were to mix 15 into the secret number,
    # the secret number would become 37.
    assert mix(42, 15) == 37

    # If the secret number is 100000000 and you were to prune the secret
    # number, the secret number would become 16113920.
    assert prune(100000000) == 16113920

    # So, if a buyer had a secret number of 123, that buyer's next ten secret
    # numbers would be...
    secret_num = 123
    example_results = [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    for result in example_results:
        assert (secret_num := evolve(secret_num)) == result

    # Example 1
    buyers: dict[int, list[int]] = {}
    for init_secret in get_input("day22example1"):
        buyers[init_secret] = []
        num = init_secret
        for _ in range(2000):
            buyers[init_secret].append(num := evolve(num))

    # In this example, for each buyer, their initial secret number and the
    # 2000th new secret number they would generate are:
    assert buyers[1][-1] == 8685429
    assert buyers[10][-1] == 4700978
    assert buyers[100][-1] == 15273692
    assert buyers[2024][-1] == 8667524
    assert calc_final_score(buyers) == 37327623

    assert (ons := ones(123, example_results)) == [
        3,
        0,
        6,
        5,
        4,
        4,
        6,
        4,
        4,
        2,
        4,
    ]

    prices = make_dict(get_changes(ons), {})
    assert max(prices.values()) == 6
    assert prices[(-1, -1, 0, 2)] == 6
    prices = make_dict(get_changes(ons), prices)

    # Example 2
    buyers: dict[int, list[int]] = {}
    for init_secret in get_input("day22example2"):
        buyers[init_secret] = []
        num = init_secret
        for _ in range(2000):
            buyers[init_secret].append(num := evolve(num))
    prices = {}
    for key, vals in buyers.items():
        prices.update(make_dict(get_changes(ones(key, vals)), prices))
    assert prices[(-2, 1, -1, 3)] == 23
    assert max(prices.values()) == 23
    logging.debug(f"{max(prices.values())=}")


def main():
    """Get the answer"""
    logging.getLogger().setLevel(logging.INFO)
    buyers: dict[int, list[int]] = {}
    for init_secret in get_input("day22input"):
        buyers[init_secret] = []
        num = init_secret
        for _ in range(2000):
            buyers[init_secret].append(num := evolve(num))
    assert 15608699004 == calc_final_score(buyers)
    prices = {}

    # Part 2
    for key, vals in buyers.items():
        prices.update(make_dict(get_changes(ones(key, vals)), prices))
    logging.critical(f"{max(prices.values())=}")


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
