"""Code for day 11 part 2

I had to look up how to do this...
I tried various methods and using cache but wasn't making much progress.
Used https://www.youtube.com/watch?v=b-1WDxUlubc as a guide.
"""

import cProfile
import math
from functools import cache


def get_input_dict(filename: str) -> dict:
    """Read the file and return a dictionary of stones."""
    with open(filename, "r", encoding="utf-8") as input_data:
        data = input_data.read().strip()
    numbers = [int(i) for i in data.split()]
    stones = {}
    for i in numbers:
        stones[i] = 1
    return stones


@cache
def math_size(i):
    """Use log10 to get number of digits."""
    return int(math.log10(i)) + 1


@cache
def split_stone(stone: int, stone_size: int) -> tuple[int, int]:
    """Split the stone in two"""
    stone_string = str(stone)
    half_stone = stone_size // 2
    stone1 = int(stone_string[:half_stone])
    stone2 = int(stone_string[half_stone:])
    return stone1, stone2


def dict_add(dict_in: dict, key: int, value: int):
    """Check for key and add if it doesn't exist"""
    if key in dict_in:
        dict_in[key] += value
    else:
        dict_in[key] = value


def blink_once_dict(stones) -> dict:
    """Use a dict to store stone information"""
    new_stones = {}
    for stone, freq in stones.items():
        if stone == 0:
            dict_add(new_stones, 1, freq)
            continue
        if math_size(stone) % 2 == 0:
            stone1, stone2 = split_stone(stone, math_size(stone))
            dict_add(new_stones, stone1, freq)
            dict_add(new_stones, stone2, freq)
            continue
        dict_add(new_stones, stone * 2024, freq)
    return new_stones


def blink(stones: dict, qty: int = 1) -> dict:
    """Observe stones and blink the qty of times."""
    # Loop for blink qty.
    for i in range(qty):
        print(f"Progress: {(i+1)}/{qty}")
        stones = blink_once_dict(stones)
    return stones


def debug_and_tests():
    """Test using the sample and examples first."""
    stone_deque = get_input_dict("day11example1")
    blink(stone_deque, 1)
    assert split_stone(12, 2) == (1, 2)
    assert split_stone(1234, 4) == (12, 34)

    # Longer example
    stone_deque = get_input_dict("day11example2")
    assert sum(blink(stone_deque, 6).values()) == 22
    assert sum(blink(stone_deque, 25).values()) == 55312


def main():
    """Get the answer"""
    stone_dict = get_input_dict("day11input")
    final_stones = blink(stone_dict, 75)
    print(sum(final_stones.values()))


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    cProfile.run("main()")
