"""Code for day 11"""

import cProfile
from collections import deque


def get_input(filename: str) -> deque:
    """Read the file and return a deque of stones."""
    with open(filename, "r", encoding="utf-8") as input_data:
        data = input_data.read().strip()
    return deque([int(i) for i in data.split()])


def determine_rule(stone_number: int) -> int:
    """Determine what rule to use with the stone"""
    # If engraved with 0
    if stone_number == 0:
        return 0
    # If engraved with even number of DIGITS
    if not len(str(stone_number)) % 2:
        return 1
    # All others
    return 2


def split_stone(stone: int) -> list[int]:
    """Split the stone in two"""
    stone_string = str(stone)
    stone1 = int(stone_string[: (len(stone_string) // 2)])
    stone2 = int(stone_string[(len(stone_string) // 2) :])
    return [stone1, stone2]


def blink(stones: deque, qty: int = 1) -> deque:
    """Observe stones and blink the qty of times."""
    # Loop for blink qty.
    for _ in range(qty):
        new_order: deque = deque()
        # Loop the old deque
        for stone in stones:
            match determine_rule(stone):
                case 0:
                    new_order.append(1)
                case 1:
                    new_order.extend(split_stone(stone))
                case 2:
                    new_order.append(stone * 2024)
        stones = new_order
    return stones


def debug_and_tests():
    """Test using the sample and examples first."""
    stone_deque = get_input("day11example1")
    assert stone_deque == deque([0, 1, 10, 99, 999])
    assert determine_rule(0) == 0
    assert determine_rule(1) == 2
    assert determine_rule(11) == 1
    assert determine_rule(111) == 2
    blink(stone_deque, 1)
    assert split_stone(12) == [1, 2]
    assert split_stone(1234) == [12, 34]
    assert blink(stone_deque, 1) == deque([1, 2024, 1, 0, 9, 9, 2021976])

    # Longer example
    stone_deque = get_input("day11example2")
    assert stone_deque == deque([125, 17])
    assert blink(stone_deque, 1) == deque([253000, 1, 7])
    assert blink(stone_deque, 2) == deque([253, 0, 2024, 14168])
    assert blink(stone_deque, 3) == deque([512072, 1, 20, 24, 28676032])
    assert blink(stone_deque, 4) == deque(
        [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    )
    assert blink(stone_deque, 5) == deque(
        [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
    )
    # I got tired of manually parsing...
    assert blink(stone_deque, 6) == deque(
        [
            int(i)
            for i in "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2".split()
        ]
    )
    assert len(blink(stone_deque, 6)) == 22
    assert len(blink(stone_deque, 25)) == 55312


def main():
    """Get the answer"""
    stone_deque = get_input("day11input")
    print(len(blink(stone_deque, 25)))


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    cProfile.run("main()")
