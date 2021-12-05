from numpy import loadtxt, ndarray, vectorize, void, where, fromfunction
from typing import Union


class SudokuSolver:
    """Loads a numpy representation of a sudoku puzzle, and has methods that can be solve via the backtrace A algorithm with some optimizations

    mostly a name space with static methods, but also some variable state for what
    would otherwise be global couters
    """

    @staticmethod
    def load_puzzle(path_to_puzzle: str) -> ndarray:
        """initalizes object instacne with a filepath to sudoku problem

        Args:
            path_to_puzzle (str): this file type must be .sd

        Returns:
            ndarray: 9x9 sudoku puzzlepuzzle
        """
        return loadtxt(path_to_puzzle, dtype=int)

    def __init__(self, path_to_puzzle) -> None:
        """initalizes object variabels that are needed.  Mostly counters that would have to be lobal otherwise.

        Args:
            path_to_puzzle (str): this file type must be .sd
        """
        self.path_to_puzzle = path_to_puzzle
        self.initial_puzzle = self.load_puzzle(path_to_puzzle)

    def __repr__(self) -> str:
        return str(self.puzzle)

    def __str__(self) -> str:
        return f"""
        naive_back_tracking_attempt_counter {self.naive_back_tracking_attempt_counter}
        """

    @staticmethod
    def assert_num_is_valid(num: int):
        assert num < 10 and num > 0

    @staticmethod
    def is_num_in_row(puzzle: ndarray, num: int, row: int) -> bool:
        __class__.assert_num_is_valid(num)
        return num in puzzle[row]

    @staticmethod
    def is_num_in_col(puzzle: ndarray, num: int, col: int) -> bool:
        __class__.assert_num_is_valid(num)
        return num in puzzle[:, col]

    @staticmethod
    def get_section_corner(row: int, col: int) -> tuple[int, int]:
        """given a row and column, return the row and column of the corner of the section of the section of the
        for example (5, 5) -> (3, 3) and  (5, 3) -> (3, 3)
        """
        return row - row % 3, col - col % 3

    @staticmethod
    def get_section(puzzle: ndarray, row: int, col: int) -> ndarray:
        """Gets the 3x3 ndarray given of the current square

        Returns:
            ndarray: 3x3 ndarray
        """
        x, y = __class__.get_section_corner(row, col)
        return puzzle[x:x+3, y:y+3]

    @staticmethod
    def is_num_in_section(puzzle: ndarray, num: int, row: int, col: int) -> bool:
        __class__.assert_num_is_valid(num)
        return num in __class__.get_section(puzzle, row, col)

    @staticmethod
    def is_safe_to_insert(puzzle: ndarray, num: int, row: int, col: int) -> bool:
        return not __class__.is_num_in_row(puzzle, num, row) \
            and not __class__.is_num_in_col(puzzle, num, col) \
            and not __class__.is_num_in_section(puzzle, num, row, col)

    @staticmethod
    def get_all_indicies_that_are_num(puzzle: ndarray, num: int) -> tuple:
        """gets all the indicies that are num int the puzzle

        Returns:
            tuple: for an index i, result[0][i], result[1][i] represents the x, y pair of a num
        """
        return where(puzzle == num)

    @staticmethod
    def get_first_blank(puzzle: ndarray) -> Union[tuple[int, int], bool]:
        """returns x, y coordinates of first blank entry in puzzle or false if there are none

        Returns:
            Union[tuple[int, int], bool]: x, y coordinates of first blank entry in puzzle or false if there are none
        """
        blanks = __class__.get_all_indicies_that_are_num(puzzle, 0)
        if len(blanks[0]) == 0:
            return False
        return blanks[0][0], blanks[1][0]

    @staticmethod
    def get_domains(puzzle: ndarray) -> ndarray:
        """set the domain property for the current puzzle state, which is a 3d boolean tensor where
        each i,j,k entry is true, if the number k-1 can be inserted into square i, j in the puzzle
        """

        # DEV NOTE: numpy's from function creates 3, 3d tensors i, j, k. the
        #  is_safe_to_insert method, is only meant to work for one entry, not
        #  to handle the full tensors.  We also dont want to iterate beacuse
        #  its slow.  So use vecttorize.
        #
        #  NOTE we dont want to vectorize the puzzle.

        vfunc = vectorize(__class__.is_safe_to_insert, excluded={"puzzle"})
        return fromfunction(
            lambda i, j, k: vfunc(puzzle=puzzle, num=k+1, row=i, col=j), (9, 9, 9), dtype=int)

    def reset_naive_back_tracking_attempt_counter(self, max_attempts: int = 10000):
        self.naive_back_tracking_attempt_counter: int = max_attempts

    def naive_back_tracking_attempt(self, puzzle: ndarray):
        if self.naive_back_tracking_attempt_counter <= 0:
            # give up, because the naive way is too long
            self.naive_back_tracking_attempt_counter = None
            return False

        self.naive_back_tracking_attempt_counter -= 1

        first_blank_tile = self.get_first_blank(puzzle)
        if(not first_blank_tile):
            return True
        return False

    def naive_back_tracking(self, max_attempts=10000):
        self.reset_naive_back_tracking_attempt_counter(max_attempts)
        return self.naive_back_tracking_attempt(self.initial_puzzle)
