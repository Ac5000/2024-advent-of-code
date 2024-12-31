"""Code for day 9 part 2"""

from collections import deque
from itertools import repeat, islice

last_file_id_inspected: int = 0


def get_input(filename: str) -> str:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        data = input_data.read().strip()
    return data


def disk_map_to_filesystem(disk_map: str) -> deque:
    """Read the disk map into deque"""
    filesystem: deque = deque()
    id_num = 0

    for i, c in enumerate(disk_map):
        # Evens -> File
        if not i % 2:
            filesystem.extend(repeat(id_num, int(c)))
            id_num += 1
        else:
            filesystem.extend(repeat(".", int(c)))
    return filesystem


def move_block(filesystem: deque, from_index: int, to_index: int):
    """Move the file block from->to"""
    from_value = filesystem[from_index]
    filesystem[to_index] = from_value
    filesystem[from_index] = "."


def swap_blocks(
    filesystem: deque, from_range: tuple[int, int], to_range: tuple[int, int]
):
    """Swaps the from and to ranges in the filesystem"""
    # Check and crash early if we somehow get mixed ranges.
    assert len(range(*from_range)) == len(range(*to_range))
    for from_index, to_index in zip(range(*from_range), range(*to_range)):
        temp = filesystem[to_index]
        filesystem[to_index] = filesystem[from_index]
        filesystem[from_index] = temp


def first_empty(filesystem: deque) -> int:
    """Return the first empty fileblock"""
    return filesystem.index(".")


def sliding_window(iterable, n: int) -> tuple[int, int] | None:
    """Collect data into overlapping fixed-length chunks or blocks."""
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for i, x in enumerate(iterator):
        window.append(x)
        if window.count(".") == n:
            return i, i + n
        continue
    return None


def last_block(filesystem: deque) -> tuple[int, object]:
    """Return the last fileblock index with ID."""
    for i, fileblock in enumerate(reversed(filesystem)):
        if fileblock != ".":
            return (len(filesystem) - 1 - i), fileblock
    raise IndexError("No blocks found")


def get_fileblock_range(filesystem: deque, file_id: int) -> tuple[int, int]:
    """Return the range notation for the file_id"""
    # Get the first index
    first_index = filesystem.index(file_id)
    # Get count of blocks with that ID
    block_count = filesystem.count(file_id)
    # Return a range
    return (first_index, first_index + block_count)


def defrag(filesystem: deque):
    """Defrag the filesystem"""
    empty: int = 0
    last: int = len(filesystem)
    length: int = last
    empty_blocks: int = filesystem.count(".")
    while empty < last:
        empty = first_empty(filesystem)
        last = last_block(filesystem)
        print(f"Progress:{abs(last-length)}/{empty_blocks}")
        # Break if we are at last defrag.
        if empty == last + 1:
            break
        move_block(filesystem, last, empty)
        # print("".join(str(x) for x in filesystem))
        # print(filesystem)


def defrag2(filesystem: deque):
    """Defrag the filesystem by blocks"""
    # Get last file ID
    last_file_id = filesystem[-1]
    denom = last_file_id
    while last_file_id > 0:
        print(f"Progress:{(last_file_id-0)/denom}")
        # Get fileblock range
        block_range = get_fileblock_range(filesystem, last_file_id)
        # Check for empty space large enough
        empty_range = sliding_window(
            filesystem, len(range(block_range[0], block_range[1]))
        )
        if empty_range is None:
            # No space for file.
            last_file_id -= 1
            continue
        if empty_range[0] >= block_range[0]:
            # Don't move blocks further back.
            last_file_id -= 1
            continue
        swap_blocks(filesystem, block_range, empty_range)
        last_file_id -= 1


def calc_checksum(filesystem: deque) -> int:
    """Calculate the checksum for the filesystem."""
    checksum: int = 0
    for i, fileblock in enumerate(filesystem):
        # Skip empty blocks
        if fileblock == ".":
            continue
        checksum += fileblock * i
    return checksum


def debug_and_tests():
    """Test using the sample and examples first."""
    print("RUNNING DEBUG AND TESTS")
    disk_map = get_input("day9example")
    assert disk_map == "2333133121414131402"
    filesystem = disk_map_to_filesystem(disk_map)
    for i, j in zip("00...111...2...333.44.5555.6666.777.888899", filesystem):
        assert i == str(j)
    assert 2 == first_empty(filesystem)
    assert (40, 42) == get_fileblock_range(filesystem, 9)
    assert (0, 2) == get_fileblock_range(filesystem, 0)
    assert (2, 4) == sliding_window(filesystem, 2)
    swap_blocks(filesystem, (40, 42), (2, 4))
    for i, j in zip("0099.111...2...333.44.5555.6666.777.8888..", filesystem):
        assert i == str(j)
    swap_blocks(filesystem, (2, 4), (40, 42))
    for i, j in zip("00...111...2...333.44.5555.6666.777.888899", filesystem):
        assert i == str(j)
    defrag2(filesystem)
    for i, j in zip("00992111777.44.333....5555.6666.....8888..", filesystem):
        assert i == str(j)
    final_checksum = calc_checksum(filesystem)
    assert final_checksum == 2858
    print(f"Final Checksum = {final_checksum}")
    print(list(filesystem))


def main():
    """Get the answer"""
    disk_map = get_input("day9input")
    filesystem = disk_map_to_filesystem(disk_map)
    print("STARTING DEFRAG")
    defrag2(filesystem)
    print(calc_checksum(filesystem))


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
