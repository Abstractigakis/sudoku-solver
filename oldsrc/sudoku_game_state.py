from typing import Union
from numpy import ndarray, loadtxt, argwhere, vectorize, fromfunction, count_nonzero
from src.exceptions import InvalidSudokuGameState, NoBlanks


class SudokuGameState:

    #######################################################################################################
    # loaders
    #######################################################################################################
    @staticmethod
    def load_game_state_from_sd_file(path_to_puzzle: str):
        return SudokuGameState(loadtxt(path_to_puzzle, dtype=int))

    #######################################################################################################
    # dunders
    #######################################################################################################
    def __init__(self, puzzle: ndarray):
        self.puzzle: ndarray = puzzle

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"puzzle:\n{self.puzzle}"""

    def __eq__(self, other):
        return (self.puzzle == other.puzzle).all()

    #######################################################################################################
    # get indicies
    #######################################################################################################

    def get_all_indicies_that_are_num(self, num: int) -> tuple:
        return argwhere(self.puzzle == num)

    def get_first_blank(self) -> tuple[int, int]:
        blanks = self.get_all_indicies_that_are_num(0)
        if len(blanks) == 0:
            raise NoBlanks
        return blanks[0]

    @staticmethod
    def get_section_corner(row: int, col: int) -> tuple[int, int]:
        return row - row % 3, col - col % 3

    def get_section(self, row: int, col: int) -> ndarray:
        x, y = __class__.get_section_corner(row, col)
        return self.puzzle[x:x+3, y:y+3]

    #######################################################################################################
    # check valid moves
    #######################################################################################################

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

    #######################################################################################################
    # information
    #######################################################################################################
    def calc_domains(self) -> ndarray:
        """set the domain property for the current puzzle state, which is a 3d boolean tensor where
        each i,j,k entry is true, if the number k-1 can be inserted into square i, j in the puzzle
        """

        # DEV NOTE: numpy's from function creates 3, 3d tensors i, j, k. the
        #  is_safe_to_insert method, is only meant to work for one entry, not
        #  to handle the full tensors.  We also dont want to iterate beacuse
        #  its slow.  So use vecttorize.
        #
        #  NOTE we dont want to vectorize the puzzle.

        # this can be called on each game state on creation, but this is an
        # expensive operation.  better to only use domains ad-hoc

        vfunc = vectorize(self.is_safe_to_insert)
        return fromfunction(
            lambda i, j, k: vfunc(num=k+1, row=i, col=j), (9, 9, 9), dtype=int)

    def use_domains(self, domains: ndarray):
        return domains if isinstance(domains, ndarray) else self.calc_domains()

    def is_square_impossible(self, row: int, col: int, domains: ndarray = None) -> bool:
        domains = self.use_domains(domains)
        return (domains[row][col] == False).all() and self.puzzle[row][col] == 0

    def is_game_state_impossible(self, domains: ndarray = None) -> bool:
        domains = self.use_domains(domains)
        vfunc = vectorize(self.is_square_impossible, excluded={"domains"})
        return (fromfunction(
            lambda i, j: vfunc(domains=domains, row=i, col=j), (9, 9), dtype=int) == True).any()

    def how_many_possibilites(self, row: int, col: int, domains: ndarray = None):
        domains = self.use_domains(domains)
        return count_nonzero(domains[row][col])

    def next_game_state(self, num: int, row: int, col: int):
        if not self.is_safe_to_insert(num, row, col):
            raise InvalidSudokuGameState
        new_puzzle = self.puzzle.copy()
        new_puzzle[row][col] = num
        return SudokuGameState(new_puzzle)
