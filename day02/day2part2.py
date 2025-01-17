"""Code for day 2 part 2."""

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


def assert_safe_levels(report: list[int]) -> bool:
    """Combine two functions into one for tests."""
    return assert_safe_level_changes(report) & assert_increasing_decreasing(
        report
    )


def dampen_level_change(report: list[int]) -> bool:
    """Figure out if we can remove a number to pass."""
    # We taking the ineffecient/lazy path here...
    for i, _ in enumerate(report):
        # Copy list to not affect original.
        temp_report = report.copy()
        # Remove a level.
        temp_report.pop(i)
        # Check if the new report passes.
        if assert_safe_levels(temp_report):
            print(f"Saved {report} by removing {report[i]}")
            return True
    # Couldn't make the report pass.
    return False


# Finally check the reports against our functions
safe_reports: int = 0
initially_unsafe_reports: list[list[int]] = []
for report_ in reports:
    if not assert_safe_level_changes(report_):
        initially_unsafe_reports.append(report_)
        continue
    if not assert_increasing_decreasing(report_):
        initially_unsafe_reports.append(report_)
        continue
    safe_reports += 1

print(f"Total reports scanned = {len(reports)}")
print(f"Safe reports pre-dampen {safe_reports}")

# Recheck with dampener.
really_unsafe_reports: list[list[int]] = []
for unsafe_report in initially_unsafe_reports:
    if not dampen_level_change(unsafe_report):
        really_unsafe_reports.append(unsafe_report)
        continue
    safe_reports += 1

print(f"Safe reports post-dampen {safe_reports}")
