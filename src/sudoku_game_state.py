from numpy import ndarray, loadtxt, argwhere
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
    def __init__(self, puzzle: ndarray) -> None:
        self.puzzle: ndarray = puzzle

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"puzzle:\n{self.puzzle}"""

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

    def next_game_state(self, num: int, row: int, col: int):
        if not self.is_safe_to_insert(num, row, col):
            raise InvalidSudokuGameState
