from numpy import ndarray, loadtxt

from src.sudoku_game_state import SudokuGameState
from src.exceptions import InvalidSudokuGameState, MaxAtteptsReached, NoBlanks, PuzzleUnsolvable


class SudokuSolver:

    #######################################################################################################
    # loaders
    #######################################################################################################
    @staticmethod
    def load_game_state_from_sd_file(path_to_puzzle: str) -> ndarray:
        return loadtxt(path_to_puzzle, dtype=int)

    #######################################################################################################
    # dunders
    #######################################################################################################
    def __init__(self, path_to_puzzle: str) -> None:
        self.new_puzzle(path_to_puzzle)
        self.reset_naive_back_tracking_attempt_number()
        self.reset_back_tracking_with_forward_checking_attempt_number()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.intial_game_state)

    #######################################################################################################
    # variable setters an resetters
    #######################################################################################################
    def new_puzzle(self, path_to_puzzle: str):
        self.path_to_puzzle = path_to_puzzle
        self.intial_game_state: SudokuGameState = SudokuGameState(
            __class__.load_game_state_from_sd_file(path_to_puzzle))

    #######################################################################################################
    # naive backtracking
    #######################################################################################################
    def reset_naive_back_tracking_attempt_number(self):
        self.naive_back_tracking_attempt_number = 0

    def increment_naive_back_tracking_attempt_number(self, max_attempts: int) -> None:
        self.naive_back_tracking_attempt_number += 1
        if self.naive_back_tracking_attempt_number == max_attempts:
            raise MaxAtteptsReached(max_attempts)

    def naive_back_tracking_attempt(self, game_state: SudokuGameState, max_attempts: int):
        self.increment_naive_back_tracking_attempt_number(max_attempts)

        # will raise NoBlanks if puzzle is solved!
        try:
            row, col = game_state.get_first_blank()
        except NoBlanks:
            # by design, if we give puzzle from the state that is valid,
            # and we reach this section of the code, then we know the puzzle
            # is solved, but really, we should check if the puzzle is valid
            return game_state

        for num in range(1, 10):
            # the case where next_puzzle is computed, meaning that it is
            # possible to insert k into X[i][j], so we should try this
            # and recursivly call backtracking on it
            try:
                next_game_state = game_state.next_game_state(num, row, col)
                reuslt_game_state = self.naive_back_tracking_attempt(
                    next_game_state, max_attempts)
                if isinstance(reuslt_game_state, SudokuGameState):
                    return reuslt_game_state

            except NoBlanks:
                # by design, if we give puzzle from the state that is valid,
                # and we reach this section of the code, then we know the puzzle
                # is solved, but really, we should check if the puzzle is valid
                return game_state

            except InvalidSudokuGameState:
                # if the result puzzle is in valid, move on and try num+1
                pass
            except PuzzleUnsolvable:
                # if our current puzzle is unsolvable, but we have more to
                # numbers to chekc continue
                pass

        # we checked all the numbers for a given spot, and they did not fit
        # for the puzzle, so need to raise puzzle unsolved
        raise PuzzleUnsolvable

    def naive_back_tracking(self, max_attempts: int = 10000) -> tuple[SudokuGameState, int]:
        self.reset_naive_back_tracking_attempt_number()
        return self.naive_back_tracking_attempt(
            self.intial_game_state, max_attempts), self.naive_back_tracking_attempt_number

    #######################################################################################################
    # backtracking with forward checking
    #######################################################################################################
    def reset_back_tracking_with_forward_checking_attempt_number(self):
        self.back_tracking_with_forward_checking_attempt_number = 0

    def increment_back_tracking_with_forward_checking_attempt_number(self, max_attempts: int) -> None:
        self.back_tracking_with_forward_checking_attempt_number += 1
        if self.back_tracking_with_forward_checking_attempt_number == max_attempts:
            raise MaxAtteptsReached(max_attempts)

    def back_tracking_with_forward_checking_attempt(self, game_state: SudokuGameState, max_attempts: int):
        self.increment_back_tracking_with_forward_checking_attempt_number(
            max_attempts)

        # will raise NoBlanks if puzzle is solved!
        try:
            row, col = game_state.get_first_blank()
        except NoBlanks:
            # by design, if we give puzzle from the state that is valid,
            # and we reach this section of the code, then we know the puzzle
            # is solved, but really, we should check if the puzzle is valid
            return game_state

        for num in range(1, 10):
            # the case where next_puzzle is computed, meaning that it is
            # possible to insert k into X[i][j], so we should try this
            # and recursivly call backtracking on it
            try:
                next_game_state = game_state.next_game_state(num, row, col)
                if next_game_state.is_impossible:
                    reuslt_game_state = self.back_tracking_with_forward_checking_attempt(
                        next_game_state, max_attempts)
                    if isinstance(reuslt_game_state, SudokuGameState):
                        return reuslt_game_state

            except NoBlanks:
                # by design, if we give puzzle from the state that is valid,
                # and we reach this section of the code, then we know the puzzle
                # is solved, but really, we should check if the puzzle is valid
                return game_state

            except InvalidSudokuGameState:
                # if the result puzzle is in valid, move on and try num+1
                pass
            except PuzzleUnsolvable:
                # if our current puzzle is unsolvable, but we have more to
                # numbers to chekc continue
                pass

        # we checked all the numbers for a given spot, and they did not fit
        # for the puzzle, so need to raise puzzle unsolved
        raise PuzzleUnsolvable

    def back_tracking_with_forward_checking(self, max_attempts: int = 10000) -> tuple[SudokuGameState, int]:
        self.reset_back_tracking_with_forward_checking_attempt_number()
        return self.back_tracking_with_forward_checking_attempt(
            self.intial_game_state, max_attempts), self.back_tracking_with_forward_checking_attempt_number
