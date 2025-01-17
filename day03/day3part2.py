"""Code for day 3 part 2."""

import re

# Open and read out the input.
with open("day3input", "r", encoding="utf-8") as input_data:
    memory: str = input_data.read()

# Regex pattern.
MY_PATTERN = r"mul\(\d+,\d+\)|don't\(\)|do\(\)"

# Find all the matches of the pattern in the input.
matches = re.findall(MY_PATTERN, memory)

total_sum: int = 0
enabled: bool = True
for m in matches:
    # Check if we need to disable/handle don't().
    if m == r"don't()":
        if enabled:
            enabled: bool = False
        continue

    # Check if we need to enable/handle do().
    if m == r"do()":
        if not enabled:
            enabled: bool = True
        continue

    # Should be left with mul(x,y) at this point.
    if enabled:
        # Strip off unnecessary characters.
        stripped = m.strip(r"mul()")
        # Split on the comma.
        x, y = stripped.split(",")
        # Convert the strings to int, multiply, and sum.
        print(f"mul({x}*{y})")
        total_sum += int(x) * int(y)
        print(f"{total_sum=}")
    else:
        print(f"ignoring {m}")
