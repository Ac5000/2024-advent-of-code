"""Code for day 4."""

from collections.abc import Iterable
from dataclasses import dataclass, field


def find_xmas(chars: list[str]) -> bool:
    """Return True if the list of characters is "XMAS"."""
    # Wrong length list.
    if len(chars) != 4:
        return False

    combined: str = ""
    for character in chars:
        combined += character.upper()
    if combined == "XMAS":
        return True
    return False


def coords_to_chars(
    coords: list[tuple[int, int]], matrix: list[str]
) -> list[str]:
    """Convert list of coordinates to list of characters."""
    if not coords:
        return []
    chars: list[str] = []
    for coord in coords:
        chars.append(matrix[coord[0]][coord[1]])
    assert chars[0].upper() == "X"
    return chars


@dataclass
class Cell:
    """Class for holding "X" cell coordinates in the matrix.

    Can't make "XMAS" without the "X" so we don't care initially about other
    characters.
    """

    value: str
    row: int
    column: int
    max_row: int = field(repr=False)
    max_column: int = field(repr=False)

    def __post_init__(self):
        self.get_search_coords()

    def _check_row_range(self, coords: Iterable[int]) -> Iterable[int]:
        """Checks the row indexes are in matrix range."""
        if any(i < 0 or i > self.max_row for i in coords):
            return []
        return coords

    def _check_column_range(self, coords: Iterable[int]) -> Iterable[int]:
        """Checks the column indexes are in matrix range."""
        if any(i < 0 or i > self.max_column for i in coords):
            return []
        return coords

    def get_up(self) -> Iterable[int]:
        """Get rows up"""
        return self._check_row_range(range(self.row, self.row - 4, -1))

    def get_down(self) -> Iterable[int]:
        """Get rows down"""
        return self._check_row_range(range(self.row, self.row + 4, 1))

    def get_left(self) -> Iterable[int]:
        """Get columns left"""
        return self._check_column_range(
            range(self.column, self.column - 4, -1)
        )

    def get_right(self) -> Iterable[int]:
        """Get columns right"""
        return self._check_column_range(range(self.column, self.column + 4, 1))

    def get_search_coords(self) -> None:
        """Get a list of coordinates around the cell to search."""
        self.ups = [(row, self.column) for row in self.get_up()]
        self.downs = [(row, self.column) for row in self.get_down()]
        self.lefts = [(self.row, column) for column in self.get_left()]
        self.rights = [(self.row, column) for column in self.get_right()]
        self.up_right = list(zip(self.get_up(), self.get_right()))
        self.up_left = list(zip(self.get_up(), self.get_left()))
        self.down_right = list(zip(self.get_down(), self.get_right()))
        self.down_left = list(zip(self.get_down(), self.get_left()))

    def check_directions(self, matrix: list[str]) -> int:
        """Check the various directions and return count of XMAS"""
        count: int = 0
        # Ordinals
        if find_xmas(chars=coords_to_chars(coords=self.ups, matrix=matrix)):
            count += 1
        if find_xmas(chars=coords_to_chars(coords=self.downs, matrix=matrix)):
            count += 1
        if find_xmas(chars=coords_to_chars(coords=self.lefts, matrix=matrix)):
            count += 1
        if find_xmas(chars=coords_to_chars(coords=self.rights, matrix=matrix)):
            count += 1

        # Diagonals
        if find_xmas(
            chars=coords_to_chars(coords=self.up_right, matrix=matrix)
        ):
            count += 1
        if find_xmas(
            chars=coords_to_chars(coords=self.up_left, matrix=matrix)
        ):
            count += 1
        if find_xmas(
            chars=coords_to_chars(coords=self.down_right, matrix=matrix)
        ):
            count += 1
        if find_xmas(
            chars=coords_to_chars(coords=self.down_left, matrix=matrix)
        ):
            count += 1
        return count


def get_matrix(filename: str) -> list[str]:
    """Read the file and return matrix structure."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def get_x_cells(matrix: list[str]) -> list[Cell]:
    """Get cells that contain X in the matrix."""
    cells: list[Cell] = []

    for x, line in enumerate(matrix):
        for y, char in enumerate(line):
            # Skip if it's not an "X"
            if char.upper() != "X":
                continue
            cells.append(
                Cell(
                    value=char,
                    row=x,
                    column=y,
                    max_row=len(matrix) - 1,
                    max_column=len(line) - 1,
                )
            )
    print(f"Found X {len(cells)} times.")
    return cells


def tally_finds(cells: list[Cell], matrix: list[str]) -> int:
    """Tally up how many 'XMAS's we find for each cell."""
    tally: int = 0
    for cell in cells:
        tally += cell.check_directions(matrix=matrix)
    print(f"Found 'XMAS' {tally} times.")
    return tally


if __name__ == "__main__":
    # Test using the sample first.
    example_matrix = get_matrix("day4example")
    assert 18 == tally_finds(
        cells=get_x_cells(example_matrix), matrix=example_matrix
    )

    # Run the input.
    input_matrix = get_matrix("day4input")
    print("Final Count:")
    print(tally_finds(cells=get_x_cells(input_matrix), matrix=input_matrix))
