from numpy import loadtxt, ndarray, vectorize, void, where, fromfunction
from typing import Union


class SudokuSolver:
    """Loads a numpy representation of a sudoku puzzle, and has methods that can be solve via the backtrace A algorithm with some optimizations
    """

    def __init__(self, path_to_puzzle: str) -> None:
        """initalizes object instacne with a filepath to sudoku problem

        Args:
            path_to_puzzle (str): this file type must be .sd
        """
        self.puzzle: ndarray = loadtxt(path_to_puzzle, dtype=int)
        self.inital_puzzle: ndarray = self.puzzle
        self.domains: ndarray = self.get_domains()

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
        return num in self.get_section(row, col)

    def is_safe_to_insert(self, num: int, row: int, col: int) -> bool:
        return not self.is_num_in_row(num, row) and not self.is_num_in_col(num, col) and not self.is_num_in_section(num, row, col)

    def get_all_indicies_that_are_num(self, num: int) -> tuple:
        """gets all the indicies that are num int the puzzle

        Returns:
            tuple: for an index i, result[0][i], result[1][i] represents the x, y pair of a num
        """
        return where(self.puzzle == num)

    def get_first_blank(self) -> Union[tuple[int, int], bool]:
        """returns x, y coordinates of first blank entry in puzzle or false if there are none

        Returns:
            Union[tuple[int, int], bool]: x, y coordinates of first blank entry in puzzle or false if there are none
        """
        blanks = self.get_all_indicies_that_are_num(0)
        if len(blanks[0]) == 0:
            return False
        return blanks[0][0], blanks[1][0]

    def get_domains(self) -> void:
        """set the domains property for the current puzzle state, which is a 3d boolean tensor where
        each i,j,k entry is true, if the number k-1 can be inserted into square i, j in the puzzle
        """

        # DEV NOTE: numpy's from function creates 3, 3d tensors i, j, k. the
        #  is_safe_to_insert method, is only meant to work for one entry, not
        #  to handle the full tensors.  We also dont want to iterate beacuse
        #  its slow.  So use vecttorize

        vfunc = vectorize(self.is_safe_to_insert)
        return fromfunction(
            lambda i, j, k: vfunc(num=k+1, row=i, col=j), (9, 9, 9), dtype=int)


if __name__ == "__main__":
    sps = SudokuSolver("../sudoku_problems/44/1.sd")
    print(sps.get_domains())
