"""Code for day 3."""

# Find "mul(X,Y)" instances.
# Multiply X*Y
# Sum with all found instances.

import re

# Open and read out the input.
with open("day3input", "r", encoding="utf-8") as input_data:
    memory: str = input_data.read()

# Regex pattern.
MY_PATTERN = r"mul\(\d+,\d+\)"

# Find all the matches of the pattern in the input.
matches = re.findall(MY_PATTERN, memory)

total_sum: int = 0

for m in matches:
    # Strip off unnecessary characters.
    stripped = m.strip(r"mul()")
    # Split on the comma.
    x, y = stripped.split(",")
    # Convert the strings to int, multiply, and sum.
    print(f"mul({x}*{y})")
    total_sum += int(x) * int(y)
    print(f"{total_sum=}")
