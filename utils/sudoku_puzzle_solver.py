from numpy import loadtxt, ndarray


class SudokuPuzzleSolver:
    """Loads a numpy representation of a sudoku puzzle, and has methods that can be solve via the backtrace A algorithm with some optimizations
    """

    def __init__(self, path_to_puzzle: str) -> None:
        """initalizes object instacne with a filepath to sudoku problem

        Args:
            path_to_puzzle (str): this file type must be .sd
        """
        self.puzzle: ndarray = loadtxt(path_to_puzzle, dtype=int)

    def __repr__(self) -> str:
        return str(self.puzzle)

    def __str__(self) -> str:
        return str(self.puzzle)

    def is_num_in_row(self, num: int, row: int) -> bool:
        return num in self.puzzle[row]

    def is_num_in_col(self, num: int, col: int) -> bool:
        return num in self.puzzle[:, col]

    def get_section_corner(self, row: int, col: int) -> tuple[int, int]:
        """given a row and column, return the row and column of the corner of the section of the section of the
        for example (5, 5) -> (3, 3) and  (5, 3) -> (3, 3)
        """
        return row - row % 3, col - col % 3

    def get_section(self, row: int, col: int) -> ndarray:
        """Gets the 3x3 ndarray given of the current square

        Returns:
            ndarray: 3x3 ndarray
        """
        x, y = self.get_section_corner(row, col)
        return self.puzzle[x:x+3, y:y+3]

    def is_num_in_section(self, num: int, row: int, col: int) -> bool:
        return num in self.get_section_corner(row, col)

    def is_safe_to_insert(self, num: int, row: int, col: int) -> bool:
        return not self.is_num_in_row(num, row) \
            and not self.is_num_in_col(num, col) \
            and not self.is_num_in_section(num, row, col)

    def get_first_blank(self):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] == 0:
                    return i, j
        return False


if __name__ == "__main__":
    sps = SudokuPuzzleSolver("../sudoku_problems/1/1.sd")
    print(sps)
