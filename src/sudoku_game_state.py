from typing import Union
from numpy import ndarray, vectorize, where, fromfunction, copy as npcopy

from exceptions import InvalidSudokuGameState, NoBlanks


class SudokuGameState:
    """keeps track of the game state of given sudoku puzzle.
    current puzzle, domains, methods to check valid moves, and generators for next game states
    """

#######################################################################################################
# dunders
#######################################################################################################

    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle
        self.domains = self.get_domains()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"puzzle:\n{self.puzzle}\n\ndomains"""

#######################################################################################################
# get indicies
#######################################################################################################

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
            raise NoBlanks
        return blanks[0][0], blanks[1][0]

    @staticmethod
    def get_section_corner(row: int, col: int) -> tuple[int, int]:
        """given a row and column, return the row and column of the corner of the section of the section of the
        for example (5, 5) -> (3, 3) and  (5, 3) -> (3, 3)
        """
        return row - row % 3, col - col % 3

    def get_section(self, row: int, col: int) -> ndarray:
        """Gets the 3x3 ndarray given of the current square

        Returns:
            ndarray: 3x3 ndarray
        """
        x, y = __class__.get_section_corner(row, col)
        return self.puzzle[x:x+3, y:y+3]

#######################################################################################################
# check valid moves
#######################################################################################################

    @staticmethod
    def assert_num_is_valid(num: int):
        assert num < 10 and num > 0

    def is_num_in_row(self, num: int, row: int) -> bool:
        return num in self.puzzle[row]

    def is_num_in_col(self, num: int, col: int) -> bool:
        return num in self.puzzle[:, col]

    def is_num_in_section(self, num: int, row: int, col: int) -> bool:
        return num in self.get_section(row, col)

    def is_safe_to_insert(self, num: int, row: int, col: int) -> bool:
        return not self.is_num_in_row(num, row) \
            and not self.is_num_in_col(num, col) \
            and not self.is_num_in_section(num, row, col)

    def is_valid(self) -> bool:
        """determines if the current puzzle has contradictos or not

        Returns:
            bool: true if puzzle is consistent, false otherwise
        """
        pass

#######################################################################################################
# domains and information
#######################################################################################################

    def get_domains(self) -> ndarray:
        """set the domain property for the current puzzle state, which is a 3d boolean tensor where
        each i,j,k entry is true, if the number k-1 can be inserted into square i, j in the puzzle
        """

        # DEV NOTE: numpy's from function creates 3, 3d tensors i, j, k. the
        #  is_safe_to_insert method, is only meant to work for one entry, not
        #  to handle the full tensors.  We also dont want to iterate beacuse
        #  its slow.  So use vecttorize.
        #
        #  NOTE we dont want to vectorize the puzzle.

        vfunc = vectorize(self.is_safe_to_insert, excluded={"puzzle"})
        return fromfunction(
            lambda i, j, k: vfunc(num=k+1, row=i, col=j), (9, 9, 9), dtype=int)

#######################################################################################################
# next state generators
#######################################################################################################
    def next_state(self, num: int, row: int, col: int) -> ndarray:
        if self.is_safe_to_insert(num, row, col):
            next_puzzle = npcopy(self.puzzle)
            next_puzzle[row][col] = num
            return SudokuGameState(next_puzzle)
        raise InvalidSudokuGameState
