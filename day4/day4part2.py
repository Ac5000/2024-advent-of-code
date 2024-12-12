"""Code for day 4."""

from collections.abc import Iterable
from dataclasses import dataclass, field


def find_mas(chars: list[str]) -> bool:
    """Return True if the list of characters is "MAS"."""
    # Wrong length list.
    if len(chars) != 3:
        return False

    combined: str = ""
    for character in chars:
        combined += character.upper()
    if combined == "MAS":
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
    assert chars[0].upper() == "M"
    return chars


@dataclass
class Cell:
    """Class for holding "M" cell coordinates in the matrix.

    Can't make "X-MAS" without the "M" so we don't care initially about other
    characters.
    """

    value: str
    row: int
    column: int
    max_row: int = field(repr=False)
    max_column: int = field(repr=False)
    a_positions: list[tuple[int, int]] = field(default_factory=list)

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
        return self._check_row_range(range(self.row, self.row - 3, -1))

    def get_down(self) -> Iterable[int]:
        """Get rows down"""
        return self._check_row_range(range(self.row, self.row + 3, 1))

    def get_left(self) -> Iterable[int]:
        """Get columns left"""
        return self._check_column_range(
            range(self.column, self.column - 3, -1)
        )

    def get_right(self) -> Iterable[int]:
        """Get columns right"""
        return self._check_column_range(range(self.column, self.column + 3, 1))

    def get_search_coords(self) -> None:
        """Get a list of coordinates around the cell to search."""
        self.up_right = list(zip(self.get_up(), self.get_right()))
        self.up_left = list(zip(self.get_up(), self.get_left()))
        self.down_right = list(zip(self.get_down(), self.get_right()))
        self.down_left = list(zip(self.get_down(), self.get_left()))

    def check_directions(self, matrix: list[str]) -> None:
        """Check the various directions and save location of the "A"
        positions.
        """
        # Diagonals
        if find_mas(
            chars=coords_to_chars(coords=self.up_right, matrix=matrix)
        ):
            self.a_positions.append(self.up_right[1])
        if find_mas(chars=coords_to_chars(coords=self.up_left, matrix=matrix)):
            self.a_positions.append(self.up_left[1])
        if find_mas(
            chars=coords_to_chars(coords=self.down_right, matrix=matrix)
        ):
            self.a_positions.append(self.down_right[1])
        if find_mas(
            chars=coords_to_chars(coords=self.down_left, matrix=matrix)
        ):
            self.a_positions.append(self.down_left[1])


def get_matrix(filename: str) -> list[str]:
    """Read the file and return matrix structure."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()
    return lines


def get_m_cells(matrix: list[str]) -> list[Cell]:
    """Get cells that contain 'M' in the matrix."""
    cells: list[Cell] = []

    for x, line in enumerate(matrix):
        for y, char in enumerate(line):
            # Skip if it's not an "M"
            if char.upper() != "M":
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
    print(f"Found M {len(cells)} times.")
    return cells


def tally_finds(cells: list[Cell], matrix: list[str]) -> int:
    """Tally up how many 'X-MAS's we find for each cell."""
    tally: int = 0
    # Get all MAS/A coordinates.
    for cell in cells:
        cell.check_directions(matrix=matrix)

    # Loop the cells again now that we have A positions.
    for cell in cells:
        # Loop the cell 'A' positions.
        for a_pos in cell.a_positions:
            # If this position matches one in another cell, tally it.
            if any(
                a_pos in cell2.a_positions and cell != cell2 for cell2 in cells
            ):
                tally += 1
    # Divide tally by 2 when done since we are finding single vectors of the X.
    tally = tally // 2
    print(f"Found 'X-MAS' {tally} times.")
    return tally


if __name__ == "__main__":
    # Test using the sample first.
    example_matrix = get_matrix("day4example")
    assert 9 == tally_finds(
        cells=get_m_cells(example_matrix), matrix=example_matrix
    )

    # Run the input.
    input_matrix = get_matrix("day4input")
    print("Final Count:")
    print(tally_finds(cells=get_m_cells(input_matrix), matrix=input_matrix))
