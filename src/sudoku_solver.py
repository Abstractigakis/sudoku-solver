from numpy import array, ndarray, loadtxt, argwhere, vectorize, fromfunction, count_nonzero

from src.exceptions import InvalidInsert, MaxAtteptsReached, NoBlanks, PuzzleUnsolvable, NotSudokuFile, CantRemoveFromBlank


class SudokuSolver:

    #######################################################################################################
    # loaders
    #######################################################################################################
    @staticmethod
    def load_game_state_from_sd_file(path_to_puzzle: str) -> ndarray:
        if path_to_puzzle[-3:] != ".sd":
            raise NotSudokuFile(path_to_puzzle)
        return loadtxt(path_to_puzzle, dtype=int)

    #######################################################################################################
    # dunders
    #######################################################################################################
    def __init__(self, path_to_puzzle: str) -> None:
        self.path_to_puzzle = path_to_puzzle
        self.X_0: ndarray = __class__.load_game_state_from_sd_file(
            path_to_puzzle)
        self.D_0: ndarray = __class__.calc_D(X=self.X_0)
        self.attempt = 0

    #######################################################################################################
    # setters
    #######################################################################################################
    def increment_attempt(self, max_attempts: int) -> None:
        self.attempt += 1
        if self.attempt == max_attempts:
            raise MaxAtteptsReached(max_attempts)

    #######################################################################################################
    # get indicies
    #######################################################################################################

    @staticmethod
    def get_all_indicies_that_are_num(X: ndarray, num: int) -> tuple:
        return argwhere(X == num)

    @staticmethod
    def get_first_blank(X: ndarray) -> tuple[int, int]:
        blanks = __class__.get_all_indicies_that_are_num(X, 0)
        if len(blanks) == 0:
            raise NoBlanks
        return blanks[0]

    @staticmethod
    def get_section_corner_coordinates(row: int, col: int) -> tuple[int, int]:
        return row - row % 3, col - col % 3

    @staticmethod
    def get_section(X: ndarray, row: int, col: int) -> ndarray:
        i, j = __class__.get_section_corner_coordinates(row, col)
        return X[i:i+3, j:j+3]

    #######################################################################################################
    # check valid moves
    #######################################################################################################

    @staticmethod
    def is_num_in_row(X: ndarray, num: int, row: int) -> bool:
        return num in X[row]

    @staticmethod
    def is_num_in_col(X: ndarray, num: int, col: int) -> bool:
        return num in X[:, col]

    @staticmethod
    def is_num_in_section(X: ndarray, num: int, row: int, col: int) -> bool:
        return num in __class__.get_section(X, row, col)

    @staticmethod
    def is_safe_to_insert(X: ndarray, num: int, row: int, col: int) -> bool:
        return not __class__.is_num_in_row(X, num, row) \
            and not __class__.is_num_in_col(X, num, col) \
            and not __class__.is_num_in_section(X, num, row, col)

    #######################################################################################################
    # calculations
    #######################################################################################################

    #######################################################################################################
    # naive backtracking
    #######################################################################################################

    # def naive_back_tracking_attempt(self, X: ndarray, max_attempts: int)->ndarray:
    #     self.increment_attempt(max_attempts)

    #     # will raise NoBlanks if puzzle is solved!
    #     try:
    #         row, col = __class__.get_first_blank(X)
    #     except NoBlanks:
    #         # by design, if we give puzzle from the state that is valid,
    #         # and we reach this section of the code, then we know the puzzle
    #         # is solved, but really, we should check if the puzzle is valid
    #         return X

    #     for num in range(1, 10):
    #         # the case where next_puzzle is computed, meaning that it is
    #         # possible to insert k into X[i][j], so we should try this
    #         # and recursivly call backtracking on it
    #         try:
    #             next_game_state = game_state.next_game_state(num, row, col)
    #             reuslt_game_state = self.naive_back_tracking_attempt(
    #                 next_game_state, max_attempts)
    #             if isinstance(reuslt_game_state, SudokuGameState):
    #                 return reuslt_game_state

    #         except NoBlanks:
    #             # by design, if we give puzzle from the state that is valid,
    #             # and we reach this section of the code, then we know the puzzle
    #             # is solved, but really, we should check if the puzzle is valid
    #             return game_state

    #         except InvalidSudokuGameState:
    #             # if the result puzzle is in valid, move on and try num+1
    #             pass
    #         except PuzzleUnsolvable:
    #             # if our current puzzle is unsolvable, but we have more to
    #             # numbers to chekc continue
    #             pass

    #     # we checked all the numbers for a given spot, and they did not fit
    #     # for the puzzle, so need to raise puzzle unsolved
    #     raise PuzzleUnsolvable

    # def naive_back_tracking(self, max_attempts: int = 10000) -> tuple[ndarray, int]:
    #     self.attempt = 0
    #     return self.naive_back_tracking_attempt(self.X_0, max_attempts), self.attempt
