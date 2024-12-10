"""Code for day 2."""

# Reports = Lines
# Levels = Each item on the line
# Must be all increasing or all decreasing
# Levels must differ by 1-3.
# Return the quantity of reports that match both conditions.

# Take input and get a list for each report and convert to ints. (List of lists)
reports: list[list[int]] = []

with open("day2input", "r", encoding="utf-8") as input_data:
    for line in input_data:
        reports.append([int(i) for i in line.split()])


def assert_increasing_decreasing(report: list[int]) -> bool:
    """Assert if the report is all increasing or all decreasing"""
    prev_level: int = 0
    increasing: bool = True

    for i, level in enumerate(report):
        # Continue past first since we need two numbers to compare.
        if i == 0:
            prev_level = level
            continue

        # Catch equals early
        if level == prev_level:
            return False

        # Determine increasing/decreasing on second level only since the rest
        # of the levels should be the same.
        if i == 1:
            if level > prev_level:
                increasing = True
            if level < prev_level:
                increasing = False
            prev_level = level
            continue

        # Check for all increasing.
        if increasing:
            if level <= prev_level:
                return False

        # Check for all decreasing.
        if not increasing:
            if level >= prev_level:
                return False

        prev_level = level

    # Made it through without returning a False, must be True.
    return True


# # True
test_report = [56, 57, 60, 63, 65, 67, 68, 70]
assert assert_increasing_decreasing(test_report)

# False
test_report = [56, 56, 60, 63, 65, 67, 68, 70]
assert not assert_increasing_decreasing(test_report)

# False
test_report = [56, 57, 60, 60, 65, 67, 68, 70]
assert not assert_increasing_decreasing(test_report)

# True
test_report = [56, 55, 54, 34]
assert assert_increasing_decreasing(test_report)


def assert_safe_level_changes(report: list[int]) -> bool:
    """Check that all the levels are changing by 1-3"""
    prev_level: int = 0

    for i, level in enumerate(report):
        # Continue past first since we need two numbers to compare.
        if i == 0:
            prev_level = level
            continue

        # Catch equals early
        if level == prev_level:
            return False

        # Check difference within acceptable limits
        if abs(prev_level - level) < 1 or abs(prev_level - level) > 3:
            return False
        prev_level = level

    # Got through the list without any values exceeding safe differences.
    return True


test_report = [56, 57, 60, 62]
assert assert_safe_level_changes(test_report)

test_report = [56, 57, 60, 63]
assert assert_safe_level_changes(test_report)

test_report = [56, 56]
assert not assert_safe_level_changes(test_report)

test_report = [7, 6, 4, 2, 1]
assert assert_safe_level_changes(test_report)

test_report = [1, 2, 7, 8, 9]
assert not assert_safe_level_changes(test_report)

# Finally check the reports against our functions
safe_reports: int = 0
for report in reports:
    if not assert_safe_level_changes(report):
        print(f"{report} - Failed for level change.")
        continue
    if not assert_increasing_decreasing(report):
        print(f"{report} - Failed for increasing/decreasing.")
        continue
    safe_reports += 1

print(f"Total reports scanned = {len(reports)}")
print(f"{safe_reports=}")
