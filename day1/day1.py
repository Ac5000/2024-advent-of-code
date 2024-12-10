"""Code for day 1."""

# Take input and get 2 lists, left and right. (Separator is spaces)
left_list: list[int] = []
right_list: list[int] = []

with open("input", "r", encoding="utf-8") as input_data:
    for line in input_data:
        a, b = line.split()
        left_list.append(int(a))
        right_list.append(int(b))

# Sort both lists.
left_list.sort()
right_list.sort()

# For each pair:
#   Get absolute of subtraction.
#   Add return to global.
TOTAL_DISTANCE = 0
for l, r in zip(left_list, right_list):
    TOTAL_DISTANCE = TOTAL_DISTANCE + abs(l - r)

print(TOTAL_DISTANCE)
