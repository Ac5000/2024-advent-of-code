"""Code for day 22"""

# pylint: disable=logging-fstring-interpolation

from __future__ import annotations

import logging
from functools import cache
from typing import Iterator

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


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
