"""Code for day 1."""

# PART 1
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
total_distance = 0
for l, r in zip(left_list, right_list):
    total_distance = total_distance + abs(l - r)

print(total_distance)

# PART 2
# Didn't realize there were parts...

# For each item in left list:
#   Get count of item in right list.
#   Multiply item by count.
#   Add return to global.
total_similarity = 0
for i in left_list:
    total_similarity = total_similarity + (i * right_list.count(i))

print(total_similarity)
