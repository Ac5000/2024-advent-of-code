"""Code for day 9"""

from collections import deque
from itertools import repeat


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


def first_empty(filesystem: deque) -> int:
    """Return the first empty fileblock"""
    return filesystem.index(".")


def last_block(filesystem: deque) -> int:
    """Return the last fileblock index with something in it."""
    for i, fileblock in enumerate(reversed(filesystem)):
        if fileblock != ".":
            return len(filesystem) - 1 - i
    raise IndexError("No blocks found")


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


def calc_checksum(filesystem: deque) -> int:
    """Calculate the checksum for the filesystem."""
    checksum: int = 0
    for i, fileblock in enumerate(filesystem):
        # Break once we hit the freespace since it should be defragged.
        if fileblock == ".":
            break
        checksum += fileblock * i
    return checksum


def debug_and_tests():
    """Test using the sample and examples first."""
    disk_map = get_input("day9example")
    assert disk_map == "2333133121414131402"
    filesystem = disk_map_to_filesystem(disk_map)
    for i, j in zip("00...111...2...333.44.5555.6666.777.888899", filesystem):
        assert i == str(j)
    assert 2 == first_empty(filesystem)
    assert 9 == filesystem[last_block(filesystem)]
    move_block(filesystem, last_block(filesystem), first_empty(filesystem))
    for i, j in zip("009..111...2...333.44.5555.6666.777.88889.", filesystem):
        assert i == str(j)
    defrag(filesystem)
    for i, j in zip("0099811188827773336446555566..............", filesystem):
        assert i == str(j)
    assert 1928 == calc_checksum(filesystem)


def main():
    """Get the answer"""
    disk_map = get_input("day9input")
    filesystem = disk_map_to_filesystem(disk_map)
    print("STARTING DEFRAG")
    defrag(filesystem)
    print(calc_checksum(filesystem))


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
